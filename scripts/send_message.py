import os
import argparse
import asyncio
from aiokafka import AIOKafkaProducer


async def main(loop):
    producer = AIOKafkaProducer(loop=loop, bootstrap_servers='localhost:9092')
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        # Produce message
        await producer.send_and_wait("model_stream_processor.iris_model.0.1.inputs",
                                     b"{\"petal_length\": 1.1, \"petal_width\": 1.2, \"sepal_length\": 1.3, \"sepal_width\": 1.4}")
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()

if __name__ == "__main__":

    loop = asyncio.get_event_loop()

    loop.run_until_complete(main(loop=loop))
