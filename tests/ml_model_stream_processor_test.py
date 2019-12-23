import unittest
from unittest import TestCase
from unittest.mock import Mock
import asyncio

from ml_model_abc import MLModel
from model_stream_processor.model_manager import ModelManager
from model_stream_processor.ml_model_stream_processor import MLModelStreamProcessor


# creating an MLModel class to test with
class MLModelMock(MLModel):
    # accessing the package metadata
    display_name = "display name"
    qualified_name = "qualified_name"
    description = "description"
    major_version = 1
    minor_version = 1
    input_schema = None
    output_schema = None

    def __init__(self):
        super().__init__()

    def predict(self, data):
        return data


class MLModelStreamProcessorTests(TestCase):

    def test1(self):
        """testing the __init__() method"""
        # arrange
        model_manager = ModelManager()
        model_manager.load_models(configuration=[
            {
                "module_name": "tests.model_manager_test",
                "class_name": "MLModelMock"
            }
        ])
        loop = asyncio.get_event_loop()
        asyncio.set_event_loop(loop)

        # act
        processor = MLModelStreamProcessor(model_qualified_name="qualified_name",
                                           loop=loop,
                                           bootstrap_servers=None)

        # assert
        self.assertTrue(processor.consumer_topic == "model_stream_processor.{}.{}.{}.inputs".format("qualified_name", 1, 1))
        self.assertTrue(processor.producer_topic == "model_stream_processor.{}.{}.{}.outputs".format("qualified_name", 1, 1))
        self.assertTrue(processor.error_producer_topic == "model_stream_processor.{}.{}.{}.errors".format("qualified_name", 1, 1))

        # closing the processor
        loop.run_until_complete(processor.stop())


if __name__ == '__main__':
    unittest.main()
