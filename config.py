from __future__ import annotations
from typing import Any, Dict

MODULE_NAME = "byt3lab"

STATUS_ACTIVE = "active"
STATUS_IN_DEVELOPMENT = "in_development"
STATUS_STRATEGIC = "strategic"

MATURITY_STATUSES = {
    STATUS_ACTIVE: {
        "key": STATUS_ACTIVE,
        "label_fr": "Opérationnel",
        "label_en": "Operational",
        "desc_fr": "Activité ouverte, avec des offres disponibles dès aujourd'hui.",
        "desc_en": "Active operation with currently available market offerings.",
    },
    STATUS_IN_DEVELOPMENT: {
        "key": STATUS_IN_DEVELOPMENT,
        "label_fr": "En développement",
        "label_en": "In development",
        "desc_fr": "Activité en cours de structuration : premières offres et partenariats en construction.",
        "desc_en": "Structuring phase: initial offerings and strategic partnerships underway.",
    },
    STATUS_STRATEGIC: {
        "key": STATUS_STRATEGIC,
        "label_fr": "Orientation stratégique",
        "label_en": "Strategic orientation",
        "desc_fr": "Axe de développement à moyen et long terme du groupe.",
        "desc_en": "Medium and long-term strategic technological direction of the group.",
    },
}

PARTNER_CATEGORIES = {
    "tech": {"label_fr": "Fournisseurs technologiques", "label_en": "Technology providers"},
    "cloud": {"label_fr": "Opérateurs d'infrastructure & Cloud", "label_en": "Cloud & Infrastructure operators"},
    "manufacturer": {"label_fr": "Fabricants & Constructeurs", "label_en": "Manufacturers & Hardware builders"},
    "academic": {"label_fr": "Institutions académiques & Recherche", "label_en": "Academic & Research institutions"},
    "commercial": {"label_fr": "Partenaires commerciaux & Distribution", "label_en": "Commercial & Distribution partners"},
}

NGRAFIX_DISCIPLINES = {
    "branding": {"label_fr": "Identité de marque & Branding", "label_en": "Brand Identity & Branding"},
    "creative_design": {"label_fr": "Design créatif & UI/UX", "label_en": "Creative Design & UI/UX"},
    "digital_exp": {"label_fr": "Expérience digitale & Web", "label_en": "Digital Experience & Web"},
    "production": {"label_fr": "Communication & Production média", "label_en": "Media Production & Content"},
}

MESSAGE_STATUSES = {
    "new": {"label_fr": "Nouveau", "label_en": "New", "badge_class": "is-new"},
    "in_progress": {"label_fr": "En cours", "label_en": "In Progress", "badge_class": "is-progress"},
    "resolved": {"label_fr": "Traité", "label_en": "Resolved", "badge_class": "is-resolved"},
}

DEFAULT_SETTINGS: Dict[str, Dict[str, Any]] = {
    # Coordonnées & Réseaux
    "contact.email": {
        "fr": "contact@byt3lab.com",
        "en": "contact@byt3lab.com",
    },
    "contact.email_support": {
        "fr": "support@byt3lab.com",
        "en": "support@byt3lab.com",
    },
    "contact.email_careers": {
        "fr": "carrieres@byt3lab.com",
        "en": "careers@byt3lab.com",
    },
    "contact.email_partners": {
        "fr": "contact@byt3lab.com",
        "en": "contact@byt3lab.com",
    },
    "contact.phone": {
        "fr": "+237 696 87 94 75",
        "en": "+237 696 87 94 75",
    },
    "contact.phone2": {
        "fr": "+237 652 35 48 37",
        "en": "+237 652 35 48 37",
    },
    "contact.whatsapp": {
        "fr": "237696879475",
        "en": "237696879475",
    },
    "contact.location": {
        "fr": "Douala · Yaoundé — Cameroun",
        "en": "Douala · Yaoundé — Cameroon",
    },
    "social.linkedin": {
        "fr": "https://linkedin.com/company/byt3lab",
        "en": "https://linkedin.com/company/byt3lab",
    },
    "social.facebook": {
        "fr": "https://facebook.com/byt3lab",
        "en": "https://facebook.com/byt3lab",
    },
    "social.youtube": {
        "fr": "https://youtube.com/@byt3lab",
        "en": "https://youtube.com/@byt3lab",
    },
    "social.ngrafix": {
        "fr": "https://www.facebook.com/profile.php?id=61571483432231",
        "en": "https://www.facebook.com/profile.php?id=61571483432231",
    },
    "legal.company": {
        "fr": "Byt3Lab",
        "en": "Byt3Lab",
    },
    "legal.footer_text": {
        "fr": "Byt3Lab est un groupe technologique camerounais à vocation africaine. Nous concevons, développons, intégrons et exploitons des technologies pour les entreprises, les industries et les infrastructures.",
        "en": "Byt3Lab is a Cameroonian technology group with a pan-African vision. We design, develop, integrate, and operate cutting-edge technologies for businesses, industries, and infrastructures.",
    },

    # Textes de la page d'accueil
    "home.hero.signature": {
        "fr": "ENGINEERING THE TECHNOLOGIES OF TOMORROW.",
        "en": "ENGINEERING THE TECHNOLOGIES OF TOMORROW.",
    },
    "home.hero.title": {
        "fr": "Concevoir les technologies de demain.",
        "en": "Engineering the Technologies of Tomorrow.",
    },
    "home.hero.subtitle": {
        "fr": "Nous concevons, développons et déployons des technologies qui renforcent les entreprises, les industries et les infrastructures de demain.",
        "en": "We design, develop, and deploy technologies that empower businesses, industries, and critical infrastructure across Africa.",
    },
    "home.about.eyebrow": {
        "fr": "Byt3Lab",
        "en": "Byt3Lab",
    },
    "home.about.title": {
        "fr": "Plus que du logiciel. De l'ingénierie technologique.",
        "en": "More than software. Full-spectrum technological engineering.",
    },
    "home.about.text": {
        "fr": "Byt3Lab est un groupe technologique et d'innovation qui conçoit, développe et intègre des solutions répondant aux besoins évolutifs des entreprises, des industries et des infrastructures numériques.",
        "en": "Byt3Lab is a technology and innovation group designing, building, and deploying solutions tailored to the evolving demands of enterprises, industries, and digital infrastructure.",
    },
    "home.about.text2": {
        "fr": "Né de l'ingénierie logicielle, Byt3Lab organise désormais ses activités en divisions technologiques, en produits et en marques spécialisées, avec une ambition claire : bâtir depuis le Cameroun un groupe technologique au service du continent africain.",
        "en": "Originating from software engineering, Byt3Lab structures its activities into specialized technology divisions, proprietary products, and focused creative brands, aiming to build a continental tech powerhouse from Cameroon.",
    },
    "home.divisions.eyebrow": {
        "fr": "Nos divisions technologiques",
        "en": "Our Technology Divisions",
    },
    "home.divisions.title": {
        "fr": "L'ingénierie à travers les domaines technologiques.",
        "en": "Engineering Across Strategic Technology Domains.",
    },
    "home.divisions.intro": {
        "fr": "Cinq divisions structurent le développement du groupe. Chacune est présentée selon son niveau réel de maturité : certaines sont opérationnelles, d'autres en construction.",
        "en": "Five strategic divisions shape the group's trajectory, clearly reflecting their genuine maturity levels: some fully operational, others in active development.",
    },
    "home.offers.eyebrow": {
        "fr": "Produits & solutions",
        "en": "Products & Solutions",
    },
    "home.offers.title": {
        "fr": "Des technologies conçues pour résoudre des problèmes réels.",
        "en": "Technologies Engineered to Solve Real-World Challenges.",
    },
    "home.offers.intro": {
        "fr": "Des produits logiciels propriétaires et une activité de services d'infrastructure, développés et exploités par Byt3Lab.",
        "en": "Proprietary software suites and enterprise infrastructure services engineered and operated by Byt3Lab.",
    },
    "home.ngrafix.eyebrow": {
        "fr": "Studio créatif de l'écosystème",
        "en": "Ecosystem Creative Studio",
    },
    "home.ngrafix.title": {
        "fr": "Au-delà de la technologie : créer des expériences de marque.",
        "en": "Beyond Technology: Shaping Distinctive Brand Experiences.",
    },
    "home.ngrafix.text": {
        "fr": "À travers NGRAFIX, Byt3Lab étend son expertise à l'identité de marque, au design créatif et à la communication digitale, pour aider les entreprises à construire des expériences de marque fortes et distinctives.",
        "en": "Through NGRAFIX, Byt3Lab expands its creative mastery into brand identity, UI/UX design, and digital communication, empowering organizations to forge memorable brand identities.",
    },
    "home.innovation.eyebrow": {
        "fr": "Technologie & innovation",
        "en": "Technology & Innovation",
    },
    "home.innovation.title": {
        "fr": "Construire ce qui vient.",
        "en": "Building What Lies Ahead.",
    },
    "home.innovation.intro": {
        "fr": "Notre feuille de route s'inscrit dans la durée. Ces domaines orientent nos investissements, nos partenariats et le développement de nos futures solutions.",
        "en": "Our forward-looking roadmap is built for lasting impact, guiding research, technological investments, and strategic ecosystem alliances.",
    },
    "home.industries.eyebrow": {
        "fr": "Secteurs",
        "en": "Industries",
    },
    "home.industries.title": {
        "fr": "La technologie au service de chaque secteur.",
        "en": "Powering Transformation Across Vital Industries.",
    },
    "home.projects.eyebrow": {
        "fr": "Réalisations",
        "en": "Achievements",
    },
    "home.projects.title": {
        "fr": "L'ingénierie mise en pratique.",
        "en": "Engineering Put into Concrete Practice.",
    },
    "home.projects.intro": {
        "fr": "Chaque projet illustre notre capacité à concevoir et déployer des solutions adaptées aux réalités de nos partenaires.",
        "en": "Each deployment demonstrates our capability to engineer and maintain robust systems aligned with real-world requirements.",
    },
    "home.partners.eyebrow": {
        "fr": "Partenariats & Alliances",
        "en": "Partnerships & Alliances",
    },
    "home.partners.title": {
        "fr": "Construire l'avenir avec nos partenaires.",
        "en": "Shaping the Future Alongside Industry Partners.",
    },
    "home.partners.intro": {
        "fr": "Fournisseurs de technologies, opérateurs cloud, constructeurs, institutions académiques et partenaires commerciaux.",
        "en": "Technology providers, cloud operators, equipment manufacturers, academic institutions, and commercial partners.",
    },
    "home.cta.title": {
        "fr": "Concevons ensemble les technologies de demain.",
        "en": "Let's Engineer the Technologies of Tomorrow Together.",
    },
    "home.cta.text": {
        "fr": "Vous avez un projet d'ingénierie, un besoin d'infrastructure ou souhaitez bâtir un partenariat stratégique ? Échangeons dès aujourd'hui.",
        "en": "Do you have an ambitious engineering project, infrastructure needs, or wish to forge a strategic partnership? Let's connect today.",
    },
}
