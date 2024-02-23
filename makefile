cryptocom_stream.test:
	cd crypto-client-producer/ && time poetry run pytest --durations=0 .

run:
	docker-compose build
	docker-compose up -d

stop:
	docker-compose stop
