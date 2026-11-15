from __future__ import annotations
from datetime import datetime
from core.routing import Request, Response
from core.page_builder import Page, Component
from ..services.settings_service import SettingsService
from ..repositories.division_repository import DivisionRepository
from ..repositories.solution_repository import SolutionRepository
from ..repositories.service_repository import ServiceRepository
from ..repositories.project_repository import ProjectRepository
from ..repositories.partner_repository import PartnerRepository
from ..repositories.ngrafix_repository import NgrafixRepository
from ..repositories.team_repository import TeamRepository
from ..repositories.job_repository import JobRepository
from ..repositories.post_repository import PostRepository


class PublicWebController:
    """
    Contrôleur Web MPA pour le site institutionnel public de BYT3LAB.
    Rendu serveur pur avec le PageBuilder propriétaire de MELODI.
    """

    @classmethod
    def _get_lang(cls, request: Request) -> str:
        try:
            query = getattr(request, "query", {}) or {}
            req_lang = query.get("lang")
            if req_lang in ("fr", "en"):
                if hasattr(request, "session") and request.session is not None:
                    request.session["lang"] = req_lang
                return req_lang
        except Exception:
            pass
        lang = (request.session or {}).get("lang")
        if not lang and hasattr(request.app, "config"):
            lang = getattr(request.app.config, "LANG", "fr")
        return lang or "fr"

    @classmethod
    def _get_site_prefix(cls, request: Request) -> str:
        # Si le site est actif au niveau racine, préfixe vide, sinon /byt3lab
        ws_mgr = getattr(request.app, "website_manager", None)
        if ws_mgr and getattr(ws_mgr, "site_active", None) == "byt3lab":
            return ""
        return "/byt3lab"

    @classmethod
    async def _build_base_context(cls, request: Request, active_nav: str = "") -> dict:
        lang = cls._get_lang(request)
        site_prefix = cls._get_site_prefix(request)
        async with request.app.db.get_session() as session:
            settings = await SettingsService.get_public_settings(session, lang=lang)
            divisions = await DivisionRepository.get_all(session, published_only=True)
            header_divisions = [d.to_dict(lang=lang) for d in divisions]

        return {
            "current_lang": lang,
            "site_prefix": site_prefix,
            "request_path": getattr(request, "path", "/"),
            "active_nav": active_nav,
            "settings": settings,
            "header_divisions": header_divisions,
            "current_year": datetime.now().year,
        }

    # 1. Accueil
    @classmethod
    async def home(cls, request: Request, response: Response):
        ctx = await cls._build_base_context(request, active_nav="home")
        lang = ctx["current_lang"]
        async with request.app.db.get_session() as session:
            divisions = await DivisionRepository.get_all(session, published_only=True)
            solutions = await SolutionRepository.get_all(session, published_only=True)
            projects = await ProjectRepository.get_all(session, published_only=True)
            partners = await PartnerRepository.get_all(session, published_only=True)

        ctx.update({
            "divisions": [d.to_dict(lang=lang) for d in divisions],
            "solutions": [s.to_dict(lang=lang) for s in solutions],
            "projects": [p.to_dict(lang=lang) for p in projects],
            "partners": [p.to_dict(lang=lang) for p in partners],
            "page_title": "Concevoir les technologies de demain",
        })

        comp = Component(module_name="byt3lab", name="public/home", context=ctx)
        page = Page(ctx["page_title"], comp)
        return await response.render_page(page)

    # 2. Technologies & Divisions
    @classmethod
    async def technologies(cls, request: Request, response: Response):
        ctx = await cls._build_base_context(request, active_nav="technologies")
        lang = ctx["current_lang"]
        async with request.app.db.get_session() as session:
            divisions = await DivisionRepository.get_all(session, published_only=True)

        ctx.update({
            "divisions": [d.to_dict(lang=lang) for d in divisions],
            "page_title": "Divisions Technologiques",
        })
        comp = Component(module_name="byt3lab", name="public/technologies", context=ctx)
        page = Page(ctx["page_title"], comp)
        return await response.render_page(page)

    @classmethod
    async def division_detail(cls, request: Request, response: Response):
        slug = (request.params or {}).get("slug")
        ctx = await cls._build_base_context(request, active_nav="technologies")
        lang = ctx["current_lang"]
        async with request.app.db.get_session() as session:
            division = await DivisionRepository.get_by_slug(session, slug)
            if not division:
                return await cls.not_found(request, response)
            related_solutions = await SolutionRepository.get_by_division(session, slug)

        ctx.update({
            "division": division.to_dict(lang=lang),
            "related_solutions": [s.to_dict(lang=lang) for s in related_solutions],
            "page_title": division.title_en if lang == "en" else division.title_fr,
        })
        comp = Component(module_name="byt3lab", name="public/division_detail", context=ctx)
        page = Page(ctx["page_title"], comp)
        return await response.render_page(page)

    # 3. Produits & Solutions
    @classmethod
    async def produits(cls, request: Request, response: Response):
        ctx = await cls._build_base_context(request, active_nav="produits")
        lang = ctx["current_lang"]
        async with request.app.db.get_session() as session:
            solutions = await SolutionRepository.get_all(session, published_only=True)

        ctx.update({
            "solutions": [s.to_dict(lang=lang) for s in solutions],
            "page_title": "Produits & Solutions",
        })
        comp = Component(module_name="byt3lab", name="public/produits", context=ctx)
        page = Page(ctx["page_title"], comp)
        return await response.render_page(page)

    @classmethod
    async def solution_detail(cls, request: Request, response: Response):
        slug = (request.params or {}).get("slug")
        ctx = await cls._build_base_context(request, active_nav="produits")
        lang = ctx["current_lang"]
        async with request.app.db.get_session() as session:
            solution = await SolutionRepository.get_by_slug(session, slug)
            if not solution:
                return await cls.not_found(request, response)

        ctx.update({
            "solution": solution.to_dict(lang=lang),
            "page_title": solution.title_en if lang == "en" else solution.title_fr,
        })
        comp = Component(module_name="byt3lab", name="public/solution_detail", context=ctx)
        page = Page(ctx["page_title"], comp)
        return await response.render_page(page)

    # 4. Services
    @classmethod
    async def services(cls, request: Request, response: Response):
        ctx = await cls._build_base_context(request, active_nav="services")
        lang = ctx["current_lang"]
        async with request.app.db.get_session() as session:
            services = await ServiceRepository.get_all(session, published_only=True)

        ctx.update({
            "services": [s.to_dict(lang=lang) for s in services],
            "page_title": "Services d'Ingénierie",
        })
        comp = Component(module_name="byt3lab", name="public/services", context=ctx)
        page = Page(ctx["page_title"], comp)
        return await response.render_page(page)

    @classmethod
    async def service_detail(cls, request: Request, response: Response):
        slug = (request.params or {}).get("slug")
        ctx = await cls._build_base_context(request, active_nav="services")
        lang = ctx["current_lang"]
        async with request.app.db.get_session() as session:
            service = await ServiceRepository.get_by_slug(session, slug)
            if not service:
                return await cls.not_found(request, response)

        ctx.update({
            "service": service.to_dict(lang=lang),
            "page_title": service.title_en if lang == "en" else service.title_fr,
        })
        comp = Component(module_name="byt3lab", name="public/service_detail", context=ctx)
        page = Page(ctx["page_title"], comp)
        return await response.render_page(page)

    # 5. Réalisations & Projets
    @classmethod
    async def realisations(cls, request: Request, response: Response):
        ctx = await cls._build_base_context(request, active_nav="realisations")
        lang = ctx["current_lang"]
        async with request.app.db.get_session() as session:
            projects = await ProjectRepository.get_all(session, published_only=True)

        ctx.update({
            "projects": [p.to_dict(lang=lang) for p in projects],
            "page_title": "Réalisations & Portfolio",
        })
        comp = Component(module_name="byt3lab", name="public/realisations", context=ctx)
        page = Page(ctx["page_title"], comp)
        return await response.render_page(page)

    @classmethod
    async def project_detail(cls, request: Request, response: Response):
        slug = (request.params or {}).get("slug")
        ctx = await cls._build_base_context(request, active_nav="realisations")
        lang = ctx["current_lang"]
        async with request.app.db.get_session() as session:
            project = await ProjectRepository.get_by_slug(session, slug)
            if not project:
                return await cls.not_found(request, response)

        ctx.update({
            "project": project.to_dict(lang=lang),
            "page_title": project.title_en if lang == "en" else project.title_fr,
        })
        comp = Component(module_name="byt3lab", name="public/project_detail", context=ctx)
        page = Page(ctx["page_title"], comp)
        return await response.render_page(page)

    # 6. NGRAFIX Studio
    @classmethod
    async def ngrafix(cls, request: Request, response: Response):
        ctx = await cls._build_base_context(request, active_nav="ngrafix")
        lang = ctx["current_lang"]
        async with request.app.db.get_session() as session:
            ngrafix_items = await NgrafixRepository.get_all(session, published_only=True)

        ctx.update({
            "is_ngrafix": True,
            "ngrafix_items": [i.to_dict(lang=lang) for i in ngrafix_items],
            "page_title": "NGRAFIX — Studio Créatif & Brand Experience",
        })
        comp = Component(module_name="byt3lab", name="public/ngrafix", context=ctx)
        page = Page(ctx["page_title"], comp)
        return await response.render_page(page)

    # 7. Recherche & Innovation
    @classmethod
    async def recherche_innovation(cls, request: Request, response: Response):
        ctx = await cls._build_base_context(request, active_nav="recherche-innovation")
        ctx["page_title"] = "Recherche & Innovation"
        comp = Component(module_name="byt3lab", name="public/recherche_innovation", context=ctx)
        page = Page(ctx["page_title"], comp)
        return await response.render_page(page)

    # 8. À Propos
    @classmethod
    async def a_propos(cls, request: Request, response: Response):
        ctx = await cls._build_base_context(request, active_nav="a-propos")
        ctx["page_title"] = "À Propos du Groupe"
        comp = Component(module_name="byt3lab", name="public/a_propos", context=ctx)
        page = Page(ctx["page_title"], comp)
        return await response.render_page(page)

    # 9. Équipe
    @classmethod
    async def equipe(cls, request: Request, response: Response):
        ctx = await cls._build_base_context(request, active_nav="equipe")
        lang = ctx["current_lang"]
        async with request.app.db.get_session() as session:
            members = await TeamRepository.get_all(session, published_only=True)

        ctx.update({
            "team_members": [m.to_dict(lang=lang) for m in members],
            "page_title": "Équipe & Gouvernance",
        })
        comp = Component(module_name="byt3lab", name="public/equipe", context=ctx)
        page = Page(ctx["page_title"], comp)
        return await response.render_page(page)

    @classmethod
    async def team_detail(cls, request: Request, response: Response):
        slug = (request.params or {}).get("slug")
        ctx = await cls._build_base_context(request, active_nav="equipe")
        lang = ctx["current_lang"]
        async with request.app.db.get_session() as session:
            member = await TeamRepository.get_by_slug(session, slug)
            if not member:
                return await cls.not_found(request, response)

        ctx.update({
            "member": member.to_dict(lang=lang),
            "page_title": member.name,
        })
        comp = Component(module_name="byt3lab", name="public/team_detail", context=ctx)
        page = Page(ctx["page_title"], comp)
        return await response.render_page(page)

    # 10. Carrières
    @classmethod
    async def carriere(cls, request: Request, response: Response):
        ctx = await cls._build_base_context(request, active_nav="carriere")
        lang = ctx["current_lang"]
        async with request.app.db.get_session() as session:
            jobs = await JobRepository.get_all(session, published_only=True)

        ctx.update({
            "jobs": [j.to_dict(lang=lang) for j in jobs],
            "page_title": "Carrières & Recrutement",
        })
        comp = Component(module_name="byt3lab", name="public/carriere", context=ctx)
        page = Page(ctx["page_title"], comp)
        return await response.render_page(page)

    @classmethod
    async def job_detail(cls, request: Request, response: Response):
        slug = (request.params or {}).get("slug")
        ctx = await cls._build_base_context(request, active_nav="carriere")
        lang = ctx["current_lang"]
        async with request.app.db.get_session() as session:
            job = await JobRepository.get_by_slug(session, slug)
            if not job:
                return await cls.not_found(request, response)

        ctx.update({
            "job": job.to_dict(lang=lang),
            "page_title": job.title_en if lang == "en" else job.title_fr,
        })
        comp = Component(module_name="byt3lab", name="public/job_detail", context=ctx)
        page = Page(ctx["page_title"], comp)
        return await response.render_page(page)

    # 11. Partenaires
    @classmethod
    async def partenaires(cls, request: Request, response: Response):
        ctx = await cls._build_base_context(request, active_nav="partenaires")
        lang = ctx["current_lang"]
        async with request.app.db.get_session() as session:
            partners = await PartnerRepository.get_all(session, published_only=True)

        ctx.update({
            "partners": [p.to_dict(lang=lang) for p in partners],
            "page_title": "Partenaires & Alliances",
        })
        comp = Component(module_name="byt3lab", name="public/partenaires", context=ctx)
        page = Page(ctx["page_title"], comp)
        return await response.render_page(page)

    # 12. Contact
    @classmethod
    async def contact(cls, request: Request, response: Response):
        ctx = await cls._build_base_context(request, active_nav="contact")
        subject = getattr(request, "args", {}).get("subject", "")
        ctx.update({
            "prefilled_subject": subject,
            "page_title": "Contact & Siège",
        })
        comp = Component(module_name="byt3lab", name="public/contact", context=ctx)
        page = Page(ctx["page_title"], comp)
        return await response.render_page(page)

    # 13. Blog & Articles
    @classmethod
    async def blog(cls, request: Request, response: Response):
        ctx = await cls._build_base_context(request, active_nav="blog")
        lang = ctx["current_lang"]
        async with request.app.db.get_session() as session:
            posts = await PostRepository.get_all(session, published_only=True)

        ctx.update({
            "posts": [p.to_dict(lang=lang) for p in posts],
            "page_title": "Blog & Actualités Technologiques",
        })
        comp = Component(module_name="byt3lab", name="public/blog", context=ctx)
        page = Page(ctx["page_title"], comp)
        return await response.render_page(page)

    @classmethod
    async def post_detail(cls, request: Request, response: Response):
        slug = (request.params or {}).get("slug")
        ctx = await cls._build_base_context(request, active_nav="blog")
        lang = ctx["current_lang"]
        async with request.app.db.get_session() as session:
            post = await PostRepository.get_by_slug(session, slug)
            if not post:
                return await cls.not_found(request, response)

        ctx.update({
            "post": post.to_dict(lang=lang),
            "page_title": post.title_en if lang == "en" else post.title_fr,
        })
        comp = Component(module_name="byt3lab", name="public/post_detail", context=ctx)
        page = Page(ctx["page_title"], comp)
        return await response.render_page(page)

    # 14. Page 404
    @classmethod
    async def not_found(cls, request: Request, response: Response):
        ctx = await cls._build_base_context(request)
        ctx["page_title"] = "Page Non Trouvée (404)"
        comp = Component(module_name="byt3lab", name="public/not_found", context=ctx)
        page = Page(ctx["page_title"], comp)
        return await response.render_page(page)
