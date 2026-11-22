"""CLI entrypoint for ToolForge Pro."""
from __future__ import annotations

import json
from .pipeline import run_pipeline


def main() -> None:
    print(json.dumps(run_pipeline(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
