<script setup lang="ts">
import { useTitle } from "@vueuse/core";

const { title, subtitle } = defineProps<{ title: string; subtitle?: string }>();
useTitle(`paperhub | ${title}`);
</script>

<template>
  <div class="header">
    <div class="left">
      <h1>{{ title }}</h1>
      <h4 v-if="subtitle">{{ subtitle }}</h4>
    </div>
    <slot name="right" />
  </div>
</template>

<style scoped>
.header {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}
</style>
