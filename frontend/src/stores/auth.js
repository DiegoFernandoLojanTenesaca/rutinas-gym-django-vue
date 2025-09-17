// src/stores/auth.js
import { defineStore } from 'pinia';
import { login as apiLogin, applyAuthToken } from '@/services/auth';

const LS_USER_KEY = 'lg_user';
const LS_TOKEN_KEY = 'lg_token';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,   // { id, nombre }
    token: null,  // string
  }),

  getters: {
    isLogged: (s) => !!s.token,
  },

  actions: {
    restoreFromStorage() {
      try {
        const user = JSON.parse(localStorage.getItem(LS_USER_KEY) || 'null');
        const token = localStorage.getItem(LS_TOKEN_KEY) || null;
        this.user = user;
        this.token = token;
        applyAuthToken(token);
      } catch (_) {
        this.user = null;
        this.token = null;
        applyAuthToken(null);
      }
    },

    async login(credentials) {
      const { id, nombre, token } = await apiLogin(credentials);
      this.user = { id, nombre };
      this.token = token;
      // persistir
      localStorage.setItem(LS_USER_KEY, JSON.stringify(this.user));
      localStorage.setItem(LS_TOKEN_KEY, token);
      applyAuthToken(token);
    },

    logout() {
      this.user = null;
      this.token = null;
      localStorage.removeItem(LS_USER_KEY);
      localStorage.removeItem(LS_TOKEN_KEY);
      applyAuthToken(null);
    },

    updateLocalUser(partial) {
      this.user = { ...(this.user || {}), ...(partial || {}) };
      localStorage.setItem('lg_user', JSON.stringify(this.user));
    },

  },
});
