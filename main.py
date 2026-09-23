import argparse
import json
import sys

from metadata_collector.collector import MetadataValidationError, collector
from metadata_collector.config import settings


def cmd_serve(_args: argparse.Namespace) -> None:
    import uvicorn

    uvicorn.run(
        "metadata_collector.app:app",
        host="0.0.0.0",
        port=settings.metadata_ingestion_port,
    )


def cmd_ingest_file(args: argparse.Namespace) -> None:
    ok, failed = 0, 0
    with open(args.path, "r", encoding="utf-8") as fh:
        for line_number, line in enumerate(fh, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                record = collector.ingest_json(line)
            except MetadataValidationError as exc:
                failed += 1
                print(f"[line {line_number}] validation failed: {exc.errors}", file=sys.stderr)
                continue
            ok += 1
            print(json.dumps(record.model_dump(mode="json")))
    print(f"\ningested {ok} record(s), {failed} failed", file=sys.stderr)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Model Metadata Collector")
    subparsers = parser.add_subparsers(dest="command")

    serve_parser = subparsers.add_parser("serve", help="Run the metadata ingestion HTTP server")
    serve_parser.set_defaults(func=cmd_serve)

    ingest_parser = subparsers.add_parser(
        "ingest-file", help="Validate and route a newline-delimited JSON (JSONL) file"
    )
    ingest_parser.add_argument("path", help="Path to a JSONL file of metadata records")
    ingest_parser.set_defaults(func=cmd_ingest_file)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if not getattr(args, "command", None):
        args.func = cmd_serve
    args.func(args)


if __name__ == "__main__":
    main()
