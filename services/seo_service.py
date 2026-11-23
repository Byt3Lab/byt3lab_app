from __future__ import annotations
from datetime import datetime, timezone
from html import escape
from typing import List
from ..repositories.division_repository import DivisionRepository
from ..repositories.solution_repository import SolutionRepository
from ..repositories.service_repository import ServiceRepository
from ..repositories.project_repository import ProjectRepository
from ..repositories.team_repository import TeamRepository
from ..repositories.job_repository import JobRepository
from ..repositories.post_repository import PostRepository
from ..repositories.blog_category_repository import BlogCategoryRepository


class SeoService:
    """Générateur dynamique de sitemap.xml multilingue, robots.txt et flux RSS bilingue."""

    STATIC_PATHS: List[tuple] = [
        ("/", "1.0", "weekly"),
        ("/technologies/", "0.9", "weekly"),
        ("/produits/", "0.9", "weekly"),
        ("/services/", "0.9", "weekly"),
        ("/realisations/", "0.8", "weekly"),
        ("/ngrafix/", "0.8", "monthly"),
        ("/a-propos/", "0.7", "monthly"),
        ("/equipe/", "0.7", "monthly"),
        ("/carriere/", "0.7", "weekly"),
        ("/partenaires/", "0.7", "monthly"),
        ("/contact/", "0.8", "monthly"),
        ("/blog/", "0.9", "daily"),
    ]

    @classmethod
    def _render_url_entry(cls, base_url: str, path: str, priority: str = "0.7", changefreq: str = "weekly", lastmod: str = "") -> str:
        fr_url = escape(f"{base_url}/lg-fr{path}")
        en_url = escape(f"{base_url}/lg-en{path}")
        lastmod_xml = f"<lastmod>{escape(lastmod)}</lastmod>" if lastmod else ""
        entries = []
        for loc in (fr_url, en_url):
            entries.append(
                f"  <url>\n"
                f"    <loc>{loc}</loc>\n"
                f"    {lastmod_xml}\n"
                f"    <changefreq>{changefreq}</changefreq>\n"
                f"    <priority>{priority}</priority>\n"
                f"    <xhtml:link rel=\"alternate\" hreflang=\"fr\" href=\"{fr_url}\"/>\n"
                f"    <xhtml:link rel=\"alternate\" hreflang=\"en\" href=\"{en_url}\"/>\n"
                f"    <xhtml:link rel=\"alternate\" hreflang=\"x-default\" href=\"{fr_url}\"/>\n"
                f"  </url>"
            )
        return "\n".join(entries)

    @classmethod
    async def generate_sitemap_xml(cls, session, base_url: str) -> str:
        base_url = base_url.rstrip("/")
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        blocks: List[str] = []

        for path, prio, freq in cls.STATIC_PATHS:
            blocks.append(cls._render_url_entry(base_url, path, prio, freq, today))

        for div in await DivisionRepository.get_all(session, published_only=True):
            blocks.append(cls._render_url_entry(base_url, f"/technologies/{div.slug}/", "0.8", "monthly"))

        for sol in await SolutionRepository.get_all(session, published_only=True):
            blocks.append(cls._render_url_entry(base_url, f"/produits/{sol.slug}/", "0.9", "weekly"))

        for srv in await ServiceRepository.get_all(session, published_only=True):
            blocks.append(cls._render_url_entry(base_url, f"/services/{srv.slug}/", "0.8", "monthly"))

        for prj in await ProjectRepository.get_all(session, published_only=True):
            blocks.append(cls._render_url_entry(base_url, f"/realisations/{prj.slug}/", "0.8", "monthly"))

        for mem in await TeamRepository.get_all(session, published_only=True):
            blocks.append(cls._render_url_entry(base_url, f"/equipe/{mem.slug}/", "0.6", "monthly"))

        for job in await JobRepository.get_all(session, published_only=True):
            blocks.append(cls._render_url_entry(base_url, f"/carriere/{job.slug}/", "0.7", "weekly"))

        for cat in await BlogCategoryRepository.get_all(session, active_only=True):
            blocks.append(cls._render_url_entry(base_url, f"/blog/categorie/{cat.slug}/", "0.7", "weekly"))

        for post in await PostRepository.get_all(session, published_only=True):
            lm = post.updated_at.strftime("%Y-%m-%d") if getattr(post, "updated_at", None) else today
            blocks.append(cls._render_url_entry(base_url, f"/blog/{post.slug}/", "0.8", "weekly", lm))

        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
            '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
            + "\n".join(blocks)
            + "\n</urlset>\n"
        )

    @staticmethod
    def generate_robots_txt(base_url: str) -> str:
        base_url = base_url.rstrip("/")
        return (
            "User-agent: *\n"
            "Allow: /\n"
            "Disallow: /admin/\n"
            "Disallow: /api/\n"
            f"Sitemap: {base_url}/sitemap.xml\n"
        )

    @classmethod
    async def generate_blog_rss_xml(cls, session, base_url: str, lang: str = "fr") -> str:
        base_url = base_url.rstrip("/")
        is_en = lang == "en"
        posts = await PostRepository.get_all(session, published_only=True)
        items_xml: List[str] = []
        for post in posts[:30]:
            d = post.to_dict(lang=lang)
            link = escape(f"{base_url}/lg-{lang}/blog/{post.slug}/")
            title = escape(d.get("title") or "")
            desc = escape(d.get("summary") or "")
            pub_date = (
                post.published_at.strftime("%a, %d %b %Y %H:%M:%S +0000")
                if post.published_at
                else datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
            )
            items_xml.append(
                "    <item>\n"
                f"      <title>{title}</title>\n"
                f"      <link>{link}</link>\n"
                f"      <guid isPermaLink=\"true\">{link}</guid>\n"
                f"      <pubDate>{pub_date}</pubDate>\n"
                f"      <description>{desc}</description>\n"
                "    </item>"
            )

        channel_title = "Byt3Lab Tech Blog" if is_en else "Le Blog Technologique Byt3Lab"
        channel_desc = (
            "Engineering, MELODI ERP, AI and African tech infrastructure insights."
            if is_en
            else "Actualités ingénierie, MELODI ERP, IA et infrastructures technologiques en Afrique."
        )
        blog_link = escape(f"{base_url}/lg-{lang}/blog/")
        return (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0">\n'
            "  <channel>\n"
            f"    <title>{escape(channel_title)}</title>\n"
            f"    <link>{blog_link}</link>\n"
            f"    <description>{escape(channel_desc)}</description>\n"
            f"    <language>{'en-us' if is_en else 'fr-fr'}</language>\n"
            + "\n".join(items_xml)
            + "\n  </channel>\n"
            "</rss>\n"
        )
