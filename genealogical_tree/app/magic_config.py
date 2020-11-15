import inspect
import os
import json
from distutils.util import strtobool

from ruamel.yaml import YAML


yaml_loader = YAML(typ='safe')


def to_bool(value):
    return bool(value if isinstance(value, bool) else strtobool(value))


def merge_dicts(*dicts):
    result = {}

    for dict_ in dicts:
        if dict_:
            result.update(dict_)

    return result


class MagicConfig:
    """Позволяет описывать классы конфиграции без дублирования ключей, с поддержкой значений по-умолчанию,
        а также использовать аннотации для приведения типов:

        >>> class Config(MagicConfig):
        >>>     APP_NAME: str
        >>>     DEBUG: bool
        >>>     TIMEOUT: int = 60
        >>>     ENVIRONMENT = 'DEV'

        >>> config = Config(params={'APP_NAME': 'test-app', 'DEBUG': 'true'})

        >>> assert config.APP_NAME == 'test-app'
        >>> assert config.DEBUG is True
        >>> assert config.TIMEOUT == 60
        >>> assert config.ENVIRONMENT == 'DEV'
    """

    def _get_value(self, attr, attr_type, annotations, attrs_info, params):
        if attr_type is bool:
            attr_type = to_bool

        if isinstance(attr_type, str):
            assert attr not in attrs_info, f'Reusable key "{attr}" can\'t be used with default value'

            new_params = {**params, attr_type: params[attr]} if attr in params else params

            return self._get_value(attr_type, annotations.get(attr_type, str), annotations, attrs_info, new_params)

        raw_value = params[attr] if attr in params else attrs_info[attr]

        if isinstance(raw_value, str) and attr_type is not str:
            attr_type = json.loads

        return attr_type(raw_value) if raw_value is not None else raw_value

    def _get_annotations(self):
        mro = inspect.getmro(type(self))
        annotations = [dict(inspect.getmembers(cls)).get('__annotations__', {}) for cls in mro]

        return merge_dicts(*reversed(annotations))

    def __init__(self, params: dict):
        self._params = params

        info = dict(inspect.getmembers(type(self)))
        annotations = self._get_annotations()

        for attr, attr_type in annotations.items():
            if not isinstance(info.get(attr), property):
                try:
                    value = self._get_value(attr, attr_type, annotations, info, params)
                except Exception as ex:
                    raise ValueError(f'Unable to parse value for attribute {attr}. all values: {params}')

                setattr(self, attr, value)

        for attr, value in info.items():
            if attr not in annotations and not attr.startswith('_') and not callable(value) \
                    and not isinstance(value, property):
                setattr(self, attr, params.get(attr, value))

    @classmethod
    def from_file(cls, filename, loader=yaml_loader) -> 'MagicConfig':
        """
        Инициализация конфига значениями из файла, а также значениями из переменных окружения.
        приоритет закрузки ключей: 'DEFAULT' -> указанное окружение -> переменные окружения.

        :param filename: имя файла
        :param loader: парсер файла, поддерживающий метод load(file_object),
                       по-умолчанию используется загрузчик yaml файлов
        """
        with open(filename) as f:
            raw_data = loader.load(f)

        prepared_data = merge_dicts(raw_data, os.environ)

        return cls(prepared_data)

