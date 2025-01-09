<script setup lang="ts">
import Button from "primevue/button";
import { useThemeStore } from "@/stores/theme-store";
import { storeToRefs } from "pinia";

const themeStore = useThemeStore();
const { toggleTheme } = themeStore;
const { isDark } = storeToRefs(themeStore);
</script>

<template>
  <Button
    style="width: auto"
    size="large"
    variant="text"
    :icon="isDark ? 'pi pi-moon' : 'pi pi-sun'"
    @click="toggleTheme"
  />
</template>
