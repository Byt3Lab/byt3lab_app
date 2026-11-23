from __future__ import annotations
import json
import math
import re
from typing import Any, Dict

_TAG_RE = re.compile(r"<[^>]+>")
_WS_RE = re.compile(r"\s+")


class BlogService:
    """Services métier pour le blog Byt3Lab (temps de lecture, JSON-LD)."""

    @staticmethod
    def compute_reading_time(*texts: str) -> int:
        combined = " ".join(t for t in texts if t)
        plain = _TAG_RE.sub(" ", combined)
        plain = _WS_RE.sub(" ", plain).strip()
        if not plain:
            return 1
        words = len(plain.split(" "))
        return max(1, math.ceil(words / 200))

    @staticmethod
    def build_blog_posting_jsonld(post: Dict[str, Any], canonical_url: str, base_url: str) -> str:
        payload: Dict[str, Any] = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": post.get("meta_title") or post.get("title") or "",
            "description": post.get("meta_description") or post.get("summary") or "",
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": canonical_url,
            },
            "author": {
                "@type": "Person" if post.get("author_name") else "Organization",
                "name": post.get("author_name") or "Byt3Lab Editorial",
            },
            "publisher": {
                "@type": "Organization",
                "name": "BYT3LAB Technology & Innovation Group",
                "url": base_url,
            },
        }
        if post.get("published_at_iso"):
            payload["datePublished"] = post["published_at_iso"]
        img = post.get("og_image") or post.get("cover_image")
        if img:
            payload["image"] = img if img.startswith("http") else f"{base_url}{img}"
        if post.get("category"):
            payload["articleSection"] = post["category"]
        if post.get("tags_list"):
            payload["keywords"] = ", ".join(post["tags_list"])
        return json.dumps(payload, ensure_ascii=False)
