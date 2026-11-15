// @ts-nocheck
export const InboxView = {
  delimiters: ['[[', ']]'],
  data() {
    return {
      activeFilter: '',
      selectedMessage: null,
    };
  },
  computed: {
    messages() {
      return this.$store.state.messages || [];
    },
    counts() {
      return this.$store.state.messagesCounts || {};
    },
    loading() {
      return this.$store.state.loading;
    },
    error() {
      return this.$store.state.error;
    },
    successMessage() {
      return this.$store.state.successMessage;
    },
  },
  methods: {
    setFilter(status) {
      this.activeFilter = status;
      this.selectedMessage = null;
      this.$store.dispatch('fetchMessages', status);
    },
    viewMessage(msg) {
      this.selectedMessage = msg;
    },
    closeDetail() {
      this.selectedMessage = null;
    },
    async updateStatus(id, newStatus) {
      const ok = await this.$store.dispatch('updateMessageStatus', { id, status: newStatus });
      if (ok && this.selectedMessage && this.selectedMessage.id === id) {
        this.selectedMessage.status = newStatus;
      }
    },
    async deleteMsg(id) {
      if (confirm('Voulez-vous vraiment supprimer ce message ?')) {
        const ok = await this.$store.dispatch('deleteMessage', id);
        if (ok && this.selectedMessage && this.selectedMessage.id === id) {
          this.selectedMessage = null;
        }
      }
    },
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
  },
  mounted() {
    this.$store.dispatch('fetchMessages');
  },
  hooks: {
    mounted() {
      this.$store.dispatch('fetchMessages');
    },
  },
  template: { el: '#tpl-byt3lab-inbox' },
};
