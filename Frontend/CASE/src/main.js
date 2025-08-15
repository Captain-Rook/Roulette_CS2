import './assets/reset.css'
import router from '@/router/index.js'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
import App from '@/App.vue'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faArrowRightFromBracket, faArrowLeft, faArrowRight, faHandHoldingDollar} from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import 'devextreme/dist/css/dx.material.purple.dark.css';
library.add(faArrowRightFromBracket, faArrowLeft, faArrowRight, faHandHoldingDollar)

const app = createApp(App)

app.component('font-awesome-icon', FontAwesomeIcon)

app.use(router)
app.use(createPinia())

app.mount('#app')  