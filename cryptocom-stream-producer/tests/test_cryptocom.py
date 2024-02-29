from time import sleep
from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

from cryptocom_stream_producer.cryptocom import create_heartbeat_response
from cryptocom_stream_producer.cryptocom import create_request_message
from cryptocom_stream_producer.cryptocom import EmptyChannelList
from cryptocom_stream_producer.cryptocom import generate_nonce


class TestCryptoCom(TestCase):
    def test_generate_nonce(self):
        actual_nonce_1 = generate_nonce()
        assert isinstance(actual_nonce_1, str)
        assert actual_nonce_1.isdigit()

        sleep(0.1)
        actual_nonce_2 = generate_nonce()
        assert actual_nonce_2 != actual_nonce_1

    @patch("cryptocom_stream_producer.cryptocom.generate_nonce")
    def test_create_request_message_when_a_valid_channel_list_is_passed(self, generate_nonce_mock: Mock):
        test_channel_list = ["test_channel"]

        actual_msg = create_request_message(test_channel_list)

        assert actual_msg.get("id") == 1
        assert actual_msg.get("method") == "subscribe"
        assert actual_msg.get("params").get("channels") == test_channel_list
        generate_nonce_mock.assert_called_once()

    def test_create_request_message_when_a_invalid_channels_list_is_passed(self):
        # EMPTY CHANNEL LIST IS EMPTY
        self.assertRaises(EmptyChannelList, create_request_message, [])

        # NO ARGS PASSED
        self.assertRaises(TypeError, create_request_message)

        # CHANNEL LIST IS NOT A LIST
        self.assertRaises(TypeError, create_request_message, {"test_key": "test_value"})
        self.assertRaises(TypeError, create_request_message, "test_channel_string")
        self.assertRaises(TypeError, create_request_message, 12345)
        self.assertRaises(TypeError, create_request_message, None)

    @patch("cryptocom_stream_producer.cryptocom.generate_nonce")
    def test_create_heartbeat_response(self, generate_nonce_mock: Mock):
        test_response_obj_id = {"id": 1}

        actual_heartbeat_res = create_heartbeat_response(test_response_obj_id)

        assert actual_heartbeat_res.get("id") == 1
        assert actual_heartbeat_res.get("method") == "public/respond-heartbeat"
        generate_nonce_mock.assert_called_once()
