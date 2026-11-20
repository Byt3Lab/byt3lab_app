// @ts-nocheck
export const ContentCrudView = {
  delimiters: ['[[', ']]'],
  data() {
    return {
      resourceName: 'divisions',
      resourceTitle: 'Divisions Technologiques',
      showModal: false,
      isEditing: false,
      activeFormTab: 'fr',
      searchQuery: '',
      formData: {},
      quillFr: null,
      quillEn: null,
      listsText: {
        expertise_list: '',
        expertise_list_en: '',
        technologies_list: '',
        technologies_list_en: '',
        services_list: '',
        services_list_en: '',
        industries_list: '',
        industries_list_en: '',
        related_slugs: '',
        features_list: '',
        features_list_en: '',
        problems_list: '',
        problems_list_en: '',
        benefits_list: '',
        benefits_list_en: '',
        requirements: '',
        requirements_en: '',
      },
    };
  },
  computed: {
    items() {
      const all = this.$store.state[this.resourceName] || [];
      if (!this.searchQuery) return all;
      const q = this.searchQuery.toLowerCase();
      return all.filter(it =>
        (it.title_fr && it.title_fr.toLowerCase().includes(q)) ||
        (it.title_en && it.title_en.toLowerCase().includes(q)) ||
        (it.name && it.name.toLowerCase().includes(q)) ||
        (it.slug && it.slug.toLowerCase().includes(q))
      );
    },
    divisions() {
      return this.$store.state.divisions || [];
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
    userPerms() {
      return (window as any).__BYT3LAB_PERMS__ || {
        read: true,
        write: true,
        publish: true,
        delete: true,
        settings: true,
        admin: true,
      };
    },
  },
  watch: {
    '$route.path': function () {
      this.updateResourceFromRoute();
    },
  },
  methods: {
    updateResourceFromRoute() {
      const hash = window.location.hash.replace('#', '') || '/divisions';
      if (hash.includes('solutions')) {
        this.resourceName = 'solutions';
        this.resourceTitle = 'Produits & Solutions';
      } else if (hash.includes('services')) {
        this.resourceName = 'services';
        this.resourceTitle = "Services d'Ingénierie";
      } else if (hash.includes('projects')) {
        this.resourceName = 'projects';
        this.resourceTitle = 'Projets & Réalisations (Portfolio)';
      } else if (hash.includes('partners')) {
        this.resourceName = 'partners';
        this.resourceTitle = 'Partenaires & Alliances';
      } else if (hash.includes('team')) {
        this.resourceName = 'team';
        this.resourceTitle = "Membres & Pôles de l'Équipe";
      } else if (hash.includes('jobs')) {
        this.resourceName = 'jobs';
        this.resourceTitle = "Offres d'Emploi & Carrières";
      } else if (hash.includes('posts')) {
        this.resourceName = 'posts';
        this.resourceTitle = 'Articles de Blog & Publications';
      } else if (hash.includes('ngrafix')) {
        this.resourceName = 'ngrafix';
        this.resourceTitle = 'Studio Créatif NGRAFIX';
      } else {
        this.resourceName = 'divisions';
        this.resourceTitle = 'Divisions Technologiques';
      }
      this.closeModal();
      this.$store.dispatch('fetchResource', this.resourceName);
      if (this.resourceName !== 'divisions' && (!this.divisions || this.divisions.length === 0)) {
        this.$store.dispatch('fetchResource', 'divisions');
      }
    },

    getItemMeta(it) {
      if (!it) return '—';
      if (this.resourceName === 'solutions') {
        const st = it.status === 'active' ? 'Opérationnel' : 'En dév.';
        return `${it.badge_fr || it.solution_type || 'Solution'} • ${st}`;
      }
      if (this.resourceName === 'services') {
        return it.division_slug || 'Général';
      }
      if (this.resourceName === 'projects') {
        return it.domain_fr || it.domain || 'Ingénierie';
      }
      if (this.resourceName === 'partners') {
        return (it.category || 'technologie').toUpperCase();
      }
      if (this.resourceName === 'team') {
        return `${it.role_fr || it.role || ''} (${it.domain || ''})`;
      }
      if (this.resourceName === 'jobs') {
        return `${it.contract_type || 'CDI'} • ${it.location || 'Cameroun'}`;
      }
      if (this.resourceName === 'posts') {
        return `${it.author_name || 'Byt3Lab'} • ${this.formatDate(it.published_at)}`;
      }
      if (this.resourceName === 'ngrafix') {
        return `${(it.discipline || 'branding').toUpperCase()} • ${it.client_name || 'Studio'}`;
      }
      return it.maturity_status === 'active' ? 'Opérationnelle' : (it.maturity_status || 'Active');
    },

    switchTab(tab) {
      this.activeFormTab = tab;
      setTimeout(() => {
        if (tab === 'fr' && this.quillFr) {
          this.quillFr.update();
        } else if (tab === 'en' && this.quillEn) {
          this.quillEn.update();
        }
      }, 50);
    },

    initQuillEditors() {
      const Quill = window.Quill;
      if (!Quill) {
        console.warn('[Byt3Lab] Quill.js library is not loaded on window.');
        return;
      }

      const toolbarOptions = [
        [{ header: [2, 3, 4, false] }],
        ['bold', 'italic', 'underline', 'strike'],
        [{ list: 'ordered' }, { list: 'bullet' }],
        ['blockquote', 'code-block'],
        [{ color: [] }, { background: [] }],
        ['link', 'clean'],
      ];

      // Init French editor
      const elFr = document.getElementById('quill-editor-fr');
      if (elFr) {
        elFr.innerHTML = '';
        this.quillFr = new Quill(elFr, {
          theme: 'snow',
          modules: { toolbar: toolbarOptions },
          placeholder: 'Rédigez la description professionnelle et structurée en français...',
        });
        if (this.formData.content_fr) {
          this.quillFr.root.innerHTML = this.formData.content_fr;
        }
        this.quillFr.on('text-change', () => {
          const html = this.quillFr.root.innerHTML;
          this.formData.content_fr = html === '<p><br></p>' ? '' : html;
        });
      }

      // Init English editor
      const elEn = document.getElementById('quill-editor-en');
      if (elEn) {
        elEn.innerHTML = '';
        this.quillEn = new Quill(elEn, {
          theme: 'snow',
          modules: { toolbar: toolbarOptions },
          placeholder: 'Write the structured, professional English description here...',
        });
        if (this.formData.content_en) {
          this.quillEn.root.innerHTML = this.formData.content_en;
        }
        this.quillEn.on('text-change', () => {
          const html = this.quillEn.root.innerHTML;
          this.formData.content_en = html === '<p><br></p>' ? '' : html;
        });
      }
    },

    openCreate() {
      this.isEditing = false;
      this.activeFormTab = 'fr';
      this.formData = {
        order_num: 1,
        is_published: true,
        maturity_status: 'active',
        status: 'active',
        solution_type: 'software',
        accent_color: '#1D7FD8',
        category: 'technologie',
        contract_type: 'CDI',
        location: 'Douala, Cameroun',
        icon: 'code',
        discipline: 'branding',
        excerpt_fr: '',
        excerpt_en: '',
        content_fr: '',
        content_en: '',
      };
      this.listsText = {
        expertise_list: '',
        expertise_list_en: '',
        technologies_list: '',
        technologies_list_en: '',
        services_list: '',
        services_list_en: '',
        industries_list: '',
        industries_list_en: '',
        related_slugs: '',
        features_list: '',
        features_list_en: '',
        problems_list: '',
        problems_list_en: '',
        benefits_list: '',
        benefits_list_en: '',
        requirements: '',
        requirements_en: '',
      };
      this.quillFr = null;
      this.quillEn = null;
      this.showModal = true;
      setTimeout(() => this.initQuillEditors(), 80);
    },

    openEdit(item) {
      this.isEditing = true;
      this.activeFormTab = 'fr';
      this.formData = {
        ...item,
        excerpt_fr: item.excerpt_fr || item.summary_fr || '',
        excerpt_en: item.excerpt_en || item.summary_en || '',
        content_fr: item.content_fr || item.description_fr || '',
        content_en: item.content_en || item.description_en || '',
      };

      const toLines = (arr) => Array.isArray(arr) ? arr.join('\n') : (arr || '');
      this.listsText = {
        expertise_list: toLines(item.expertise_list_fr || item.expertise_list),
        expertise_list_en: toLines(item.expertise_list_en),
        technologies_list: toLines(item.technologies_list_fr || item.technologies_list),
        technologies_list_en: toLines(item.technologies_list_en),
        services_list: toLines(item.services_list_fr || item.services_list),
        services_list_en: toLines(item.services_list_en),
        industries_list: toLines(item.industries_list_fr || item.industries_list),
        industries_list_en: toLines(item.industries_list_en),
        related_slugs: toLines(item.related_slugs),
        features_list: toLines(item.features_list_fr || item.features_list),
        features_list_en: toLines(item.features_list_en),
        problems_list: toLines(item.problems_list_fr || item.problems_list),
        problems_list_en: toLines(item.problems_list_en),
        benefits_list: toLines(item.benefits_list_fr || item.benefits_list),
        benefits_list_en: toLines(item.benefits_list_en),
        requirements: toLines(item.requirements_fr || item.requirements),
        requirements_en: toLines(item.requirements_en),
      };
      this.quillFr = null;
      this.quillEn = null;
      this.showModal = true;
      setTimeout(() => this.initQuillEditors(), 80);
    },

    closeModal() {
      this.showModal = false;
      this.formData = {};
      this.quillFr = null;
      this.quillEn = null;
    },

    async saveItem() {
      if (this.quillFr && this.quillFr.root) {
        const htmlFr = this.quillFr.root.innerHTML;
        this.formData.content_fr = htmlFr === '<p><br></p>' ? '' : htmlFr;
      }
      if (this.quillEn && this.quillEn.root) {
        const htmlEn = this.quillEn.root.innerHTML;
        this.formData.content_en = htmlEn === '<p><br></p>' ? '' : htmlEn;
      }

      const toArr = (txt) => (txt || '').split('\n').map(s => s.trim()).filter(Boolean);

      const payload = {
        ...this.formData,
        summary_fr: this.formData.excerpt_fr || this.formData.summary_fr || '',
        summary_en: this.formData.excerpt_en || this.formData.summary_en || '',
        description_fr: this.formData.content_fr || this.formData.description_fr || '',
        description_en: this.formData.content_en || this.formData.description_en || '',
      };

      if (this.resourceName === 'divisions') {
        payload.expertise_list = toArr(this.listsText.expertise_list);
        payload.expertise_list_en = toArr(this.listsText.expertise_list_en);
        payload.technologies_list = toArr(this.listsText.technologies_list);
        payload.technologies_list_en = toArr(this.listsText.technologies_list_en);
        payload.services_list = toArr(this.listsText.services_list);
        payload.services_list_en = toArr(this.listsText.services_list_en);
        payload.industries_list = toArr(this.listsText.industries_list);
        payload.industries_list_en = toArr(this.listsText.industries_list_en);
        payload.related_slugs = toArr(this.listsText.related_slugs);
      } else if (this.resourceName === 'solutions') {
        payload.features_list = toArr(this.listsText.features_list);
        payload.features_list_en = toArr(this.listsText.features_list_en);
        payload.problems_list = toArr(this.listsText.problems_list);
        payload.problems_list_en = toArr(this.listsText.problems_list_en);
        payload.benefits_list = toArr(this.listsText.benefits_list);
        payload.benefits_list_en = toArr(this.listsText.benefits_list_en);
      } else if (this.resourceName === 'jobs') {
        payload.requirements = toArr(this.listsText.requirements);
        payload.requirements_en = toArr(this.listsText.requirements_en);
      }

      const id = this.isEditing ? this.formData.id : null;
      const ok = await this.$store.dispatch('saveResource', {
        resourceName: this.resourceName,
        id,
        data: payload,
      });

      if (ok) {
        this.closeModal();
      }
    },

    async deleteItem(id) {
      if (confirm('Êtes-vous certain de vouloir supprimer cet élément ?')) {
        await this.$store.dispatch('deleteResource', {
          resourceName: this.resourceName,
          id,
        });
      }
    },

    formatDate(d) {
      if (!d) return '—';
      if (typeof d === 'string' && d.includes('/')) return d;
      try {
        const dt = new Date(d);
        return isNaN(dt.getTime()) ? d : dt.toLocaleDateString();
      } catch (e) {
        return d;
      }
    },
  },

  mounted() {
    this.updateResourceFromRoute();
  },

  hooks: {
    mounted() {
      this.updateResourceFromRoute();
    },
  },

  template: { el: '#tpl-byt3lab-crud' },
};

export function createContentCrudView(defaultResource, defaultTitle) {
  return {
    ...ContentCrudView,
    data() {
      return {
        ...ContentCrudView.data(),
        resourceName: defaultResource,
        resourceTitle: defaultTitle,
      };
    },
  };
}
