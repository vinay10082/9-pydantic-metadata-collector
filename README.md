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
Instructions for defining new metadata schemas and registering them within the central discriminated union registry.

## Testing & CI
Benchmark testing utilizing `pytest-benchmark` to ensure validation throughput meets latency Service Level Agreements (SLAs).
