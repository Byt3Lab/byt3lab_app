from __future__ import annotations
import logging
from core.module import ApplicationModule, Permission
from .models.models import (
    Byt3labDivisionModel,
    Byt3labSolutionModel,
    Byt3labServiceModel,
    Byt3labProjectModel,
    Byt3labPartnerModel,
    Byt3labNgrafixModel,
    Byt3labTeamModel,
    Byt3labJobModel,
    Byt3labPostModel,
    Byt3labMessageModel,
    Byt3labSettingModel,
)
from .controllers.public_web import PublicWebController
from .controllers.admin_web import AdminWebController
from .controllers.api import By3labAPIController
from .services.content_service import ContentService

logger = logging.getLogger("byt3lab.module")


class Byt3labModule(ApplicationModule):
    """
    Module BYT3LAB — Site Institutionnel MPA & Console d'Administration SPA.
    Strictement conforme aux directives et standards architecturaux AGENTS.md.
    """

    def __init__(self):
        super().__init__(name="byt3lab_app", router_name="byt3lab_app")

    def _get_permissions(self):
        return [
            Permission(self, "byt3lab_app:read", "Consulter le contenu BYT3LAB"),
            Permission(self, "byt3lab_app:write", "Créer et modifier le contenu BYT3LAB"),
            Permission(self, "byt3lab_app:publish", "Publier et dépublier le contenu"),
            Permission(self, "byt3lab_app:admin", "Administration complète et réglages du site BYT3LAB"),
        ]

    async def run_dev_migrations(self):
        """Crée automatiquement les tables SQL du module via app.db.create_all."""
        await self.app.db.create_all([
            Byt3labDivisionModel,
            Byt3labSolutionModel,
            Byt3labServiceModel,
            Byt3labProjectModel,
            Byt3labPartnerModel,
            Byt3labNgrafixModel,
            Byt3labTeamModel,
            Byt3labJobModel,
            Byt3labPostModel,
            Byt3labMessageModel,
            Byt3labSettingModel,
        ])

        # Seeding des données initiales si nécessaire
        try:
            async with self.app.db.get_session() as session:
                await ContentService.seed_initial_content(session)
                await session.commit()
        except Exception as e:
            logger.warning("Échec du seed initial BYT3LAB: %s", e)

    async def load(self):
        # 1. Enregistrement des permissions RBAC
        self.permissions = self._get_permissions()

        # 2. Migrations automatiques en mode développement
        if self.app and hasattr(self.app, "server") and hasattr(self.app.server, "app") and self.app.server.app.debug:
            await self.run_dev_migrations()
        else:
            try:
                await self.run_dev_migrations()
            except Exception as e:
                logger.debug("Migration dev BYT3LAB ignorée: %s", e)

        # 3. Enregistrement de la route d'administration Web (SPA Shell unique)
        self.admin_router.add_route("", AdminWebController.spa_shell, methods=["GET"])
        self.admin_router.add_route("/", AdminWebController.spa_shell, methods=["GET"])

        # 4. Enregistrement des routes API REST (Publique et Admin SPA)
        for router in (self.api_admin_router, self.api_router):
            # Publique
            router.add_route("/contact", By3labAPIController.handle_contact_submission, methods=["POST"])
            router.add_route("/divisions", By3labAPIController.list_divisions, methods=["GET"])
            router.add_route("/solutions", By3labAPIController.list_solutions, methods=["GET"])
            router.add_route("/settings", By3labAPIController.get_settings, methods=["GET"])

            # Admin Dashboard
            router.add_route("/admin/dashboard", By3labAPIController.get_admin_dashboard, methods=["GET"])

            # Admin Messages (Inbox)
            router.add_route("/admin/messages", By3labAPIController.list_admin_messages, methods=["GET"])
            router.add_route("/admin/messages/<id>/status", By3labAPIController.update_admin_message_status, methods=["PUT"])
            router.add_route("/admin/messages/<id>", By3labAPIController.delete_admin_message, methods=["DELETE"])

            # Admin Settings
            router.add_route("/admin/settings", By3labAPIController.get_admin_settings, methods=["GET"])
            router.add_route("/admin/settings", By3labAPIController.save_admin_settings, methods=["POST"])

            # Admin Divisions
            router.add_route("/admin/divisions", By3labAPIController.list_admin_divisions, methods=["GET"])
            router.add_route("/admin/divisions", By3labAPIController.save_admin_division, methods=["POST"])
            router.add_route("/admin/divisions/<id>", By3labAPIController.save_admin_division, methods=["PUT"])
            router.add_route("/admin/divisions/<id>", By3labAPIController.delete_admin_division, methods=["DELETE"])

            # Admin Solutions
            router.add_route("/admin/solutions", By3labAPIController.list_admin_solutions, methods=["GET"])
            router.add_route("/admin/solutions", By3labAPIController.save_admin_solution, methods=["POST"])
            router.add_route("/admin/solutions/<id>", By3labAPIController.save_admin_solution, methods=["PUT"])
            router.add_route("/admin/solutions/<id>", By3labAPIController.delete_admin_solution, methods=["DELETE"])

            # Admin Services
            router.add_route("/admin/services", By3labAPIController.list_admin_services, methods=["GET"])
            router.add_route("/admin/services", By3labAPIController.save_admin_service, methods=["POST"])
            router.add_route("/admin/services/<id>", By3labAPIController.save_admin_service, methods=["PUT"])
            router.add_route("/admin/services/<id>", By3labAPIController.delete_admin_service, methods=["DELETE"])

            # Admin Projects
            router.add_route("/admin/projects", By3labAPIController.list_admin_projects, methods=["GET"])
            router.add_route("/admin/projects", By3labAPIController.save_admin_project, methods=["POST"])
            router.add_route("/admin/projects/<id>", By3labAPIController.save_admin_project, methods=["PUT"])
            router.add_route("/admin/projects/<id>", By3labAPIController.delete_admin_project, methods=["DELETE"])

            # Admin Partners
            router.add_route("/admin/partners", By3labAPIController.list_admin_partners, methods=["GET"])
            router.add_route("/admin/partners", By3labAPIController.save_admin_partner, methods=["POST"])
            router.add_route("/admin/partners/<id>", By3labAPIController.save_admin_partner, methods=["PUT"])
            router.add_route("/admin/partners/<id>", By3labAPIController.delete_admin_partner, methods=["DELETE"])

            # Admin Team
            router.add_route("/admin/team", By3labAPIController.list_admin_team, methods=["GET"])
            router.add_route("/admin/team", By3labAPIController.save_admin_team, methods=["POST"])
            router.add_route("/admin/team/<id>", By3labAPIController.save_admin_team, methods=["PUT"])
            router.add_route("/admin/team/<id>", By3labAPIController.delete_admin_team, methods=["DELETE"])

            # Admin Jobs
            router.add_route("/admin/jobs", By3labAPIController.list_admin_jobs, methods=["GET"])
            router.add_route("/admin/jobs", By3labAPIController.save_admin_job, methods=["POST"])
            router.add_route("/admin/jobs/<id>", By3labAPIController.save_admin_job, methods=["PUT"])
            router.add_route("/admin/jobs/<id>", By3labAPIController.delete_admin_job, methods=["DELETE"])

            # Admin Posts
            router.add_route("/admin/posts", By3labAPIController.list_admin_posts, methods=["GET"])
            router.add_route("/admin/posts", By3labAPIController.save_admin_post, methods=["POST"])
            router.add_route("/admin/posts/<id>", By3labAPIController.save_admin_post, methods=["PUT"])
            router.add_route("/admin/posts/<id>", By3labAPIController.delete_admin_post, methods=["DELETE"])

        # 5. Enregistrement des routes publiques du site Web MPA
        self.router.add_route("", PublicWebController.home, methods=["GET"])
        self.router.add_route("/", PublicWebController.home, methods=["GET"])

        self.router.add_route("/technologies", PublicWebController.technologies, methods=["GET"])
        self.router.add_route("/technologies/", PublicWebController.technologies, methods=["GET"])
        self.router.add_route("/technologies/<slug>", PublicWebController.division_detail, methods=["GET"])
        self.router.add_route("/technologies/<slug>/", PublicWebController.division_detail, methods=["GET"])

        self.router.add_route("/produits", PublicWebController.produits, methods=["GET"])
        self.router.add_route("/produits/", PublicWebController.produits, methods=["GET"])
        self.router.add_route("/produits/<slug>", PublicWebController.solution_detail, methods=["GET"])
        self.router.add_route("/produits/<slug>/", PublicWebController.solution_detail, methods=["GET"])

        self.router.add_route("/services", PublicWebController.services, methods=["GET"])
        self.router.add_route("/services/", PublicWebController.services, methods=["GET"])
        self.router.add_route("/services/<slug>", PublicWebController.service_detail, methods=["GET"])
        self.router.add_route("/services/<slug>/", PublicWebController.service_detail, methods=["GET"])

        self.router.add_route("/realisations", PublicWebController.realisations, methods=["GET"])
        self.router.add_route("/realisations/", PublicWebController.realisations, methods=["GET"])
        self.router.add_route("/realisations/<slug>", PublicWebController.project_detail, methods=["GET"])
        self.router.add_route("/realisations/<slug>/", PublicWebController.project_detail, methods=["GET"])

        self.router.add_route("/ngrafix", PublicWebController.ngrafix, methods=["GET"])
        self.router.add_route("/ngrafix/", PublicWebController.ngrafix, methods=["GET"])

        self.router.add_route("/recherche-innovation", PublicWebController.recherche_innovation, methods=["GET"])
        self.router.add_route("/recherche-innovation/", PublicWebController.recherche_innovation, methods=["GET"])

        self.router.add_route("/a-propos", PublicWebController.a_propos, methods=["GET"])
        self.router.add_route("/a-propos/", PublicWebController.a_propos, methods=["GET"])

        self.router.add_route("/equipe", PublicWebController.equipe, methods=["GET"])
        self.router.add_route("/equipe/", PublicWebController.equipe, methods=["GET"])
        self.router.add_route("/equipe/<slug>", PublicWebController.team_detail, methods=["GET"])
        self.router.add_route("/equipe/<slug>/", PublicWebController.team_detail, methods=["GET"])

        self.router.add_route("/carriere", PublicWebController.carriere, methods=["GET"])
        self.router.add_route("/carriere/", PublicWebController.carriere, methods=["GET"])
        self.router.add_route("/carriere/<slug>", PublicWebController.job_detail, methods=["GET"])
        self.router.add_route("/carriere/<slug>/", PublicWebController.job_detail, methods=["GET"])

        self.router.add_route("/partenaires", PublicWebController.partenaires, methods=["GET"])
        self.router.add_route("/partenaires/", PublicWebController.partenaires, methods=["GET"])

        self.router.add_route("/contact", PublicWebController.contact, methods=["GET"])
        self.router.add_route("/contact/", PublicWebController.contact, methods=["GET"])

        self.router.add_route("/blog", PublicWebController.blog, methods=["GET"])
        self.router.add_route("/blog/", PublicWebController.blog, methods=["GET"])
        self.router.add_route("/blog/<slug>", PublicWebController.post_detail, methods=["GET"])
        self.router.add_route("/blog/<slug>/", PublicWebController.post_detail, methods=["GET"])

        self.router.add_route("/404", PublicWebController.not_found, methods=["GET"])

        # 6. Déclaration auprès du WebSiteManager de MELODI
        if hasattr(self.app, "website_manager") and self.app.website_manager:
            self.register_webSite(infos={
                "name": "BYT3LAB",
                "description": "Site officiel du groupe Byt3Lab Technology & Innovation"
            })

        # 7. Enregistrement de la navigation dans la barre latérale d'administration MELODI
        self.register_navigation(
            id="byt3lab_app_admin",
            label="BYT3LAB Contenu",
            icon="name=language&fill=white",
            url="/admin/byt3lab_app",
            priority=60,
            children=[
                {"label": "Tableau de bord", "icon": "name=dashboard&fill=white", "url": "/admin/byt3lab_app#/"},
                {"label": "Boîte de réception", "icon": "name=inbox&fill=white", "url": "/admin/byt3lab_app#/inbox"},
                {"label": "Divisions", "icon": "name=layers&fill=white", "url": "/admin/byt3lab_app#/divisions"},
                {"label": "Solutions & Offres", "icon": "name=apps&fill=white", "url": "/admin/byt3lab_app#/solutions"},
                {"label": "Services", "icon": "name=build&fill=white", "url": "/admin/byt3lab_app#/services"},
                {"label": "Projets & Portfolio", "icon": "name=folder&fill=white", "url": "/admin/byt3lab_app#/projects"},
                {"label": "Partenaires", "icon": "name=handshake&fill=white", "url": "/admin/byt3lab_app#/partners"},
                {"label": "Équipe", "icon": "name=people&fill=white", "url": "/admin/byt3lab_app#/team"},
                {"label": "Carrières", "icon": "name=work&fill=white", "url": "/admin/byt3lab_app#/jobs"},
                {"label": "Articles de Blog", "icon": "name=article&fill=white", "url": "/admin/byt3lab_app#/posts"},
                {"label": "Réglages du site", "icon": "name=settings&fill=white", "url": "/admin/byt3lab_app#/settings"},
            ]
        )


module = Byt3labModule()
