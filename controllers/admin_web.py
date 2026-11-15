from __future__ import annotations
from core.routing import Request, Response
from core.page_builder import Page, Component
from base.components import admin_layout


class AdminWebController:
    """
    Contrôleur de la console d'administration « BYT3LAB Contenu ».
    Conforme au standard Module-as-SPA (§8.6 & §8.6.1 Mode 3 d'AGENTS.md).
    0 requête SQL dans le contrôleur Web : sert une seule fois la coquille SPA
    enrichie des templates pré-traduits Jinja2 et des composants ds_*.
    """

    @classmethod
    async def spa_shell(cls, request: Request, response: Response):
        """Coquille SPA unique de l'administration BYT3LAB."""
        content_comp = Component(module_name="byt3lab", name="admin/spa_shell")
        root = admin_layout(content_comp)
        page = Page("BYT3LAB Contenu — Console d'Administration", root)
        return await response.render_page(page)
