<script setup lang="ts">
import { ref } from "vue";
import InputGroup from "primevue/inputgroup";
import InputText from "primevue/inputtext";
import InputGroupAddon from "primevue/inputgroupaddon";
import Button from "primevue/button";

const query = ref("");
</script>

<template>
  <InputGroup>
    <InputText
      size="large"
      variant="filled"
      v-model="query"
      placeholder="Search for any paper..."
    />
    <InputGroupAddon>
      <Button size="large" icon="pi pi-search" />
    </InputGroupAddon>
  </InputGroup>
</template>
