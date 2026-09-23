from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from .collector import MetadataValidationError, collector
from .registry import known_kinds

app = FastAPI(title="Model Metadata Collector")


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "registered_kinds": known_kinds()}


@app.post("/ingest")
async def ingest(request: Request) -> JSONResponse:
    raw = await request.body()
    try:
        record = collector.ingest_json(raw)
    except MetadataValidationError as exc:
        raise HTTPException(status_code=422, detail=exc.errors) from exc
    return JSONResponse(content=record.model_dump(mode="json"))


@app.get("/metadata/{kind}")
async def list_metadata(kind: str) -> list[dict]:
    if kind not in known_kinds():
        raise HTTPException(status_code=404, detail=f"Unknown metadata kind: {kind}")
    return [record.model_dump(mode="json") for record in collector.get_records(kind)]


@app.get("/stats")
async def stats() -> dict:
    return collector.stats()
