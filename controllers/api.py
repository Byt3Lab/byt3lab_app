from __future__ import annotations
from core.routing import Request, Response, require_permission
from ..services.contact_service import ContactService
from ..services.settings_service import SettingsService
from ..services.blog_service import BlogService
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
from ..repositories.message_repository import MessageRepository


class By3labAPIController:
    """
    Contrôleur API REST JSON pour BYT3LAB.
    Conforme aux normes de contrat API-First de MELODI ERP (§8.2).
    Fournit toutes les routes publiques et d'administration SPA.
    """

    # --- ROUTES PUBLIQUES ---

    @classmethod
    async def handle_contact_submission(cls, request: Request, response: Response):
        """POST /api/byt3lab/contact"""
        data = dict(request.json or {}) if isinstance(request.json, dict) and request.json else {}
        if not data:
            form = request.form or {}
            data = form.to_dict() if hasattr(form, "to_dict") else dict(form)

        client_ip = request.remote_addr or getattr(request, "client_ip", "")
        lang = (request.session or {}).get("lang") or "fr"

        async with request.app.db.get_session() as session:
            ok, msg, extra = await ContactService.process_submission(
                session=session,
                data=data,
                client_ip=client_ip,
                lang=lang,
            )
            if ok:
                await session.commit()
                return response.send_json({
                    "success": True,
                    "data": {
                        "message": msg,
                        "whatsapp_url": extra.get("whatsapp_url", ""),
                        "message_id": extra.get("message_id"),
                    }
                }), 201
            else:
                return response.send_json({
                    "success": False,
                    "error": {
                        "code": "VALIDATION_FAILED",
                        "message": msg,
                    },
                    "data": {
                        "message": msg,
                    }
                }), 400

    @classmethod
    async def list_divisions(cls, request: Request, response: Response):
        """GET /api/byt3lab/divisions"""
        lang = (request.session or {}).get("lang") or "fr"
        async with request.app.db.get_session() as session:
            divisions = await DivisionRepository.get_all(session, published_only=True)
            return response.render_json({
                "success": True,
                "data": [d.to_dict(lang=lang) for d in divisions]
            })

    @classmethod
    async def list_solutions(cls, request: Request, response: Response):
        """GET /api/byt3lab/solutions"""
        lang = (request.session or {}).get("lang") or "fr"
        async with request.app.db.get_session() as session:
            solutions = await SolutionRepository.get_all(session, published_only=True)
            return response.render_json({
                "success": True,
                "data": [s.to_dict(lang=lang) for s in solutions]
            })

    @classmethod
    async def get_settings(cls, request: Request, response: Response):
        """GET /api/byt3lab/settings"""
        lang = (request.session or {}).get("lang") or "fr"
        async with request.app.db.get_session() as session:
            settings = await SettingsService.get_public_settings(session, lang=lang)
            return response.render_json({
                "success": True,
                "data": settings
            })

    # --- ROUTES ADMIN SPA ---

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:read")
    async def get_admin_dashboard(request: Request, response: Response):
        """GET /api/admin/byt3lab/dashboard"""
        async with request.app.db.get_session() as session:
            divisions = await DivisionRepository.get_all(session, published_only=False)
            solutions = await SolutionRepository.get_all(session, published_only=False)
            services = await ServiceRepository.get_all(session, published_only=False)
            projects = await ProjectRepository.get_all(session, published_only=False)
            partners = await PartnerRepository.get_all(session, published_only=False)
            team = await TeamRepository.get_all(session, published_only=False)
            jobs = await JobRepository.get_all(session, published_only=False)
            posts = await PostRepository.get_all(session, published_only=False)
            ngrafix = await NgrafixRepository.get_all(session, published_only=False)
            messages = await MessageRepository.get_all(session)
            unread_count = await MessageRepository.count_unread(session)

            recent_messages = [m.to_dict() for m in messages[:10]]

            return response.render_json({
                "success": True,
                "data": {
                    "counts": {
                        "divisions": len(divisions),
                        "solutions": len(solutions),
                        "services": len(services),
                        "projects": len(projects),
                        "partners": len(partners),
                        "team": len(team),
                        "jobs": len(jobs),
                        "posts": len(posts),
                        "ngrafix": len(ngrafix),
                        "messages": len(messages),
                        "unread_messages": unread_count,
                    },
                    "recent_messages": recent_messages,
                }
            })

    # --- MESSAGES (INBOX) ---

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:read")
    async def list_admin_messages(request: Request, response: Response):
        """GET /api/admin/byt3lab/messages"""
        status_filter = getattr(request, "args", {}).get("status")
        async with request.app.db.get_session() as session:
            all_messages = await MessageRepository.get_all(session)
            if status_filter:
                filtered = [m for m in all_messages if m.status == status_filter]
            else:
                filtered = all_messages

            return response.render_json({
                "success": True,
                "data": [m.to_dict() for m in filtered],
                "counts": {
                    "total": len(all_messages),
                    "new": len([m for m in all_messages if m.status == "new"]),
                    "in_progress": len([m for m in all_messages if m.status == "in_progress"]),
                    "resolved": len([m for m in all_messages if m.status == "resolved"]),
                }
            })

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:write")
    async def update_admin_message_status(request: Request, response: Response):
        """PUT /api/admin/byt3lab/messages/<id>/status"""
        msg_id = int((request.params or {}).get("id") or 0)
        data = request.json or {}
        new_status = data.get("status")
        if not msg_id or not new_status:
            return response.render_json({"success": False, "message": "ID et statut requis."}, 400)

        async with request.app.db.get_session() as session:
            updated = await MessageRepository.update_status(session, msg_id, str(new_status))
            await session.commit()
            if updated:
                return response.render_json({"success": True, "data": updated.to_dict()})
            return response.render_json({"success": False, "message": "Message introuvable."}, 404)

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:delete")
    async def delete_admin_message(request: Request, response: Response):
        """DELETE /api/admin/byt3lab/messages/<id>"""
        msg_id = int((request.params or {}).get("id") or 0)
        async with request.app.db.get_session() as session:
            ok = await MessageRepository.delete(session, msg_id)
            await session.commit()
            return response.render_json({"success": ok})

    # --- REGLAGES (SETTINGS) ---

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:read")
    async def get_admin_settings(request: Request, response: Response):
        """GET /api/admin/byt3lab/settings"""
        async with request.app.db.get_session() as session:
            raw = await SettingsService.get_admin_settings(session)
            return response.render_json({"success": True, "data": raw})

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:settings")
    async def save_admin_settings(request: Request, response: Response):
        """POST /api/admin/byt3lab/settings"""
        data = request.json or {}
        async with request.app.db.get_session() as session:
            await SettingsService.save_settings(session, data)
            await session.commit()
            updated = await SettingsService.get_admin_settings(session)
            return response.render_json({"success": True, "data": updated})

    # --- DIVISIONS CRUD ---

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:read")
    async def list_admin_divisions(request: Request, response: Response):
        """GET /api/admin/byt3lab/divisions"""
        async with request.app.db.get_session() as session:
            items = await DivisionRepository.get_all(session, published_only=False)
            return response.render_json({"success": True, "data": [i.to_dict(lang="fr") for i in items]})

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:write")
    async def save_admin_division(request: Request, response: Response):
        """POST /api/admin/byt3lab/divisions & PUT /api/admin/byt3lab/divisions/<id>"""
        item_id = int((request.params or {}).get("id") or 0)
        data = request.json or {}
        async with request.app.db.get_session() as session:
            if item_id:
                item = await DivisionRepository.update(session, item_id, data)
            else:
                item = await DivisionRepository.create(session, data)
            await session.commit()
            return response.render_json({"success": True, "data": item.to_dict(lang="fr") if item else None})

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:delete")
    async def delete_admin_division(request: Request, response: Response):
        """DELETE /api/admin/byt3lab/divisions/<id>"""
        item_id = int((request.params or {}).get("id") or 0)
        async with request.app.db.get_session() as session:
            ok = await DivisionRepository.delete(session, item_id)
            await session.commit()
            return response.render_json({"success": ok})

    # --- SOLUTIONS CRUD ---

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:read")
    async def list_admin_solutions(request: Request, response: Response):
        """GET /api/admin/byt3lab/solutions"""
        async with request.app.db.get_session() as session:
            items = await SolutionRepository.get_all(session, published_only=False)
            return response.render_json({"success": True, "data": [i.to_dict(lang="fr") for i in items]})

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:write")
    async def save_admin_solution(request: Request, response: Response):
        """POST /api/admin/byt3lab/solutions & PUT /api/admin/byt3lab/solutions/<id>"""
        item_id = int((request.params or {}).get("id") or 0)
        data = request.json or {}
        async with request.app.db.get_session() as session:
            if item_id:
                item = await SolutionRepository.update(session, item_id, data)
            else:
                item = await SolutionRepository.create(session, data)
            await session.commit()
            return response.render_json({"success": True, "data": item.to_dict(lang="fr") if item else None})

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:delete")
    async def delete_admin_solution(request: Request, response: Response):
        """DELETE /api/admin/byt3lab/solutions/<id>"""
        item_id = int((request.params or {}).get("id") or 0)
        async with request.app.db.get_session() as session:
            ok = await SolutionRepository.delete(session, item_id)
            await session.commit()
            return response.render_json({"success": ok})

    # --- SERVICES CRUD ---

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:read")
    async def list_admin_services(request: Request, response: Response):
        """GET /api/admin/byt3lab/services"""
        async with request.app.db.get_session() as session:
            items = await ServiceRepository.get_all(session, published_only=False)
            return response.render_json({"success": True, "data": [i.to_dict(lang="fr") for i in items]})

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:write")
    async def save_admin_service(request: Request, response: Response):
        """POST /api/admin/byt3lab/services & PUT /api/admin/byt3lab/services/<id>"""
        item_id = int((request.params or {}).get("id") or 0)
        data = request.json or {}
        async with request.app.db.get_session() as session:
            if item_id:
                item = await ServiceRepository.update(session, item_id, data)
            else:
                item = await ServiceRepository.create(session, data)
            await session.commit()
            return response.render_json({"success": True, "data": item.to_dict(lang="fr") if item else None})

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:delete")
    async def delete_admin_service(request: Request, response: Response):
        """DELETE /api/admin/byt3lab/services/<id>"""
        item_id = int((request.params or {}).get("id") or 0)
        async with request.app.db.get_session() as session:
            ok = await ServiceRepository.delete(session, item_id)
            await session.commit()
            return response.render_json({"success": ok})

    # --- PROJETS CRUD ---

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:read")
    async def list_admin_projects(request: Request, response: Response):
        """GET /api/admin/byt3lab/projects"""
        async with request.app.db.get_session() as session:
            items = await ProjectRepository.get_all(session, published_only=False)
            return response.render_json({"success": True, "data": [i.to_dict(lang="fr") for i in items]})

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:write")
    async def save_admin_project(request: Request, response: Response):
        """POST /api/admin/byt3lab/projects & PUT /api/admin/byt3lab/projects/<id>"""
        item_id = int((request.params or {}).get("id") or 0)
        data = request.json or {}
        async with request.app.db.get_session() as session:
            if item_id:
                item = await ProjectRepository.update(session, item_id, data)
            else:
                item = await ProjectRepository.create(session, data)
            await session.commit()
            return response.render_json({"success": True, "data": item.to_dict(lang="fr") if item else None})

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:delete")
    async def delete_admin_project(request: Request, response: Response):
        """DELETE /api/admin/byt3lab/projects/<id>"""
        item_id = int((request.params or {}).get("id") or 0)
        async with request.app.db.get_session() as session:
            ok = await ProjectRepository.delete(session, item_id)
            await session.commit()
            return response.render_json({"success": ok})

    # --- PARTENAIRES CRUD ---

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:read")
    async def list_admin_partners(request: Request, response: Response):
        """GET /api/admin/byt3lab/partners"""
        async with request.app.db.get_session() as session:
            items = await PartnerRepository.get_all(session, published_only=False)
            return response.render_json({"success": True, "data": [i.to_dict(lang="fr") for i in items]})

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:write")
    async def save_admin_partner(request: Request, response: Response):
        """POST /api/admin/byt3lab/partners & PUT /api/admin/byt3lab/partners/<id>"""
        item_id = int((request.params or {}).get("id") or 0)
        data = request.json or {}
        async with request.app.db.get_session() as session:
            if item_id:
                item = await PartnerRepository.update(session, item_id, data)
            else:
                item = await PartnerRepository.create(session, data)
            await session.commit()
            return response.render_json({"success": True, "data": item.to_dict(lang="fr") if item else None})

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:delete")
    async def delete_admin_partner(request: Request, response: Response):
        """DELETE /api/admin/byt3lab/partners/<id>"""
        item_id = int((request.params or {}).get("id") or 0)
        async with request.app.db.get_session() as session:
            ok = await PartnerRepository.delete(session, item_id)
            await session.commit()
            return response.render_json({"success": ok})

    # --- EQUIPE CRUD ---

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:read")
    async def list_admin_team(request: Request, response: Response):
        """GET /api/admin/byt3lab/team"""
        async with request.app.db.get_session() as session:
            items = await TeamRepository.get_all(session, published_only=False)
            return response.render_json({"success": True, "data": [i.to_dict(lang="fr") for i in items]})

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:write")
    async def save_admin_team(request: Request, response: Response):
        """POST /api/admin/byt3lab/team & PUT /api/admin/byt3lab/team/<id>"""
        item_id = int((request.params or {}).get("id") or 0)
        data = request.json or {}
        async with request.app.db.get_session() as session:
            if item_id:
                item = await TeamRepository.update(session, item_id, data)
            else:
                item = await TeamRepository.create(session, data)
            await session.commit()
            return response.render_json({"success": True, "data": item.to_dict(lang="fr") if item else None})

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:delete")
    async def delete_admin_team(request: Request, response: Response):
        """DELETE /api/admin/byt3lab/team/<id>"""
        item_id = int((request.params or {}).get("id") or 0)
        async with request.app.db.get_session() as session:
            ok = await TeamRepository.delete(session, item_id)
            await session.commit()
            return response.render_json({"success": ok})

    # --- CARRIERE / EMPLOIS CRUD ---

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:read")
    async def list_admin_jobs(request: Request, response: Response):
        """GET /api/admin/byt3lab/jobs"""
        async with request.app.db.get_session() as session:
            items = await JobRepository.get_all(session, published_only=False)
            return response.render_json({"success": True, "data": [i.to_dict(lang="fr") for i in items]})

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:write")
    async def save_admin_job(request: Request, response: Response):
        """POST /api/admin/byt3lab/jobs & PUT /api/admin/byt3lab/jobs/<id>"""
        item_id = int((request.params or {}).get("id") or 0)
        data = request.json or {}
        async with request.app.db.get_session() as session:
            if item_id:
                item = await JobRepository.update(session, item_id, data)
            else:
                item = await JobRepository.create(session, data)
            await session.commit()
            return response.render_json({"success": True, "data": item.to_dict(lang="fr") if item else None})

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:delete")
    async def delete_admin_job(request: Request, response: Response):
        """DELETE /api/admin/byt3lab/jobs/<id>"""
        item_id = int((request.params or {}).get("id") or 0)
        async with request.app.db.get_session() as session:
            ok = await JobRepository.delete(session, item_id)
            await session.commit()
            return response.render_json({"success": ok})

    # --- ARTICLES BLOG CRUD ---

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:read")
    async def list_admin_posts(request: Request, response: Response):
        """GET /api/admin/byt3lab/posts"""
        async with request.app.db.get_session() as session:
            items = await PostRepository.get_all(session, published_only=False)
            return response.render_json({"success": True, "data": [i.to_dict(lang="fr") for i in items]})

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:write")
    async def save_admin_post(request: Request, response: Response):
        """POST /api/admin/byt3lab/posts & PUT /api/admin/byt3lab/posts/<id>"""
        item_id = int((request.params or {}).get("id") or 0)
        data = dict(request.json or {})
        if "category_id" in data:
            raw_cat = data["category_id"]
            data["category_id"] = int(raw_cat) if raw_cat not in (None, "", 0, "0") else None
        if not data.get("reading_time_min"):
            data["reading_time_min"] = BlogService.compute_reading_time(
                data.get("content_fr") or "",
                data.get("content_en") or "",
                data.get("summary_fr") or "",
            )
        async with request.app.db.get_session() as session:
            if item_id:
                item = await PostRepository.update(session, item_id, data)
            else:
                item = await PostRepository.create(session, data)
            await session.commit()
            return response.render_json({"success": True, "data": item.to_dict(lang="fr") if item else None})

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:delete")
    async def delete_admin_post(request: Request, response: Response):
        """DELETE /api/admin/byt3lab/posts/<id>"""
        item_id = int((request.params or {}).get("id") or 0)
        async with request.app.db.get_session() as session:
            ok = await PostRepository.delete(session, item_id)
            await session.commit()
            return response.render_json({"success": ok})

    # --- CATÉGORIES BLOG ---

    @classmethod
    async def list_public_posts(cls, request: Request, response: Response):
        """GET /api/byt3lab_app/posts"""
        query = getattr(request, "query", {}) or getattr(request, "args", {}) or {}
        lang = query.get("lang") if query.get("lang") in ("fr", "en") else ((request.session or {}).get("lang") or "fr")
        q = str(query.get("q") or "").strip()
        category = str(query.get("categorie") or query.get("category") or "").strip()
        tag = str(query.get("tag") or "").strip()
        try:
            page = max(1, int(query.get("page") or 1))
            per_page = max(1, min(50, int(query.get("per_page") or 9)))
        except Exception:
            page, per_page = 1, 9
        async with request.app.db.get_session() as session:
            posts, total = await PostRepository.search_paginated(
                session, q=q, category_slug=category, tag=tag, page=page, per_page=per_page, published_only=True
            )
            return response.render_json({
                "success": True,
                "data": [p.to_dict(lang=lang) for p in posts],
                "meta": {"total": total, "page": page, "per_page": per_page},
            })

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:read")
    async def list_admin_blog_categories(request: Request, response: Response):
        async with request.app.db.get_session() as session:
            items = await BlogCategoryRepository.get_all(session, active_only=False)
            return response.render_json({"success": True, "data": [i.to_dict(lang="fr") for i in items]})

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:write")
    async def save_admin_blog_category(request: Request, response: Response):
        item_id = int((request.params or {}).get("id") or 0)
        data = dict(request.json or {})
        if not data.get("name_fr") and data.get("title_fr"):
            data["name_fr"] = data["title_fr"]
        if not data.get("name_en") and data.get("title_en"):
            data["name_en"] = data["title_en"]
        if not data.get("name_en") and data.get("name_fr"):
            data["name_en"] = data["name_fr"]
        if "description_fr" not in data and data.get("content_fr"):
            data["description_fr"] = data["content_fr"]
        if "description_en" not in data and data.get("content_en"):
            data["description_en"] = data["content_en"]
        if "is_active" not in data and "is_published" in data:
            data["is_active"] = bool(data["is_published"])
        async with request.app.db.get_session() as session:
            if item_id:
                item = await BlogCategoryRepository.update(session, item_id, data)
            else:
                item = await BlogCategoryRepository.create(session, data)
            await session.commit()
            return response.render_json({"success": True, "data": item.to_dict(lang="fr") if item else None})

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:delete")
    async def delete_admin_blog_category(request: Request, response: Response):
        item_id = int((request.params or {}).get("id") or 0)
        async with request.app.db.get_session() as session:
            ok = await BlogCategoryRepository.delete(session, item_id)
            await session.commit()
            return response.render_json({"success": ok})


    # --- NGRAFIX STUDIO CRUD ---

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:read")
    async def list_admin_ngrafix(request: Request, response: Response):
        """GET /api/admin/byt3lab_app/ngrafix"""
        async with request.app.db.get_session() as session:
            items = await NgrafixRepository.get_all(session, published_only=False)
            return response.render_json({"success": True, "data": [i.to_dict(lang="fr") for i in items]})

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:write")
    async def save_admin_ngrafix(request: Request, response: Response):
        """POST /api/admin/byt3lab_app/ngrafix & PUT /api/admin/byt3lab_app/ngrafix/<id>"""
        item_id = int((request.params or {}).get("id") or 0)
        data = request.json or {}
        async with request.app.db.get_session() as session:
            if item_id:
                item = await NgrafixRepository.update(session, item_id, data)
            else:
                item = await NgrafixRepository.create(session, data)
            await session.commit()
            return response.render_json({"success": True, "data": item.to_dict(lang="fr") if item else None})

    @staticmethod
    @require_permission("byt3lab_app.byt3lab_app:delete")
    async def delete_admin_ngrafix(request: Request, response: Response):
        """DELETE /api/admin/byt3lab_app/ngrafix/<id>"""
        item_id = int((request.params or {}).get("id") or 0)
        async with request.app.db.get_session() as session:
            ok = await NgrafixRepository.delete(session, item_id)
            await session.commit()
            return response.render_json({"success": ok})
