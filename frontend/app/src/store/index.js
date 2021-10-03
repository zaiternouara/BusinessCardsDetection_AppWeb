import Vue from "vue";
import Vuex from "vuex";
Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    dialog: false,
  },
  mutations: {
    changeValue: (state) => {
      state.dialog = state.dialog = !state.dialog;
    },
  },
  actions: { show: (context) => context.commit("changeValue") },
  getters: { getDialog: (state) => state.dialog },
  modules: {},
});
