cryptocom-stream.test:
	cd crypto-client-producer/ && time poetry run pytest --durations=0 .

run:
	docker-compose build
	docker-compose up -d

stop:
	docker-compose stop

check-healcheck:
	docker inspect crypto-kafka | jq ".[0].State.Health"
