<script setup lang="ts">
import AppLogo from "@/components/AppLogo.vue";
import NavbarLinks from "@/components/navbar/NavbarLinks.vue";
import ThemeButton from "@/components/navbar/ThemeButton.vue";
import UserAvatar from "@/components/navbar/UserAvatar.vue";
import { useThemeStore } from "@/stores/theme-store";
import { storeToRefs } from "pinia";
import MobileMenu from "./MobileMenu.vue";
import { useWindowScroll } from "@vueuse/core";

const themeStore = useThemeStore();
const { isMobile } = storeToRefs(themeStore);

const { y } = useWindowScroll();
</script>

<template>
  <div class="navbar" :class="{ 'navbar-mobile': isMobile, scrolled: y > 100 }">
    <AppLogo :width="50" :height="50" />
    <NavbarLinks v-if="!isMobile" />
    <div class="user-content">
      <ThemeButton />
      <UserAvatar v-if="!isMobile" />
      <MobileMenu v-if="isMobile" />
    </div>
  </div>
</template>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  padding: 2rem;
  width: 100%;
  max-width: 1920px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  backdrop-filter: blur(15px);
}

.navbar::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: var(--p-card-background);
  opacity: 0;
  z-index: -1;
  transition: opacity 0.3s;
}

.navbar.scrolled::after {
  opacity: 0.7;
}

.navbar-mobile {
  padding: 1rem;
}

.user-content {
  display: flex;
  align-items: center;
  gap: 1rem;
}
</style>
