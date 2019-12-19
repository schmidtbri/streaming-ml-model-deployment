"""Configuration for the faust application."""


class Config(dict):
    """Configuration for all environments."""

    models = [
        {
            "module_name": "iris_model.iris_predict",
            "class_name": "IrisModel"
        }
    ]


class ProdConfig(Config):
    """Configuration for the prod environment."""

    bootstrap_servers = 'localhost:9092'
    async_produce = False


class BetaConfig(Config):
    """Configuration for the beta environment."""

    bootstrap_servers = 'localhost:9092'
    async_produce = False


class TestConfig(Config):
    """Configuration for the test environment."""

    bootstrap_servers = 'localhost:9092'
    async_produce = False


class DevConfig(Config):
    """Configuration for the dev environment."""

    bootstrap_servers = 'localhost:9092'
    async_produce = False
