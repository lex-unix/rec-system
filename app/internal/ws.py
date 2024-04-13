from fastapi import WebSocket


class WSManager:
    def __init__(self) -> None:
        self.active_connections: list[WebSocket] = []

    async def connect(self, client: WebSocket):
        await client.accept()
        self.active_connections.append(client)

    def disconnect(self, client: WebSocket):
        self.active_connections.remove(client)

    async def broadcast(self, message: dict, sender: WebSocket):
        for client in self.active_connections:
            if client != sender:
                await client.send_json(message)

    async def send_personal_message(self, message: str, client: WebSocket):
        await client.send_text(message)


manager = WSManager()
