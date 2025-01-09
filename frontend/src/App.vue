<script setup lang="ts">
import { computed, onMounted, watch } from "vue";
import { useThemeStore } from "@/stores/theme-store";
import { storeToRefs } from "pinia";
import { RouterView } from "vue-router";
import { useCurrentUser } from "vuefire";
import { useApi } from "@/api/use-api";
import routes from "@/api/routes";
import { useUserStore } from "@/stores/user-store";
import type { User } from "@/api/types";
import { useFavicon } from "@vueuse/core";
import AppToast from "@/components/AppToast.vue";

const themeStore = useThemeStore();
const { isDark } = storeToRefs(themeStore);

const favicon = computed(() => (isDark.value ? "/favicon-dark.ico" : "/favicon-light.ico"));
useFavicon(favicon);

const firebaseUser = useCurrentUser();
const { get } = useApi(routes.users.get.currentUser);
const userStore = useUserStore();
const { user } = storeToRefs(userStore);

onMounted(() => themeStore.initializeTheme());

watch(firebaseUser, async (newUser, oldUser) => {
  if (!newUser && oldUser) {
    // User logged out
    user.value = null;
    return;
  }

  if (newUser && !oldUser) {
    // User logged in
    if (!newUser.emailVerified) {
      // User logged in but email not verified
      return;
    }
    const response = await get<User>();
    if (!response?.data) return;
    user.value = response.data;
  }
});
</script>

<template>
  <AppToast />
  <RouterView />
</template>
