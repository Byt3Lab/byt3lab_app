from __future__ import annotations
from typing import Dict, Any
from ..repositories.setting_repository import SettingRepository


class SettingsService:

    @classmethod
    async def get_public_settings(cls, session, lang: str = "fr") -> Dict[str, str]:
        return await SettingRepository.get_all_as_dict(session, lang=lang)

    @classmethod
    async def get_admin_settings(cls, session) -> Dict[str, Dict[str, str]]:
        return await SettingRepository.get_raw_settings(session)

    @classmethod
    async def save_settings(cls, session, settings_data: Dict[str, Any]):
        for key, vals in settings_data.items():
            if isinstance(vals, dict):
                v_fr = str(vals.get("fr") or "")
                v_en = str(vals.get("en") or "")
            else:
                v_fr = str(vals or "")
                v_en = v_fr
            await SettingRepository.set_setting(session, key, v_fr, v_en)
