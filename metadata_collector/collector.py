from collections import defaultdict

from pydantic import BaseModel, ValidationError

from .config import Settings, settings
from .registry import build_type_adapter


class MetadataValidationError(Exception):
    def __init__(self, errors: list[dict]):
        self.errors = errors
        super().__init__(str(errors))


class MetadataCollector:
    """Validates incoming metadata records and routes them by their `kind`."""

    def __init__(self, settings: Settings = settings):
        self._settings = settings
        self._adapter = build_type_adapter()
        self._buckets: dict[str, list[BaseModel]] = defaultdict(list)

    def ingest_json(self, raw: str | bytes) -> BaseModel:
        try:
            record = self._adapter.validate_json(
                raw, strict=self._settings.strict_validation_mode
            )
        except ValidationError as exc:
            raise MetadataValidationError(exc.errors()) from exc
        self._route(record)
        return record

    def ingest_dict(self, data: dict) -> BaseModel:
        try:
            record = self._adapter.validate_python(
                data, strict=self._settings.strict_validation_mode
            )
        except ValidationError as exc:
            raise MetadataValidationError(exc.errors()) from exc
        self._route(record)
        return record

    def _route(self, record: BaseModel) -> None:
        self._buckets[record.kind].append(record)

    def get_records(self, kind: str) -> list[BaseModel]:
        return list(self._buckets.get(kind, []))

    def stats(self) -> dict[str, int]:
        return {kind: len(records) for kind, records in self._buckets.items()}


collector = MetadataCollector()
