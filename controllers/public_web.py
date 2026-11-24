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

    @classmethod
    async def _render_public_page(cls, response: Response, component_name: str, ctx: dict):
        root = Component(module_name="byt3lab_app", name="public/byt3lab_layout", anchor="byt3lab", context=ctx)
        root.add(Component(module_name="byt3lab_app", name="public/byt3lab_header", context=ctx), slot="header")
        root.add(Component(module_name="byt3lab_app", name=component_name, context=ctx), slot="content")
        root.add(Component(module_name="byt3lab_app", name="public/byt3lab_footer", context=ctx), slot="footer")
        page = Page(ctx["page_title"], root, context=ctx, module_name="byt3lab_app")
        return await response.render_page(page)

    # 1. Accueil
    @classmethod
    async def home(cls, request: Request, response: Response):
        ctx = await cls._build_base_context(request, active_nav="home")
        lang = ctx["current_lang"]
        async with request.app.db.get_session() as session:
            divisions = await DivisionRepository.get_all(session, published_only=True)
            solutions = await SolutionRepository.get_all(session, published_only=True)
            projects = await ProjectRepository.get_all(session, published_only=True)
            ngrafix_items = await NgrafixRepository.get_all(session, published_only=True)
            partners = await PartnerRepository.get_all(session, published_only=True)

        ctx.update({
            "divisions": [d.to_dict(lang=lang) for d in divisions],
            "solutions": [s.to_dict(lang=lang) for s in solutions],
            "projects": [p.to_dict(lang=lang) for p in projects],
            "ngrafix_items": [n.to_dict(lang=lang) for n in ngrafix_items],
            "partners": [p.to_dict(lang=lang) for p in partners],
            "page_title": "Building technology solutions that move businesses forward" if lang == "en" else "Solutions technologiques qui font avancer les entreprises",
        })

        return await cls._render_public_page(response, "public/home", ctx)

    # 2. Nos 4 Pôles Stratégiques (Software, Web Services, Equipment, ngrafix)
    @classmethod
    async def poles(cls, request: Request, response: Response):
        ctx = await cls._build_base_context(request, active_nav="poles")
        lang = ctx["current_lang"]
        ctx.update({
            "page_title": "Our 4 Divisions & Poles" if lang == "en" else "Nos 4 Pôles Technologiques",
            "meta_description": (
                "Discover Byt3Lab's four complementary poles: Software, Web Services, Equipment and ngrafix."
                if lang == "en" else
                "Découvrez les quatre pôles complémentaires de Byt3Lab : Software, Web Services, Equipment et ngrafix."
            ),
        })
        return await cls._render_public_page(response, "public/poles", ctx)

    @classmethod
    async def pole_software(cls, request: Request, response: Response):
        ctx = await cls._build_base_context(request, active_nav="poles")
        lang = ctx["current_lang"]
        async with request.app.db.get_session() as session:
            all_solutions = await SolutionRepository.get_all(session, published_only=True)
            all_services = await ServiceRepository.get_all(session, published_only=True)
        software_solutions = [
            s.to_dict(lang=lang) for s in all_solutions
            if s.slug in ("melodi-erp", "asso", "suku")
        ]
        ctx.update({
            "software_solutions": software_solutions,
            "services": [s.to_dict(lang=lang) for s in all_services],
            "page_title": "Byt3Lab Software — Software Development & MELODI ERP",
            "meta_description": (
                "Custom business software, ERP & CRM solutions, APIs and MELODI ERP modular platform."
                if lang == "en" else
                "Développement de logiciels métier, ERP & CRM, API et plateforme modulaire MELODI ERP."
            ),
        })
        return await cls._render_public_page(response, "public/pole_software", ctx)

    @classmethod
    async def pole_web_services(cls, request: Request, response: Response):
        ctx = await cls._build_base_context(request, active_nav="poles")
        lang = ctx["current_lang"]
        ctx.update({
            "page_title": "Byt3Lab Web Services — Cloud, Hosting & Managed Services",
            "meta_description": (
                "Application hosting, VPS, dedicated servers, system administration and managed cloud services in Africa."
                if lang == "en" else
                "Hébergement d'applications, serveurs, administration système, infogérance et services cloud managés."
            ),
        })
        return await cls._render_public_page(response, "public/pole_web_services", ctx)

    @classmethod
    async def pole_equipment(cls, request: Request, response: Response):
        ctx = await cls._build_base_context(request, active_nav="poles")
        lang = ctx["current_lang"]
        ctx.update({
            "page_title": "Byt3Lab Equipment — IT, Energy & Equipment as a Service",
            "meta_description": (
                "Complete IT equipment, enterprise networking, security, solar backup energy and Equipment as a Service."
                if lang == "en" else
                "Équipements informatiques, réseaux, vidéosurveillance, solutions énergétiques et Equipment as a Service."
            ),
        })
        return await cls._render_public_page(response, "public/pole_equipment", ctx)

    # 3. Solutions orientées besoins clients
    @classmethod
    async def solutions(cls, request: Request, response: Response):
        ctx = await cls._build_base_context(request, active_nav="solutions")
        lang = ctx["current_lang"]
        async with request.app.db.get_session() as session:
            solutions = await SolutionRepository.get_all(session, published_only=True)
            services = await ServiceRepository.get_all(session, published_only=True)

        ctx.update({
            "solutions": [s.to_dict(lang=lang) for s in solutions],
            "services": [s.to_dict(lang=lang) for s in services],
            "page_title": "Business & Technology Solutions" if lang == "en" else "Solutions par Besoin Métier",
        })
        return await cls._render_public_page(response, "public/solutions", ctx)

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
        return await cls._render_public_page(response, "public/solution_detail", ctx)

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
        return await cls._render_public_page(response, "public/services", ctx)

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
        return await cls._render_public_page(response, "public/service_detail", ctx)

    # 5. Réalisations & Projets
    @classmethod
    async def realisations(cls, request: Request, response: Response):
        ctx = await cls._build_base_context(request, active_nav="realisations")
        lang = ctx["current_lang"]
        query = getattr(request, "query", {}) or getattr(request, "args", {}) or {}
        active_pole = str(query.get("pole") or "").strip().lower()
        async with request.app.db.get_session() as session:
            projects = await ProjectRepository.get_all(session, published_only=True)
            ngrafix_items = await NgrafixRepository.get_all(session, published_only=True)

        ctx.update({
            "projects": [p.to_dict(lang=lang) for p in projects],
            "ngrafix_items": [n.to_dict(lang=lang) for n in ngrafix_items],
            "active_pole": active_pole,
            "page_title": "Portfolio & Case Studies" if lang == "en" else "Réalisations & Portfolio",
        })
        return await cls._render_public_page(response, "public/realisations", ctx)

    @classmethod
    async def project_detail(cls, request: Request, response: Response):
        slug = (request.params or {}).get("slug")
        ctx = await cls._build_base_context(request, active_nav="realisations")
        lang = ctx["current_lang"]
        async with request.app.db.get_session() as session:
            project = await ProjectRepository.get_by_slug(session, slug)
            if not project:
                return await cls.not_found(request, response)
            all_projects = await ProjectRepository.get_all(session, published_only=True)

        related_projects = [
            p.to_dict(lang=lang)
            for p in all_projects
            if p.slug != slug
        ][:3]

        ctx.update({
            "project": project.to_dict(lang=lang),
            "related_projects": related_projects,
            "page_title": project.title_en if lang == "en" else project.title_fr,
        })
        return await cls._render_public_page(response, "public/project_detail", ctx)

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
        return await cls._render_public_page(response, "public/ngrafix", ctx)

    # 7. À Propos
    @classmethod
    async def a_propos(cls, request: Request, response: Response):
        ctx = await cls._build_base_context(request, active_nav="a-propos")
        ctx["page_title"] = "À Propos du Groupe"
        return await cls._render_public_page(response, "public/a_propos", ctx)

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
        return await cls._render_public_page(response, "public/equipe", ctx)

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
        return await cls._render_public_page(response, "public/team_detail", ctx)

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
        return await cls._render_public_page(response, "public/carriere", ctx)

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
        return await cls._render_public_page(response, "public/job_detail", ctx)

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
        return await cls._render_public_page(response, "public/partenaires", ctx)

    # 12. Contact
    @classmethod
    async def contact(cls, request: Request, response: Response):
        ctx = await cls._build_base_context(request, active_nav="contact")
        lang = ctx["current_lang"]
        query = getattr(request, "query", {}) or getattr(request, "args", {}) or {}
        subject = str(query.get("need") or query.get("subject") or "").strip()
        pole = str(query.get("pole") or "").strip().lower()
        ctx.update({
            "prefilled_subject": subject,
            "prefilled_pole": pole,
            "page_title": "Contact & Project Inquiry" if lang == "en" else "Contact & Demande de Devis",
        })
        return await cls._render_public_page(response, "public/contact", ctx)

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
        return await cls._render_public_page(response, "public/blog", ctx)

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
        return await cls._render_public_page(response, "public/post_detail", ctx)

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
        return await cls._render_public_page(response, "public/not_found", ctx)
