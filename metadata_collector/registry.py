from typing import Annotated, Union

from pydantic import BaseModel, Field, TypeAdapter

from .schemas import FileMetadata, SensorMetadata, TransactionMetadata

_REGISTRY: dict[str, type[BaseModel]] = {}


def register_schema(model: type[BaseModel]) -> type[BaseModel]:
    """Register a metadata model under its `kind` discriminator value."""
    kind = model.model_fields["kind"].default
    _REGISTRY[kind] = model
    return model


for _model in (SensorMetadata, FileMetadata, TransactionMetadata):
    register_schema(_model)


def known_kinds() -> list[str]:
    return list(_REGISTRY.keys())


def build_type_adapter() -> TypeAdapter:
    """Build the discriminated-union TypeAdapter from all currently registered schemas."""
    models = tuple(_REGISTRY.values())
    if not models:
        raise RuntimeError("No metadata schemas registered")
    if len(models) == 1:
        return TypeAdapter(models[0])
    union_type = Union[models]
    return TypeAdapter(Annotated[union_type, Field(discriminator="kind")])
