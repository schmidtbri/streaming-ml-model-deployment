"""Faust application."""
import os
import faust
from model_stream_processor.config import Config
from model_stream_processor.model_manager import ModelManager


app = faust.App('model-stream-processor')

app.config_from_object('model_stream_processor.config.{}'.format(os.environ['APP_SETTINGS']))

# instantiating the model manager class
model_manager = ModelManager()

# loading the MLModel objects from configuration
model_manager.load_models(configuration=Config.models)
