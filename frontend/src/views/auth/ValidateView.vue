<script setup lang="ts">
import { applyActionCode, verifyPasswordResetCode, signOut } from "firebase/auth";
import { useToast } from "primevue";
import ProgressSpinner from "primevue/progressspinner";
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useFirebaseAuth } from "vuefire";

const { mode, oobCode } = defineProps<{ mode?: string; oobCode?: string }>();

const auth = useFirebaseAuth()!;
const loading = ref(true);
const toast = useToast();
const router = useRouter();

const handleResetPassword = async (code: string) => {
  try {
    const email = await verifyPasswordResetCode(auth, code);
    router.push(`/auth/reset-password?email=${email}&oobCode=${code}`);
  } catch {
    toast.add({
      severity: "error",
      summary: "Error",
      detail: "Failed to reset password. Please try requesting a new password reset email.",
      life: 5000,
    });
    router.push("/auth/login");
  } finally {
    loading.value = false;
  }
};

const handleVerifyEmail = async (code: string) => {
  try {
    await applyActionCode(auth, code);
    await signOut(auth);
    toast.add({
      severity: "success",
      summary: "Success",
      detail: "Email address confirmed. You can now log in!",
      life: 5000,
    });
    router.push("/auth/login");
  } catch {
    toast.add({
      severity: "error",
      summary: "Error",
      detail: "Failed to confirm email address. Please try requesting a new confirmation email.",
      life: 5000,
    });
    router.push("/auth/verify-email");
  } finally {
    loading.value = false;
  }
};

const handler = () => {
  if (!mode || !oobCode) {
    router.push("/auth/login");
    return;
  }

  switch (mode) {
    case "resetPassword":
      handleResetPassword(oobCode);
      break;

    case "verifyEmail":
      handleVerifyEmail(oobCode);
      break;

    default:
      router.push("/auth/login");
  }
};

onMounted(handler);
</script>

<template>
  <ProgressSpinner
    v-if="loading"
    style="width: 50px; height: 50px"
    strokeWidth="8"
    fill="transparent"
    animationDuration=".5s"
  />
</template>
