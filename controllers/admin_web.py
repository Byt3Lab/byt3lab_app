from __future__ import annotations
import json
from core.routing import Request, Response, require_permission
from core.page_builder import Page, Component
from core.utils.permissions import check_user_permission
from base.components import admin_layout


class AdminWebController:
    """
    Contrôleur de la console d'administration « BYT3LAB Contenu ».
    Conforme au standard Module-as-SPA (§8.6 & §8.6.1 Mode 3 d'AGENTS.md).
    0 requête SQL dans le contrôleur Web : sert une seule fois la coquille SPA
    enrichie des templates pré-traduits Jinja2 et des composants ds_*.
    """

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:read")
    async def spa_shell(request: Request, response: Response):
        """Coquille SPA unique de l'administration BYT3LAB avec injection des droits RBAC."""
        user_raw = request.get_session("user_payload") or request.data_context.get("user_payload", None)
        user = json.loads(user_raw) if isinstance(user_raw, str) else (user_raw or {})
        is_sudo = bool(user.get("is_sudo"))

        perms = {
            "is_sudo": is_sudo,
            "read": is_sudo or check_user_permission(user, "byt3lab_app.byt3lab_app:read", request.app),
            "write": is_sudo or check_user_permission(user, "byt3lab_app.byt3lab_app:write", request.app),
            "publish": is_sudo or check_user_permission(user, "byt3lab_app.byt3lab_app:publish", request.app),
            "delete": is_sudo or check_user_permission(user, "byt3lab_app.byt3lab_app:delete", request.app),
            "settings": is_sudo or check_user_permission(user, "byt3lab_app.byt3lab_app:settings", request.app),
            "admin": is_sudo or check_user_permission(user, "byt3lab_app.byt3lab_app:admin", request.app),
        }

        content_comp = Component(
            module_name="byt3lab_app",
            name="admin/spa_shell",
            context={"user_perms_json": json.dumps(perms)},
        )
        root = admin_layout(content_comp)
        page = Page("BYT3LAB Contenu — Console d'Administration", root)
        return await response.render_page(page)
