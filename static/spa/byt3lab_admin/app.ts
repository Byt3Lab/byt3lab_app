// @ts-nocheck
import { createApp } from '/static/base/melodiJS/index.js';
import { router } from './router.js';
import { store } from './store.js';

function startByt3labAdminApp() {
  const mountEl = document.getElementById('byt3lab-admin-app');
  if (!mountEl) return;

  const app = createApp({
    delimiters: ['[[', ']]'],
    data() {
      return {
        activePath: (window.location.hash.replace('#', '') || '/').split('?')[0],
      };
    },
    computed: {
      currentPath() {
        return this.activePath || (this.$route && this.$route.path) || '/';
      },
      unreadCount() {
        return (this.$store.state.dashboard && this.$store.state.dashboard.counts && this.$store.state.dashboard.counts.unread_messages) || 0;
      },
    },
    methods: {
      syncActivePath() {
        const raw = window.location.hash.replace('#', '') || '/';
        this.activePath = raw.split('?')[0] || '/';
      },
    },
    mounted() {
      this.syncActivePath();
      window.addEventListener('hashchange', this.syncActivePath);
    },
    hooks: {
      mounted() {
        this.syncActivePath();
        window.addEventListener('hashchange', this.syncActivePath);
      },
    },
    template: `
      <div class="byt3lab-admin-spa-root">
        <div class="ds-card p-2 mb-4 shadow-sm byt3lab-spa-nav" id="byt3lab-spa-nav">
          <a href="#/" class="ds-btn ds-btn-sm" :class="currentPath === '/' ? 'ds-btn-primary' : 'ds-btn-secondary'">📊 Vue d'ensemble</a>
          <a href="#/inbox" class="ds-btn ds-btn-sm" :class="currentPath === '/inbox' ? 'ds-btn-primary' : 'ds-btn-secondary'">
            📥 Réception
            <span v-if="unreadCount > 0" class="badge bg-danger ms-1">[[ unreadCount ]]</span>
          </a>
          <a href="#/poles" class="ds-btn ds-btn-sm" :class="(currentPath === '/poles' || currentPath === '/divisions') ? 'ds-btn-primary' : 'ds-btn-secondary'">🧭 Nos 4 Pôles</a>
          <a href="#/solutions" class="ds-btn ds-btn-sm" :class="currentPath === '/solutions' ? 'ds-btn-primary' : 'ds-btn-secondary'">🚀 Solutions</a>
          <a href="#/services" class="ds-btn ds-btn-sm" :class="currentPath === '/services' ? 'ds-btn-primary' : 'ds-btn-secondary'">🛠️ Services</a>
          <a href="#/projects" class="ds-btn ds-btn-sm" :class="currentPath === '/projects' ? 'ds-btn-primary' : 'ds-btn-secondary'">💼 Portfolio</a>
          <a href="#/ngrafix" class="ds-btn ds-btn-sm" :class="currentPath === '/ngrafix' ? 'ds-btn-primary' : 'ds-btn-secondary'">🎨 ngrafix</a>
          <a href="#/partners" class="ds-btn ds-btn-sm" :class="currentPath === '/partners' ? 'ds-btn-primary' : 'ds-btn-secondary'">🤝 Partenaires</a>
          <a href="#/team" class="ds-btn ds-btn-sm" :class="currentPath === '/team' ? 'ds-btn-primary' : 'ds-btn-secondary'">👥 Équipe</a>
          <a href="#/jobs" class="ds-btn ds-btn-sm" :class="currentPath === '/jobs' ? 'ds-btn-primary' : 'ds-btn-secondary'">🎯 Carrières</a>
          <a href="#/posts" class="ds-btn ds-btn-sm" :class="currentPath === '/posts' ? 'ds-btn-primary' : 'ds-btn-secondary'">📰 Blog</a>
          <a href="#/settings" class="ds-btn ds-btn-sm" :class="currentPath === '/settings' ? 'ds-btn-primary' : 'ds-btn-secondary'">⚙️ Réglages</a>
        </div>
        <router-view></router-view>
      </div>
    `,
  });

  app.use(router);
  app.use(store);
  app.mount(mountEl);
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', startByt3labAdminApp);
} else {
  setTimeout(startByt3labAdminApp, 0);
}
