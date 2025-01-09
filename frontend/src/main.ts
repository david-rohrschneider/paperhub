import "@/assets/styles/main.css";
import { createApp } from "vue";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";
import { ToastService } from "primevue";
import Tooltip from "primevue/tooltip";
import { VueFire, VueFireAuth } from "vuefire";
import { plugin as VueInputAutowidth } from "vue-input-autowidth";
import App from "@/App.vue";
import router from "@/router";
import primeVueTheme from "@/prime-vue-theme";
import { firebaseApp } from "@/firebase";

const app = createApp(App);

app.use(PrimeVue, primeVueTheme);
app.use(ToastService);
app.directive("tooltip", Tooltip);

app.use(VueInputAutowidth);

app.use(VueFire, {
  firebaseApp,
  modules: [VueFireAuth()],
});

app.use(createPinia());
app.use(router);

app.mount("#app");
