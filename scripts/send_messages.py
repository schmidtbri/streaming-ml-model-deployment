import sys
import argparse
import asyncio
from aiokafka import AIOKafkaProducer


async def main(loop, topic, bootstrap_servers):
    producer = AIOKafkaProducer(loop=loop, bootstrap_servers=bootstrap_servers)
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()

    try:
        for line in sys.stdin:
            await producer.send_and_wait(topic, line.encode())
    except KeyboardInterrupt:
        await producer.stop()
        return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send messages to kafka topic.')
    parser.add_argument('--topic', type=str, help='Topic to send messages to.')
    parser.add_argument('--bootstrap_servers', type=str, help='Server to send messages to.')
    args = parser.parse_args()

    loop = asyncio.get_event_loop()

    loop.run_until_complete(main(loop=loop, topic=args.topic, bootstrap_servers=args.bootstrap_servers))

    loop.close()

