"""Application that holds MLModel stream processors."""
import os
import logging
import asyncio

from model_stream_processor.config import Config
from model_stream_processor.model_manager import ModelManager
from model_stream_processor.ml_model_stream_processor import MLModelStreamProcessor


logging.basicConfig(level=logging.INFO)

# importing the right configuration
configuration = __import__("model_stream_processor").\
    __getattribute__("config"). \
    __getattribute__(os.environ["APP_SETTINGS"])

# instantiating the ModelManager singleton
model_manager = ModelManager()
model_manager.load_models(Config.models)


def main():
    """Start application."""
    # starting the asyncio event loop that will be used by the application
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)

    # create a stream processor object for each model in the ModelManager
    stream_processors = []
    for model in model_manager.get_models():
        stream_processors.append(MLModelStreamProcessor(model_qualified_name=model["qualified_name"],
                                                        loop=loop,
                                                        bootstrap_servers=configuration.bootstrap_servers))

    for stream_processor in stream_processors:
        loop.run_until_complete(stream_processor.start())

    try:
        for stream_processor in stream_processors:
            loop.run_until_complete(stream_processor.process())
    except KeyboardInterrupt:
        logging.info("Process interrupted.")
    finally:
        for stream_processor in stream_processors:
            loop.run_until_complete(stream_processor.stop())
        loop.close()
        logging.info("Successfully shutdown the processors.")


if __name__ == "__main__":
    main()
