from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
api_router = APIRouter()
api_router.include_router(auth_router)


from app.api.v1.crm import router as crm_router
api_router.include_router(crm_router)

from app.api.v1.automations import router as automations_router
api_router.include_router(automations_router)

from app.api.v1.whatsapp_dashboard import router as whatsapp_dashboard_router
api_router.include_router(whatsapp_dashboard_router)

from app.api.v1.whatsapp_leads import router as whatsapp_leads_router
api_router.include_router(whatsapp_leads_router)

from app.api.v1.site_intake import router as site_intake_router
api_router.include_router(site_intake_router)

from app.api.v1.whatsapp_messages import router as whatsapp_messages_router
api_router.include_router(whatsapp_messages_router)

from app.api.v1.instagram_messages import router as instagram_messages_router
api_router.include_router(instagram_messages_router)
