from __future__ import annotations
from typing import Dict, Any, List
from datetime import datetime, timezone
from ..repositories.division_repository import DivisionRepository
from ..repositories.solution_repository import SolutionRepository
from ..repositories.service_repository import ServiceRepository
from ..repositories.partner_repository import PartnerRepository
from ..repositories.ngrafix_repository import NgrafixRepository
from ..repositories.team_repository import TeamRepository
from ..repositories.job_repository import JobRepository
from ..repositories.project_repository import ProjectRepository
from ..repositories.post_repository import PostRepository
from ..repositories.blog_category_repository import BlogCategoryRepository
from ..repositories.message_repository import MessageRepository
from ..config import (
    STATUS_ACTIVE,
    STATUS_IN_DEVELOPMENT,
    STATUS_STRATEGIC,
    PARTNER_CATEGORIES,
)


class ContentService:

    @classmethod
    async def seed_initial_content(cls, session, force: bool = False):
        """
        Injecte un jeu complet de données de démonstration et de production initiales
        pour toutes les tables du module BYT3LAB si elles sont vides ou si force=True.
        Met à jour de manière idempotente les enregistrements existants lorsque force=True.
        """

        # 1. LES 4 PÔLES OFFICIELS DU GROUPE BYT3LAB
        existing_divisions = await DivisionRepository.get_all(session, published_only=False)
        if not existing_divisions or force:
            divisions_data = [
                {
                    "slug": "software",
                    "title_fr": "Byt3Lab Software",
                    "title_en": "Byt3Lab Software",
                    "icon": "code",
                    "order_num": 1,
                    "maturity_status": STATUS_ACTIVE,
                    "excerpt_fr": "Développement logiciel, plateforme modulaire MELODI ERP, modules ASSO (gestion commerciale) & SUKU (gestion scolaire), APIs et automatisation.",
                    "excerpt_en": "Software development, modular MELODI ERP platform, ASSO (commercial management) & SUKU (school management) modules, APIs and automation.",
                    "content_fr": "Byt3Lab Software conçoit et commercialise des solutions logicielles permettant aux entreprises de gérer, automatiser et optimiser leurs activités, autour du socle stratégique MELODI ERP.",
                    "content_en": "Byt3Lab Software designs and delivers business software solutions enabling organizations to manage, automate and optimize operations around the MELODI ERP platform.",
                    "vision_fr": "Donner aux entreprises et institutions africaines des logiciels fiables, modulaires et pérennes.",
                    "vision_en": "Empowering African enterprises with reliable, modular and future-proof business software.",
                    "expertise_list": ["Plateforme modulaire MELODI ERP", "Logiciels métier & CRM", "Applications web & mobiles", "Développement d'APIs & automatisation"],
                    "technologies_list": ["Python asynchrone", "PostgreSQL", "TypeScript & MelodiJS", "REST & Webhooks"],
                    "services_list": ["Déploiement MELODI ERP", "Modules ASSO & SUKU", "Développement sur mesure"],
                    "industries_list": ["Commerce & Distribution", "Éducation", "Services & PME"],
                    "related_slugs": ["melodi-erp", "asso", "suku"],
                    "is_published": True,
                },
                {
                    "slug": "web-services",
                    "title_fr": "Byt3Lab Web Services",
                    "title_en": "Byt3Lab Web Services",
                    "icon": "cloud",
                    "order_num": 2,
                    "maturity_status": STATUS_ACTIVE,
                    "excerpt_fr": "Hébergement web & applicatif, serveurs VPS & dédiés, cloud computing, sauvegardes et infogérance managée.",
                    "excerpt_en": "Web & application hosting, VPS & dedicated servers, cloud computing, automated backups and managed operations.",
                    "content_fr": "Byt3Lab Web Services fournit les infrastructures numériques et services managés nécessaires pour héberger, exploiter et sécuriser les applications et données d'entreprise.",
                    "content_en": "Byt3Lab Web Services delivers the digital infrastructure and managed services required to host, operate and secure business applications and data.",
                    "vision_fr": "Développer des capacités d'hébergement et des services cloud fiables adaptés aux entreprises africaines.",
                    "vision_en": "Building reliable hosting and cloud capabilities tailored to African businesses.",
                    "expertise_list": ["Hébergement web & applicatif", "Serveurs VPS & dédiés", "Sauvegardes & haute disponibilité", "Administration système & infogérance"],
                    "technologies_list": ["Linux Enterprise", "Nginx & HAProxy", "PostgreSQL & Redis", "Docker"],
                    "services_list": ["Hébergement applicatif", "Infogérance & supervision", "Déploiement continu"],
                    "industries_list": ["PME & ETI", "Finance", "Institutions"],
                    "related_slugs": ["bws"],
                    "is_published": True,
                },
                {
                    "slug": "equipment",
                    "title_fr": "Byt3Lab Equipment",
                    "title_en": "Byt3Lab Equipment",
                    "icon": "server",
                    "order_num": 3,
                    "maturity_status": STATUS_ACTIVE,
                    "excerpt_fr": "Équipements informatiques, réseaux, vidéosurveillance, énergie de secours (solaire/onduleurs) et Equipment as a Service.",
                    "excerpt_en": "IT hardware, enterprise networking, IP surveillance, backup energy (solar/UPS) and Equipment as a Service.",
                    "content_fr": "Byt3Lab Equipment accompagne les organisations dans l'acquisition ou la location (Equipment as a Service) de leurs parcs informatiques, réseaux, sécurité physique et solutions énergétiques avec maintenance.",
                    "content_en": "Byt3Lab Equipment supports organizations in purchasing or subscribing (Equipment as a Service) to IT hardware, networks, physical security and backup energy with ongoing maintenance.",
                    "vision_fr": "Faciliter l'accès aux équipements technologiques et énergétiques professionnels sans frein financier.",
                    "vision_en": "Making professional IT and energy infrastructure accessible without heavy upfront capital.",
                    "expertise_list": ["Équipements informatiques & serveurs", "Réseaux d'entreprise & télécoms", "Vidéosurveillance IP & contrôle d'accès", "Onduleurs & solaire hybride", "Equipment as a Service (EaaS)"],
                    "technologies_list": ["Réseaux Wi-Fi & fibre", "Caméras IP & NVR", "Onduleurs & stockage solaire"],
                    "services_list": ["Équipement complet de bureaux", "Location avec maintenance (EaaS)", "Maintenance préventive & corrective"],
                    "industries_list": ["Entreprises & Sièges sociaux", "Établissements scolaires", "Commerce & Industrie"],
                    "related_slugs": [],
                    "is_published": True,
                },
                {
                    "slug": "ngrafix",
                    "title_fr": "ngrafix",
                    "title_en": "ngrafix",
                    "icon": "palette",
                    "order_num": 4,
                    "maturity_status": STATUS_ACTIVE,
                    "excerpt_fr": "Marque créative du groupe : identité visuelle, branding, UI/UX design, communication digitale et production graphique.",
                    "excerpt_en": "Creative brand of the group: visual identity, branding, UI/UX design, digital communication and graphic production.",
                    "content_fr": "ngrafix accompagne les entreprises dans la construction de leur identité visuelle, la conception d'interfaces numériques UI/UX, leur communication digitale et la production de supports graphiques.",
                    "content_en": "ngrafix helps organizations build distinctive brand identities, intuitive UI/UX digital products, digital communication campaigns and print production.",
                    "vision_fr": "Allier rigueur stratégique et exigence créative pour valoriser les marques africaines.",
                    "vision_en": "Combining strategic clarity and creative excellence to elevate African brands.",
                    "expertise_list": ["Branding & identité visuelle", "UI/UX Design d'applications & sites web", "Communication & marketing digital", "Production graphique & print"],
                    "technologies_list": ["Figma", "Adobe Creative Suite", "Design Systems"],
                    "services_list": ["Logos & chartes graphiques", "Maquettage UI/UX", "Campagnes & supports imprimés"],
                    "industries_list": ["Startups & Tech", "Corporate & Institutions", "Commerce & Marques"],
                    "related_slugs": [],
                    "is_published": True,
                },
            ]
            for div_data in divisions_data:
                existing = await DivisionRepository.get_by_slug(session, div_data["slug"])
                if existing:
                    await DivisionRepository.update(session, existing.id, div_data)
                else:
                    await DivisionRepository.create(session, div_data)

        # 2. PRODUITS & SOLUTIONS (Socle MELODI ERP + Modules Verticaux ASSO, SUKU & BWS)
        existing_solutions = await SolutionRepository.get_all(session, published_only=False)
        existing_slugs = {s.slug for s in existing_solutions}
        if not existing_solutions or "asso" not in existing_slugs or force:
            solutions_data = [
                {
                    "slug": "melodi-erp",
                    "title_fr": "MELODI ERP",
                    "title_en": "MELODI ERP",
                    "solution_type": "software",
                    "status": STATUS_ACTIVE,
                    "division_slug": "software",
                    "badge_fr": "Socle ERP Fondateur",
                    "badge_en": "Foundational ERP Core",
                    "tagline_fr": "Le socle progiciel de base modulaire pour concevoir et propulser des modules métier spécialisés (ASSO, SUKU, etc.).",
                    "tagline_en": "The foundational modular ERP core engineered to build and power specialized business modules (ASSO, SUKU, etc.).",
                    "accent_color": "#1D7FD8",
                    "order_num": 1,
                    "excerpt_fr": "Socle applicatif modulaire de nouvelle génération : noyau asynchrone, gestion des permissions RBAC, multi-sociétés, comptabilité OHADA et bus d'événements permettant de développer des modules métier ciblés comme ASSO (gestion commerciale) et SUKU (gestion scolaire).",
                    "excerpt_en": "Next-generation modular application core: asynchronous engine, RBAC security, multi-company foundation, OHADA accounting, and event bus powering vertical modules like ASSO (commercial management) and SUKU (school management).",
                    "content_fr": """<h3>Le Socle Technologique &amp; Progiciel de Base pour vos Modules Métiers</h3>
<p><strong>MELODI ERP</strong> est le socle fondateur de l'écosystème logiciel BYT3LAB. Conçu comme une véritable plateforme d'architecture modulaire (<em>Core Engine</em>), MELODI fournit les fondations critiques communes à toute organisation moderne — authentification, RBAC granulaire, multi-devises, multi-agences, bus d'événements asynchrone et conformité comptable OHADA — afin de bâtir rapidement des modules spécialisés par secteur d'activité.</p>
<h4>Des Modules Verticaux Propulsés par le Socle MELODI :</h4>
<ul>
  <li><strong>ASSO (Gestion commerciale) :</strong> Module dédié au commerce, à la distribution, aux stocks multi-dépôts, à la facturation et aux terminaux de caisse tactiles.</li>
  <li><strong>SUKU (Gestion scolaire) :</strong> Module intégré dédié aux écoles, collèges, lycées et instituts supérieurs.</li>
  <li><strong>Extensions Sur-Mesure :</strong> Un moteur ouvert par hooks et API permettant aux entreprises d'assembler leurs propres modules métiers sans repartir de zéro.</li>
</ul>
<p>Grâce à son moteur asynchrone haute performance et son architecture <em>API-First</em>, MELODI ERP garantit une souveraineté totale des données, un déploiement hybride (Cloud ou local) et une évolutivité sans limite.</p>""",
                    "content_en": """<h3>The Foundational Modular ERP Core Powering Domain-Specific Modules</h3>
<p><strong>MELODI ERP</strong> is the foundational software engine of the BYT3LAB ecosystem. Designed as an extensible <em>Core Engine</em>, MELODI provides the unified enterprise backbone — authentication, granular RBAC permissions, multi-currency, multi-branch isolation, asynchronous event bus, and OHADA accounting — enabling rapid development of vertical modules tailored to specific industries.</p>
<h4>Vertical Modules Built on the MELODI Core:</h4>
<ul>
  <li><strong>ASSO (Commercial Management):</strong> Dedicated commerce, multi-warehouse inventory, invoicing, and offline-resilient Point-of-Sale module.</li>
  <li><strong>SUKU (School Management):</strong> Integrated academic lifecycle module for primary schools, high schools, and higher education campuses.</li>
  <li><strong>Custom Vertical Extensions:</strong> A hook-based, API-first architecture allowing organizations to deploy custom modules without reinventing core infrastructure.</li>
</ul>
<p>Built on a high-throughput asynchronous engine, MELODI ERP guarantees full data sovereignty, hybrid deployment (Sovereign Cloud or On-Premises), and seamless scalability.</p>""",
                    "features_list": [
                        "Architecture modulaire hot-pluggable servant de socle à des modules verticaux (ASSO, SUKU)",
                        "Noyau asynchrone Python / PostgreSQL haute performance et API-First",
                        "Sécurité RBAC granulaire par rôles, permissions et multi-agences",
                        "Bus d'événements persistant et système de hooks inter-modules découplé",
                        "Comptabilité générale & États financiers conformes SYSCOHADA",
                        "Trésorerie unifiée, devises multiples et passerelles de paiement",
                        "Interface hybride réactive (MelodiJS) & support hors-ligne synchronisé",
                        "Déploiement souverain (Cloud BWS ou Serveur local d'entreprise)",
                    ],
                    "problems_list": [
                        "Rigidité des progiciels monolithiques impossibles à adapter à un secteur précis",
                        "Duplication coûteuse des briques de base (utilisateurs, sécurité, comptabilité) sur chaque projet",
                        "Manque de souveraineté et dépendance vis-à-vis de licences étrangères fermées",
                        "Difficulté à unifier les flux entre plusieurs activités ou filiales",
                    ],
                    "benefits_list": [
                        "Un socle unique et éprouvé pour propulser ASSO, SUKU et vos applications sur-mesure",
                        "Réduction drastique des délais de développement de nouveaux produits métiers",
                        "Traçabilité totale et interopérabilité native entre tous les modules activés",
                        "Accompagnement direct et support de proximité par les ingénieurs BYT3LAB",
                    ],
                    "button_label_fr": "Découvrir le socle MELODI",
                    "button_label_en": "Explore MELODI Core",
                    "button_url": "https://melodi.byt3lab.com",
                    "is_published": True,
                },
                {
                    "slug": "asso",
                    "title_fr": "ASSO",
                    "title_en": "ASSO",
                    "solution_type": "software",
                    "status": STATUS_ACTIVE,
                    "division_slug": "software",
                    "badge_fr": "Gestion commerciale",
                    "badge_en": "Commercial Management",
                    "tagline_fr": "Module de gestion commerciale, stocks multi-dépôts, facturation et caisse tactile (POS) bâti sur le socle MELODI ERP.",
                    "tagline_en": "Commercial management, multi-warehouse inventory, invoicing, and POS module powered by the MELODI ERP core.",
                    "accent_color": "#10B981",
                    "order_num": 2,
                    "excerpt_fr": "Module de gestion commerciale complet propulsé par MELODI ERP : devis, commandes, facturation conforme, caisse POS tactile hors-ligne, stocks multi-entrepôts et suivi des règlements.",
                    "excerpt_en": "Complete commercial management module powered by MELODI ERP: quotations, orders, compliant invoicing, offline-ready POS registers, multi-warehouse stock, and payment tracking.",
                    "content_fr": """<h3>Gestion commerciale &amp; Point de Vente propulsés par MELODI ERP</h3>
<p><strong>ASSO</strong> est le module de gestion commerciale de BYT3LAB dédié au pilotage du négoce, de la distribution et de la vente au détail (Retail). Développé directement sur le <strong>socle technologique MELODI ERP</strong>, ASSO combine la puissance d'un ERP comptable et financier à la rapidité d'exécution d'une caisse moderne.</p>
<h4>Périmètre fonctionnel d'ASSO :</h4>
<ul>
  <li><strong>Cycle de Vente &amp; Facturation :</strong> Élaboration rapide de devis, bons de commande, bons de livraison, factures proforma/définitives et avoirs avec gestion fine des remises et taxes.</li>
  <li><strong>Terminal Point de Vente (POS) Tactile :</strong> Interface d'encaissement fluide adaptée aux boutiques, supermarchés et points de distribution, avec mode résilient hors-ligne et synchronisation automatique.</li>
  <li><strong>Gestion des Stocks Multi-Dépôts :</strong> Suivi en temps réel des entrées/sorties, transferts inter-magasins, alertes de seuil critique, valorisation et inventaires tournants par code-barres.</li>
  <li><strong>Suivi Clients &amp; Encaissements :</strong> Gestion des comptes clients, plafonds de crédit, échéanciers, relances et intégration directe Mobile Money (Orange Money, MTN MoMo).</li>
</ul>
<p>Parce qu'il repose nativement sur le socle MELODI ERP, chaque vente effectuée dans ASSO alimente automatiquement votre trésorerie et votre comptabilité sans double saisie.</p>""",
                    "content_en": """<h3>Commercial Management &amp; Point-of-Sale Powered by MELODI ERP</h3>
<p><strong>ASSO</strong> is BYT3LAB's commercial management module engineered for retail, wholesale distribution, and sales operations. Built directly on the <strong>MELODI ERP foundation</strong>, ASSO combines enterprise-grade financial and inventory control with lightning-fast counter checkout.</p>
<h4>Core Capabilities of ASSO:</h4>
<ul>
  <li><strong>End-to-End Sales &amp; Invoicing:</strong> Quotations, sales orders, delivery notes, compliant tax invoicing, credit notes, and multi-tier pricing rules.</li>
  <li><strong>Touchscreen Point-of-Sale (POS):</strong> High-speed checkout interface built for retail stores and distribution counters, featuring offline continuity and automatic sync.</li>
  <li><strong>Multi-Warehouse Inventory Control:</strong> Real-time stock movements, inter-branch transfers, barcode inventory audits, and low-stock alerts.</li>
  <li><strong>Customer Accounts &amp; Payments:</strong> Credit limit enforcement, installment tracking, and native Mobile Money &amp; bank payment reconciliation.</li>
</ul>
<p>Because ASSO runs natively on the MELODI ERP core, every transaction automatically updates your general ledger and treasury dashboards in real time.</p>""",
                    "features_list": [
                        "Terminal Point de Vente (POS) tactile avec continuité hors-ligne",
                        "Gestion des devis, commandes, livraisons et facturation certifiée",
                        "Gestion avancée des stocks multi-dépôts & transferts inter-agences",
                        "Lecteur code-barres, étiquetage et inventaires rapides",
                        "Gestion des prix multi-niveaux, promotions et remises clients",
                        "Suivi des créances clients, règlements partiels et Mobile Money",
                        "Intégration comptable et trésorerie native via le socle MELODI ERP",
                        "Rapports de marge, chiffre d'affaires et rotation des stocks en direct",
                    ],
                    "problems_list": [
                        "Écarts récurrents d'inventaire et ruptures de stock non détectées à temps",
                        "Pertes financières liées aux encaissements manuels non rapprochés",
                        "Interruptions de vente aux caisses lors des coupures d'accès Internet",
                        "Saisie comptable manuelle fastidieuse en fin de journée ou de mois",
                    ],
                    "benefits_list": [
                        "Zéro rupture de service en caisse grâce à l'architecture résiliente MELODI",
                        "Visibilité immédiate sur les marges par produit, boutique ou vendeur",
                        "Comptabilisation automatique des ventes et encaissements sans double saisie",
                        "Évolutivité garantie vers d'autres modules du socle MELODI ERP",
                    ],
                    "button_label_fr": "Découvrir ASSO",
                    "button_label_en": "Explore ASSO",
                    "button_url": "https://byt3lab.com",
                    "is_published": True,
                },
                {
                    "slug": "suku",
                    "title_fr": "SUKU",
                    "title_en": "SUKU",
                    "solution_type": "software",
                    "status": STATUS_ACTIVE,
                    "division_slug": "software",
                    "badge_fr": "Gestion scolaire",
                    "badge_en": "School Management",
                    "tagline_fr": "Plateforme technologique intégrée dédiée à la gestion des établissements scolaires et académiques, propulsée par le socle MELODI ERP.",
                    "tagline_en": "Comprehensive educational ecosystem for schools and campuses, powered by the MELODI ERP foundational core.",
                    "accent_color": "#1E9E6A",
                    "order_num": 3,
                    "excerpt_fr": "Solution métier de gestion scolaire bâtie sur le socle MELODI ERP : inscriptions, scolarité, bulletins électroniques, emplois du temps et portail parents.",
                    "excerpt_en": "Vertical school management solution built on the MELODI ERP core: admissions, tuition fees, digital report cards, schedules, and parent portals.",
                    "content_fr": """<h3>L'écosystème numérique tout-en-un pour établissements scolaires (Propulsé par le socle MELODI ERP)</h3>
<p><strong>SUKU</strong> est le produit métier spécialisé pour le secteur éducatif, conçu directement sur l'architecture du <strong>socle MELODI ERP</strong>. Elle digitalise l'intégralité de la vie académique, financière et administrative des établissements scolaires, collèges, lycées et instituts universitaires. La plateforme connecte en temps réel la direction générale, le corps professoral, les apprenants et les parents d'élèves au sein d'une interface intuitive et sécurisée.</p>
<h4>Fonctionnalités clés de SUKU :</h4>
<ul>
  <li><strong>Gestion des scolarités &amp; Encaissements sécurisés :</strong> Collecte des droits d'inscription par Mobile Money, suivi des impayés et reçus électroniques horodatés.</li>
  <li><strong>Relevés de notes &amp; Bulletins automatisés :</strong> Calcul automatique des moyennes, classements par filière et génération en un clic des bulletins officiels conformes aux arrêtés ministériels.</li>
  <li><strong>Assiduité &amp; Discipline en direct :</strong> Pointage des absences par cours, notifications instantanées aux parents par SMS et WhatsApp.</li>
  <li><strong>Espace Parents &amp; Vie Scolaire :</strong> Portail web et mobile dédié permettant aux familles de suivre l'évolution scolaire et d'échanger avec l'administration.</li>
</ul>
<p>Avec SUKU, gagnez jusqu'à 80% de temps sur les tâches administratives et offrez une expérience d'excellence aux familles.</p>""",
                    "content_en": """<h3>The Comprehensive All-in-One Digital Campus &amp; School Management System</h3>
<p><strong>SUKU</strong> digitizes the entire academic, financial, and operational lifecycle of primary schools, secondary institutions, and higher education campuses. It provides a cohesive, unified digital environment bridging school administrators, educators, students, and parents.</p>
<h4>Key Platform Modules:</h4>
<ul>
  <li><strong>Tuition Collection &amp; Financial Tracking:</strong> Secure tuition fee collection via Mobile Money and bank cards, automated payment reminders, and digital receipts.</li>
  <li><strong>Automated Grading &amp; Report Cards:</strong> Instant GPA and weighted average computations, ranking generation, and ministry-compliant digital report cards.</li>
  <li><strong>Real-Time Attendance &amp; Discipline:</strong> Session-by-session student check-ins with automated instant alerts sent to parents via SMS and push notifications.</li>
  <li><strong>Parent &amp; Student Portal:</strong> Dedicated mobile-first portal for real-time grade monitoring, fee schedules, homework tracking, and school announcements.</li>
</ul>
<p>SUKU reduces administrative overhead by up to 80% while restoring parental trust through transparent, timely communication.</p>""",
                    "features_list": [
                        "Gestion des admissions et dossiers scolaires numériques",
                        "Suivi des frais de scolarité et paiements mobiles (MTN, Orange)",
                        "Saisie des notes, calculs de moyennes et génération automatique de bulletins",
                        "Gestion des absences, retards et discipline en temps réel",
                        "Portail web et mobile interactif pour les parents d'élèves",
                        "Gestion des emplois du temps et affectation des salles",
                    ],
                    "problems_list": [
                        "Files d'attente interminables lors des rentrées et des paiements de scolarité",
                        "Calculs manuels fastidieux de moyennes avec risques d'erreurs récurrentes",
                        "Manque de communication fluide entre l'école et les parents sur l'assiduité",
                    ],
                    "benefits_list": [
                        "Sécurisation des encaissements de scolarité sans déperdition",
                        "Génération instantanée des bulletins conformes aux normes ministérielles",
                        "Transparence totale pour les parents et valorisation de l'établissement",
                    ],
                    "button_label_fr": "Découvrir SUKU",
                    "button_label_en": "Discover SUKU",
                    "button_url": "https://suku.byt3lab.com",
                    "is_published": True,
                },
                {
                    "slug": "bws",
                    "title_fr": "BWS — Byt3Lab Web Services",
                    "title_en": "BWS — Byt3Lab Web Services",
                    "solution_type": "service_activity",
                    "status": STATUS_IN_DEVELOPMENT,
                    "division_slug": "web-services",
                    "badge_fr": "Services d'Infrastructure",
                    "badge_en": "Cloud Infrastructure",
                    "tagline_fr": "Hébergement managé haute disponibilité et infogérance cloud professionnelle.",
                    "tagline_en": "High-availability managed hosting, enterprise cloud, and proactive systems management.",
                    "accent_color": "#0B3D6B",
                    "order_num": 3,
                    "excerpt_fr": "Serveurs dédiés, hébergement web managé, infogérance d'applications critiques, sauvegardes répliquées et sécurité.",
                    "excerpt_en": "Dedicated servers, managed cloud hosting, critical app operations, offsite backups, and cybersecurity.",
                    "content_fr": """<h3>Byt3Lab Web Services (BWS) : Infrastructures Cloud &amp; Infogérance Proactive</h3>
<p><strong>BWS</strong> est l'activité d'infrastructure managée et de services cloud de Byt3Lab. Conçue pour héberger des applications critiques et des progiciels d'entreprise, BWS allie performance matérielle de pointe, isolation stricte et accompagnement technique de proximité.</p>
<h4>Offres d'infrastructures et engagements :</h4>
<ul>
  <li><strong>Serveurs Dédiés &amp; VPS Haute Performance :</strong> Hébergement sur architectures sécurisées avec disques NVMe et réseau très haut débit redondant.</li>
  <li><strong>Infogérance 24/7 &amp; Télémesure :</strong> Surveillance active des métriques système (CPU, RAM, I/O disque), détection proactive d'anomalies et interventions rapides.</li>
  <li><strong>Plan de Reprise d'Activité (PRA) &amp; Sauvegardes :</strong> Sauvegardes automatisées quotidiennes répliquées sur des sites géographiquement distincts.</li>
  <li><strong>Sécurité Réseau &amp; Protection Anti-DDoS :</strong> Filtrage du trafic malveillant, durcissement des systèmes d'exploitation et certificats SSL managés.</li>
</ul>
<p>Confiez l'exploitation technique de vos serveurs à une équipe d'ingénieurs chevronnés et concentrez-vous sur votre cœur de métier.</p>""",
                    "content_en": """<h3>Byt3Lab Web Services (BWS): Mission-Critical Managed Cloud Infrastructure</h3>
<p><strong>BWS</strong> represents Byt3Lab's enterprise managed cloud and systems engineering division. Engineered to host business-critical ERP workloads, APIs, and transactional databases, BWS delivers enterprise reliability, robust data protection, and dedicated engineering oversight.</p>
<h4>Infrastructure Services &amp; Guarantees:</h4>
<ul>
  <li><strong>High-Performance Dedicated Servers &amp; VPS:</strong> Compute nodes backed by high-speed enterprise NVMe storage and multi-gigabit redundant network uplinks.</li>
  <li><strong>24/7 Proactive Monitoring &amp; Telemetry:</strong> Continuous health checks across operating systems, database queries, and network latencies with guaranteed response SLAs.</li>
  <li><strong>Disaster Recovery &amp; Automated Backups:</strong> Daily automated snapshots replicated to isolated offsite data vaults with verified restore procedures.</li>
  <li><strong>Cybersecurity Hardening &amp; DDoS Shielding:</strong> Perimeter firewall defenses, intrusion prevention, encrypted communications, and managed SSL certificates.</li>
</ul>
<p>Delegate server management complexity to our systems engineering team and ensure uninterrupted uptime for your critical business applications.</p>""",
                    "features_list": [
                        "Serveurs virtuels (VPS) et serveurs dédiés haute performance",
                        "Infogérance proactive et monitoring temps réel 24/7",
                        "Sauvegardes automatisées quotidiennes hors-site",
                        "Certificats SSL et protection DDoS intégrée",
                        "Support technique réactif et accompagnement au déploiement",
                    ],
                    "problems_list": [
                        "Applications hébergées sans supervision ni sauvegardes fiables",
                        "Absence de compétences système en interne chez les clients",
                        "Pannes non anticipées et risques de perte définitive de données",
                    ],
                    "benefits_list": [
                        "Tranquillité d'esprit avec un SLA garanti",
                        "Interlocuteur technique local expert et accessible",
                        "Infrastructures modernes et évolutives selon les montées en charge",
                    ],
                    "button_label_fr": "Demander une offre BWS",
                    "button_label_en": "Request a BWS Proposal",
                    "button_url": "/contact/",
                    "is_published": True,
                },
            ]
            for sol_data in solutions_data:
                existing = await SolutionRepository.get_by_slug(session, sol_data["slug"])
                if existing:
                    await SolutionRepository.update(session, existing.id, sol_data)
                else:
                    await SolutionRepository.create(session, sol_data)

        # 3. SERVICES D'INGÉNIERIE (4 offres bilingues avec HTML riche Quill)
        existing_services = await ServiceRepository.get_all(session, published_only=False)
        if not existing_services or force:
            services_data = [
                {
                    "slug": "architecture-conseil-logiciel",
                    "title_fr": "Architecture & Conseil Logiciel",
                    "title_en": "Software Architecture & Consulting",
                    "division_slug": "software",
                    "icon": "layers",
                    "order_num": 1,
                    "status": STATUS_ACTIVE,
                    "excerpt_fr": "Cadrage technique, modélisation de bases de données, choix technologiques et conception de systèmes résilients.",
                    "excerpt_en": "Technical scoping, database schema design, technology selection, and resilient system architecture.",
                    "content_fr": """<h3>Cadrage stratégique, modélisation de données et conception de systèmes résilients</h3>
<p>Avant d'écrire la moindre ligne de code, la réussite d'un système d'information repose sur des choix d'architecture solides. Byt3Lab accompagne les directions techniques et générales dans la structuration de leurs plateformes logicielles complexes.</p>
<h4>Nos champs d'intervention :</h4>
<ul>
  <li><strong>Audit &amp; Diagnostic d'architecture :</strong> Analyse des goulots d'étranglement, dettes techniques et limites de passage à l'échelle.</li>
  <li><strong>Modélisation relationnelle &amp; Bases de données :</strong> Schémas relationnels optimisés pour PostgreSQL, indexation fine et gestion des transactions concurrentes.</li>
  <li><strong>Architecture orientée services &amp; Événements :</strong> Découpage modulaire clair, bus d'événements et patterns microservices asynchrones.</li>
  <li><strong>Sélection de la pile technologique :</strong> Choix rigoureux des frameworks, langages et bibliothèques assurant longévité et maintenabilité.</li>
</ul>""",
                    "content_en": """<h3>Strategic Architecture, Data Modeling, and Resilient Software Systems Design</h3>
<p>The long-term success of an enterprise platform relies on solid architectural blueprints prior to implementation. Byt3Lab guides engineering leaders and executives in conceptualizing resilient, maintainable, and scalable software ecosystems.</p>
<h4>Our Core Architecture Practices:</h4>
<ul>
  <li><strong>Architecture Audits &amp; Scalability Roadmaps:</strong> Deep investigation of application bottlenecks, technical debt, and concurrency ceilings.</li>
  <li><strong>Relational Data Architecture:</strong> High-performance PostgreSQL schema design, fine-grained indexing, and transactional isolation tuning.</li>
  <li><strong>Service-Oriented &amp; Event-Driven Architecture:</strong> Clear modular domain boundaries, asynchronous message brokers, and clean API gateways.</li>
  <li><strong>Technology Stack Rationalization:</strong> Rigorous evaluation and selection of frameworks, ensuring sustainable maintainability and security.</li>
</ul>""",
                    "is_published": True,
                },
                {
                    "slug": "developpement-applicatif-sur-mesure",
                    "title_fr": "Développement Applicatif Sur-Mesure",
                    "title_en": "Custom Software Development",
                    "division_slug": "software",
                    "icon": "code",
                    "order_num": 2,
                    "status": STATUS_ACTIVE,
                    "excerpt_fr": "Conception d'applications web et mobiles métier, APIs haute performance et micro-services.",
                    "excerpt_en": "Enterprise web and mobile applications, high-throughput APIs, and micro-services.",
                    "content_fr": """<h3>Conception et développement sur-mesure d'applications web, mobiles et progiciels métier</h3>
<p>Nous concevons des logiciels métier performants qui s'alignent avec précision sur vos processus organisationnels et industriels. De la première maquette ergonomique à la mise en production, nos cycles de développement agiles garantissent transparence et vélocité.</p>
<h4>Notre savoir-faire technique :</h4>
<ul>
  <li><strong>Applications Web &amp; Portails Métier :</strong> Interfaces réactives modernes (TypeScript, MelodiJS, Vue/React) et backends asynchrones Python / Node.js.</li>
  <li><strong>APIs RESTful &amp; Microservices :</strong> Interfaces de programmation sécurisées, documentées (OpenAPI/Swagger) et conçues pour supporter de fortes charges.</li>
  <li><strong>Applications Mobiles Multiplateformes :</strong> Solutions iOS et Android avec synchronisation hors-ligne pour les équipes sur le terrain.</li>
  <li><strong>Intégration de Systèmes Existants :</strong> Connecteurs d'échanges de données avec vos outils comptables, CRM et passerelles de paiement.</li>
</ul>""",
                    "content_en": """<h3>End-to-End Custom Development of Enterprise Web, Mobile, and Business Systems</h3>
<p>We build tailor-made enterprise software tailored to your specific organizational workflows and industrial challenges. From ergonomic UX wireframing to high-availability deployment, our agile engineering approach ensures velocity and quality.</p>
<h4>Our Technical Capabilities:</h4>
<ul>
  <li><strong>Enterprise Web Applications:</strong> Modern, responsive single-page applications (TypeScript, MelodiJS, Vue/React) and high-concurrency Python backends.</li>
  <li><strong>RESTful APIs &amp; Microservices:</strong> High-throughput, OpenAPI-documented web services engineered for secure inter-system communication.</li>
  <li><strong>Cross-Platform Mobile Apps:</strong> Fast iOS and Android applications with robust offline sync capabilities for distributed field workforces.</li>
  <li><strong>Legacy System Integrations:</strong> Custom middleware and ETL connectors integrating seamlessly with accounting packages, CRMs, and payment gateways.</li>
</ul>""",
                    "is_published": True,
                },
                {
                    "slug": "audit-securite-code",
                    "title_fr": "Audit de Sécurité & Revue de Code",
                    "title_en": "Security Audit & Code Review",
                    "division_slug": "software",
                    "icon": "shield",
                    "order_num": 3,
                    "status": STATUS_ACTIVE,
                    "excerpt_fr": "Évaluation de vulnérabilités, tests d'intrusion applicatifs et optimisation des performances SQL.",
                    "excerpt_en": "Vulnerability assessment, application penetration testing, and SQL database performance tuning.",
                    "content_fr": """<h3>Évaluation rigoureuse des vulnérabilités, tests d'intrusion applicatifs et durcissement</h3>
<p>À l'ère des cybermenaces persistantes, la sécurité logicielle ne peut être un simple ajout de dernière minute. Byt3Lab conduit des audits de sécurité exhaustifs et indépendants sur vos applications web, APIs et bases de données.</p>
<h4>Nos prestations d'audit :</h4>
<ul>
  <li><strong>Revue de code statique et dynamique :</strong> Analyse systématique des failles OWASP Top 10 (injections SQL, failles XSS, CSRF, contrôles d'accès défaillants).</li>
  <li><strong>Tests d'intrusion applicatifs (Pentest) :</strong> Simulation d'attaques réalistes pour éprouver la robustesse de vos mécanismes d'authentification et d'autorisation.</li>
  <li><strong>Contrôle des secrets et dépendances :</strong> Détection de clés d'API exposées, analyse des dépendances tierces vulnérables et conformité légale.</li>
  <li><strong>Plan de remédiation priorisé :</strong> Remise d'un rapport exécutif et technique contenant des correctifs de code actionnables immédiatement.</li>
</ul>""",
                    "content_en": """<h3>Rigorous Vulnerability Assessment, Application Penetration Testing, and Code Hardening</h3>
<p>In an era of sophisticated cybersecurity threats, software resilience must be baked into the development lifecycle. Byt3Lab conducts exhaustive, independent security assessments across enterprise web applications, APIs, and databases.</p>
<h4>Security Assessment Scope:</h4>
<ul>
  <li><strong>Static &amp; Dynamic Code Review:</strong> Comprehensive inspection of OWASP Top 10 vectors (SQL injection, XSS, broken access control, cryptographic failures).</li>
  <li><strong>Application Penetration Testing:</strong> Realistic black-box and white-box penetration simulations validating defenses against unauthorized data exfiltration.</li>
  <li><strong>Secrets &amp; Dependency Scanning:</strong> Automated detection of leaked secrets, API keys, and vulnerable third-party open-source libraries.</li>
  <li><strong>Actionable Remediation Roadmap:</strong> Delivery of executive briefings and detailed technical reports with prioritized, production-ready code fixes.</li>
</ul>""",
                    "is_published": True,
                },
                {
                    "slug": "infogerance-devops-cloud",
                    "title_fr": "Infogérance & DevOps Cloud",
                    "title_en": "Managed Cloud & DevOps",
                    "division_slug": "web-services",
                    "icon": "cloud",
                    "order_num": 4,
                    "status": STATUS_ACTIVE,
                    "excerpt_fr": "Déploiement automatisé, conteneurisation Docker, supervision 24/7 et plans de sauvegarde.",
                    "excerpt_en": "Automated deployments, Docker container orchestration, 24/7 telemetry, and disaster recovery.",
                    "content_fr": """<h3>Supervision 24/7, conteneurisation Docker, pipelines CI/CD et exploitation continue</h3>
<p>Garantissez la disponibilité absolue de vos applications critiques grâce à nos services d'infogérance et d'ingénierie DevOps. Nous transformons vos déploiements manuels à risque en pipelines automatisés reproductibles et résilients.</p>
<h4>Nos services DevOps &amp; Cloud :</h4>
<ul>
  <li><strong>Conteneurisation &amp; Orchestration :</strong> Standardisation des environnements applicatifs via Docker et gestion de clusters de serveurs.</li>
  <li><strong>Pipelines CI/CD Automatisés :</strong> Intégration continue, tests automatisés systématiques et déploiements sans interruption de service (zero-downtime).</li>
  <li><strong>Surveillance &amp; Alerting Proactif :</strong> Tableaux de bord de métriques en direct, journalisation centralisée et astreinte technique d'urgence.</li>
  <li><strong>Politique de Sauvegarde &amp; Restauration :</strong> Sauvegardes automatisées chiffrées avec exercices périodiques de restauration certifiés.</li>
</ul>""",
                    "content_en": """<h3>24/7 Proactive Monitoring, Container Orchestration, CI/CD Automation, and Cloud Ops</h3>
<p>Ensure maximum uptime and operational resilience for your mission-critical applications. Byt3Lab's DevOps and managed operations team converts manual, error-prone releases into reliable, automated deployment pipelines.</p>
<h4>DevOps &amp; Infrastructure Services:</h4>
<ul>
  <li><strong>Containerization &amp; Orchestration:</strong> Application standardization via Docker, reproducible runtime environments, and cluster clustering.</li>
  <li><strong>Automated CI/CD Pipelines:</strong> Continuous testing and zero-downtime deployment pipelines delivering rapid, verifiable software updates.</li>
  <li><strong>Proactive Telemetry &amp; Alerting:</strong> Real-time infrastructure observability dashboards, centralized log aggregation, and rapid incident response protocols.</li>
  <li><strong>Backup &amp; Disaster Recovery Verification:</strong> Encrypted offsite snapshot replication coupled with regular drill-tested data recovery protocols.</li>
</ul>""",
                    "is_published": True,
                },
            ]
            for s_data in services_data:
                existing = await ServiceRepository.get_by_slug(session, s_data["slug"])
                if existing:
                    await ServiceRepository.update(session, existing.id, s_data)
                else:
                    await ServiceRepository.create(session, s_data)

        # 4. PROJETS & RÉALISATIONS PORTFOLIO (3 études de cas bilingues avec HTML riche Quill)
        existing_projects = await ProjectRepository.get_all(session, published_only=False)
        if not existing_projects or force:
            projects_data = [
                {
                    "slug": "deploiement-erp-distribution-agroalimentaire",
                    "title_fr": "Déploiement ERP & POS pour Réseau de Distribution Agroalimentaire",
                    "title_en": "Enterprise ERP & POS Rollout for Food Distribution Network",
                    "domain_fr": "Commerce & Distribution",
                    "domain_en": "Retail & Distribution",
                    "image_url": "",
                    "order_num": 1,
                    "excerpt_fr": "Unification de 14 points de vente et 3 dépôts centraux avec synchronisation temps réel des inventaires et encaissements.",
                    "excerpt_en": "Unified operations across 14 retail branches and 3 centralized warehouses with real-time stock sync.",
                    "content_fr": """<h3>Transformation numérique globale d'un acteur majeur de la distribution agroalimentaire</h3>
<p>Le client, un réseau agroalimentaire exploitant 14 points de vente régionaux et 3 entrepôts logistiques centraux, souffrait d'une déconnexion chronique entre ses ventes en magasin et ses niveaux de stocks réels. Les ruptures de stock récurrentes et les écarts de caisse affectaient sévèrement sa rentabilité.</p>
<h4>Solution déployée :</h4>
<ul>
  <li>Déploiement complet de <strong>MELODI ERP</strong> avec son module de commerce et de stocks multi-dépôts.</li>
  <li>Installation de terminaux de caisse tactiles (POS) interconnectés, capables de fonctionner hors-ligne lors des coupures réseau locales.</li>
  <li>Synchronisation automatique des ventes, calcul des marges brutes en direct et déclenchement automatique des ordres de réapprovisionnement.</li>
  <li>Intégration du module comptable OHADA pour l'automatisation intégrale des journaux de vente et des clôtures mensuelles.</li>
</ul>
<p><strong>Résultats obtenus :</strong> Réduction de 92% des écarts d'inventaire, suppression des ruptures de produits phares et clôture comptable mensuelle réduite de 18 jours à seulement 2 jours.</p>""",
                    "content_en": """<h3>Enterprise ERP &amp; POS Digital Transformation for a Leading Food Distribution Chain</h3>
<p>Operating 14 retail branches and 3 regional distribution centers, the client struggled with severe data fragmentation between storefront registers and central inventory depots. Inaccurate stock counts and delayed financial reconciliation caused significant revenue leakages.</p>
<h4>Implementation Scope:</h4>
<ul>
  <li>Comprehensive rollout of <strong>MELODI ERP</strong>, configuring multi-warehouse inventory and procurement workflows.</li>
  <li>Deployment of networked POS touch-screen terminals equipped with offline-first synchronization for intermittent connectivity.</li>
  <li>Real-time automated margin calculations, automated stock depletion alerts, and algorithmic reorder schedules.</li>
  <li>Native SYSCOHADA general ledger integration automating daily sales journals and month-end financial closings.</li>
</ul>
<p><strong>Key Measurable Impact:</strong> 92% reduction in inventory discrepancies, elimination of stockouts on high-demand goods, and month-end financial closing accelerated from 18 days down to 48 hours.</p>""",
                    "is_published": True,
                },
                {
                    "slug": "cloud-prive-banque-microfinance",
                    "title_fr": "Infrastructure Cloud Privé Résiliente pour Institution Financière",
                    "title_en": "Resilient Private Cloud Backbone for Financial Institution",
                    "domain_fr": "Services Financiers & Banque",
                    "domain_en": "Banking & Microfinance",
                    "image_url": "",
                    "order_num": 2,
                    "excerpt_fr": "Mise en place d'un cluster haute disponibilité avec réplication synchrone et chiffrement des transactions.",
                    "excerpt_en": "High-availability server clustering with synchronous transactional replication and data encryption.",
                    "content_fr": """<h3>Architecture Cloud Privé Haute Disponibilité pour Établissement Financier Régional</h3>
<p>Dans un contexte d'exigences réglementaires strictes imposées par la Commission Bancaire, cette institution financière nécessitait une modernisation complète de son infrastructure serveur afin de garantir la continuité d'activité et la souveraineté des données bancaires de ses 65 000 sociétaires.</p>
<h4>Réalisations d'ingénierie :</h4>
<ul>
  <li>Conception et déploiement d'une architecture cloud privé sur mesure opérée par <strong>BWS (Byt3Lab Web Services)</strong>.</li>
  <li>Cluster de serveurs redondés avec basculement automatique sans perte (High Availability Failover) et réplication synchrone des bases PostgreSQL.</li>
  <li>Chiffrement de bout en bout des données au repos (AES-256) et en transit (TLS 1.3), avec isolation réseau stricte par sous-réseaux dédiés.</li>
  <li>Mise en œuvre d'un Plan de Reprise d'Activité (PRA) garantissant un RPO inférieur à 5 minutes et un RTO inférieur à 15 minutes.</li>
</ul>
<p><strong>Bénéfice majeur :</strong> Zéro interruption de service constatée au cours des 18 derniers mois et conformité totale auditée avec les normes de cybersécurité bancaire.</p>""",
                    "content_en": """<h3>High-Availability Private Cloud Infrastructure for Regulated Microfinance Institution</h3>
<p>Serving over 65,000 active members, this financial institution required complete infrastructure modernization to comply with rigorous central banking regulatory audits and ensure continuous operational resilience against power and network disturbances.</p>
<h4>Engineering Milestones:</h4>
<ul>
  <li>Design and deployment of a hardened, dedicated private cloud backbone engineered by <strong>BWS (Byt3Lab Web Services)</strong>.</li>
  <li>Clustered database failover architecture featuring synchronous PostgreSQL replication and zero-data-loss automated switchover.</li>
  <li>End-to-end data encryption at rest (AES-256) and in transit (TLS 1.3) within dedicated, micro-segmented network VLANs.</li>
  <li>Institutional Disaster Recovery Plan (DRP) execution achieving a Recovery Point Objective (RPO) &lt; 5 minutes and RTO &lt; 15 minutes.</li>
</ul>
<p><strong>Measurable Outcome:</strong> 99.98% verified uptime maintained across 18 consecutive months with zero regulatory non-compliance findings.</p>""",
                    "is_published": True,
                },
                {
                    "slug": "digitalisation-complexe-scolaire-polyvalent",
                    "title_fr": "Système de Gestion Numérique Intégré pour Complexe Scolaire",
                    "title_en": "Integrated School Management Cloud for Multi-Campus Academy",
                    "domain_fr": "Éducation & Formation",
                    "domain_en": "Education & Academics",
                    "image_url": "",
                    "order_num": 3,
                    "excerpt_fr": "Digitalisation complète des inscriptions, bulletins et paiements pour 2 800 élèves via la plateforme SUKU.",
                    "excerpt_en": "End-to-end automation of tuition collections, grading, and parent alerts for 2,800 enrolled students.",
                    "content_fr": """<h3>Digitalisation intégrale des inscriptions, scolarités et bulletins pour 2 800 apprenants</h3>
<p>Un groupe scolaire polyvalent comptant une école maternelle, un cycle primaire et un collège-lycée faisait face à d'importantes files d'attente lors des rentrées scolaires, des erreurs récurrentes dans les calculs de moyennes et des retards dans l'émission des bulletins trimestriels.</p>
<h4>Déploiement de SUKU :</h4>
<ul>
  <li>Mise en place de la plateforme <strong>SUKU</strong> pour l'ensemble des 2 800 dossiers élèves et 110 enseignants.</li>
  <li>Intégration du paiement des frais de scolarité via Mobile Money, supprimant la manipulation d'espèces au guichet et sécurisant les recettes.</li>
  <li>Génération automatisée des bulletins trimestriels en un clic dès la validation des notes par le conseil des professeurs.</li>
  <li>Ouverture de l'application mobile parents pour le suivi en direct de l'assiduité, des notes et des communications de l'établissement.</li>
</ul>
<p><strong>Impact opérationnel :</strong> Disparition totale des files d'attente d'inscription, sécurisation à 100% des encaissements et publication des bulletins le jour même des conseils de classe.</p>""",
                    "content_en": """<h3>End-to-End Digital Transformation for a 2,800-Student Multi-Campus Academy</h3>
<p>Encompassing kindergarten, primary, and secondary cycles, this educational institution experienced massive administrative bottlenecks during registration periods, recurring grade computation discrepancies, and delayed report card distributions.</p>
<h4>SUKU Implementation:</h4>
<ul>
  <li>Seamless deployment of the <strong>SUKU</strong> academic management platform managing 2,800 student records and 110 faculty members.</li>
  <li>Direct integration with Mobile Money payment channels, eliminating physical cash collection risks and streamlining reconciliation.</li>
  <li>Automated single-click generation of weighted official report cards immediately following academic board evaluations.</li>
  <li>Launch of the mobile parent portal enabling real-time attendance notifications, homework tracking, and school communications.</li>
</ul>
<p><strong>Tangible Impact:</strong> 100% elimination of registration queues, total financial accountability on tuition fees, and same-day electronic report card distribution.</p>""",
                    "is_published": True,
                },
            ]
            for p_data in projects_data:
                existing = await ProjectRepository.get_by_slug(session, p_data["slug"])
                if existing:
                    await ProjectRepository.update(session, existing.id, p_data)
                else:
                    await ProjectRepository.create(session, p_data)

        # 5. PARTENAIRES & ALLIANCES (5 partenaires représentatifs)
        existing_partners = await PartnerRepository.get_all(session, published_only=False)
        if not existing_partners or force:
            partners_data = [
                {
                    "name": "Supermicro Enterprise",
                    "category": "constructeurs",
                    "description_fr": "Constructeur mondial de serveurs haute performance et architectures pour centres de données.",
                    "description_en": "Global manufacturer of high-performance enterprise server and storage backbones.",
                    "logo_url": "",
                    "website_url": "https://www.supermicro.com",
                    "order_num": 1,
                    "is_published": True,
                },
                {
                    "name": "PostgreSQL Community",
                    "category": "technologie",
                    "description_fr": "Moteur de base de données relationnelle et spatiale open source le plus avancé au monde.",
                    "description_en": "The world's most advanced open-source relational database management system.",
                    "logo_url": "",
                    "website_url": "https://www.postgresql.org",
                    "order_num": 2,
                    "is_published": True,
                },
                {
                    "name": "Debian Enterprise Project",
                    "category": "infrastructure",
                    "description_fr": "Système d'exploitation universel reconnu pour sa stabilité et sa sécurité sur serveurs critiques.",
                    "description_en": "Universal Linux operating system renowned for enterprise server rock-solid reliability.",
                    "logo_url": "",
                    "website_url": "https://www.debian.org",
                    "order_num": 3,
                    "is_published": True,
                },
                {
                    "name": "Instituts Technologiques & Universités",
                    "category": "academique",
                    "description_fr": "Partenariat pour la formation, l'accueil de talents ingénieurs et la recherche appliquée.",
                    "description_en": "Academic cooperation for engineering talent development and applied research.",
                    "logo_url": "",
                    "website_url": "https://byt3lab.com",
                    "order_num": 4,
                    "is_published": True,
                },
                {
                    "name": "Opérateurs Télécoms & Connectivité",
                    "category": "commercial",
                    "description_fr": "Interconnexion fibre optique et passerelles SMS / Mobile Money pour nos solutions logicielles.",
                    "description_en": "Fiber optic providers and telco SMS/mobile money gateways powering our platform apps.",
                    "logo_url": "",
                    "website_url": "https://byt3lab.com",
                    "order_num": 5,
                    "is_published": True,
                },
            ]
            for pt_data in partners_data:
                # Find by name
                partner_match = next((p for p in (existing_partners or []) if p.name == pt_data["name"]), None)
                if partner_match:
                    await PartnerRepository.update(session, partner_match.id, pt_data)
                else:
                    await PartnerRepository.create(session, pt_data)

        # 6. ÉQUIPE & GOUVERNANCE (4 domaines d'ingénierie et de direction)
        existing_team = await TeamRepository.get_all(session, published_only=False)
        if not existing_team or force:
            team_data = [
                {
                    "slug": "direction-ingenierie-logicielle",
                    "name": "Pôle Ingénierie Logicielle & ERP",
                    "role_fr": "Conception des Progiciels & Systèmes Distribués",
                    "role_en": "Core Software Engineering & ERP Platforms",
                    "domain": "software",
                    "bio_fr": "Équipe pluridisciplinaire d'ingénieurs Python, TypeScript et spécialistes de bases de données assurant le développement des plateformes MELODI ERP et SUKU.",
                    "bio_en": "Multidisciplinary software engineering team building the core MELODI ERP and SUKU engines.",
                    "photo_url": "",
                    "order_num": 1,
                    "is_published": True,
                },
                {
                    "slug": "direction-systemes-cloud-reseaux",
                    "name": "Pôle Systèmes, Cloud & BWS",
                    "role_fr": "Architecture Infrastructure & DevOps",
                    "role_en": "Infrastructure Architecture & DevOps Operations",
                    "domain": "web-services",
                    "bio_fr": "Administrateurs systèmes Linux et experts réseau supervisant la disponibilité 24/7 de nos fermes de serveurs et nos déploiements clients.",
                    "bio_en": "Linux systems administrators ensuring 99.9% availability across all BWS clusters.",
                    "photo_url": "",
                    "order_num": 2,
                    "is_published": True,
                },
                {
                    "slug": "studio-creatif-ngrafix",
                    "name": "Studio Créatif & Expérience NGRAFIX",
                    "role_fr": "Direction Artistique & Design Numérique",
                    "role_en": "Creative Direction & Brand Experience",
                    "domain": "ngrafix",
                    "bio_fr": "Designers UI/UX et créateurs d'identités visuelles forgeant la personnalité graphique du groupe et de ses clients.",
                    "bio_en": "UI/UX designers crafting impactful brand identities and user-centric interfaces.",
                    "photo_url": "",
                    "order_num": 3,
                    "is_published": True,
                },
                {
                    "slug": "direction-recherche-innovation",
                    "name": "Pôle Recherche, IoT & Systèmes Cyber-Physiques",
                    "role_fr": "R&D & Technologies Industrielles",
                    "role_en": "Applied R&D & Cyber-Physical Systems",
                    "domain": "equipment",
                    "bio_fr": "Recherche appliquée sur les technologies industrielles, l'intelligence artificielle locale et la résilience énergétique.",
                    "bio_en": "Applied research exploring edge AI, industrial IoT, and resilient energy systems.",
                    "photo_url": "",
                    "order_num": 4,
                    "is_published": True,
                },
            ]
            for tm_data in team_data:
                existing = await TeamRepository.get_by_slug(session, tm_data["slug"])
                if existing:
                    await TeamRepository.update(session, existing.id, tm_data)
                else:
                    await TeamRepository.create(session, tm_data)

        # 7. CARRIÈRES & OFFRES D'EMPLOI (3 offres bilingues avec HTML riche Quill)
        existing_jobs = await JobRepository.get_all(session, published_only=False)
        if not existing_jobs or force:
            jobs_data = [
                {
                    "slug": "ingenieur-python-backend-senior",
                    "title_fr": "Ingénieur Logiciel Backend Python / AsyncIO (Senior)",
                    "title_en": "Senior Python Backend Engineer (AsyncIO)",
                    "division_slug": "software",
                    "location": "Douala, Cameroun (Hybride)",
                    "contract_type": "CDI",
                    "description_fr": """<h3>Rejoignez le cœur d'ingénierie logicielle MELODI ERP et bâtissez des architectures résilientes</h3>
<p>Au sein du pôle <em>Ingénierie Logicielle &amp; ERP</em> de Byt3Lab, vous jouerez un rôle déterminant dans l'évolution du moteur asynchrone de notre progiciel d'entreprise et dans la conception de modules métiers stratégiques.</p>
<h4>Missions &amp; Responsabilités :</h4>
<ul>
  <li>Concevoir et développer des modules métiers en Python 3.10+ avec le framework asynchrone Quart et asyncpg.</li>
  <li>Optimiser les requêtes SQL, concevoir des schémas de données relationnels robustes et garantir l'intégrité transactionnelle (ACID).</li>
  <li>Développer et maintenir des APIs RESTful performantes, sécurisées et documentées selon les normes OpenAPI.</li>
  <li>Participer activement aux revues de code, à la rédaction des tests unitaires/d'intégration et à l'amélioration continue des pipelines CI/CD.</li>
  <li>Collaborer avec les architectes systèmes pour assurer une haute scalabilité et une isolation modulaire stricte.</li>
</ul>
<h4>Ce que nous offrons :</h4>
<p>Un environnement technologique d'excellence sans bureaucratie, des projets à fort impact sur l'économie locale et continentale, une rémunération compétitive et des perspectives d'évolution au sein d'une équipe passionnée d'ingénierie logicielle.</p>""",
                    "description_en": """<h3>Join the Core MELODI ERP Engineering Team and Build Mission-Critical Async Systems</h3>
<p>As part of Byt3Lab's <em>Core Software Engineering &amp; ERP</em> division, you will play a pivotal role in evolving the high-concurrency asynchronous engine of our flagship platform and crafting mission-critical business modules.</p>
<h4>Key Responsibilities:</h4>
<ul>
  <li>Architect and implement business modules in modern Python (3.10+) utilizing Quart, AsyncIO, and asyncpg.</li>
  <li>Tune complex PostgreSQL queries, architect normalized schema models, and enforce strict transactional integrity (ACID).</li>
  <li>Design and document secure, high-throughput RESTful APIs compliant with OpenAPI standards.</li>
  <li>Champion engineering excellence through thorough code reviews, comprehensive automated testing, and CI/CD maintenance.</li>
  <li>Collaborate with infrastructure architects to guarantee strict modular isolation and zero-downtime scalability.</li>
</ul>
<h4>What We Offer:</h4>
<p>A fast-paced, high-standard engineering environment, meaningful challenges delivering real business impact across Africa, competitive compensation, and clear leadership growth pathways.</p>""",
                    "requirements": [
                        "Maîtrise approfondie de Python 3.10+, AsyncIO et des architectures modulaires",
                        "Excellente maîtrise de PostgreSQL et modélisation relationnelle",
                        "Expérience en tests unitaires et intégration continue CI/CD",
                        "Sens aigu de la rigueur de code et de la documentation",
                    ],
                    "is_published": True,
                },
                {
                    "slug": "ingenieur-systemes-devops-cloud",
                    "title_fr": "Ingénieur Systèmes Linux & DevOps Cloud",
                    "title_en": "Linux Systems & Cloud DevOps Engineer",
                    "division_slug": "web-services",
                    "location": "Douala / Yaoundé (Sur site / Hybride)",
                    "contract_type": "CDI",
                    "description_fr": """<h3>Supervisez et automatisez nos fermes de serveurs BWS et nos infrastructures critiques</h3>
<p>En tant qu'Ingénieur Systèmes Linux &amp; DevOps Cloud au sein du pôle <em>Systèmes, Cloud &amp; BWS</em>, vous aurez la responsabilité de garantir la haute disponibilité, la sécurité et la résilience de l'ensemble des environnements de production de Byt3Lab et de ses clients sous contrat d'infogérance.</p>
<h4>Missions principales :</h4>
<ul>
  <li>Administrer et durcir des fermes de serveurs Linux (Debian, Rocky Linux) dédiées à l'hébergement d'applications d'entreprise.</li>
  <li>Concevoir et orchestrer les conteneurs applicatifs Docker et maintenir les hyperviseurs de virtualisation (KVM / Proxmox).</li>
  <li>Automatiser les déploiements logiciels via des scripts et des pipelines d'intégration/déploiement continus (CI/CD).</li>
  <li>Mettre en place et superviser les sondes de monitoring temps réel (Prometheus, Grafana, alertes d'astreinte 24/7).</li>
  <li>Gérer les politiques de sauvegardes automatisées chiffrées et éprouver périodiquement les plans de reprise d'activité (PRA).</li>
</ul>
<h4>Profil recherché :</h4>
<p>Passionné par les systèmes d'exploitation libres, vous possédez une rigueur exemplaire, le sens du service critique et une capacité démontrée à intervenir sereinement lors d'incidents techniques complexes.</p>""",
                    "description_en": """<h3>Scale and Secure Mission-Critical Server Clusters across Byt3Lab Web Services</h3>
<p>As a Linux Systems &amp; Cloud DevOps Engineer in our <em>Infrastructure &amp; BWS</em> division, you will be responsible for the continuous uptime, automated provisioning, and cybersecurity posture of all production server fleets powering Byt3Lab and our enterprise clients.</p>
<h4>Core Responsibilities:</h4>
<ul>
  <li>Manage, tune, and harden enterprise Linux distributions (Debian, Rocky Linux) hosting high-throughput transactional systems.</li>
  <li>Orchestrate production container workloads via Docker and maintain bare-metal virtualization clusters (KVM / Proxmox).</li>
  <li>Automate deployment routines and infrastructure-as-code through robust CI/CD pipelines.</li>
  <li>Deploy and monitor real-time telemetry systems (Prometheus, Grafana, structured log aggregation, and 24/7 on-call alerting).</li>
  <li>Enforce encrypted offsite backup regimes and regularly validate institutional Disaster Recovery Plans (DRP).</li>
</ul>
<h4>Who You Are:</h4>
<p>An autonomous, disciplined systems administrator who values reproducible infrastructure, proactive monitoring, and methodical incident troubleshooting under pressure.</p>""",
                    "requirements": [
                        "Excellente connaissance de l'administration Linux Debian / Rocky",
                        "Maîtrise de la conteneurisation Docker et de la virtualisation KVM / Proxmox",
                        "Compétences réseau avancées (routage, pare-feu, VPN WireGuard)",
                    ],
                    "is_published": True,
                },
                {
                    "slug": "designer-ui-ux-ngrafix",
                    "title_fr": "Designer UI/UX & Systèmes Visuels (NGRAFIX)",
                    "title_en": "UI/UX Designer & Design Systems Lead (NGRAFIX)",
                    "division_slug": "software",
                    "location": "Douala (Présentiel)",
                    "contract_type": "CDI",
                    "description_fr": """<h3>Façonnez l'identité visuelle et l'expérience ergonomique des produits Byt3Lab</h3>
<p>Rejoignez le studio créatif <em>NGRAFIX</em> pour diriger la conception des interfaces utilisateurs de notre suite logicielle (MELODI ERP, SUKU) et créer des chartes graphiques percutantes pour nos marques et nos partenaires stratégiques.</p>
<h4>Vos responsabilités :</h4>
<ul>
  <li>Concevoir les parcours utilisateurs (UX) et les interfaces ergonomiques (UI) pour des applications web d'entreprise et mobiles.</li>
  <li>Structurer et enrichir le <strong>MELODI Design System</strong> (composants réutilisables, tokens de couleurs, typographie, modes sombre/clair).</li>
  <li>Créer des prototypes interactifs haute fidélité sur Figma pour validation avant implémentation par les développeurs frontend.</li>
  <li>Collaborer étroitement avec les équipes de développement frontend (TypeScript, SCSS) pour veiller au respect méticuleux des spécifications visuelles.</li>
  <li>Participer à la création de supports de communication visuelle corporate, infographies et identités visuelles de marque.</li>
</ul>""",
                    "description_en": """<h3>Shape the Ergonomic User Experience and Visual Identity of Byt3Lab Platforms</h3>
<p>Join our creative studio <em>NGRAFIX</em> to direct user interface architecture across our enterprise product lines (MELODI ERP, SUKU) and craft compelling brand identities for our strategic products and corporate partners.</p>
<h4>Your Responsibilities:</h4>
<ul>
  <li>Design intuitive user journeys (UX) and crisp interfaces (UI) for data-dense enterprise web dashboards and mobile tools.</li>
  <li>Standardize and expand the <strong>MELODI Design System</strong> (reusable design tokens, component libraries, typography, dark/light modes).</li>
  <li>Produce interactive, pixel-perfect Figma prototypes for stakeholder alignment prior to frontend engineering sprints.</li>
  <li>Partner closely with frontend software engineers (TypeScript, SCSS) to ensure high-fidelity implementation of visual designs.</li>
  <li>Craft impactful corporate branding assets, data visualizations, and marketing illustrations.</li>
</ul>""",
                    "requirements": [
                        "Portfolio solide en design d'interfaces web et mobiles",
                        "Maîtrise de Figma et des tokens de design systems",
                        "Culture typographique et sens du détail visuel",
                    ],
                    "is_published": True,
                },
            ]
            for j_data in jobs_data:
                existing = await JobRepository.get_by_slug(session, j_data["slug"])
                if existing:
                    await JobRepository.update(session, existing.id, j_data)
                else:
                    await JobRepository.create(session, j_data)

        # 8. CATÉGORIES BLOG PAR DÉFAUT
        existing_blog_cats = await BlogCategoryRepository.get_all(session, active_only=False)
        if not existing_blog_cats or force:
            default_cats = [
                {
                    "slug": "ingenierie-erp",
                    "name_fr": "Ingénierie & ERP",
                    "name_en": "Engineering & ERP",
                    "description_fr": "Architecture modulaire, MELODI ERP, ASSO (gestion commerciale), SUKU (gestion scolaire) et bonnes pratiques Python/PostgreSQL.",
                    "description_en": "Modular architecture, MELODI ERP, ASSO (commercial management), SUKU (school management) and Python/PostgreSQL best practices.",
                    "color": "#0284c7",
                    "order_num": 1,
                    "is_active": True,
                },
                {
                    "slug": "ia-data",
                    "name_fr": "IA & Data Science",
                    "name_en": "AI & Data Science",
                    "description_fr": "Intelligence artificielle appliquée, automatisation et analytique décisionnelle.",
                    "description_en": "Applied artificial intelligence, automation and decision analytics.",
                    "color": "#7c3aed",
                    "order_num": 2,
                    "is_active": True,
                },
                {
                    "slug": "cloud-infrastructure",
                    "name_fr": "Cloud & Infrastructure",
                    "name_en": "Cloud & Infrastructure",
                    "description_fr": "Hébergement haute disponibilité, BWS, réseaux d'entreprise et souveraineté numérique.",
                    "description_en": "High-availability hosting, BWS, enterprise networking and digital sovereignty.",
                    "color": "#059669",
                    "order_num": 3,
                    "is_active": True,
                },
                {
                    "slug": "actualites-groupe",
                    "name_fr": "Actualités Groupe",
                    "name_en": "Group News",
                    "description_fr": "Annonces officielles, partenariats stratégiques et événements Byt3Lab.",
                    "description_en": "Official announcements, strategic partnerships and Byt3Lab events.",
                    "color": "#ea580c",
                    "order_num": 4,
                    "is_active": True,
                },
            ]
            for c_data in default_cats:
                existing_cat = await BlogCategoryRepository.get_by_slug(session, c_data["slug"])
                if not existing_cat:
                    await BlogCategoryRepository.create(session, c_data)

        # 8b. ARTICLES DE BLOG & RECHERCHE (2 publications bilingues avec HTML riche Quill)
        existing_posts = await PostRepository.get_all(session, published_only=False)
        if not existing_posts or force:
            posts_data = [
                {
                    "slug": "pourquoi-developper-un-erp-modulaire-proprietaire-en-afrique",
                    "title_fr": "Pourquoi concevoir un ERP modulaire propriétaire en Afrique ?",
                    "title_en": "Why build a modular enterprise ERP in Africa?",
                    "summary_fr": "Analyse des limites des solutions monolithiques d'importation et plaidoyer pour une ingénierie logicielle locale adaptée aux réalités opérationnelles africaines.",
                    "summary_en": "Analyzing the shortcomings of generic enterprise software imports and the case for local high-grade software engineering.",
                    "content_fr": """<h3>Pourquoi concevoir un ERP modulaire propriétaire en Afrique ?</h3>
<p>Dans un paysage d'affaires en pleine mutation sur le continent africain, la grande majorité des entreprises de taille intermédiaire et des PME restent prisonnières d'un dilemme technologique coûteux : adopter des progiciels internationaux surdimensionnés et hors de prix, ou composer avec un bricolage précaire de feuilles de calcul dispersées.</p>
<h4>1. Le piège des progiciels d'importation monolithiques</h4>
<p>Les géants traditionnels de l'ERP ont été conçus il y a des décennies pour des multinationales occidentales. Leurs modèles de licence en devises étrangères pèsent lourdement sur les trésoreries locales, tandis que leurs processus rigides ignorent les réalités du terrain :</p>
<ul>
  <li><strong>Instabilité de la connectivité réseau :</strong> Les solutions 100% cloud traditionnelles s'arrêtent dès que la connexion Internet locale vacille.</li>
  <li><strong>Paiements mobiles :</strong> L'absence d'intégration native avec le Mobile Money (Orange Money, MTN MoMo) complique la collecte des fonds au quotidien.</li>
  <li><strong>Normes comptables spécifiques :</strong> L'adaptation au référentiel SYSCOHADA révisé nécessite des personnalisations onéreuses et souvent défaillantes.</li>
</ul>
<h4>2. Le choix de la souveraineté et de l'ingénierie modulaire</h4>
<p>Byt3Lab a fait le choix stratégique de bâtir <strong>MELODI ERP</strong> à partir de fondations vierges en s'appuyant sur les technologies asynchrones modernes de Python et PostgreSQL. Notre vision repose sur trois piliers intransigeants :</p>
<ol>
  <li><strong>Modularité hot-pluggable :</strong> Une entreprise ne paye et n'active que les fonctionnalités dont elle a besoin.</li>
  <li><strong>Résilience opérationnelle :</strong> Des caisses et points de vente capables d'opérer en mode déconnecté avec resynchronisation transparente.</li>
  <li><strong>Support technologique direct :</strong> Un éditeur local accessible, capable d'intervenir en quelques heures plutôt qu'à travers des centres d'appels délocalisés.</li>
</ol>
<p>Investir dans une ingénierie logicielle locale d'excellence, c'est choisir l'autonomie stratégique et la maîtrise pérenne de ses données d'affaires.</p>""",
                    "content_en": """<h3>Why Build a Sovereign, Modular Enterprise ERP in Africa?</h3>
<p>Across emerging markets in Africa, growing enterprises face a persistent technological dilemma: invest fortunes into monolithic legacy software suites built for foreign multinationals, or endure the operational chaos of disconnected, fragile spreadsheets.</p>
<h4>1. The Costly Reality of Monolithic Imports</h4>
<p>Legacy ERP platforms were engineered decades ago around assumptions that rarely hold true in fast-evolving local environments. Their expensive foreign-currency licensing structures bleed operating cash, while their architectures struggle with real-world infrastructure constraints:</p>
<ul>
  <li><strong>Intermittent Internet Connectivity:</strong> Cloud-only monoliths halt storefront sales the moment regional internet backbones fluctuate.</li>
  <li><strong>Mobile Money Ecosystems:</strong> Lack of deep native integration with regional payment rails (Orange Money, MTN MoMo) forces clumsy manual bookkeeping.</li>
  <li><strong>OHADA Accounting Standards:</strong> Retrofitting revised SYSCOHADA financial accounting onto foreign platforms triggers expensive, fragile custom consulting.</li>
</ul>
<h4>2. The Imperative for Sovereign, Modular Engineering</h4>
<p>Byt3Lab engineered <strong>MELODI ERP</strong> from first principles using high-throughput asynchronous Python and PostgreSQL. Our technological approach delivers three structural advantages:</p>
<ol>
  <li><strong>True Hot-Pluggable Modularity:</strong> Businesses activate and pay solely for the operational components they actually deploy.</li>
  <li><strong>Offline-First Resilience:</strong> Storefront POS terminals operate uninterrupted during network brownouts and auto-synchronize upon reconnect.</li>
  <li><strong>Direct Engineering Accountability:</strong> Immediate access to the core software developers rather than distant, outsourced support desks.</li>
</ol>
<p>Building high-performance software locally is not merely an engineering achievement—it is a critical requirement for long-term digital sovereignty.</p>""",
                    "cover_image": "",
                    "author_name": "Équipe Recherche Byt3Lab",
                    "published_at": datetime.now(timezone.utc),
                    "is_published": True,
                },
                {
                    "slug": "resilience-cloud-et-souverainete-numerique",
                    "title_fr": "Résilience des infrastructures cloud et souveraineté numérique locale",
                    "title_en": "Cloud Resilience & Digital Sovereignty in Emerging Markets",
                    "summary_fr": "Comment l'infogérance proactive BWS garantit la continuité de service des organisations critiques face aux aléas d'infrastructure.",
                    "summary_en": "How proactive systems engineering guarantees data availability and operational uptime.",
                    "content_fr": """<h3>Résilience des infrastructures cloud et souveraineté numérique locale</h3>
<p>À mesure que les opérations d'entreprise se numérisent, la question de l'emplacement et de la résilience des serveurs hébergeant les données stratégiques devient une préoccupation de premier ordre pour les dirigeants et directeurs des systèmes d'information.</p>
<h4>Les risques de la dépendance externe non maîtrisée</h4>
<p>Héberger la totalité de ses applications critiques sur des centres de données distants engendre des latences inutiles lors des transactions quotidiennes et expose les organisations à des aléas géopolitiques et juridiques majeurs (extraterritorialité des données, modifications unilatérales de tarifs en devises fortes).</p>
<h4>L'approche BWS : Proximité, Sécurité et Disponibilité garantie</h4>
<p>À travers <strong>Byt3Lab Web Services (BWS)</strong>, nous développons une offre d'hébergement managé et de cloud privé conçue pour apporter :</p>
<ul>
  <li><strong>Temps de réponse minimaux :</strong> Une proximité réseau réduisant drastiquement les temps de chargement pour les utilisateurs finaux.</li>
  <li><strong>Plan de reprise d'activité éprouvé :</strong> Réplication des données entre des centres de données géographiquement redondés avec basculement automatique.</li>
  <li><strong>Protection des données sensibles :</strong> Chiffrement systématique au repos et en transit garantissant la confidentialité absolue de votre patrimoine informationnel.</li>
</ul>
<p>La souveraineté numérique ne se décrète pas : elle se construit brique par brique à travers des infrastructures maîtrisées et des compétences techniques locales d'exception.</p>""",
                    "content_en": """<h3>Cloud Infrastructure Resilience and Digital Sovereignty in Emerging Markets</h3>
<p>As mission-critical business workflows transition to the cloud, the geographical location, regulatory jurisdiction, and resilience of underlying servers become paramount concerns for executive leadership and IT directors.</p>
<h4>The Hidden Costs of Unmitigated Remote Dependence</h4>
<p>Relying exclusively on overseas cloud hyper-scalers introduces noticeable network latency during high-frequency transactional operations, alongside acute foreign exchange exposure and cross-border regulatory compliance risks.</p>
<h4>The BWS Engineering Paradigm: Proximity, Hardened Security, and SLA-Backed Uptime</h4>
<p>Through <strong>Byt3Lab Web Services (BWS)</strong>, Byt3Lab delivers managed hosting and private cloud infrastructure engineered specifically for enterprise requirements:</p>
<ul>
  <li><strong>Low-Latency Regional Performance:</strong> Network proximity delivering sub-second response times for regional corporate users.</li>
  <li><strong>Tested Disaster Recovery Pipelines:</strong> Automated snapshot replication across diverse geographical zones with proven zero-loss failover procedures.</li>
  <li><strong>Complete Data Sovereignty:</strong> Enterprise-grade AES-256 encryption at rest and TLS 1.3 in transit, ensuring proprietary business records remain protected.</li>
</ul>
<p>True digital sovereignty is achieved through local engineering competence and infrastructure that you can trust and verify.</p>""",
                    "cover_image": "",
                    "author_name": "Pôle Systèmes BWS",
                    "published_at": datetime.now(timezone.utc),
                    "is_published": True,
                },
            ]
            for p_post in posts_data:
                existing = await PostRepository.get_by_slug(session, p_post["slug"])
                if existing:
                    await PostRepository.update(session, existing.id, p_post)
                else:
                    await PostRepository.create(session, p_post)

        # 9. MESSAGES DE DÉMONSTRATION DANS L'INBOX (2 messages pour tester les filtres)
        existing_msgs = await MessageRepository.get_all(session)
        if not existing_msgs:
            messages_data = [
                {
                    "form_type": "contact",
                    "sender_name": "Alexandre Mbarga",
                    "organization": "Groupe Agro-Industriel Camerounais",
                    "email": "a.mbarga@agrocam.cm",
                    "phone": "+237 699 12 34 56",
                    "subject": "Demande de démonstration MELODI ERP Multi-Dépôts",
                    "message": "Bonjour l'équipe Byt3Lab,\n\nNous gérons actuellement 8 entrepôts régionaux au Cameroun et souhaitons remplacer nos outils actuels par une solution ERP unifiée capable de gérer nos inventaires et nos points de vente en direct.\n\nPouvons-nous planifier un échange technique cette semaine ?\n\nCordialement,\nAlexandre Mbarga",
                    "status": "new",
                    "ip_address": "127.0.0.1",
                },
                {
                    "form_type": "partner",
                    "sender_name": "Dr. Jean-Paul Talla",
                    "organization": "Institut Supérieur de Technologie",
                    "email": "j.talla@ist-universite.cm",
                    "phone": "+237 677 88 99 00",
                    "partner_type": "Partenariat Académique & Recrutement",
                    "website": "https://ist-universite.cm",
                    "message": "Madame, Monsieur,\n\nNous formons chaque année plus de 200 ingénieurs en génie logiciel et réseaux. Nous souhaiterions établir une convention de partenariat avec Byt3Lab pour l'accueil de stagiaires et l'animation d'ateliers techniques.\n\nDans l'attente de votre retour,\nDr. Talla",
                    "status": "in_progress",
                    "ip_address": "127.0.0.1",
                },
            ]
            for m_data in messages_data:
                await MessageRepository.create(session, m_data)
