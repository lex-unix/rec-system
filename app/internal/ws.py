from fastapi import WebSocket


class ChatUser:
    def __init__(self, client: WebSocket, user_id: int):
        self.client = client
        self.user_id = user_id


class WSManager:
    def __init__(self) -> None:
        self.rooms: dict[int, list[WebSocket]] = {}

    async def connect(self, client: WebSocket, room: int):
        await client.accept()

        if room not in self.rooms:
            self.rooms[room] = []

        self.rooms[room].append(client)

    def disconnect(self, client: WebSocket, room: int):
        self.rooms[room].remove(client)

    async def broadcast(self, message: dict, sender: WebSocket, room: int):
        if room not in self.rooms:
            return

        for client in self.rooms[room]:
            if client != sender:
                await client.send_json(message)

    async def send_personal(self, message: dict, client: WebSocket):
        await client.send_json(message)


manager = WSManager()
