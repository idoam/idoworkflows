from fastapi import APIRouter

from .docs import router as docs_router
from .pattern import router as pattern_router

router = APIRouter()
router.include_router(docs_router)
router.include_router(pattern_router)
