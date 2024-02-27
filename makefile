# Makefile

ENV := $(PWD)/.env

include $(ENV)
export

producer.test:
	cd $(PRODUCER_BASE_PATH) && time poetry run pytest --durations=0 .

run:
	docker-compose build
	docker-compose up -d

stop:
	docker-compose stop
	yes | docker container prune

check-kafka-healcheck:
	docker inspect $(KAFKA_CONTAINER_NAME) | jq ".[0].State.Health"

check-kafka-messages:
	docker exec -it $(KAFKA_CONTAINER_NAME) /bin/bash -c \
		"kafka-console-consumer.sh \
		--consumer.config /opt/bitnami/kafka/config/consumer.properties \
		--bootstrap-server $(KAFKA_BOOTSTRAP_SERVER) \
		--topic $(KAFKA_TOPIC) --from-beginning"

check-producer-logs:
	docker logs -f $(PRODUCER_CONTAINER_NAME)
