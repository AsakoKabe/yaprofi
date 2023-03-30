from app.endpoints.ping import api_router as application_health_router
from app.endpoints.group import api_router as application_promo


list_of_routes = [
    application_health_router,
    application_promo,
]


__all__ = [
    "list_of_routes",
]
