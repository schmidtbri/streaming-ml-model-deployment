"""Faust agent hosts an MlModel object."""
import logging
import json
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

from model_stream_processor import __name__
from model_stream_processor.model_manager import ModelManager

logger = logging.getLogger(__name__)


class MLModelStreamProcessor(object):
    """Processor class for MLModel stream processors."""

    def __init__(self, model_qualified_name, loop, bootstrap_servers):
        """Create an agent for a model.

        :param model_qualified_name: The qualified name of the model that will be hosted in this stream processor.
        :type model: str
        :param loop: The asyncio event loop to be used by the stream processor.
        :type loop: _UnixSelectorEventLoop
        :param bootstrap_servers: The kafka brokers to connect to.
        :type bootstrap_servers: str
        :returns: An instance of MLModelStreamProcessor.
        :rtype: MLModelStreamProcessor

        """
        model_manager = ModelManager()
        self._model = model_manager.get_model(model_qualified_name)

        logger.info("Initializing stream processor for model: {}".format(self._model.qualified_name))

        if self._model is None:
            raise ValueError("'{}' not found in ModelManager instance.".format(model_qualified_name))

        base_topic_name = "model_stream_processor.{}.{}.{}".format(model_qualified_name,
                                                                   self._model.major_version,
                                                                   self._model.minor_version)
        # the topic from which the model will receive prediction inputs
        self.consumer_topic = "{}.inputs".format(base_topic_name)
        # the topic to which the model will send prediction outputs
        self.producer_topic = "{}.outputs".format(base_topic_name)
        # the topic to which the model will send prediction errors
        self.error_producer_topic = "{}.errors".format(base_topic_name)

        logger.info("Consuming messages from topic {}.".format(self.consumer_topic))
        logger.info("Producing messages to topics {} and {}.".format(self.producer_topic, self.error_producer_topic))

        self._consumer = AIOKafkaConsumer(self.consumer_topic, loop=loop, bootstrap_servers=bootstrap_servers,
                                          group_id=__name__)
        self._producer = AIOKafkaProducer(loop=loop, bootstrap_servers=bootstrap_servers)

    def __repr__(self):
        """Return string representation of stream processor."""
        return "{} model: {} version: {}".format(super().__repr__(), self._model.qualified_name,
                                                 str(self._model.major_version) + "." + str(self._model.minor_version))

    async def start(self):
        """Start the consumers and producers."""
        logger.info("{} stream processor: Starting consumer and producer.".format(self._model.qualified_name))
        await self._consumer.start()
        await self._producer.start()

    async def process(self):
        """Make predictions on records in a stream."""
        async for message in self._consumer:
            try:
                data = json.loads(message.value)
                prediction = self._model.predict(data=data)
                serialized_prediction = json.dumps(prediction).encode()
                await self._producer.send_and_wait(self.producer_topic, serialized_prediction)
            except Exception as e:
                logger.error("{} stream processor: Exception: {}".format(self._model.qualified_name, str(e)))
                await self._producer.send_and_wait(self.error_producer_topic, message.value)

    async def stop(self):
        """Stop the streaming processor."""
        logger.info("{} stream processor: Stopping consumer and producer.".format(self._model.qualified_name))
        await self._consumer.stop()
        await self._producer.stop()
