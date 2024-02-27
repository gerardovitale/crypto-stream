import json
import logging
import time
from typing import List

import websockets

logger = logging.getLogger(__name__)


class EmptyChannelList(Exception):
    ...


async def get_response(websocket_client: websockets.WebSocketClientProtocol):
    logging.info("Receiving websocket response...")
    response = await websocket_client.recv()
    return json.loads(response)


def generate_nonce() -> str:
    return str(int(time.time() * 1000))


def create_request_message(channel_list: List[str]) -> dict:
    if not isinstance(channel_list, list):
        raise TypeError
    if len(channel_list) == 0:
        raise EmptyChannelList
    return {
        "id": 1,
        "method": "subscribe",
        "params": {"channels": channel_list},
        "nonce": generate_nonce(),
    }


def create_heartbeat_response(response_obj_id: dict) -> dict:
    return {
        "id": response_obj_id.get("id"),
        "method": "public/respond-heartbeat",
        "nonce": generate_nonce(),
    }
