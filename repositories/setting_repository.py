from __future__ import annotations
from typing import Dict, Optional
from sqlalchemy import select
from ..models.models import Byt3labSettingModel
from ..config import DEFAULT_SETTINGS


class SettingRepository:

    @classmethod
    async def get_all_as_dict(cls, session, lang: str = "fr") -> Dict[str, str]:
        stmt = select(Byt3labSettingModel)
        result = await session.execute(stmt)
        saved = {item.key: (item.value_en if lang == "en" and item.value_en else item.value_fr) for item in result.scalars().all()}

        merged: Dict[str, str] = {}
        for key, defaults in DEFAULT_SETTINGS.items():
            if key in saved and saved[key] is not None and saved[key] != "":
                merged[key] = saved[key]
            else:
                merged[key] = defaults.get(lang, defaults.get("fr", ""))
        return merged

    @classmethod
    async def get_raw_settings(cls, session) -> Dict[str, Dict[str, str]]:
        stmt = select(Byt3labSettingModel)
        result = await session.execute(stmt)
        saved = {item.key: {"fr": item.value_fr or "", "en": item.value_en or ""} for item in result.scalars().all()}

        full: Dict[str, Dict[str, str]] = {}
        for key, defaults in DEFAULT_SETTINGS.items():
            if key in saved:
                full[key] = {
                    "fr": saved[key]["fr"] or defaults.get("fr", ""),
                    "en": saved[key]["en"] or defaults.get("en", ""),
                }
            else:
                full[key] = {
                    "fr": defaults.get("fr", ""),
                    "en": defaults.get("en", ""),
                }
        return full

    @classmethod
    async def set_setting(cls, session, key: str, value_fr: str, value_en: str):
        stmt = select(Byt3labSettingModel).where(Byt3labSettingModel.key == key)
        result = await session.execute(stmt)
        setting = result.scalars().first()
        if setting:
            setting.value_fr = value_fr
            setting.value_en = value_en
        else:
            setting = Byt3labSettingModel(key=key, value_fr=value_fr, value_en=value_en)
            session.add(setting)
        await session.flush()
        return setting
