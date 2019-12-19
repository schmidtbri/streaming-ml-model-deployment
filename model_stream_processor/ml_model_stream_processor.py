"""Faust agent hosts an MlModel object."""
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

from model_stream_processor.model_manager import ModelManager


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

        if self._model is None:
            raise ValueError("'{}' not found in ModelManager instance.".format(model_qualified_name))

        # the topic from which the model will receive prediction inputs
        self.consumer_topic = "model_stream_processor.{}.{}.{}.inputs".format(model_qualified_name, self._model.major_version, self._model.minor_version)
        # the topic to which the model will send prediction outputs
        self.producer_topic = "model_stream_processor.{}.{}.{}.outputs".format(model_qualified_name, self._model.major_version, self._model.minor_version)
        # the topic to which the model will send prediction errors
        self.error_producer_topic = "model_stream_processor.{}.{}.{}.errors".format(model_qualified_name, self._model.major_version, self._model.minor_version)

        print(self.consumer_topic)

        self._consumer = AIOKafkaConsumer(self.consumer_topic, loop=loop, bootstrap_servers=bootstrap_servers, group_id="my-group")
        self._producer = AIOKafkaProducer(loop=loop, bootstrap_servers=bootstrap_servers)

    def __repr__(self):
        return "{} model: {} version: {}".format(super().__repr__(), self._model.qualified_name,
                                                 str(self._model.major_version) + "." + str(self._model.minor_version))

    async def start(self):
        """Start the consumers and producers."""
        await self._consumer.start()
        await self._producer.start()

    async def process(self):
        """Make predictions on records in a stream."""
        async for msg in self._consumer:
            try:
                result = self._model.predict(data=msg.value)
                print("consumed: ", msg.topic, msg.partition, msg.offset, msg.key, msg.value, msg.timestamp)
                await self._producer.send_and_wait(self.producer_topic, bytes(result))
            except:
                await self._producer.send_and_wait(self.error_producer_topic, msg.value)

    async def stop(self):
        """"""
        await self._consumer.stop()
        await self._producer.stop()
