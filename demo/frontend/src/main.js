import Vue from 'vue'
import 'ant-design-vue/dist/antd.css'
import Antd from 'ant-design-vue'
import App from './App'


Vue.use(Antd)

new Vue({
    render: h => h(App),
}).$mount('#app')
