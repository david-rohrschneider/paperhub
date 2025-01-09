<script setup lang="ts">
import { RouterView } from "vue-router";
import NavBar from "@/components/navbar/NavBar.vue";
import { useThemeStore } from "@/stores/theme-store";
import { storeToRefs } from "pinia";

const themeStore = useThemeStore();
const { isMobile } = storeToRefs(themeStore);
</script>

<template>
  <NavBar />
  <div :class="isMobile ? 'navbar-spacer-mobile' : 'navbar-spacer'" />
  <div class="page-container">
    <RouterView />
  </div>
</template>

<style scoped>
.navbar-spacer {
  height: 6rem;
}

.navbar-spacer-mobile {
  height: 3.5rem;
}

.page-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}
</style>
