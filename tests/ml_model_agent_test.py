import pytest
import unittest
from unittest import TestCase
import faust
from ml_model_abc import MLModel
from tests.helper import _run

from model_stream_processor.model_manager import ModelManager
from model_stream_processor.ml_model_agent import MLModelAgent


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


class MLModelAgentTests(TestCase):

    def test1(self):
        """  """
        # arrange
        model_manager = ModelManager()
        model_manager.load_models(configuration=[
            {
                "module_name": "tests.model_manager_test",
                "class_name": "MLModelMock"
            }
        ])

        app = faust.App('test app')

        source_channel = app.channel()
        destination_channel = app.channel()

        #ml_model_agent = MLModelAgent(app=app,
        #                              model_qualified_name="qualified_name",
        #                              source_stream=source_channel,
        #                              destination_stream=destination_channel)

        #app.agents["qualified_name"] = ml_model_agent

        # act
        _run(source_channel.put(1))

        # assert
        print(source_channel.empty())


if __name__ == '__main__':
    unittest.main()
