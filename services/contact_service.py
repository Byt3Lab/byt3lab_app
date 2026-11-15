from __future__ import annotations
import time
import urllib.parse
from typing import Dict, Any, Tuple
from ..repositories.message_repository import MessageRepository
from ..repositories.setting_repository import SettingRepository


class ContactService:

    @classmethod
    async def process_submission(
        cls,
        session,
        data: Dict[str, Any],
        client_ip: str = "",
        lang: str = "fr"
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Traite une soumission de formulaire (Contact ou Partenariat) :
        - Vérification Honeypot (byt3lab_hp)
        - Vérification Time-trap (byt3lab_ts >= 2 secondes)
        - Validation des champs obligatoires
        - Enregistrement dans la base de données
        - Génération du lien WhatsApp optionnel
        """
        # 1. Protection Honeypot
        if data.get("byt3lab_hp"):
            return False, "Soumission bloquée (détection automatisée)." if lang == "fr" else "Submission blocked (automated detection).", {}

        # 2. Protection Time-trap (au moins 2 secondes)
        try:
            ts = int(data.get("byt3lab_ts") or 0)
            if ts > 0 and (int(time.time()) - ts) < 2:
                msg = "Envoi trop rapide. Veuillez patienter deux secondes avant de valider." if lang == "fr" else "Submission was too fast. Please wait two seconds before submitting."
                return False, msg, {}
        except Exception:
            pass

        # 3. Extraction et validation
        form_type = str(data.get("form_type") or "contact").strip()
        if form_type not in ("contact", "partner"):
            form_type = "contact"

        name = str(data.get("name") or data.get("contact_name") or "").strip()
        email = str(data.get("email") or data.get("contact_email") or "").strip()
        message = str(data.get("message") or data.get("contact_message") or "").strip()
        phone = str(data.get("phone") or data.get("contact_phone") or "").strip()
        org = str(data.get("org") or data.get("contact_org") or "").strip()
        subject = str(data.get("subject") or data.get("contact_subject") or ("Demande de partenariat" if form_type == "partner" else "Prise de contact")).strip()

        partner_type = str(data.get("partner_type") or "").strip()
        domain = str(data.get("domain") or "").strip()
        website = str(data.get("website") or "").strip()

        if not name or not email or not message:
            err = "Veuillez renseigner votre nom, votre e-mail et votre message." if lang == "fr" else "Please fill in your name, email address, and message."
            return False, err, {}

        # 4. Enregistrement en base
        message_data = {
            "form_type": form_type,
            "sender_name": name,
            "organization": org,
            "email": email,
            "phone": phone,
            "subject": subject,
            "partner_type": partner_type,
            "domain": domain,
            "website": website,
            "message": message,
            "status": "new",
            "ip_address": client_ip,
        }
        msg_record = await MessageRepository.create(session, message_data)

        # 5. Récupération du numéro WhatsApp configuré pour redirection optionnelle
        settings = await SettingRepository.get_all_as_dict(session, lang=lang)
        whatsapp_raw = settings.get("contact.whatsapp", "237696879475").replace("+", "").replace(" ", "").replace("-", "")

        whatsapp_text = f"Bonjour Byt3Lab, je suis {name}"
        if org:
            whatsapp_text += f" de l'organisation {org}"
        whatsapp_text += f". J'ai soumis une demande sur votre site web (Réf: #{msg_record.id})."

        whatsapp_url = f"https://wa.me/{whatsapp_raw}?text={urllib.parse.quote(whatsapp_text)}"

        success_msg = (
            "Votre demande a été transmise avec succès à l'équipe Byt3Lab ! Nous vous répondrons dans les plus brefs délais."
            if lang == "fr"
            else "Your request has been successfully transmitted to the Byt3Lab team! We will get back to you shortly."
        )

        return True, success_msg, {
            "message_id": msg_record.id,
            "whatsapp_url": whatsapp_url,
        }
