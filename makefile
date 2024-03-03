# Makefile

ENV := $(PWD)/.env

include $(ENV)
export

run:
	docker-compose build
	docker-compose up -d

stop:
	docker-compose stop

clean:
	yes | docker container prune
	yes | docker image prune
	yes | docker volume prune


# PRODUCER
producer.run:
	docker-compose up $(PRODUCER_CONTAINER_NAME)

producer.test:
	cd $(PRODUCER_BASE_PATH) && time poetry run pytest -vv --durations=0 .


# CONSUMER
consumer.run:
	cd $(CONSUMER_BASE_PATH) && poetry run python3 cryptocom_stream_consumer/main.py

consumer.test:
	cd $(CONSUMER_BASE_PATH) && time poetry run pytest --durations=0 .


# KAFKA
kafka.run:
	docker-compose up $(KAFKA_CONTAINER_NAME)

kafka.check-healthcheck:
	docker inspect $(KAFKA_CONTAINER_NAME) | jq ".[0].State.Health"

kafka.check-messages:
	docker run --rm -it --network crypto-stream_default \
	--name my_container --entrypoint /bin/bash \
	bitnami/kafka:3.4.1 -c "kafka-console-consumer.sh \
	--consumer.config /opt/bitnami/kafka/config/consumer.properties \
	--bootstrap-server $(KAFKA_BOOTSTRAP_SERVER) \
	--topic $(KAFKA_TOPIC) --from-beginning"
