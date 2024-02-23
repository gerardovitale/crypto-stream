import asyncio
import json
import logging
import os
import time

import websockets
from confluent_kafka import Producer
from cryptocom import create_heartbeat_response
from cryptocom import create_request_message
from cryptocom import get_response
from dotenv import load_dotenv
from kafka import create_topic_if_not_exists
from kafka import generate_msg_from_res

LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOGGING_LEVEL = logging.DEBUG


async def main() -> None:
    logging.basicConfig(format=LOGGING_FORMAT, level=LOGGING_LEVEL)
    logging.info("Starting main")

    logging.info("Loading ENV variables")
    load_dotenv()

    uri = os.getenv("CRYPTOCOM_PROD_MARKET_ENDPOINT_V1")
    channel_list = ["ticker.BTC_EUR"]
    kafka_topic_name = os.getenv("KAFKA_TOPIC")
    kafka_config = {
        "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVER"),
    }

    await create_topic_if_not_exists(kafka_config, kafka_topic_name)
    kafka_producer = Producer(kafka_config)

    async with websockets.connect(uri) as websocket_client:
        time.sleep(1)
        logging.info("Building request message")
        message = create_request_message(channel_list)

        # Send the subscribe message
        logging.info("Sending message")
        await websocket_client.send(json.dumps(message))

        while True:
            res_obj = await get_response(websocket_client)

            logging.info(res_obj)
            if res_obj.get("method") == "public/heartbeat":
                logging.info("Heartbeat...")
                heartbeat_response = create_heartbeat_response(res_obj)
                logging.info(heartbeat_response)
                await websocket_client.send(json.dumps(heartbeat_response))

            else:
                kafka_producer.produce(kafka_topic_name, value=generate_msg_from_res(res_obj))
                logging.info(f"Published into kafka serve in topic: {kafka_topic_name}")
                kafka_producer.poll(1)
                logging.info("Message polled!!")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
