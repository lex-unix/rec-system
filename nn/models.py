import tensorflow as tf
import tensorflow_recommenders as tfrs


class CustomerModel(tf.keras.Model):
    def __init__(
        self, unique_customer_names, ticket_subjects, ticket_types, ticket_descriptions
    ):
        super().__init__()

        max_tokens = 10_000
        embedding_dim = 32

        self.customer_embedding = tf.keras.Sequential(
            [
                tf.keras.layers.StringLookup(
                    vocabulary=unique_customer_names, mask_token=None
                ),
                tf.keras.layers.Embedding(len(unique_customer_names) + 1, embedding_dim),
            ]
        )

        self.ticket_subject_vectorizer = tf.keras.layers.TextVectorization(
            max_tokens=max_tokens
        )

        self.ticket_description_vectorizer = tf.keras.layers.TextVectorization(
            max_tokens=max_tokens
        )

        self.ticket_type_vectorizer = tf.keras.layers.TextVectorization(
            max_tokens=max_tokens
        )

        self.ticket_subject_embedding = tf.keras.Sequential(
            [
                self.ticket_subject_vectorizer,
                tf.keras.layers.Embedding(max_tokens, embedding_dim),
                tf.keras.layers.GlobalAveragePooling1D(),
            ]
        )

        self.ticket_description_embedding = tf.keras.Sequential(
            [
                self.ticket_description_vectorizer,
                tf.keras.layers.Embedding(max_tokens, embedding_dim),
                tf.keras.layers.GlobalAveragePooling1D(),
            ]
        )

        self.ticket_type_embedding = tf.keras.Sequential(
            [
                self.ticket_type_vectorizer,
                tf.keras.layers.Embedding(max_tokens, embedding_dim),
                tf.keras.layers.GlobalAveragePooling1D(),
            ]
        )

        self.ticket_subject_vectorizer.adapt(ticket_subjects)
        self.ticket_description_vectorizer.adapt(ticket_descriptions)
        self.ticket_type_vectorizer.adapt(ticket_types)

    def call(self, inputs):
        return tf.concat(
            [
                self.customer_embedding(inputs['customer_name']),
                self.ticket_subject_embedding(inputs['ticket_subject']),
                self.ticket_description_embedding(inputs['ticket_description']),
                self.ticket_type_embedding(inputs['ticket_type']),
            ],
            axis=1,
        )


class OperatorModel(tf.keras.Model):
    def __init__(self, unique_operator_names):
        super().__init__()

        self.operator_embedding = tf.keras.Sequential(
            [
                tf.keras.layers.StringLookup(
                    vocabulary=unique_operator_names, mask_token=None
                ),
                tf.keras.layers.Embedding(len(unique_operator_names) + 1, 32),
            ]
        )

    def call(self, inputs):
        return self.operator_embedding(inputs)


class QueryModel(tf.keras.Model):
    def __init__(
        self,
        layer_sizes,
        unique_customer_names,
        ticket_subjects,
        ticket_types,
        ticket_descriptions,
    ):
        super().__init__()

        self.embedding_model = CustomerModel(
            unique_customer_names, ticket_subjects, ticket_types, ticket_descriptions
        )

        self.dense_layers = tf.keras.Sequential()

        for layer_size in layer_sizes[:-1]:
            self.dense_layers.add(tf.keras.layers.Dense(layer_size, activation='relu'))

        for layer_size in layer_sizes[-1:]:
            self.dense_layers.add(tf.keras.layers.Dense(layer_size))

    def call(self, inputs):
        feature_embedding = self.embedding_model(inputs)
        return self.dense_layers(feature_embedding)


class CandidateModel(tf.keras.Model):
    def __init__(self, layer_sizes, unique_operator_names):
        super().__init__()

        self.embedding_model = OperatorModel(unique_operator_names)

        self.dense_layers = tf.keras.Sequential()

        for layer_size in layer_sizes[:-1]:
            self.dense_layers.add(tf.keras.layers.Dense(layer_size, activation='relu'))

        for layer_size in layer_sizes[-1:]:
            self.dense_layers.add(tf.keras.layers.Dense(layer_size))

    def call(self, inputs):
        feature_embedding = self.embedding_model(inputs)
        return self.dense_layers(feature_embedding)


class RetrievalModel(tfrs.models.Model):
    def __init__(
        self,
        operators,
        layer_sizes,
        unique_operator_names,
        unique_customer_names,
        ticket_subjects,
        ticket_types,
        ticket_descriptions,
    ):
        super().__init__()
        self.query_model = QueryModel(
            layer_sizes,
            unique_customer_names,
            ticket_subjects,
            ticket_types,
            ticket_descriptions,
        )
        self.candidate_model = CandidateModel(layer_sizes, unique_operator_names)
        self.task = tfrs.tasks.Retrieval(
            metrics=tfrs.metrics.FactorizedTopK(
                candidates=operators.batch(128).map(self.candidate_model),
            ),
        )

    def compute_loss(self, features, training=False):
        query_embeddings = self.query_model(
            {
                'customer_name': features['customer_name'],
                'ticket_subject': features['ticket_subject'],
                'ticket_type': features['ticket_type'],
                'ticket_description': features['ticket_description'],
            }
        )
        candidate_embedding = self.candidate_model(features['operator_name'])

        return self.task(query_embeddings, candidate_embedding)


class OperatorRankingModel(tf.keras.Model):
    def __init__(self, unique_customer_names, unique_operator_names):
        super().__init__()
        embedding_dimension = 32

        self.customer_embeddings = tf.keras.Sequential(
            [
                tf.keras.layers.StringLookup(
                    vocabulary=unique_customer_names, mask_token=None
                ),
                tf.keras.layers.Embedding(
                    len(unique_customer_names) + 1, embedding_dimension
                ),
            ]
        )

        self.operator_embeddings = tf.keras.Sequential(
            [
                tf.keras.layers.StringLookup(
                    vocabulary=unique_operator_names, mask_token=None
                ),
                tf.keras.layers.Embedding(
                    len(unique_operator_names) + 1, embedding_dimension
                ),
            ]
        )

        self.ratings = tf.keras.Sequential(
            [
                tf.keras.layers.Dense(128),
                tf.keras.layers.BatchNormalization(),
                tf.keras.layers.Activation('relu'),
                tf.keras.layers.Dropout(0.5),
                tf.keras.layers.Dense(64),
                tf.keras.layers.BatchNormalization(),
                tf.keras.layers.Activation('relu'),
                tf.keras.layers.Dropout(0.5),
                tf.keras.layers.Dense(1),
            ]
        )

    def call(self, inputs):
        customer_id, operator_name = inputs

        customer_embedding = self.customer_embeddings(customer_id)
        operator_embedding = self.operator_embeddings(operator_name)

        return self.ratings(tf.concat([customer_embedding, operator_embedding], axis=1))


class RankingModel(tfrs.models.Model):
    def __init__(self, unique_customer_names, unique_operator_names):
        super().__init__()
        self.ranking_model = OperatorRankingModel(
            unique_customer_names=unique_customer_names,
            unique_operator_names=unique_operator_names,
        )
        self.task = tfrs.tasks.Ranking(
            loss=tf.keras.losses.MeanSquaredError(),
            metrics=[tf.keras.metrics.RootMeanSquaredError()],
        )

    def call(self, features):
        return self.ranking_model((features['customer_name'], features['operator_name']))

    def compute_loss(self, features, training=False) -> tf.Tensor:
        labels = features.pop('rating')

        rating_predictions = self(features)

        return self.task(labels=labels, predictions=rating_predictions)
