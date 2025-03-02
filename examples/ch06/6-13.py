# stream.py


class WSConnectionManager:
    ...

    async def broadcast(self, message: str | bytes | list | dict) -> None:
        for connection in self.active_connections:
            await self.send(message, connection)
