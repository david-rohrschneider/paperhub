import { createRouter, createWebHistory } from "vue-router";
import AuthLayout from "@/layouts/AuthLayout.vue";
import AppLayout from "@/layouts/AppLayout.vue";
import authRoutes from "@/router/auth-routes";
import appRoutes from "@/router/app-routes";
import { getCurrentUser } from "vuefire";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/auth",
      name: "authentication",
      component: AuthLayout,
      redirect: "/auth/login",
      children: [...authRoutes],
    },
    {
      path: "/",
      name: "app",
      component: AppLayout,
      children: [...appRoutes],
    },
  ],
});

router.beforeEach(async (to) => {
  const authPages = authRoutes.map((route) => `/auth/${route.path}`);
  const isAppPage = !authPages.includes(to.path);

  const user = await getCurrentUser();

  if (user?.emailVerified === false) {
    if (to.path === "/auth/verify-email") return;
    if (to.path === "/auth/validate") return;
    return "/auth/verify-email";
  }

  if (isAppPage && !user) {
    return "/auth";
  }

  if (!isAppPage && user) {
    return "/";
  }
});

export default router;
