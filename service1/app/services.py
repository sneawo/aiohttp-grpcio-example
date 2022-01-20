import logging


logger = logging.getLogger(__name__)


async def process_name(*, name: str) -> str:
    name = name.upper()
    logger.info(f"action=process_name, status=success, name={name}")
    return name
