// @ts-nocheck
import { MelodiRouter } from '/static/base/melodiJS/index.js';
import { DashboardView } from './views/DashboardView.js';
import { InboxView } from './views/InboxView.js';
import { SettingsView } from './views/SettingsView.js';
import { createContentCrudView } from './views/ContentCrudView.js';

export const router = new MelodiRouter({
  mode: 'hash',
  routes: [
    {
      path: '/',
      name: 'byt3lab-dashboard',
      component: DashboardView,
    },
    {
      path: '/inbox',
      name: 'byt3lab-inbox',
      component: InboxView,
    },
    {
      path: '/settings',
      name: 'byt3lab-settings',
      component: SettingsView,
    },
    {
      path: '/divisions',
      name: 'byt3lab-divisions',
      component: createContentCrudView('divisions', 'Divisions Technologiques'),
    },
    {
      path: '/solutions',
      name: 'byt3lab-solutions',
      component: createContentCrudView('solutions', 'Produits & Solutions'),
    },
    {
      path: '/services',
      name: 'byt3lab-services',
      component: createContentCrudView('services', "Services d'Ingénierie"),
    },
    {
      path: '/projects',
      name: 'byt3lab-projects',
      component: createContentCrudView('projects', 'Projets & Réalisations (Portfolio)'),
    },
    {
      path: '/partners',
      name: 'byt3lab-partners',
      component: createContentCrudView('partners', 'Partenaires & Alliances'),
    },
    {
      path: '/team',
      name: 'byt3lab-team',
      component: createContentCrudView('team', "Membres & Pôles de l'Équipe"),
    },
    {
      path: '/jobs',
      name: 'byt3lab-jobs',
      component: createContentCrudView('jobs', "Offres d'Emploi & Carrières"),
    },
    {
      path: '/posts',
      name: 'byt3lab-posts',
      component: createContentCrudView('posts', 'Articles de Blog & Publications'),
    },
    {
      path: '/blog-categories',
      name: 'byt3lab-blog-categories',
      component: createContentCrudView('blog-categories', 'Catégories du Blog'),
    },
    {
      path: '/ngrafix',
      name: 'byt3lab-ngrafix',
      component: createContentCrudView('ngrafix', 'Studio Créatif NGRAFIX'),
    },
    {
      path: '*',
      name: 'byt3lab-fallback',
      component: DashboardView,
    },
  ],
});
