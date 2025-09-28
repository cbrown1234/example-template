"""Pydantic model integration helpers."""

import prompt_toolkit
from jinja2 import Environment
from jinja2.ext import Extension
from pydantic import BaseModel, StrictStr, ValidationError

validation_toolbar_init = prompt_toolkit.widgets.ValidationToolbar.__init__


def validation_toolbar_init_patched(
    self: prompt_toolkit.widgets.ValidationToolbar, *args: tuple, **kwargs: dict
) -> None:
    """Wrap ValidationToolbar __init__ for patching."""
    validation_toolbar_init(self, *args, **kwargs)

    # Uncap validation message length to enable multiline error messages
    self.container.content.height = None


prompt_toolkit.widgets.ValidationToolbar.__init__ = validation_toolbar_init_patched


def copier_validator(model: BaseModel) -> callable:
    """Create Copier validator of model jinja filter.

    Creates a function that returns text of the error from creating
    an instance of the model

    Add as a jinja environment filter `example_validator_str`
    to use like so in copier.yml
    ```
    validated_example:
        type: yaml
        validator: "{{ validated_example | example_validator_str }}"
    ```
    """

    def validator(value: dict) -> str:
        """Single line error message for copier validator."""
        messages = []
        try:
            model.model_validate(value, strict=True)
        except ValidationError as err:
            messages = [f'{":".join(e["loc"])}: {e["msg"]}' for e in err.errors()]
        return '\n'.join(messages)

    return validator


def jinja_test(model: BaseModel) -> callable:
    """Add as jinja environment test."""

    def test(value: dict) -> bool:
        try:
            model.model_validate(value)
        except ValidationError:
            return False
        return True

    return test


def to(model: BaseModel) -> callable:
    """Create helper closure."""

    def to_model(value: dict) -> dict:
        """Convert to dict of model."""
        return dict(model.model_validate(value))

    return to_model


class Example(BaseModel):
    """Example."""

    a: StrictStr
    b: StrictStr
    c: StrictStr = '123'


models = {
    'example': Example,
}


class PydanticExtension(Extension):
    """Adds Pydantic model Copier helpers."""

    def __init__(self, environment: Environment) -> None:
        """Implement extension logic."""
        super().__init__(environment)
        for key, model in models.items():
            # `validator: '{{ input | example_validator_str }}'`
            environment.filters[f'{key}_validator_str'] = copier_validator(model)
            # `{{ input | to_example }}` e.g. support partial default values
            environment.filters[f'to_{key}'] = to(model)
            # `{% if input is example %}`
            environment.tests[key] = jinja_test(model)
