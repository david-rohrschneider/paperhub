<script setup lang="ts">
import NavbarLink from "@/components/navbar/NavbarLink.vue";
import navbarLinks from "@/components/navbar/navbar-links";
</script>

<template>
  <div class="navbar-links">
    <NavbarLink v-for="link in navbarLinks" :key="link.label" :to="link.to" :label="link.label" />
  </div>
</template>

<style scoped>
.navbar-links {
  display: flex;
  gap: 1rem;
}
</style>
