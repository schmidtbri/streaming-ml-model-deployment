"""Configuration for the faust application."""


class Config(object):
    """Configuration for all environments."""

    models = [
        {
            "module_name": "iris_model.iris_predict",
            "class_name": "IrisModel"
        }
    ]


class ProdConfig(Config):
    """Configuration for the prod environment."""

    broker = 'kafka://localhost:9092'
    value_serializer = 'raw'


class BetaConfig(Config):
    """Configuration for the beta environment."""

    broker = 'kafka://localhost:9092'
    value_serializer = 'raw'


class TestConfig(Config):
    """Configuration for the test environment."""

    broker = 'kafka://localhost:9092'
    value_serializer = 'raw'


class DevConfig(Config):
    """Configuration for the dev environment."""

    broker = 'kafka://localhost:9092'
    value_serializer = 'raw'
