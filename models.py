"""Models for use in Copier jinja templates via extension."""

from pydantic import BaseModel, RootModel, StrictStr


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
