import argparse
import asyncio
from aiokafka import AIOKafkaConsumer


async def main(loop, topic, bootstrap_servers):
    consumer = AIOKafkaConsumer(topic, loop=loop,
                                bootstrap_servers=bootstrap_servers, group_id="script")
    await consumer.start()

    try:
        async for msg in consumer:
            print(msg.value.decode())
    except KeyboardInterrupt:
        await consumer.stop()
        return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send messages to kafka topic.')
    parser.add_argument('--topic', type=str, help='Topic to send messages to.')
    parser.add_argument('--bootstrap_servers', type=str, help='Server to send messages to.')

    args = parser.parse_args()

    loop = asyncio.get_event_loop()

    loop.run_until_complete(main(loop=loop, topic=args.topic, bootstrap_servers=args.bootstrap_servers))

    loop.close()

