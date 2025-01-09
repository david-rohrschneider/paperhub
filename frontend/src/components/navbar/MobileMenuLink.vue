<script setup lang="ts">
import { useLink } from "vue-router";
import Button from "primevue/button";
import { computed } from "vue";

const { to, label, icon } = defineProps<{
  to: string;
  label: string;
  icon?: string;
}>();

const link = useLink({ to });
const variant = computed(() => (link.isExactActive.value ? undefined : "outlined"));

const emit = defineEmits<{
  click: [];
}>();
</script>

<template>
  <Button
    :icon="icon"
    size="large"
    as="router-link"
    :variant="variant"
    :to="link.route"
    :label="label"
    @click="emit('click')"
  />
</template>
