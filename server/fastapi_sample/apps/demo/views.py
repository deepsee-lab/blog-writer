from loguru import logger
from fastapi import APIRouter

router = APIRouter(
    prefix="/demo"
)


@router.get("/heartbeat")
def heartbeat():
    logger.info('run heartbeat')
    return 'heartbeat'
