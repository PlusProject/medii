import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import vuetify from '../plugins/vuetify'

Vue.config.productionTip = false
Vue.config.devtools = true


new Vue(Vue.util.extend({ router, store, vuetify }, App)).$mount('#app')