from fastapi import APIRouter

from .docs import router as docs_router
from .pattern import router as pattern_router
from .pattern_node import router as pattern_node_router

router = APIRouter()
router.include_router(docs_router)
router.include_router(pattern_router)
router.include_router(pattern_node_router)
