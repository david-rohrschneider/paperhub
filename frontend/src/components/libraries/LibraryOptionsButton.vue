<script setup lang="ts">
import Button from "primevue/button";
import Menu from "primevue/menu";
import { ref, useTemplateRef } from "vue";

const emit = defineEmits(["settings", "delete"]);

const items = ref([
  {
    label: "Settings",
    icon: "pi pi-cog",
    command: () => emit("settings"),
  },
  {
    label: "Delete Library",
    icon: "pi pi-trash",
    command: () => emit("delete"),
  },
]);

const menu = useTemplateRef("menu");

const toggle = (e: Event) => menu.value?.toggle(e);
</script>

<template>
  <Button variant="text" icon="pi pi-ellipsis-v" @click="toggle" />
  <Menu ref="menu" :model="items" :popup="true" />
</template>
