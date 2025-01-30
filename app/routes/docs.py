import settings
from fastapi import APIRouter
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

router = APIRouter(prefix="/docs", include_in_schema=False)


@router.get("/")
def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="idoworkflows - Swagger UI",
        init_oauth={"clientId": settings.KEYCLOAK_CLIENT_ID},
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@router.get("/oauth2-redirect.html")
def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()
