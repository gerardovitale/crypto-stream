import logging
import os
from ast import literal_eval

import apache_beam as beam
from apache_beam.io.kafka import ReadFromKafka
from dotenv import load_dotenv

LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOGGING_LEVEL = logging.DEBUG


def convert_kafka_bytes_to_dictionary(record):
    # the records have 'value' attribute when --WITH_METADATA is given
    if hasattr(record, "value"):
        bytes_record = record.value
    elif isinstance(record, tuple):
        bytes_record = record[1]
    else:
        raise RuntimeError("unknown record type: {0}".format(type(record)))
    return literal_eval(bytes_record.decode("UTF-8"))


def run_pipeline():
    logging.basicConfig(format=LOGGING_FORMAT, level=LOGGING_LEVEL)
    logging.info("Starting main")

    logging.info("Loading ENV variables")
    load_dotenv()

    KAFKA_CONFIG = {"bootstrap.servers": "localhost:9094"}
    KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
    WITH_METADATA = True

    # pipeline_options when deployiing in Dataflow
    # pipeline_args = ['--project', 'my-project',
    #                  '--runner', 'DataflowRunner',
    #                  '--temp_location', 'my-temp-location',
    #                  '--region', 'my-region',
    #                  '--num_workers', 'my-num-workers']

    with beam.Pipeline() as pipeline:
        _ = (
            pipeline
            | "Read data source"
            >> ReadFromKafka(
                consumer_config=KAFKA_CONFIG,
                topics=[KAFKA_TOPIC],
                with_metadata=WITH_METADATA,
            )
            | "Convert bytes to dict" >> beam.Map(lambda record: convert_kafka_bytes_to_dictionary(record))
            | "Write in console as logs" >> beam.FlatMap(lambda message: logging.info(message))
        )


if __name__ == "__main__":
    run_pipeline()
