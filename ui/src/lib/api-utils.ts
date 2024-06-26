import { PUBLIC_API_URL } from '$env/static/public';
import { ResponseError } from './response-error';
import type { Issue, User, Chat, Feeback } from './types';

const ISSUES_ENDPOINT = PUBLIC_API_URL + '/issues';
const USERS_ENDPOINT = PUBLIC_API_URL + '/users';
const CHAT_ENDPOINT = PUBLIC_API_URL + '/chats';
const FEEDBACK_ENDPOINT = PUBLIC_API_URL + '/feedbacks';

const requestOptions: RequestInit = {
  credentials: 'include',
  headers: {
    'Content-Type': 'application/json'
  }
};

async function sendPostRequest<T>(
  endpoint: string,
  body: string
): Promise<{ ok: true; data: T } | { ok: false; error: ResponseError }> {
  try {
    const response = await fetch(endpoint, {
      ...requestOptions,
      method: 'POST',
      body
    });
    const json = await response.json();
    if (!response.ok) {
      const error = new ResponseError(response.status, json.detail);
      return { ok: false, error };
    }
    return { ok: true, data: json };
  } catch (e) {
    console.error(e);
    const error = new ResponseError(500, 'The server encountered an error');
    return { ok: false, error };
  }
}

async function sendGetRequest<T>(
  endpoint: string
): Promise<{ ok: true; data: T } | { ok: false; error: ResponseError }> {
  try {
    const response = await fetch(endpoint, {
      method: 'GET',
      credentials: 'include'
    });
    const json = await response.json();
    if (!response.ok) {
      const error = new ResponseError(response.status, json.detail);
      return { ok: false, error };
    }
    return { ok: true, data: json };
  } catch (e) {
    console.error(e);
    const error = new ResponseError(500, 'The server encountered an error');
    return { ok: false, error };
  }
}

async function sendDeleteRequest(
  endpoint: string
): Promise<{ ok: true } | { ok: false; error: ResponseError }> {
  try {
    const response = await fetch(endpoint, {
      method: 'DELETE',
      credentials: 'include'
    });
    if (!response.ok) {
      const json = await response.json();
      const error = new ResponseError(response.status, json.detail);
      return { ok: false, error };
    }
    return { ok: true };
  } catch (e) {
    console.error(e);
    const error = new ResponseError(500, 'The server encountered an error');
    return { ok: false, error };
  }
}

export function login(body: string) {
  return sendPostRequest<User>(`${USERS_ENDPOINT}/login`, body);
}

export function register(body: string) {
  return sendPostRequest<User>(`${USERS_ENDPOINT}/register`, body);
}

export function createIssue(body: string) {
  return sendPostRequest<Issue>(ISSUES_ENDPOINT + '/', body);
}

export function createChat(body: string) {
  return sendPostRequest<Chat>(CHAT_ENDPOINT + '/', body);
}

export function fetchCustomerIssues() {
  return sendGetRequest<Issue[]>(ISSUES_ENDPOINT + '/customer');
}

export function fetchOperatorIssues() {
  return sendGetRequest<Issue[]>(ISSUES_ENDPOINT + '/operator');
}

export function fetchCustomerIssue(id: string) {
  return sendGetRequest<Issue>(`${ISSUES_ENDPOINT}/customer/${id}`);
}

export function fetchChats() {
  return sendGetRequest<Chat[]>(CHAT_ENDPOINT + '/');
}

export function fetchChat(id: string) {
  return sendGetRequest<Chat>(`${CHAT_ENDPOINT}/${id} `);
}

export function createFeedback(issueId: string, body: string) {
  return sendPostRequest<Feeback>(`${FEEDBACK_ENDPOINT}/${issueId}`, body);
}

export function deleteIssue(issueId: string) {
  return sendDeleteRequest(`${ISSUES_ENDPOINT}/${issueId}`);
}

export function changeIssueStatus(issueId: string, body: string) {
  return sendPostRequest(`${ISSUES_ENDPOINT}/customer/${issueId}/status`, body);
}

export function changeOperatoravAilability(
  operatorId: string | number,
  body: string
) {
  return sendPostRequest(
    `${USERS_ENDPOINT}/operators/${operatorId}/availability`,
    body
  );
}
