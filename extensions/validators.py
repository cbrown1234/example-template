"""Pydantic model integration helpers."""

from typing import Any

import prompt_toolkit
from jinja2 import Environment
from jinja2.ext import Extension
from pydantic import BaseModel, RootModel, StrictStr, ValidationError

validation_toolbar_init = prompt_toolkit.widgets.ValidationToolbar.__init__


def validation_toolbar_init_patched(
    self: prompt_toolkit.widgets.ValidationToolbar, *args: tuple, **kwargs: dict
) -> None:
    """Wrap ValidationToolbar __init__ for patching."""
    validation_toolbar_init(self, *args, **kwargs)

    # Uncap validation message length to enable multiline error messages
    self.container.content.height = None


prompt_toolkit.widgets.ValidationToolbar.__init__ = validation_toolbar_init_patched


class Example(BaseModel):
    """Example."""

    a: StrictStr
    b: StrictStr
    c: StrictStr = '123'


class PerEnvConfig(BaseModel):
    """Config needed per environment."""

    db_host: str
    db_port: int


class EnvsConfig(RootModel[dict[str, PerEnvConfig]]):
    """Config for environment."""


models = {
    'example': Example,
    'envs_config': EnvsConfig,
}


def to_model(value: Any, model: type[BaseModel], **kwargs: dict) -> BaseModel:
    """Jinja filter for instantiating model instance.

    `{{ value | to_model(Example) }}`
    """
    return model.model_validate(value, strict=True, **kwargs)


def to_model_dict(value: Any, model: type[BaseModel], **kwargs: dict) -> dict:
    """Jinja filter for instantiating model instance as dictionary.

    `{{ value | to_model_dict(Example) }}`

    Useful if you want simpler usage in jinja, but supports default values etc
    """
    return model.model_validate(value, strict=True, **kwargs).model_dump()


def validate_as(value: Any, model: type[BaseModel]) -> str:
    """Jinja filter for model validation string in copier.yml.

    ```
    input:
      type: yaml
      multiline: true
      validator: {{ input | validate_as(Example) }}
    ```
    """
    try:
        model.model_validate(value, strict=True)
    except ValidationError as err:
        return str(err)
    return ''


def is_valid_as(model: type[BaseModel]) -> callable:
    """Construct jinja test for compatibility with model."""

    def test(value: dict) -> bool:
        try:
            model.model_validate(value, strict=True)
        except ValidationError:
            return False
        return True

    return test


def is_model_instance_test(model: type[BaseModel]) -> callable:
    """Construct jinja test for model instance."""

    def test(value: Any) -> bool:
        return isinstance(value, model)

    return test


class PydanticExtension(Extension):
    """Adds Pydantic models and helpers."""

    def __init__(self, environment: Environment) -> None:
        """Implement extension logic."""
        super().__init__(environment)

        # Enable lookup via alias
        environment.globals['models'] = models

        for model in models.values():
            # Add models to namespace for use with generic functions
            environment.globals[model.__name__] = model

            # Add generic functions
            # `{{ input | to_model(Example) }}` e.g. for default values
            environment.filters['to_model'] = to_model
            # `{{ input | to_model_dict(Example) }}` e.g. for default values
            environment.filters['to_model_dict'] = to_model_dict
            # `validator: {{ input | validate_as(Example) }}`
            environment.filters['validate_as'] = validate_as

            # Pre-create other helpers
            # `{% if input is Example %}`
            environment.tests[f'{model.__name__}'] = is_valid_as(model)
            # `{% if input is Example_Model %}`
            environment.tests[f'{model.__name__}_Model'] = is_model_instance_test(model)


if __name__ == '__main__':
    # Helpful for debugging
    for model in models.values():
        print(model.__name__)  # noqa: T201
