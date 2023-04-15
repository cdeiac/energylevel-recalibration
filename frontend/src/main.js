/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'

// Plugins
import { registerPlugins } from '@/plugins'

// Highcharts
import HighchartsVue from 'highcharts-vue'
import Highcharts from 'highcharts'
import draggablePoints from 'highcharts/modules/draggable-points'
import Xrange from 'highcharts/modules/xrange'

const app = createApp(App)
app.use(HighchartsVue)
//Xrange(Highcharts)
registerPlugins(app)

app.mount('#app')
