import Vue from 'vue'
import App from './App.vue'
import router from './router'
import 'materialize-css/dist/js/materialize.min'
// import vuex from 'vuex'

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
