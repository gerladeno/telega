import Vue from 'vue'
import Vuex from 'vuex'
import session from "./modules/session";
import axios from 'axios'
axios.defaults.baseURL = "http://127.0.0.1:5000"

Vue.use(Vuex)

export default new Vuex.Store({
    modules: { session }
})