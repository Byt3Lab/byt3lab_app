import{createApp as r}from"/static/base/melodiJS/index.js";import{router as n}from"./router.js";import{store as e}from"./store.js";function a(){const t=document.getElementById("byt3lab-admin-app");if(!t)return;const s=r({delimiters:["[[","]]"],computed:{currentPath(){return this.$route&&this.$route.path||"/"},unreadCount(){return this.$store.state.dashboard&&this.$store.state.dashboard.counts&&this.$store.state.dashboard.counts.unread_messages||0}},template:`
      <div class="byt3lab-admin-spa-root">
        <div class="ds-card p-2 mb-4 shadow-sm" id="byt3lab-spa-nav" style="display: flex; flex-direction: row; flex-wrap: wrap; align-items: center; gap: 0.5rem;">
          <a href="#/" class="ds-btn ds-btn-sm" :class="currentPath === '/' ? 'ds-btn-primary' : 'ds-btn-secondary'">\u{1F4CA} Vue d'ensemble</a>
          <a href="#/inbox" class="ds-btn ds-btn-sm" :class="currentPath === '/inbox' ? 'ds-btn-primary' : 'ds-btn-secondary'">
            \u{1F4E5} R\xE9ception
            <span v-if="unreadCount > 0" class="badge bg-danger ms-1">[[ unreadCount ]]</span>
          </a>
          <a href="#/divisions" class="ds-btn ds-btn-sm" :class="currentPath === '/divisions' ? 'ds-btn-primary' : 'ds-btn-secondary'">\u{1F3DB}\uFE0F Divisions</a>
          <a href="#/solutions" class="ds-btn ds-btn-sm" :class="currentPath === '/solutions' ? 'ds-btn-primary' : 'ds-btn-secondary'">\u{1F680} Solutions</a>
          <a href="#/services" class="ds-btn ds-btn-sm" :class="currentPath === '/services' ? 'ds-btn-primary' : 'ds-btn-secondary'">\u{1F6E0}\uFE0F Services</a>
          <a href="#/projects" class="ds-btn ds-btn-sm" :class="currentPath === '/projects' ? 'ds-btn-primary' : 'ds-btn-secondary'">\u{1F4BC} Portfolio</a>
          <a href="#/partners" class="ds-btn ds-btn-sm" :class="currentPath === '/partners' ? 'ds-btn-primary' : 'ds-btn-secondary'">\u{1F91D} Partenaires</a>
          <a href="#/team" class="ds-btn ds-btn-sm" :class="currentPath === '/team' ? 'ds-btn-primary' : 'ds-btn-secondary'">\u{1F465} \xC9quipe</a>
          <a href="#/jobs" class="ds-btn ds-btn-sm" :class="currentPath === '/jobs' ? 'ds-btn-primary' : 'ds-btn-secondary'">\u{1F3AF} Carri\xE8res</a>
          <a href="#/posts" class="ds-btn ds-btn-sm" :class="currentPath === '/posts' ? 'ds-btn-primary' : 'ds-btn-secondary'">\u{1F4F0} Blog</a>
          <a href="#/settings" class="ds-btn ds-btn-sm" :class="currentPath === '/settings' ? 'ds-btn-primary' : 'ds-btn-secondary'">\u2699\uFE0F R\xE9glages</a>
        </div>
        <router-view></router-view>
      </div>
    `});s.use(n),s.use(e),s.mount(t)}document.readyState==="loading"?document.addEventListener("DOMContentLoaded",a):setTimeout(a,0);
//# sourceMappingURL=app.js.map
