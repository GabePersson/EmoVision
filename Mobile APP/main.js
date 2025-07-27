import TabBar from '@/components/TabBar/index.vue'
import NavBar from '@/components/NavBar/index.vue'
import SearchBar from '@/components/SearchBar/index.vue'
import SwiperWindow from '@/components/SwiperWindow/index.vue'
import Modal from '@/components/Modal/index.vue'
// #ifndef VUE3
import Vue from 'vue'
import App from './App'


Vue.config.productionTip = false

App.mpType = 'app'

const app = new Vue({
	...App
})
app.$mount()
// #endif

// #ifdef VUE3
import {
	createSSRApp
} from 'vue'
import App from './App.vue'
export function createApp() {
	const app = createSSRApp(App)
	return {
		app
	}
}
// #endif

Vue.component('TabBar', TabBar)
Vue.component('NavBar', NavBar)
Vue.component('SearchBar', SearchBar)
Vue.component('SwiperWindow', SwiperWindow)
Vue.component('Modal', Modal)