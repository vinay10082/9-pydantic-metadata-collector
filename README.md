# Model Metadata Collector

## Description
A high-performance metadata validation and routing engine engineered for massive data ingestion pipelines.

## Architecture Overview
Pydantic V2 implementation leveraging Rust-backed `model_validate_json()` and discriminated unions for O(1) schema routing.

## Prerequisites
* Python 3.11+
* `pydantic>=2.0`

## Environment Variables
* `STRICT_VALIDATION_MODE` (boolean)
* `METADATA_INGESTION_PORT`

## Quick Start & Usage

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and adjust values as needed.
3. Run the ingestion HTTP server (entry point is `main.py`):
   ```
   python main.py serve
   ```
   This starts the server on `METADATA_INGESTION_PORT`, exposing:
   * `POST /ingest` — validate and route a raw JSON metadata record
   * `GET /metadata/{kind}` — list validated records collected for a given schema kind
   * `GET /stats` — record counts per schema kind
   * `GET /health` — service status and registered schema kinds

4. Alternatively, batch-validate a newline-delimited JSON (JSONL) file without starting a server:
   ```
   python main.py ingest-file path/to/records.jsonl
   ```

### Defining new metadata schemas
Add a new `pydantic.BaseModel` subclass to [metadata_collector/schemas.py](metadata_collector/schemas.py) with a `kind: Literal["your_kind"]` discriminator field, then register it in [metadata_collector/registry.py](metadata_collector/registry.py) by adding it to the tuple passed to `register_schema`. The discriminated union `TypeAdapter` is rebuilt automatically from the registry.
