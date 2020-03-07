import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from "vuex-persistedstate";
import session from "./modules/sessionStore";
import axios from 'axios'

axios.defaults.baseURL = "http://127.0.0.1:5000"
Vue.use(Vuex)

export default new Vuex.Store({
    modules: { session },
    plugins: [createPersistedState()],
})