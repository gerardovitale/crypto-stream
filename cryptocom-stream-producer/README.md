# Producer

## Data consumed via websocket subcription

### ticker.{instrument_name}

#### Response

| Name            | Type   | Description              |
|-----------------|--------|--------------------------|
| instrument_name | string | e.g. BTCUSD-PERP         |
| subscription    | string | ticker.{instrument_name} |
| channel         | string | Always ticker            |
| data            | array  | See below                |

#### Data

| Name | Type   | Mapped Name         | Description                                                     |
|------|--------|---------------------|-----------------------------------------------------------------|
| h    | string | highest             | Price of the 24h highest trade                                  |
| l    | string | lowest              | Price of the 24h lowest trade, null if there weren't any trades |
| a    | string | latest              | The price of the latest trade, null if there weren't any trades |
| c    | string | price_chance        | 24-hour price change, null if there weren't any trades          |
| b    | string | best_bid_price      | The current best bid price, null if there aren't any bids       |
| bs   | string | best_bid_size       | The current best bid size, null if there aren't any bids        |
| k    | string | best_ask_price      | The current best ask price, null if there aren't any asks       |
| ks   | string | best_ask_size       | The current best ask size, null if there aren't any bids        |
| i    | string | instrument_name     | Instrument name                                                 |
| v    | string | traded_volume       | The total 24h traded volume                                     |
| vv   | string | traded_volume_value | The total 24h traded volume value (in USD)                      |
| oi   | string | open_interest       | The open interest                                               |
| t    | number | trade_timestamp     | Trade timestamp                                                 |

## Kafka Producer documentation

[Source Link](https://docs.confluent.io/kafka-clients/python/current/overview.html#ak-producer)

```python
from confluent_kafka import Producer
import socket

conf = {'bootstrap.servers': 'host1:9092,host2:9092',
        'client.id': socket.gethostname()}

producer = Producer(conf)

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))

producer.produce(topic, key="key", value="value", callback=acked)

# Wait up to 1 second for events. Callbacks will be invoked during
# this method call if the message is acknowledged.
producer.poll(1)
```
