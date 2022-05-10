import api from "../api"

export default {
  state: {
    userInfo: {
      isAuth: false,
    },
    accessToken: null,
  },
  getters: {
    userInfo: (state) => state.userInfo,
    accessToken: (state) => {
      return state.accessToken
        ? state.accessToken
        : localStorage.accessToken || null
    },
  },
  mutations: {
    setUserInfo(state, info) {
      state.userInfo = info
    },
    clearUserInfo(state) {
      state.userInfo = {
        isAuth: false,
      }
    },
    setAccessToken(state, token) {
      state.accessToken = token
      localStorage.accessToken = token
    },
    clearAccessToken(state) {
      state.accessToken = null
    },
  },
  actions: {
    async getCurrentUser({ commit, getters }) {
      if (!getters.userInfo.username) {
        const currentUser = {
          ...(await api.user.getCurrentUser()).data,
          isAuth: true,
        }
        commit("setUserInfo", currentUser)
      }
      return getters.userInfo
    },
  },
}
