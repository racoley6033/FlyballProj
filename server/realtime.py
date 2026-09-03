from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.clients = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.clients.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.clients.remove(websocket)

    async def broadcast(self, message: dict):
        for client in self.clients:
            await client.send_json(message)

manager = ConnectionManager()