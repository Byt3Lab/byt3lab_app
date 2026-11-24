from __future__ import annotations
import re
import unicodedata
from typing import Type, Dict, Any


def _slugify(value: str) -> str:
    norm = unicodedata.normalize("NFKD", value or "").encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", norm.lower()).strip("-")
    return slug or "item"


def sanitize_model_data(model_cls: Type[Any], data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Filtre les données entrantes pour ne conserver que les colonnes valides du modèle SQLAlchemy,
    tout en appliquant des fallbacks bilingues FR<->EN et une génération automatique de slug
    afin d'éviter les erreurs NOT NULL lors de la saisie depuis l'administration.
    """
    valid_cols = {c.name for c in model_cls.__table__.columns}
    cleaned: Dict[str, Any] = {
        k: v
        for k, v in (data or {}).items()
        if k in valid_cols and k not in ("id", "created_at", "updated_at")
    }

    # Fallbacks automatiques FR <-> EN pour les colonnes bilingues présentes sur le modèle
    bilingual_bases = ("title", "role", "excerpt", "summary", "content", "description", "badge", "tagline")
    for base in bilingual_bases:
        fr_col, en_col = f"{base}_fr", f"{base}_en"
        if fr_col in valid_cols and en_col in valid_cols:
            fr_val = cleaned.get(fr_col)
            en_val = cleaned.get(en_col)
            if fr_val and not en_val:
                cleaned[en_col] = fr_val
            elif en_val and not fr_val:
                cleaned[fr_col] = en_val

    # Génération automatique du slug s'il est requis et absent/vide
    if "slug" in valid_cols and not cleaned.get("slug"):
        seed = cleaned.get("title_fr") or cleaned.get("title_en") or cleaned.get("name")
        if seed:
            cleaned["slug"] = _slugify(str(seed))

    return cleaned
