from __future__ import annotations
from datetime import datetime
from core import get_prefix_table
from core.db.base_module_tables import BaseModuleTables
from sqlalchemy import Column, JSON, func
from core.orm.model import (
    BaseModel as Model,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
)
from ..config import (
    MODULE_NAME,
    STATUS_ACTIVE,
    STATUS_IN_DEVELOPMENT,
    STATUS_STRATEGIC,
)

PREFIX_TABLE = get_prefix_table(MODULE_NAME)


class Byt3labTables(BaseModuleTables):
    DIVISIONS = f"{PREFIX_TABLE}divisions"
    SOLUTIONS = f"{PREFIX_TABLE}solutions"
    SERVICES = f"{PREFIX_TABLE}services"
    PROJECTS = f"{PREFIX_TABLE}projects"
    PARTNERS = f"{PREFIX_TABLE}partners"
    NGRAFIX = f"{PREFIX_TABLE}ngrafix"
    TEAM = f"{PREFIX_TABLE}team"
    JOBS = f"{PREFIX_TABLE}jobs"
    POSTS = f"{PREFIX_TABLE}posts"
    MESSAGES = f"{PREFIX_TABLE}messages"
    SETTINGS = f"{PREFIX_TABLE}settings"


class Byt3labDivisionModel(Model):
    """5 Divisions technologiques fondamentales de Byt3Lab."""
    __tablename__ = Byt3labTables.DIVISIONS

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    title_fr = Column(String(200), nullable=False)
    title_en = Column(String(200), nullable=False)
    excerpt_fr = Column(Text, nullable=True)
    excerpt_en = Column(Text, nullable=True)
    content_fr = Column(Text, nullable=True)
    content_en = Column(Text, nullable=True)
    icon = Column(String(50), default="layers")
    order_num = Column(Integer, default=0)
    maturity_status = Column(String(50), default=STATUS_ACTIVE)
    vision_fr = Column(Text, nullable=True)
    vision_en = Column(Text, nullable=True)
    expertise_list = Column(JSON, default=list)
    technologies_list = Column(JSON, default=list)
    services_list = Column(JSON, default=list)
    industries_list = Column(JSON, default=list)
    related_slugs = Column(JSON, default=list)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    def to_dict(self, lang: str = "fr") -> dict:
        is_en = lang == "en"
        return {
            "id": self.id,
            "slug": self.slug,
            "title": self.title_en if is_en and self.title_en else self.title_fr,
            "title_fr": self.title_fr,
            "title_en": self.title_en,
            "excerpt": self.excerpt_en if is_en and self.excerpt_en else self.excerpt_fr,
            "excerpt_fr": self.excerpt_fr,
            "excerpt_en": self.excerpt_en,
            "content": self.content_en if is_en and self.content_en else self.content_fr,
            "content_fr": self.content_fr,
            "content_en": self.content_en,
            "icon": self.icon or "layers",
            "order_num": self.order_num or 0,
            "maturity_status": self.maturity_status or STATUS_ACTIVE,
            "vision": self.vision_en if is_en and self.vision_en else self.vision_fr,
            "vision_fr": self.vision_fr,
            "vision_en": self.vision_en,
            "expertise_list": self.expertise_list or [],
            "technologies_list": self.technologies_list or [],
            "services_list": self.services_list or [],
            "industries_list": self.industries_list or [],
            "related_slugs": self.related_slugs or [],
            "is_published": self.is_published,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Byt3labSolutionModel(Model):
    """Produits (MELODI ERP, SUKU) et Offres d'infrastructure (BWS)."""
    __tablename__ = Byt3labTables.SOLUTIONS

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    title_fr = Column(String(200), nullable=False)
    title_en = Column(String(200), nullable=False)
    solution_type = Column(String(50), default="product")  # product, service_activity
    status = Column(String(50), default=STATUS_ACTIVE)
    division_slug = Column(String(100), nullable=True)
    badge_fr = Column(String(100), nullable=True)
    badge_en = Column(String(100), nullable=True)
    tagline_fr = Column(String(300), nullable=True)
    tagline_en = Column(String(300), nullable=True)
    accent_color = Column(String(20), default="#1D7FD8")
    order_num = Column(Integer, default=0)
    excerpt_fr = Column(Text, nullable=True)
    excerpt_en = Column(Text, nullable=True)
    content_fr = Column(Text, nullable=True)
    content_en = Column(Text, nullable=True)
    features_list = Column(JSON, default=list)
    problems_list = Column(JSON, default=list)
    benefits_list = Column(JSON, default=list)
    button_label_fr = Column(String(100), default="Découvrir")
    button_label_en = Column(String(100), default="Explore")
    button_url = Column(String(300), nullable=True)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    def to_dict(self, lang: str = "fr") -> dict:
        is_en = lang == "en"
        return {
            "id": self.id,
            "slug": self.slug,
            "title": self.title_en if is_en and self.title_en else self.title_fr,
            "title_fr": self.title_fr,
            "title_en": self.title_en,
            "solution_type": self.solution_type,
            "status": self.status,
            "division_slug": self.division_slug,
            "badge": self.badge_en if is_en and self.badge_en else self.badge_fr,
            "badge_fr": self.badge_fr,
            "badge_en": self.badge_en,
            "tagline": self.tagline_en if is_en and self.tagline_en else self.tagline_fr,
            "tagline_fr": self.tagline_fr,
            "tagline_en": self.tagline_en,
            "accent_color": self.accent_color or "#1D7FD8",
            "order_num": self.order_num or 0,
            "excerpt": self.excerpt_en if is_en and self.excerpt_en else self.excerpt_fr,
            "excerpt_fr": self.excerpt_fr,
            "excerpt_en": self.excerpt_en,
            "content": self.content_en if is_en and self.content_en else self.content_fr,
            "content_fr": self.content_fr,
            "content_en": self.content_en,
            "features_list": self.features_list or [],
            "problems_list": self.problems_list or [],
            "benefits_list": self.benefits_list or [],
            "button_label": self.button_label_en if is_en and self.button_label_en else self.button_label_fr,
            "button_label_fr": self.button_label_fr,
            "button_label_en": self.button_label_en,
            "button_url": self.button_url or "",
            "is_published": self.is_published,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class Byt3labServiceModel(Model):
    """Services d'ingénierie logicielle, intégration IT et conseil."""
    __tablename__ = Byt3labTables.SERVICES

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    title_fr = Column(String(200), nullable=False)
    title_en = Column(String(200), nullable=False)
    excerpt_fr = Column(Text, nullable=True)
    excerpt_en = Column(Text, nullable=True)
    content_fr = Column(Text, nullable=True)
    content_en = Column(Text, nullable=True)
    division_slug = Column(String(100), nullable=True)
    icon = Column(String(50), default="briefcase")
    order_num = Column(Integer, default=0)
    status = Column(String(50), default=STATUS_ACTIVE)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    def to_dict(self, lang: str = "fr") -> dict:
        is_en = lang == "en"
        return {
            "id": self.id,
            "slug": self.slug,
            "title": self.title_en if is_en and self.title_en else self.title_fr,
            "title_fr": self.title_fr,
            "title_en": self.title_en,
            "excerpt": self.excerpt_en if is_en and self.excerpt_en else self.excerpt_fr,
            "excerpt_fr": self.excerpt_fr,
            "excerpt_en": self.excerpt_en,
            "content": self.content_en if is_en and self.content_en else self.content_fr,
            "content_fr": self.content_fr,
            "content_en": self.content_en,
            "division_slug": self.division_slug,
            "icon": self.icon or "briefcase",
            "order_num": self.order_num or 0,
            "status": self.status,
            "is_published": self.is_published,
        }


class Byt3labProjectModel(Model):
    """Études de cas et projets réels réalisés par Byt3Lab."""
    __tablename__ = Byt3labTables.PROJECTS

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    title_fr = Column(String(200), nullable=False)
    title_en = Column(String(200), nullable=False)
    domain_fr = Column(String(100), nullable=True)
    domain_en = Column(String(100), nullable=True)
    excerpt_fr = Column(Text, nullable=True)
    excerpt_en = Column(Text, nullable=True)
    content_fr = Column(Text, nullable=True)
    content_en = Column(Text, nullable=True)
    image_url = Column(String(300), nullable=True)
    order_num = Column(Integer, default=0)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    def to_dict(self, lang: str = "fr") -> dict:
        is_en = lang == "en"
        return {
            "id": self.id,
            "slug": self.slug,
            "title": self.title_en if is_en and self.title_en else self.title_fr,
            "title_fr": self.title_fr,
            "title_en": self.title_en,
            "domain": self.domain_en if is_en and self.domain_en else self.domain_fr,
            "domain_fr": self.domain_fr,
            "domain_en": self.domain_en,
            "excerpt": self.excerpt_en if is_en and self.excerpt_en else self.excerpt_fr,
            "excerpt_fr": self.excerpt_fr,
            "excerpt_en": self.excerpt_en,
            "content": self.content_en if is_en and self.content_en else self.content_fr,
            "content_fr": self.content_fr,
            "content_en": self.content_en,
            "image_url": self.image_url or "",
            "order_num": self.order_num or 0,
            "is_published": self.is_published,
        }


class Byt3labPartnerModel(Model):
    """Partenaires technologiques, cloud, industriels et institutionnels."""
    __tablename__ = Byt3labTables.PARTNERS

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    category = Column(String(50), default="tech")  # tech, cloud, manufacturer, academic, commercial
    description_fr = Column(Text, nullable=True)
    description_en = Column(Text, nullable=True)
    logo_url = Column(String(300), nullable=True)
    website_url = Column(String(300), nullable=True)
    order_num = Column(Integer, default=0)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())

    def to_dict(self, lang: str = "fr") -> dict:
        is_en = lang == "en"
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "description": self.description_en if is_en and self.description_en else self.description_fr,
            "description_fr": self.description_fr,
            "description_en": self.description_en,
            "logo_url": self.logo_url or "",
            "website_url": self.website_url or "",
            "order_num": self.order_num or 0,
            "is_published": self.is_published,
        }


class Byt3labNgrafixModel(Model):
    """Réalisations et disciplines du studio créatif NGRAFIX."""
    __tablename__ = Byt3labTables.NGRAFIX

    id = Column(Integer, primary_key=True, autoincrement=True)
    title_fr = Column(String(200), nullable=False)
    title_en = Column(String(200), nullable=False)
    discipline = Column(String(50), default="branding")  # branding, creative_design, digital_exp, production
    description_fr = Column(Text, nullable=True)
    description_en = Column(Text, nullable=True)
    image_url = Column(String(300), nullable=True)
    client_name = Column(String(150), nullable=True)
    order_num = Column(Integer, default=0)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())

    def to_dict(self, lang: str = "fr") -> dict:
        is_en = lang == "en"
        return {
            "id": self.id,
            "title": self.title_en if is_en and self.title_en else self.title_fr,
            "title_fr": self.title_fr,
            "title_en": self.title_en,
            "discipline": self.discipline,
            "description": self.description_en if is_en and self.description_en else self.description_fr,
            "description_fr": self.description_fr,
            "description_en": self.description_en,
            "image_url": self.image_url or "",
            "client_name": self.client_name or "",
            "order_num": self.order_num or 0,
            "is_published": self.is_published,
        }


class Byt3labTeamModel(Model):
    """Membres de l'équipe et pôles d'expertise."""
    __tablename__ = Byt3labTables.TEAM

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(150), nullable=False)
    role_fr = Column(String(150), nullable=False)
    role_en = Column(String(150), nullable=False)
    domain = Column(String(100), nullable=True)
    bio_fr = Column(Text, nullable=True)
    bio_en = Column(Text, nullable=True)
    photo_url = Column(String(300), nullable=True)
    order_num = Column(Integer, default=0)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())

    def to_dict(self, lang: str = "fr") -> dict:
        is_en = lang == "en"
        return {
            "id": self.id,
            "slug": self.slug,
            "name": self.name,
            "role": self.role_en if is_en and self.role_en else self.role_fr,
            "role_fr": self.role_fr,
            "role_en": self.role_en,
            "domain": self.domain or "",
            "bio": self.bio_en if is_en and self.bio_en else self.bio_fr,
            "bio_fr": self.bio_fr,
            "bio_en": self.bio_en,
            "photo_url": self.photo_url or "",
            "order_num": self.order_num or 0,
            "is_published": self.is_published,
        }


class Byt3labJobModel(Model):
    """Offres d'emploi et carrières ouvertes au sein du groupe."""
    __tablename__ = Byt3labTables.JOBS

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    title_fr = Column(String(200), nullable=False)
    title_en = Column(String(200), nullable=False)
    division_slug = Column(String(100), nullable=True)
    location = Column(String(100), default="Douala / Yaoundé — Cameroun")
    contract_type = Column(String(50), default="CDI / Plein temps")
    description_fr = Column(Text, nullable=True)
    description_en = Column(Text, nullable=True)
    requirements = Column(JSON, default=list)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    def to_dict(self, lang: str = "fr") -> dict:
        is_en = lang == "en"
        return {
            "id": self.id,
            "slug": self.slug,
            "title": self.title_en if is_en and self.title_en else self.title_fr,
            "title_fr": self.title_fr,
            "title_en": self.title_en,
            "division_slug": self.division_slug,
            "location": self.location,
            "contract_type": self.contract_type,
            "description": self.description_en if is_en and self.description_en else self.description_fr,
            "description_fr": self.description_fr,
            "description_en": self.description_en,
            "requirements": self.requirements or [],
            "is_published": self.is_published,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Byt3labPostModel(Model):
    """Articles du blog institutionnel et actualités du groupe."""
    __tablename__ = Byt3labTables.POSTS

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String(150), unique=True, nullable=False, index=True)
    title_fr = Column(String(250), nullable=False)
    title_en = Column(String(250), nullable=False)
    summary_fr = Column(Text, nullable=True)
    summary_en = Column(Text, nullable=True)
    content_fr = Column(Text, nullable=True)
    content_en = Column(Text, nullable=True)
    cover_image = Column(String(300), nullable=True)
    author_name = Column(String(100), default="Byt3Lab Editorial")
    published_at = Column(DateTime(timezone=True), default=func.now())
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    def to_dict(self, lang: str = "fr") -> dict:
        is_en = lang == "en"
        return {
            "id": self.id,
            "slug": self.slug,
            "title": self.title_en if is_en and self.title_en else self.title_fr,
            "title_fr": self.title_fr,
            "title_en": self.title_en,
            "summary": self.summary_en if is_en and self.summary_en else self.summary_fr,
            "summary_fr": self.summary_fr,
            "summary_en": self.summary_en,
            "content": self.content_en if is_en and self.content_en else self.content_fr,
            "content_fr": self.content_fr,
            "content_en": self.content_en,
            "cover_image": self.cover_image or "",
            "author_name": self.author_name or "Byt3Lab",
            "published_at": self.published_at.strftime("%d/%m/%Y") if self.published_at else "",
            "is_published": self.is_published,
        }


class Byt3labMessageModel(Model):
    """Boîte de réception des demandes reçues (Contact & Partenariat)."""
    __tablename__ = Byt3labTables.MESSAGES

    id = Column(Integer, primary_key=True, autoincrement=True)
    form_type = Column(String(50), default="contact")  # contact, partner
    sender_name = Column(String(150), nullable=False)
    organization = Column(String(150), nullable=True)
    email = Column(String(150), nullable=False)
    phone = Column(String(50), nullable=True)
    subject = Column(String(200), nullable=True)
    partner_type = Column(String(100), nullable=True)
    domain = Column(String(100), nullable=True)
    website = Column(String(200), nullable=True)
    message = Column(Text, nullable=False)
    status = Column(String(50), default="new")  # new, in_progress, resolved
    ip_address = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "form_type": self.form_type,
            "sender_name": self.sender_name,
            "organization": self.organization or "",
            "email": self.email,
            "phone": self.phone or "",
            "subject": self.subject or "",
            "partner_type": self.partner_type or "",
            "domain": self.domain or "",
            "website": self.website or "",
            "message": self.message,
            "status": self.status,
            "ip_address": self.ip_address or "",
            "created_at": self.created_at.strftime("%d/%m/%Y %H:%M") if self.created_at else "",
        }


class Byt3labSettingModel(Model):
    """Paires clé-valeur bilingues pour les réglages du site."""
    __tablename__ = Byt3labTables.SETTINGS

    key = Column(String(150), primary_key=True)
    value_fr = Column(Text, nullable=True)
    value_en = Column(Text, nullable=True)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    def to_dict(self) -> dict:
        return {
            "key": self.key,
            "value_fr": self.value_fr or "",
            "value_en": self.value_en or "",
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
