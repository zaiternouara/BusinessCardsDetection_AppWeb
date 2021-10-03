const state = {
  dialog: false,
};
const mutations = {
  changeValue: (state) => {
    state.dialog = state.dialog= !state.dialog
  },
};
const actions = {
  show: (context) => context.commit("changeValue"),
};
const getters = {
  getDialog: (state) => state.dialog,
};

export default {
  state,
  getters,
  actions,
  mutations
};
