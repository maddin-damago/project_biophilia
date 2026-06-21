import logging
from rich.console import Console
from rich.pretty import Pretty
from typing import Any


def print_my_data(title: str, data: Any):
    logger = logging.getLogger("uvicorn.error")

    logger.info(f"[DEBUG] {title.upper()}:")

    console = Console()
    console.print(Pretty(data, expand_all=True))

    print()
