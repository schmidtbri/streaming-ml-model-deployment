""""""
import argparse
from kafka.admin import KafkaAdminClient, NewTopic

from model_stream_processor.config import Config
from model_stream_processor.model_manager import ModelManager

# instantiating the ModelManager singleton
model_manager = ModelManager()
model_manager.load_models(Config.models)


def main(configuration):
    admin_client = KafkaAdminClient(bootstrap_servers=configuration.bootstrap_servers)

    for model in model_manager.get_models():
        # creating the topics needed for one model stream processor
        topic_list = [
            NewTopic(name="model_stream_processor.{}.{}.{}.inputs".format(model["qualified_name"], model["major_version"], model["minor_version"]), num_partitions=1, replication_factor=1),
            NewTopic(name="model_stream_processor.{}.{}.{}.outputs".format(model["qualified_name"], model["major_version"], model["minor_version"]), num_partitions=1, replication_factor=1),
            NewTopic(name="model_stream_processor.{}.{}.{}.errors".format(model["qualified_name"], model["major_version"], model["minor_version"]), num_partitions=1, replication_factor=1)
        ]
        admin_client.create_topics(new_topics=topic_list, validate_only=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--environment', type=str, help='Environment used for configuration.')

    args = parser.parse_args()

    # using the right configuration
    configuration = __import__("model_stream_processor").__getattribute__("config").__getattribute__(args.environment)

    main(configuration=configuration)
