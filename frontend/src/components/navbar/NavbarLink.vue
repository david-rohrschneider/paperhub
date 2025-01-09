<script setup lang="ts">
import { useLink, useRoute } from "vue-router";
import Button from "primevue/button";
import { computed } from "vue";

const { to, label } = defineProps<{
  to: string;
  label: string;
}>();

const route = useRoute();

const link = useLink({ to });
const variant = computed(() => {
  if (to == "/" && route.path !== "/") return "text";
  return link.isActive.value ? undefined : "link";
});
</script>

<template>
  <Button size="large" as="router-link" :variant="variant" :to="link.route" :label="label" />
</template>
