from fastapi import APIRouter

from .docs import router as docs_router
from .element import router as element_router
from .instance import router as instance_router

router = APIRouter()
router.include_router(docs_router)
router.include_router(instance_router)
router.include_router(element_router)
