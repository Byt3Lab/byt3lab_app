from __future__ import annotations
import logging
from core.module import ApplicationModule, Permission
from core.module.module import RoleDefinition
from .models.models import (
    Byt3labDivisionModel,
    Byt3labSolutionModel,
    Byt3labServiceModel,
    Byt3labProjectModel,
    Byt3labPartnerModel,
    Byt3labNgrafixModel,
    Byt3labTeamModel,
    Byt3labJobModel,
    Byt3labBlogCategoryModel,
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
            Permission(self, "byt3lab_app:read", "Consulter le tableau de bord et les contenus BYT3LAB"),
            Permission(self, "byt3lab_app:write", "Créer et modifier les contenus (services, produits, portfolio, etc.)"),
            Permission(self, "byt3lab_app:publish", "Publier et dépublier le contenu sur le site public"),
            Permission(self, "byt3lab_app:delete", "Supprimer des éléments de contenu"),
            Permission(self, "byt3lab_app:settings", "Modifier les coordonnées et réglages généraux du site"),
            Permission(self, "byt3lab_app:admin", "Administration complète et gestion du module BYT3LAB"),
        ]

    def _get_roles(self):
        mod_dir = getattr(self, "dirname", None) or "byt3lab_app"
        return [
            RoleDefinition(
                module=self,
                slug="byt3lab_reader",
                name="Lecteur BYT3LAB",
                description="Accès en lecture seule au tableau de bord, statistiques et contenus du module BYT3LAB.",
                permissions=[
                    f"{mod_dir}.byt3lab_app:read",
                ],
                is_system=True,
            ),
            RoleDefinition(
                module=self,
                slug="byt3lab_editor",
                name="Éditeur BYT3LAB",
                description="Gestion éditoriale complète : création, modification et publication des produits, services, réalisations, offres et articles.",
                permissions=[
                    f"{mod_dir}.byt3lab_app:read",
                    f"{mod_dir}.byt3lab_app:write",
                    f"{mod_dir}.byt3lab_app:publish",
                ],
                is_system=True,
            ),
            RoleDefinition(
                module=self,
                slug="byt3lab_admin",
                name="Administrateur BYT3LAB",
                description="Contrôle total du module BYT3LAB : contenus, suppressions, réglages généraux et administration.",
                permissions=[
                    f"{mod_dir}.byt3lab_app:read",
                    f"{mod_dir}.byt3lab_app:write",
                    f"{mod_dir}.byt3lab_app:publish",
                    f"{mod_dir}.byt3lab_app:delete",
                    f"{mod_dir}.byt3lab_app:settings",
                    f"{mod_dir}.byt3lab_app:admin",
                ],
                is_system=True,
            ),
        ]

    async def run_dev_migrations(self):
        """Crée automatiquement les tables SQL du module via app.db.create_all et applique les colonnes manquantes."""
        await self.app.db.create_all([
            Byt3labDivisionModel,
            Byt3labSolutionModel,
            Byt3labServiceModel,
            Byt3labProjectModel,
            Byt3labPartnerModel,
            Byt3labNgrafixModel,
            Byt3labTeamModel,
            Byt3labJobModel,
            Byt3labBlogCategoryModel,
            Byt3labPostModel,
            Byt3labMessageModel,
            Byt3labSettingModel,
        ])

        # Migration additive idempotente pour les nouvelles colonnes
        from sqlalchemy import text
        from .models.models import Byt3labTables
        alter_statements = [
            f"ALTER TABLE {Byt3labTables.SERVICES} ADD COLUMN IF NOT EXISTS featured_image VARCHAR(300)",
            f"ALTER TABLE {Byt3labTables.PROJECTS} ADD COLUMN IF NOT EXISTS url VARCHAR(300)",
            f"ALTER TABLE {Byt3labTables.PROJECTS} ADD COLUMN IF NOT EXISTS stack VARCHAR(250)",
            f"ALTER TABLE {Byt3labTables.PROJECTS} ADD COLUMN IF NOT EXISTS impact_fr TEXT",
            f"ALTER TABLE {Byt3labTables.PROJECTS} ADD COLUMN IF NOT EXISTS impact_en TEXT",
            f"ALTER TABLE {Byt3labTables.TEAM} ADD COLUMN IF NOT EXISTS linkedin VARCHAR(300)",
            f"ALTER TABLE {Byt3labTables.TEAM} ADD COLUMN IF NOT EXISTS github VARCHAR(300)",
            f"ALTER TABLE {Byt3labTables.JOBS} ADD COLUMN IF NOT EXISTS department_fr VARCHAR(100)",
            f"ALTER TABLE {Byt3labTables.JOBS} ADD COLUMN IF NOT EXISTS department_en VARCHAR(100)",
            f"ALTER TABLE {Byt3labTables.JOBS} ADD COLUMN IF NOT EXISTS experience_fr VARCHAR(100)",
            f"ALTER TABLE {Byt3labTables.JOBS} ADD COLUMN IF NOT EXISTS experience_en VARCHAR(100)",
            f"ALTER TABLE {Byt3labTables.JOBS} ADD COLUMN IF NOT EXISTS deadline_fr VARCHAR(100)",
            f"ALTER TABLE {Byt3labTables.JOBS} ADD COLUMN IF NOT EXISTS deadline_en VARCHAR(100)",
            f"ALTER TABLE {Byt3labTables.JOBS} ADD COLUMN IF NOT EXISTS order_num INTEGER DEFAULT 0",
            f"ALTER TABLE {Byt3labTables.DIVISIONS} ADD COLUMN IF NOT EXISTS expertise_list_en JSON",
            f"ALTER TABLE {Byt3labTables.DIVISIONS} ADD COLUMN IF NOT EXISTS technologies_list_en JSON",
            f"ALTER TABLE {Byt3labTables.DIVISIONS} ADD COLUMN IF NOT EXISTS services_list_en JSON",
            f"ALTER TABLE {Byt3labTables.DIVISIONS} ADD COLUMN IF NOT EXISTS industries_list_en JSON",
            f"ALTER TABLE {Byt3labTables.SOLUTIONS} ADD COLUMN IF NOT EXISTS features_list_en JSON",
            f"ALTER TABLE {Byt3labTables.SOLUTIONS} ADD COLUMN IF NOT EXISTS problems_list_en JSON",
            f"ALTER TABLE {Byt3labTables.SOLUTIONS} ADD COLUMN IF NOT EXISTS benefits_list_en JSON",
            f"ALTER TABLE {Byt3labTables.SOLUTIONS} ADD COLUMN IF NOT EXISTS image_url VARCHAR(300)",
            f"ALTER TABLE {Byt3labTables.JOBS} ADD COLUMN IF NOT EXISTS requirements_en JSON",
            f"ALTER TABLE {Byt3labTables.POSTS} ADD COLUMN IF NOT EXISTS category_id INTEGER REFERENCES {Byt3labTables.BLOG_CATEGORIES}(id) ON DELETE SET NULL",
            f"ALTER TABLE {Byt3labTables.POSTS} ADD COLUMN IF NOT EXISTS tags_fr VARCHAR(300)",
            f"ALTER TABLE {Byt3labTables.POSTS} ADD COLUMN IF NOT EXISTS tags_en VARCHAR(300)",
            f"ALTER TABLE {Byt3labTables.POSTS} ADD COLUMN IF NOT EXISTS reading_time_min INTEGER DEFAULT 3",
            f"ALTER TABLE {Byt3labTables.POSTS} ADD COLUMN IF NOT EXISTS is_featured BOOLEAN DEFAULT FALSE",
            f"ALTER TABLE {Byt3labTables.POSTS} ADD COLUMN IF NOT EXISTS views_count INTEGER DEFAULT 0",
            f"ALTER TABLE {Byt3labTables.POSTS} ADD COLUMN IF NOT EXISTS meta_title_fr VARCHAR(250)",
            f"ALTER TABLE {Byt3labTables.POSTS} ADD COLUMN IF NOT EXISTS meta_title_en VARCHAR(250)",
            f"ALTER TABLE {Byt3labTables.POSTS} ADD COLUMN IF NOT EXISTS meta_description_fr TEXT",
            f"ALTER TABLE {Byt3labTables.POSTS} ADD COLUMN IF NOT EXISTS meta_description_en TEXT",
            f"ALTER TABLE {Byt3labTables.POSTS} ADD COLUMN IF NOT EXISTS og_image VARCHAR(300)",
        ]
        try:
            async with self.app.db.get_session() as session:
                for sql in alter_statements:
                    try:
                        await session.execute(text(sql))
                    except Exception:
                        pass
                await session.commit()
        except Exception as e:
            logger.debug("Migration additive BYT3LAB: %s", e)

        # Seeding des données initiales si nécessaire
        try:
            async with self.app.db.get_session() as session:
                await ContentService.seed_initial_content(session)
                await session.commit()
        except Exception as e:
            logger.warning("Échec du seed initial BYT3LAB: %s", e)

    async def load(self):
        # 1. Enregistrement des permissions RBAC et des 3 rôles par défaut
        self.permissions = self._get_permissions()
        self.roles = self._get_roles()

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
            router.add_route("/posts", By3labAPIController.list_public_posts, methods=["GET"])

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

            # Admin Blog Categories
            router.add_route("/admin/blog-categories", By3labAPIController.list_admin_blog_categories, methods=["GET"])
            router.add_route("/admin/blog-categories", By3labAPIController.save_admin_blog_category, methods=["POST"])
            router.add_route("/admin/blog-categories/<id>", By3labAPIController.save_admin_blog_category, methods=["PUT"])
            router.add_route("/admin/blog-categories/<id>", By3labAPIController.delete_admin_blog_category, methods=["DELETE"])

            # Admin NGRAFIX
            router.add_route("/admin/ngrafix", By3labAPIController.list_admin_ngrafix, methods=["GET"])
            router.add_route("/admin/ngrafix", By3labAPIController.save_admin_ngrafix, methods=["POST"])
            router.add_route("/admin/ngrafix/<id>", By3labAPIController.save_admin_ngrafix, methods=["PUT"])
            router.add_route("/admin/ngrafix/<id>", By3labAPIController.delete_admin_ngrafix, methods=["DELETE"])

        # 5. Enregistrement des routes publiques du site Web MPA (bilingue SEO /lg-fr/... & /lg-en/... + routes directes)
        def _add_seo_route(path: str, handler):
            clean_path = path if path.startswith("/") else f"/{path}"
            if clean_path == "/":
                self.router.add_route("", handler, methods=["GET"])
                self.router.add_route("/", handler, methods=["GET"])
                for lp in ("/lg-fr", "/lg-en"):
                    self.router.add_route(lp, handler, methods=["GET"])
                    self.router.add_route(f"{lp}/", handler, methods=["GET"])
            else:
                no_slash = clean_path.rstrip("/")
                with_slash = f"{no_slash}/"
                self.router.add_route(no_slash, handler, methods=["GET"])
                self.router.add_route(with_slash, handler, methods=["GET"])
                for lp in ("/lg-fr", "/lg-en"):
                    self.router.add_route(f"{lp}{no_slash}", handler, methods=["GET"])
                    self.router.add_route(f"{lp}{with_slash}", handler, methods=["GET"])

        _add_seo_route("/", PublicWebController.home)
        _add_seo_route("/poles", PublicWebController.poles)
        _add_seo_route("/poles/software", PublicWebController.pole_software)
        _add_seo_route("/poles/web-services", PublicWebController.pole_web_services)
        _add_seo_route("/poles/equipment", PublicWebController.pole_equipment)
        _add_seo_route("/poles/ngrafix", PublicWebController.ngrafix)
        _add_seo_route("/solutions", PublicWebController.solutions)
        _add_seo_route("/produits/<slug>", PublicWebController.solution_detail)
        _add_seo_route("/services", PublicWebController.services)
        _add_seo_route("/services/<slug>", PublicWebController.service_detail)
        _add_seo_route("/realisations", PublicWebController.realisations)
        _add_seo_route("/realisations/<slug>", PublicWebController.project_detail)
        _add_seo_route("/a-propos", PublicWebController.a_propos)
        _add_seo_route("/equipe", PublicWebController.equipe)
        _add_seo_route("/equipe/<slug>", PublicWebController.team_detail)
        _add_seo_route("/carriere", PublicWebController.carriere)
        _add_seo_route("/carriere/<slug>", PublicWebController.job_detail)
        _add_seo_route("/partenaires", PublicWebController.partenaires)
        _add_seo_route("/contact", PublicWebController.contact)

        _add_seo_route("/blog", PublicWebController.blog)
        _add_seo_route("/blog/categorie/<slug>", PublicWebController.blog_category)
        _add_seo_route("/blog/tag/<tag>", PublicWebController.blog_tag)
        _add_seo_route("/blog/<slug>", PublicWebController.post_detail)

        # Flux RSS & SEO techniques
        self.router.add_route("/blog/rss.xml", PublicWebController.blog_rss, methods=["GET"])
        self.router.add_route("/lg-fr/blog/rss.xml", PublicWebController.blog_rss, methods=["GET"])
        self.router.add_route("/lg-en/blog/rss.xml", PublicWebController.blog_rss, methods=["GET"])
        self.router.add_route("/sitemap.xml", PublicWebController.sitemap_xml, methods=["GET"])
        self.router.add_route("/robots.txt", PublicWebController.robots_txt, methods=["GET"])

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
