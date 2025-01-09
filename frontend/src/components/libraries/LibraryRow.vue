<script setup lang="ts">
import Card from "primevue/card";
import Tag from "primevue/tag";
import type { Library } from "@/api/types";
import { computed } from "vue";

const { library } = defineProps<{ library: Library }>();
const emit = defineEmits(["click"]);

const numPapersString = computed(() => {
  if (library.num_papers === 1) return "1 Paper";
  return `${library.num_papers} Papers`;
});
</script>

<template>
  <Card :class="$style.libraryrow" @click="emit('click')">
    <template #title>{{ library.title }}</template>
    <template #content>
      <div :class="$style.tags">
        <Tag
          :icon="library.private ? 'pi pi-lock' : 'pi pi-lock-open'"
          :value="library.private ? 'Private' : 'Public'"
        />
        <Tag icon="pi pi-book" :value="numPapersString" />
        <Tag v-if="library.default" value="Default" />
      </div>
    </template>
  </Card>
</template>

<style scoped module>
.libraryrow {
  width: 100%;
  border: 1px solid var(--p-card-border);
  cursor: pointer;
}

.libraryrow:hover {
  background: var(--p-card-hover-background);
}

.libraryrow:active {
  background: var(--p-card-active-background);
}

.tags {
  display: flex;
  gap: 0.5rem;
}
</style>
