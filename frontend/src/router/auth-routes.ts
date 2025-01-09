import type { RouteRecordRaw } from "vue-router";
import LoginView from "@/views/auth/LoginView.vue";
import RegisterView from "@/views/auth/RegisterView.vue";
import VerifyEmailView from "@/views/auth/VerifyEmailView.vue";
import ResetPasswordView from "@/views/auth/ResetPasswordView.vue";
import ValidateView from "@/views/auth/ValidateView.vue";

const authRoutes: RouteRecordRaw[] = [
  {
    path: "login",
    name: "login",
    component: LoginView,
  },
  {
    path: "register",
    name: "register",
    component: RegisterView,
  },
  {
    path: "validate",
    name: "validate",
    component: ValidateView,
    props: (route) => ({
      mode: route.query.mode,
      oobCode: route.query.oobCode,
    }),
  },
  {
    path: "verify-email",
    name: "verifyEmail",
    component: VerifyEmailView,
  },
  {
    path: "reset-password",
    name: "resetPassword",
    component: ResetPasswordView,
    props: (route) => ({
      email: route.query.email,
      oobCode: route.query.oobCode,
    }),
  },
];

export default authRoutes;
