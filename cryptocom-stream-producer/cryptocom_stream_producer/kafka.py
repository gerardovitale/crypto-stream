import json
import logging

from confluent_kafka.admin import AdminClient
from confluent_kafka.admin import NewTopic

logger = logging.getLogger(__name__)


async def create_topic_if_not_exists(kafka_config: str, topic: str) -> None:
    logging.info(f"Kafka config loaded: {kafka_config}")
    admin_client = AdminClient(kafka_config)
    topic_metadata = admin_client.list_topics(timeout=10)
    if topic not in topic_metadata.topics:
        logging.debug(f"Creating topic `{topic}`")
        admin_client.create_topics([NewTopic(topic, num_partitions=1, replication_factor=1)])
        logging.info(f"Topic `{topic}` created")
        return
    logging.info(f"Topic `{topic}` already exists")


def generate_msg_from_res(response: dict) -> str:
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
    return json.dumps([_generate_message(obj) for obj in data])


def acked(err, msg):
    if err is not None:
        logger.error("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        logger.info("Message produced: %s" % (str(msg)))
