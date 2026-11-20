from __future__ import annotations
from typing import Type, Dict, Any


def sanitize_model_data(model_cls: Type[Any], data: Dict[str, Any]) -> Dict[str, Any]:
    """Filtre les données entrantes pour ne conserver que les colonnes valides du modèle SQLAlchemy."""
    valid_cols = {c.name for c in model_cls.__table__.columns}
    return {
        k: v
        for k, v in (data or {}).items()
        if k in valid_cols and k not in ("id", "created_at", "updated_at")
    }
