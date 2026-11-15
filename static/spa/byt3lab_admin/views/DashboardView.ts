// @ts-nocheck
export const DashboardView = {
  delimiters: ['[[', ']]'],
  computed: {
    dashboard() {
      return this.$store.state.dashboard;
    },
    counts() {
      return this.dashboard ? this.dashboard.counts : {};
    },
    recentMessages() {
      return this.dashboard ? this.dashboard.recent_messages : [];
    },
    loading() {
      return this.$store.state.loading;
    },
    error() {
      return this.$store.state.error;
    },
  },
  methods: {
    formatDate(d) {
      if (!d) return '—';
      if (typeof d === 'string' && d.includes('/')) return d;
      try {
        const dt = new Date(d);
        return isNaN(dt.getTime()) ? d : dt.toLocaleString();
      } catch (e) {
        return d;
      }
    },
    goTo(path) {
      this.$router.push(path);
    },
  },
  mounted() {
    this.$store.dispatch('fetchDashboard');
  },
  hooks: {
    mounted() {
      this.$store.dispatch('fetchDashboard');
    },
  },
  template: { el: '#tpl-byt3lab-dashboard' },
};
