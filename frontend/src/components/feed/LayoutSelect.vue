<script setup lang="ts">
import SelectButton from "primevue/selectbutton";

const layout = defineModel<"list" | "grid">({ required: true });
</script>

<template>
  <SelectButton
    style="height: 3rem"
    v-model="layout"
    :options="['list', 'grid']"
    :allowEmpty="false"
  >
    <template #option="{ option }">
      <i :class="[option === 'list' ? 'pi pi-bars' : 'pi pi-table']" />
    </template>
  </SelectButton>
</template>
