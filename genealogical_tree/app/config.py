import os

from genealogical_tree.app.magic_config import MagicConfig


ENVIRONMENT = 'TEST'
CONFIG_FILE = os.environ.get('CONFIG_FILE', f'config/{ENVIRONMENT.lower()}.yml')

README_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    'README.md',
)


class Environments:
    TEST = 'TEST'


class BaseConfig(MagicConfig):
    ENVIRONMENT: str
    APP_NAME: str

    DB_PG_NAME: str
    DB_PG_USERNAME: str
    DB_PG_PASSWORD: str
    DB_PG_HOST: str
    DB_PG_PORT: int = 5432

    DB_SCHEMA: 'DB_PG_NAME' # noqa
    DB_NAME: 'DB_PG_NAME' # noqa

    @property
    def ENVIRONMENT(self):
        return str(ENVIRONMENT).upper()

    @property
    def DB_URL(self):
        return 'postgresql://{user}:{password}@{host}:{port}/{name}'.format(
            user=self.DB_PG_USERNAME,
            password=self.DB_PG_PASSWORD,
            host=self.DB_PG_HOST,
            port=self.DB_PG_PORT,
            name=self.DB_PG_NAME,
        )

    README_PATH = README_PATH


class DevConfig(BaseConfig):
    pass


class TestConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    """Для запуска юнит тестов"""
    INIT_LOGGING: bool = False
    TESTING: bool = True
    DEBUG: bool = True


class StageConfig(BaseConfig):
    pass


class ProdConfig(BaseConfig):
    pass


class LocalConfig(BaseConfig):
    pass


config_class = {
    Environments.TEST: TestConfig,
}.get(ENVIRONMENT.upper(), BaseConfig)


config: BaseConfig = config_class.from_file(CONFIG_FILE)
