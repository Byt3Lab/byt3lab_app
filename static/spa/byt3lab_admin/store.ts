// @ts-nocheck
import { MelodiStore } from '/static/base/melodiJS/index.js';

export const store = new MelodiStore({
  state: {
    dashboard: null,
    messages: [],
    messagesCounts: { total: 0, new: 0, in_progress: 0, resolved: 0 },
    divisions: [],
    solutions: [],
    services: [],
    projects: [],
    partners: [],
    team: [],
    jobs: [],
    posts: [],
    ngrafix: [],
    settings: {},
    loading: false,
    error: null,
    successMessage: null,
  },

  mutations: {
    SET_LOADING(state, val) {
      state.loading = !!val;
    },
    SET_ERROR(state, err) {
      state.error = err;
    },
    SET_SUCCESS_MESSAGE(state, msg) {
      state.successMessage = msg;
    },
    SET_DASHBOARD(state, data) {
      state.dashboard = data;
    },
    SET_MESSAGES(state, payload) {
      if (Array.isArray(payload)) {
        state.messages = payload;
      } else if (payload && typeof payload === 'object') {
        state.messages = payload.data || [];
        state.messagesCounts = payload.counts || { total: 0, new: 0, in_progress: 0, resolved: 0 };
      }
    },
    SET_DIVISIONS(state, data) {
      state.divisions = Array.isArray(data) ? data : [];
    },
    SET_SOLUTIONS(state, data) {
      state.solutions = Array.isArray(data) ? data : [];
    },
    SET_SERVICES(state, data) {
      state.services = Array.isArray(data) ? data : [];
    },
    SET_PROJECTS(state, data) {
      state.projects = Array.isArray(data) ? data : [];
    },
    SET_PARTNERS(state, data) {
      state.partners = Array.isArray(data) ? data : [];
    },
    SET_TEAM(state, data) {
      state.team = Array.isArray(data) ? data : [];
    },
    SET_JOBS(state, data) {
      state.jobs = Array.isArray(data) ? data : [];
    },
    SET_POSTS(state, data) {
      state.posts = Array.isArray(data) ? data : [];
    },
    SET_NGRAFIX(state, data) {
      state.ngrafix = Array.isArray(data) ? data : [];
    },
    SET_SETTINGS(state, data) {
      state.settings = data || {};
    },
  },

  actions: {
    async fetchDashboard({ commit }) {
      commit('SET_LOADING', true);
      commit('SET_ERROR', null);
      try {
        const res = await window.melodi.api.get('/api/byt3lab_app/admin/dashboard');
        const payload = (res && res.data && res.data.counts)
          ? res.data
          : (res && res.data && res.data.data ? res.data.data : null);
        if (payload) {
          commit('SET_DASHBOARD', payload);
        }
      } catch (e) {
        commit('SET_ERROR', e.message || 'Erreur lors du chargement du tableau de bord');
      } finally {
        commit('SET_LOADING', false);
      }
    },

    async fetchMessages({ commit }, statusFilter = '') {
      commit('SET_LOADING', true);
      commit('SET_ERROR', null);
      try {
        const url = statusFilter
          ? `/api/byt3lab_app/admin/messages?status=${encodeURIComponent(statusFilter)}`
          : '/api/byt3lab_app/admin/messages';
        const res = await window.melodi.api.get(url);
        if (res && Array.isArray(res.data)) {
          commit('SET_MESSAGES', res);
        } else if (res && res.data && Array.isArray(res.data.data)) {
          commit('SET_MESSAGES', res.data);
        }
      } catch (e) {
        commit('SET_ERROR', e.message || 'Erreur lors du chargement des messages');
      } finally {
        commit('SET_LOADING', false);
      }
    },

    async updateMessageStatus({ commit, dispatch }, { id, status }) {
      try {
        const res = await window.melodi.api.put(`/api/byt3lab_app/admin/messages/${id}/status`, { status });
        if (res && (res.success || (res.data && res.data.success))) {
          commit('SET_SUCCESS_MESSAGE', 'Statut du message mis à jour');
          dispatch('fetchMessages');
          dispatch('fetchDashboard');
          return true;
        }
      } catch (e) {
        commit('SET_ERROR', e.message);
      }
      return false;
    },

    async deleteMessage({ commit, dispatch }, id) {
      try {
        const res = await window.melodi.api.delete(`/api/byt3lab_app/admin/messages/${id}`);
        if (res && (res.success || (res.data && res.data.success))) {
          commit('SET_SUCCESS_MESSAGE', 'Message supprimé');
          dispatch('fetchMessages');
          dispatch('fetchDashboard');
          return true;
        }
      } catch (e) {
        commit('SET_ERROR', e.message);
      }
      return false;
    },

    async fetchSettings({ commit }) {
      commit('SET_LOADING', true);
      try {
        const res = await window.melodi.api.get('/api/byt3lab_app/admin/settings');
        const payload = (res && res.data && res.data.data)
          ? res.data.data
          : (res && res.data ? res.data : null);
        if (payload) {
          commit('SET_SETTINGS', payload);
        }
      } catch (e) {
        commit('SET_ERROR', e.message);
      } finally {
        commit('SET_LOADING', false);
      }
    },

    async saveSettings({ commit }, settingsData) {
      commit('SET_LOADING', true);
      try {
        const res = await window.melodi.api.post('/api/byt3lab_app/admin/settings', settingsData);
        const payload = (res && res.data && res.data.data)
          ? res.data.data
          : (res && res.data ? res.data : null);
        if (res && (res.success || payload)) {
          if (payload) commit('SET_SETTINGS', payload);
          commit('SET_SUCCESS_MESSAGE', 'Réglages enregistrés avec succès');
          return true;
        }
      } catch (e) {
        commit('SET_ERROR', e.message);
      } finally {
        commit('SET_LOADING', false);
      }
      return false;
    },

    // Generic list fetcher
    async fetchResource({ commit }, resourceName) {
      commit('SET_LOADING', true);
      try {
        const res = await window.melodi.api.get(`/api/byt3lab_app/admin/${resourceName}`);
        const items = (res && Array.isArray(res.data))
          ? res.data
          : (res && res.data && Array.isArray(res.data.data) ? res.data.data : []);
        const mutationName = `SET_${resourceName.toUpperCase()}`;
        commit(mutationName, items);
      } catch (e) {
        commit('SET_ERROR', e.message);
      } finally {
        commit('SET_LOADING', false);
      }
    },

    // Generic saver (POST or PUT)
    async saveResource({ commit, dispatch }, { resourceName, id, data }) {
      commit('SET_LOADING', true);
      try {
        let res;
        if (id) {
          res = await window.melodi.api.put(`/api/byt3lab_app/admin/${resourceName}/${id}`, data);
        } else {
          res = await window.melodi.api.post(`/api/byt3lab_app/admin/${resourceName}`, data);
        }
        if (res && (res.success || (res.data && res.data.success))) {
          commit('SET_SUCCESS_MESSAGE', 'Enregistrement réussi');
          await dispatch('fetchResource', resourceName);
          dispatch('fetchDashboard');
          return true;
        }
      } catch (e) {
        commit('SET_ERROR', e.message);
      } finally {
        commit('SET_LOADING', false);
      }
      return false;
    },

    // Generic deleter
    async deleteResource({ commit, dispatch }, { resourceName, id }) {
      try {
        const res = await window.melodi.api.delete(`/api/byt3lab_app/admin/${resourceName}/${id}`);
        if (res && (res.success || (res.data && res.data.success))) {
          commit('SET_SUCCESS_MESSAGE', 'Suppression réussie');
          await dispatch('fetchResource', resourceName);
          dispatch('fetchDashboard');
          return true;
        }
      } catch (e) {
        commit('SET_ERROR', e.message);
      }
      return false;
    },
  },
});
