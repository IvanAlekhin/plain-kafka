# plain-kafka

Producer and consumer (worker) for working with kafka.

## Usage

```$ pip install plain-kafka```

### Producer:

```python
from plain_kafka import AsyncProducer, Producer
import asyncio
import os

config = {"bootstrap.servers": "kafka-05.your.host:9092, kafka-03.your.host:9092",
          "security.protocol": "SASL_PLAINTEXT",
          "sasl.mechanism": "SCRAM-SHA-256",
          "sasl.username": "username",
          "sasl.password": os.environ['KAFKA_PSWD']}

async def produce_something_async(topic: str, message: str):
    aio_p = AsyncProducer(config)
    await aio_p.produce(topic, message)
    # You can don't close producer and use one producer instance for all project.
    aio_p.close()


def produce_something(topic: str, message: str):
    p = Producer(config)
    p.produce(topic, message)
    p.close()


if __name__ == '__main__':
    asyncio.run(produce_something_async('my_topic', 'my_message'))
    produce_something('my_topic', 'my_message2')

```

### Consumer(worker):
```python
from plain_kafka import AsyncWorker, AsyncRetryWorker
import asyncio
import os

def sync_service(kafka_msg):
    print(kafka_msg)


async def async_service(kafka_msg):
    await asyncio.sleep(1)
    print(kafka_msg)


# For more security use environment variables for credentials. 
consumer_config = {"bootstrap.servers": "kafka-05.preprod.local:9092, kafka-03.preprod.local:9092",
                   "security.protocol": "SASL_PLAINTEXT",
                   "sasl.mechanism": "SCRAM-SHA-256",
                   "sasl.username": "username",
                   "sasl.password": os.environ['KAFKA_PSWD'],
                   "group.id": "my_group_id",
                   "enable.auto.commit": False,
                   "auto.offset.reset": 'earliest'}

producer_config = {"bootstrap.servers": "kafka-05.preprod.local:9092, kafka-03.preprod.local:9092",
                   "security.protocol": "SASL_PLAINTEXT",
                   "sasl.mechanism": "SCRAM-SHA-256",
                   "sasl.username": "username",
                   "sasl.password": os.environ['KAFKA_PSWD']}

async_w = AsyncWorker(consumer_topic="my_topic", service=async_service, consumer_conf=consumer_config,
                      failed_topic='my_topic_retry', producer_conf=producer_config)

r_async_w = AsyncRetryWorker(consumer_topic='my_topic_retry', service=async_service, consumer_conf=consumer_config,
                             failed_topic='my_topic_failed', producer_conf=producer_config)


# You can use sync service in this Worker. It will work in blocking mode.
# In plans write new sync worker in separated class.
sync_w = AsyncWorker(consumer_topic="my_topic", service=sync_service, consumer_conf=consumer_config,
                     failed_topic='my_topic_retry', producer_conf=producer_config)


async def main():
    await asyncio.gather(sync_w.start(), async_w.start(), r_async_w.start())


if __name__ == '__main__':
    asyncio.run(main())

```

## Local installation
- Install [poetry](https://python-poetry.org/docs/).

- ```$ git clone https://github.com/IvanAlekhin/plain-kafka.git```

- ```$ cd plain-kafka```

- ```$ poetry install```

- ```$ poetry shell```
