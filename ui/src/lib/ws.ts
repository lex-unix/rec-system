const WS_URL = 'ws://localhost:8000';

export function createSocket(endpoint: string): WebSocket {
  const socket = new WebSocket(`${WS_URL}/${endpoint}`);
  return socket;
}
