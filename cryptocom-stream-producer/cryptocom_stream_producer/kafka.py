import json
import logging

from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient
from confluent_kafka.admin import NewTopic

logger = logging.getLogger(__name__)


async def create_topic_if_not_exists(kafka_config: dict, topic: str) -> None:
    logging.info(f"Kafka config loaded: {kafka_config}")
    admin_client = AdminClient(kafka_config)
    topic_metadata = admin_client.list_topics(timeout=10)
    if topic not in topic_metadata.topics:
        logging.debug(f"Creating topic `{topic}`")
        admin_client.create_topics([NewTopic(topic, num_partitions=1, replication_factor=1)])
        logging.info(f"Topic `{topic}` created")
        return
    logging.info(f"Topic `{topic}` already exists")


def ingest_into_kafka(producer: Producer, topic_name: str, response: dict) -> None:
    data_list = get_data_from_response(response)
    for data_point in data_list:
        producer.produce(topic_name, value=generate_kafka_message(data_point), callback=acked)
        logger.info(f"Published into kafka serve in topic: {topic_name}")
        producer.poll(1)
        logger.info("Message polled!!")


def generate_kafka_message(data: dict) -> str:
    return json.dumps(data)


def get_data_from_response(response: dict):
    def _generate_message(obj: dict) -> dict:
        return {
            "highest": obj.get("h", ""),
            "lowest": obj.get("l", ""),
            "latest": obj.get("a", ""),
            "price_chance": obj.get("c", ""),
            "best_bid_price": obj.get("b", ""),
            "best_bid_size": obj.get("bs", ""),
            "best_ask_price": obj.get("k", ""),
            "best_ask_size": obj.get("ks", ""),
            "instrument_name": obj.get("i", ""),
            "traded_volume": obj.get("v", ""),
            "traded_volume_value": obj.get("vv", ""),
            "open_interest": obj.get("oi", ""),
            "trade_timestamp": obj.get("t", ""),
        }

    data = response.get("result", {}).get("data", {})
    return map(_generate_message, data)


def acked(err, msg):
    if err is not None:
        logger.error("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    logger.info("Message produced: %s" % (str(msg)))
