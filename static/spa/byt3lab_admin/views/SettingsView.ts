// @ts-nocheck
const SETTING_KEYS = [
  'contact.email',
  'contact.email_support',
  'contact.phone',
  'contact.whatsapp',
  'contact.location',
  'social.linkedin',
  'social.facebook',
  'social.youtube',
  'social.ngrafix',
  'home.hero.signature',
  'home.hero.title',
  'home.hero.subtitle',
  'legal.company',
  'legal.footer_text',
];

function toFlatKey(dotKey, lang) {
  return `${dotKey.replace(/\./g, '_')}_${lang}`;
}

export const SettingsView = {
  delimiters: ['[[', ']]'],
  data() {
    const initialForm = {};
    for (const k of SETTING_KEYS) {
      initialForm[toFlatKey(k, 'fr')] = '';
      initialForm[toFlatKey(k, 'en')] = '';
    }
    return {
      activeTab: 'contact',
      form: initialForm,
    };
  },
  computed: {
    settings() {
      return this.$store.state.settings || {};
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
  watch: {
    settings(newVal) {
      if (newVal) {
        this.initForm(newVal);
      }
    },
  },
  methods: {
    initForm(data) {
      const next = { ...this.form };
      for (const k of SETTING_KEYS) {
        const entry = data && data[k];
        if (entry) {
          next[toFlatKey(k, 'fr')] = entry.fr || '';
          next[toFlatKey(k, 'en')] = entry.en || entry.fr || '';
        }
      }
      this.form = next;
    },
    async submitForm() {
      const payload = {};
      for (const k of SETTING_KEYS) {
        const frVal = this.form[toFlatKey(k, 'fr')] || '';
        const enVal = this.form[toFlatKey(k, 'en')] || frVal;
        payload[k] = { fr: frVal, en: enVal };
      }
      await this.$store.dispatch('saveSettings', payload);
    },
  },
  async mounted() {
    await this.$store.dispatch('fetchSettings');
    if (this.$store.state.settings) {
      this.initForm(this.$store.state.settings);
    }
  },
  hooks: {
    async mounted() {
      await this.$store.dispatch('fetchSettings');
      if (this.$store.state.settings) {
        this.initForm(this.$store.state.settings);
      }
    },
  },
  template: { el: '#tpl-byt3lab-settings' },
};
