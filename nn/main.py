import logging
import os

import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_recommenders as tfrs

from nn.models import RankingModel
from nn.models import RetrievalModel

logger = tf.get_logger()
logger.setLevel(logging.ERROR)

DATASET_PATH = os.path.join(os.getcwd(), 'datasets', 'clean_data.csv')
RETRIEVAL_MODEL_PATH = os.path.join(os.getcwd(), 'model-weights', 'retrieval_model')
RANKING_MODEL_PATH = os.path.join(os.getcwd(), 'model-weights', 'ranking_model')


def load_data():
    data = pd.read_csv(DATASET_PATH)
    return data[:8000]


def preprocess_data(df: pd.DataFrame):
    operators = tf.data.Dataset.from_tensor_slices(df['operator'].unique())
    customer_ratings = tf.data.Dataset.from_tensor_slices(dict(df))  # type: ignore
    customer_ratings = customer_ratings.map(
        lambda x: {
            'operator_name': x['operator'],
            'customer_name': x['customer_name'],
            'ticket_subject': x['ticket_subject'],
            'ticket_type': x['ticket_type'],
            'ticket_description': x['ticket_description'],
        }
    )
    return operators, customer_ratings


def get_unqiue_operators_and_customers(operator_names, customer_names):
    unique_operator_names = np.unique(np.concatenate(list(operator_names)))
    unique_customer_names = np.unique(np.concatenate(list(customer_names)))
    return unique_operator_names, unique_customer_names


def prepare_data(operators, customer_ratings):
    operator_names = operators.batch(2_000)
    customer_names = customer_ratings.batch(4_000).map(lambda x: x['customer_name'])
    ticket_subjects = customer_ratings.batch(200).map(lambda x: x['ticket_subject'])
    ticket_types = customer_ratings.batch(200).map(lambda x: x['ticket_type'])
    ticket_descriptions = customer_ratings.batch(200).map(
        lambda x: x['ticket_description']
    )

    return (
        operator_names,
        customer_names,
        ticket_subjects,
        ticket_types,
        ticket_descriptions,
    )


def load_retrieval_model(
    operators,
    unique_customer_names,
    unique_operator_names,
    ticket_subjects,
    ticket_descriptions,
    ticket_types,
    layer_sizes=[1024, 256, 128, 64, 32],
):
    retrieval_model = RetrievalModel(
        operators=operators,
        layer_sizes=layer_sizes,
        unique_customer_names=unique_customer_names,
        unique_operator_names=unique_operator_names,
        ticket_subjects=ticket_subjects,
        ticket_types=ticket_types,
        ticket_descriptions=ticket_descriptions,
    )
    retrieval_model.compile(optimizer=tf.keras.optimizers.Adagrad(learning_rate=0.001))
    retrieval_model.load_weights(RETRIEVAL_MODEL_PATH).expect_partial()

    return retrieval_model


def load_indexer(retrieval_model: RetrievalModel, operators):
    index = tfrs.layers.factorized_top_k.BruteForce(retrieval_model.query_model, k=20)
    index.index_from_dataset(
        tf.data.Dataset.zip(
            (
                operators.batch(100),
                operators.batch(100).map(retrieval_model.candidate_model),
            )
        )
    )

    return index


def load_ranking_model(unique_customer_names, unique_operator_names):
    ranking_model = RankingModel(
        unique_customer_names=unique_customer_names,
        unique_operator_names=unique_operator_names,
    )
    ranking_model.compile(optimizer=tf.keras.optimizers.Adagrad(learning_rate=0.002))
    ranking_model.load_weights(RANKING_MODEL_PATH).expect_partial()

    return ranking_model


def load_models() -> dict[str, tfrs.models.Model]:
    df = load_data()

    operators, customer_ratings = preprocess_data(df)

    operator_names, customer_names, ticket_subjects, ticket_types, ticket_descriptions = (
        prepare_data(
            operators,
            customer_ratings,
        )
    )
    print(ticket_types)

    unique_operator_names, unique_customer_names = get_unqiue_operators_and_customers(
        operator_names,
        customer_names,
    )

    retrieval_model = load_retrieval_model(
        operators=operators,
        unique_customer_names=unique_customer_names,
        unique_operator_names=unique_operator_names,
        ticket_subjects=ticket_subjects,
        ticket_types=ticket_types,
        ticket_descriptions=ticket_descriptions,
    )
    ranking_model = load_ranking_model(
        unique_operator_names=unique_operator_names,
        unique_customer_names=unique_customer_names,
    )

    index = load_indexer(retrieval_model=retrieval_model, operators=operators)

    models = {
        'retrieval': retrieval_model,
        'ranking': ranking_model,
        'index': index,
    }

    return models


def predict(
    models,
    customer_name: str,
    ticket_subject: str,
    ticket_type: str,
    ticket_description: str,
):
    customer_input = {
        'customer_name': tf.expand_dims(customer_name, axis=0),
        'ticket_subject': tf.expand_dims(ticket_subject, axis=0),
        'ticket_type': tf.expand_dims(ticket_type, axis=0),
        'ticket_description': tf.expand_dims(ticket_description, axis=-1),
    }

    _, operator_suggestions = models['index'](customer_input)

    suggested_titles = operator_suggestions[0].numpy()

    output = {}
    for operator_name in suggested_titles:
        output[operator_name] = models['ranking'](
            {
                'customer_name': np.array([customer_name]),
                'operator_name': np.array([operator_name]),
            }
        )
    results = []
    for name, score in sorted(output.items(), key=lambda x: x[1], reverse=True):
        results.append({'operator': name.decode('utf-8'), 'rating': score.numpy()[0, 0]})

    return results
