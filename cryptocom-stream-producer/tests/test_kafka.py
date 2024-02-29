from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

from cryptocom_stream_producer.kafka import acked
from cryptocom_stream_producer.kafka import get_data_from_response
from cryptocom_stream_producer.kafka import ingest_into_kafka


class TestKafkaIntegration(TestCase):
    def setUp(self) -> None:
        logger_patch = patch("cryptocom_stream_producer.kafka.logger")
        self.addCleanup(logger_patch.stop)
        self.mock_logger = logger_patch.start()

    def test_ingest_into_kafka(self):
        mock_producer = Mock()
        test_topic_name = "test_topic"
        test_response = {
            "id": -1,
            "method": "subscribe",
            "code": 0,
            "result": {
                "instrument_name": "BTC_EUR",
                "subscription": "ticker.BTC_EUR",
                "channel": "ticker",
                "data": [
                    {
                        "h": "59024.20",
                        "l": "54500.00",
                        "a": "58023.14",
                        "c": "0.0372",
                        "b": "57966.40",
                        "bs": "0.00014",
                        "k": "57999.51",
                        "ks": "0.00520",
                        "i": "BTC_EUR",
                        "v": "142.3314",
                        "vv": "8731433.08",
                        "oi": "1234.567",
                        "t": 1709215389684,
                    },
                ],
            },
        }
        expected_value = (
            '{"highest": "59024.20", "lowest": "54500.00", "latest": "58023.14", '
            '"price_chance": "0.0372", "best_bid_price": "57966.40", "best_bid_size": "0.00014", '
            '"best_ask_price": "57999.51", "best_ask_size": "0.00520", "instrument_name": "BTC_EUR", '
            '"traded_volume": "142.3314", "traded_volume_value": "8731433.08", '
            '"open_interest": "1234.567", "trade_timestamp": 1709215389684}'
        )

        ingest_into_kafka(mock_producer, test_topic_name, test_response)

        assert len(mock_producer.produce.mock_calls) == 1
        assert len(mock_producer.poll.mock_calls) == 1
        mock_producer.produce.assert_called_with(test_topic_name, value=expected_value, callback=acked)


class TestKafka(TestCase):
    def setUp(self) -> None:
        logger_patch = patch("cryptocom_stream_producer.kafka.logger")
        self.addCleanup(logger_patch.stop)
        self.mock_logger = logger_patch.start()

    @patch("cryptocom_stream_producer.kafka.generate_kafka_message")
    @patch("cryptocom_stream_producer.kafka.get_data_from_response")
    def test_ingest_into_kafka(self, mock_get_data_from_response: Mock, mock_generate_kafka_message: Mock):
        mock_producer = Mock()
        test_topic_name = "test_topic"
        test_response = {"key": "value"}
        mock_get_data_from_response.return_value = [{"key": "value"}]

        ingest_into_kafka(mock_producer, test_topic_name, test_response)

        mock_get_data_from_response.assert_called_once()
        mock_producer.produce.assert_called_once()
        mock_generate_kafka_message.assert_called_once()

    def test_get_data_from_response_when_data_is_populated(self):
        test_res_obj = {
            "id": -1,
            "method": "subscribe",
            "code": 0,
            "result": {
                "instrument_name": "BTC_EUR",
                "subscription": "ticker.BTC_EUR",
                "channel": "ticker",
                "data": [
                    {
                        "h": "59024.20",
                        "l": "54500.00",
                        "a": "58023.14",
                        "c": "0.0372",
                        "b": "57966.40",
                        "bs": "0.00014",
                        "k": "57999.51",
                        "ks": "0.00520",
                        "i": "BTC_EUR",
                        "v": "142.3314",
                        "vv": "8731433.08",
                        "oi": "1234.567",
                        "t": 1709215389684,
                    },
                    {
                        "t": 1709215389684,
                    },
                ],
            },
        }
        expected_data = [
            {
                "highest": "59024.20",
                "lowest": "54500.00",
                "latest": "58023.14",
                "price_chance": "0.0372",
                "best_bid_price": "57966.40",
                "best_bid_size": "0.00014",
                "best_ask_price": "57999.51",
                "best_ask_size": "0.00520",
                "instrument_name": "BTC_EUR",
                "traded_volume": "142.3314",
                "traded_volume_value": "8731433.08",
                "open_interest": "1234.567",
                "trade_timestamp": 1709215389684,
            },
            {
                "highest": "",
                "lowest": "",
                "latest": "",
                "price_chance": "",
                "best_bid_price": "",
                "best_bid_size": "",
                "best_ask_price": "",
                "best_ask_size": "",
                "instrument_name": "",
                "traded_volume": "",
                "traded_volume_value": "",
                "open_interest": "",
                "trade_timestamp": 1709215389684,
            },
        ]
        actual_data = get_data_from_response(test_res_obj)
        assert list(actual_data) == expected_data

    def test_get_data_from_response_when_data_is_not_populated(self):
        test_res_obj = {
            "id": -1,
            "method": "subscribe",
            "code": 0,
            "result": {
                "instrument_name": "BTC_EUR",
                "subscription": "ticker.BTC_EUR",
                "channel": "ticker",
                "data": [],
            },
        }
        expected_data = []
        actual_data = get_data_from_response(test_res_obj)
        assert list(actual_data) == expected_data

    def test_get_data_from_response_when_result_is_empty(self):
        test_res_obj = {
            "id": -1,
            "method": "subscribe",
            "code": 0,
            "result": {},
        }
        expected_data = []
        actual_data = get_data_from_response(test_res_obj)
        assert list(actual_data) == expected_data

    def test_get_data_from_response_when_response_is_empty(self):
        test_res_obj = {}
        expected_data = []
        actual_data = get_data_from_response(test_res_obj)
        assert list(actual_data) == expected_data
