"""Faust agent hosts an MlModel object."""
from faust.agents.agent import Agent
from model_stream_processor.model_manager import ModelManager


class MLModelAgent(Agent):
    """Agent class for MLModel processors."""

    def __init__(self, model_qualified_name, source_stream, destination_stream, **kwargs):
        """Create an agent for a model."""
        Agent.__init__(self,  function=MLModelAgent.process, **kwargs)
        self._model_qualified_name = model_qualified_name
        self.source_stream = source_stream
        self.destination_stream = destination_stream

        model_manager = ModelManager()
        self._model = model_manager.get_model(self._model_qualified_name)

    async def process(self, stream):
        """Make predictions on records in a stream."""
        async for record in stream:
            result = self._model.predict(data=record)
            await self.destination_stream.send(result)
