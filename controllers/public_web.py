from __future__ import annotations
import math
from datetime import datetime
from core.routing import Request, Response
from core.page_builder import Page, Component
from ..services.settings_service import SettingsService
from ..services.blog_service import BlogService
from ..services.seo_service import SeoService
from ..repositories.division_repository import DivisionRepository
from ..repositories.solution_repository import SolutionRepository
from ..repositories.service_repository import ServiceRepository
from ..repositories.project_repository import ProjectRepository
from ..repositories.partner_repository import PartnerRepository
from ..repositories.ngrafix_repository import NgrafixRepository
from ..repositories.team_repository import TeamRepository
from ..repositories.job_repository import JobRepository
from ..repositories.post_repository import PostRepository
from ..repositories.blog_category_repository import BlogCategoryRepository


class PublicWebController:
    """
    Contrôleur Web MPA pour le site institutionnel public de BYT3LAB.
    Rendu serveur pur avec le PageBuilder propriétaire de MELODI.
    """

    @classmethod
    def _get_base_prefix(cls, request: Request) -> str:
        ws_mgr = getattr(request.app, "website_manager", None)
        if ws_mgr and getattr(ws_mgr, "site_active", None) in ("byt3lab", "byt3lab_app"):
            return ""
        return "/byt3lab_app"

    @classmethod
    def _get_lang(cls, request: Request) -> str:
        path = getattr(request, "path", "") or "/"
        for code in ("fr", "en"):
            marker = f"/lg-{code}"
            if path == marker or path.startswith(f"{marker}/") or f"{marker}/" in path or path.endswith(marker):
                try:
                    if hasattr(request, "session") and request.session is not None:
                        request.session["lang"] = code
                except Exception:
                    pass
                return code

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
        return lang if lang in ("fr", "en") else "fr"

    @classmethod
    def _get_site_prefix(cls, request: Request, lang: str = None) -> str:
        base_prefix = cls._get_base_prefix(request)
        resolved_lang = lang or cls._get_lang(request)
        return f"{base_prefix}/lg-{resolved_lang}"

    @classmethod
    def _get_base_url(cls, request: Request) -> str:
        headers = getattr(request, "headers", {}) or {}
        host = headers.get("x-forwarded-host") or headers.get("host") or "localhost:3000"
        proto = headers.get("x-forwarded-proto") or getattr(request, "scheme", None) or "http"
        return f"{proto}://{host}".rstrip("/")

    @classmethod
    def _compute_seo_urls(cls, request: Request, lang: str) -> dict:
        base_prefix = cls._get_base_prefix(request)
        raw_path = getattr(request, "path", "/") or "/"
        rel = raw_path
        if base_prefix and rel.startswith(base_prefix):
            rel = rel[len(base_prefix):] or "/"
        for lp in ("/lg-fr", "/lg-en"):
            if rel == lp:
                rel = "/"
                break
            if rel.startswith(f"{lp}/"):
                rel = rel[len(lp):]
                break
        if not rel.startswith("/"):
            rel = f"/{rel}"
        alt_fr_path = f"{base_prefix}/lg-fr{rel}"
        alt_en_path = f"{base_prefix}/lg-en{rel}"
        base_url = cls._get_base_url(request)
        return {
            "base_url": base_url,
            "alt_fr_url": alt_fr_path,
            "alt_en_url": alt_en_path,
            "alt_fr_full": f"{base_url}{alt_fr_path}",
            "alt_en_full": f"{base_url}{alt_en_path}",
            "canonical_url": f"{base_url}{base_prefix}/lg-{lang}{rel}",
        }

    @classmethod
    async def _build_base_context(cls, request: Request, active_nav: str = "") -> dict:
        lang = cls._get_lang(request)
        site_prefix = cls._get_site_prefix(request, lang=lang)
        seo_urls = cls._compute_seo_urls(request, lang)
        async with request.app.db.get_session() as session:
            settings = await SettingsService.get_public_settings(session, lang=lang)
            divisions = await DivisionRepository.get_all(session, published_only=True)
            header_divisions = [d.to_dict(lang=lang) for d in divisions]

        return {
            "current_lang": lang,
            "site_prefix": site_prefix,
            "base_prefix": cls._get_base_prefix(request),
            "request_path": getattr(request, "path", "/"),
            "active_nav": active_nav,
            "settings": settings,
            "header_divisions": header_divisions,
            "current_year": datetime.now().year,
            **seo_urls,
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

        comp = Component(module_name="byt3lab_app", name="public/home", context=ctx)
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
        comp = Component(module_name="byt3lab_app", name="public/technologies", context=ctx)
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
        comp = Component(module_name="byt3lab_app", name="public/division_detail", context=ctx)
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
        comp = Component(module_name="byt3lab_app", name="public/produits", context=ctx)
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
        comp = Component(module_name="byt3lab_app", name="public/solution_detail", context=ctx)
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
        comp = Component(module_name="byt3lab_app", name="public/services", context=ctx)
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
        comp = Component(module_name="byt3lab_app", name="public/service_detail", context=ctx)
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
        comp = Component(module_name="byt3lab_app", name="public/realisations", context=ctx)
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
        comp = Component(module_name="byt3lab_app", name="public/project_detail", context=ctx)
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
        comp = Component(module_name="byt3lab_app", name="public/ngrafix", context=ctx)
        page = Page(ctx["page_title"], comp)
        return await response.render_page(page)

    # 7. À Propos
    @classmethod
    async def a_propos(cls, request: Request, response: Response):
        ctx = await cls._build_base_context(request, active_nav="a-propos")
        ctx["page_title"] = "À Propos du Groupe"
        comp = Component(module_name="byt3lab_app", name="public/a_propos", context=ctx)
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
        comp = Component(module_name="byt3lab_app", name="public/equipe", context=ctx)
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
        comp = Component(module_name="byt3lab_app", name="public/team_detail", context=ctx)
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
        comp = Component(module_name="byt3lab_app", name="public/carriere", context=ctx)
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
        comp = Component(module_name="byt3lab_app", name="public/job_detail", context=ctx)
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
        comp = Component(module_name="byt3lab_app", name="public/partenaires", context=ctx)
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
        comp = Component(module_name="byt3lab_app", name="public/contact", context=ctx)
        page = Page(ctx["page_title"], comp)
        return await response.render_page(page)

    # 13. Blog & Articles (Pagination, Recherche, Catégories, Tags, Commentaires, JSON-LD)
    @classmethod
    async def _render_blog_listing(
        cls,
        request: Request,
        response: Response,
        *,
        category_slug: str = "",
        tag: str = "",
    ):
        ctx = await cls._build_base_context(request, active_nav="blog")
        lang = ctx["current_lang"]
        query = getattr(request, "query", {}) or getattr(request, "args", {}) or {}
        q = str(query.get("q") or "").strip()
        if not category_slug:
            category_slug = str(query.get("categorie") or query.get("category") or "").strip()
        try:
            page_num = max(1, int(query.get("page") or 1))
        except Exception:
            page_num = 1
        per_page = 9

        async with request.app.db.get_session() as session:
            categories = await BlogCategoryRepository.get_with_counts(session, lang=lang)
            posts, total = await PostRepository.search_paginated(
                session,
                q=q,
                category_slug=category_slug,
                tag=tag,
                page=page_num,
                per_page=per_page,
                published_only=True,
            )
            active_category = None
            if category_slug:
                cat_obj = await BlogCategoryRepository.get_by_slug(session, category_slug)
                if cat_obj:
                    active_category = cat_obj.to_dict(lang=lang)

        total_pages = max(1, math.ceil(total / per_page))
        posts_dicts = [p.to_dict(lang=lang) for p in posts]
        featured_post = None
        if page_num == 1 and not q and not category_slug and not tag and posts_dicts:
            featured_post = next((p for p in posts_dicts if p.get("is_featured")), None) or posts_dicts[0]

        page_title = "Blog & Tech Insights" if lang == "en" else "Blog & Actualités Technologiques"
        if active_category:
            page_title = f"{active_category['name']} — {page_title}"
        elif tag:
            page_title = f"#{tag} — {page_title}"

        ctx.update({
            "posts": posts_dicts,
            "featured_post": featured_post,
            "categories": categories,
            "active_category": active_category,
            "active_category_slug": category_slug,
            "active_tag": tag,
            "search_query": q,
            "current_page": page_num,
            "total_pages": total_pages,
            "total_posts": total,
            "page_title": page_title,
        })
        comp = Component(module_name="byt3lab_app", name="public/blog", context=ctx)
        page = Page(ctx["page_title"], comp)
        return await response.render_page(page)

    @classmethod
    async def blog(cls, request: Request, response: Response):
        return await cls._render_blog_listing(request, response)

    @classmethod
    async def blog_category(cls, request: Request, response: Response):
        slug = (request.params or {}).get("slug", "")
        return await cls._render_blog_listing(request, response, category_slug=slug)

    @classmethod
    async def blog_tag(cls, request: Request, response: Response):
        tag = (request.params or {}).get("tag", "")
        return await cls._render_blog_listing(request, response, tag=tag)

    @classmethod
    async def post_detail(cls, request: Request, response: Response):
        slug = (request.params or {}).get("slug")
        ctx = await cls._build_base_context(request, active_nav="blog")
        lang = ctx["current_lang"]
        async with request.app.db.get_session() as session:
            post = await PostRepository.get_by_slug(session, slug)
            if not post:
                return await cls.not_found(request, response)
            post_dict = post.to_dict(lang=lang)
            post_dict["views_count"] = (post_dict.get("views_count") or 0) + 1
            related = await PostRepository.get_related(session, post, limit=3)
            related_dicts = [r.to_dict(lang=lang) for r in related]
            await PostRepository.increment_views(session, post.id)
            await session.commit()

        json_ld = BlogService.build_blog_posting_jsonld(
            post_dict,
            canonical_url=ctx["canonical_url"],
            base_url=ctx["base_url"],
        )
        ctx.update({
            "post": post_dict,
            "related_posts": related_dicts,
            "page_title": post_dict["meta_title"],
            "meta_description": post_dict["meta_description"],
            "og_image": post_dict["og_image"],
            "og_type": "article",
            "json_ld": json_ld,
        })
        comp = Component(module_name="byt3lab_app", name="public/post_detail", context=ctx)
        page = Page(ctx["page_title"], comp)
        return await response.render_page(page)

    # 14. Endpoints SEO (sitemap.xml, robots.txt, blog/rss.xml)
    @classmethod
    async def sitemap_xml(cls, request: Request, response: Response):
        base_url = f"{cls._get_base_url(request)}{cls._get_base_prefix(request)}"
        async with request.app.db.get_session() as session:
            xml = await SeoService.generate_sitemap_xml(session, base_url=base_url)
        return await response.make_response(
            xml,
            status=200,
            headers={"Content-Type": "application/xml; charset=utf-8"},
        )

    @classmethod
    async def robots_txt(cls, request: Request, response: Response):
        base_url = f"{cls._get_base_url(request)}{cls._get_base_prefix(request)}"
        txt = SeoService.generate_robots_txt(base_url=base_url)
        return await response.make_response(
            txt,
            status=200,
            headers={"Content-Type": "text/plain; charset=utf-8"},
        )

    @classmethod
    async def blog_rss(cls, request: Request, response: Response):
        lang = cls._get_lang(request)
        base_url = f"{cls._get_base_url(request)}{cls._get_base_prefix(request)}"
        async with request.app.db.get_session() as session:
            rss = await SeoService.generate_blog_rss_xml(session, base_url=base_url, lang=lang)
        return await response.make_response(
            rss,
            status=200,
            headers={"Content-Type": "application/rss+xml; charset=utf-8"},
        )

    # 15. Page 404
    @classmethod
    async def not_found(cls, request: Request, response: Response):
        ctx = await cls._build_base_context(request)
        ctx["page_title"] = "Page Non Trouvée (404)"
        comp = Component(module_name="byt3lab_app", name="public/not_found", context=ctx)
        page = Page(ctx["page_title"], comp)
        return await response.render_page(page)
