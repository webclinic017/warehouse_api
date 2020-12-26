"""Module with the Websocket server instance for the generic api"""
import logging
import os
from typing import List, Dict, Any

from fastapi import WebSocket


class WebsocketConnectionManager:
    active_connections: Dict[str, List[WebSocket]] = {}
    sleep_interval: float = float(os.environ.get('WEBSOCKET_SLEEP_INTERVAL', 60))

    @classmethod
    async def connect(cls, websocket: WebSocket, path: str):
        await websocket.accept()

        if path not in cls.active_connections:
            cls.active_connections[path] = []

        cls.active_connections[path].append(websocket)
        logging.info(f'new websocket connection on {path}')

    @classmethod
    def disconnect(cls, websocket: WebSocket, path: str):
        cls.active_connections[path].remove(websocket)

        logging.info(f'websocket disconnected from {path}')

    @classmethod
    async def send(cls, message: Any, websocket: WebSocket):
        await websocket.send_json(message)

    @classmethod
    async def receive(cls, websocket: WebSocket):
        return await websocket.receive_json()

    @classmethod
    async def broadcast(cls, message: Any, path: str):
        for connection in cls.active_connections[path]:
            await connection.send_json(message)
