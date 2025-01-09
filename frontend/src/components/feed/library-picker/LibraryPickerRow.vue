<script setup lang="ts">
import Tag from "primevue/tag";
import type { Library } from "@/api/types";

const { library } = defineProps<{ library: Library }>();
const emit = defineEmits<{
  click: [event: MouseEvent];
}>();
</script>

<template>
  <div
    class="libraryrow"
    :class="{ disabled: library.contains_paper }"
    @click="(e) => emit('click', e)"
    v-tooltip="library.contains_paper ? 'Already contains paper' : undefined"
  >
    <b :style="{ fontSize: '1rem' }">
      {{ library.title }}
    </b>
    <Tag
      severity="secondary"
      :icon="library.private ? 'pi pi-lock' : 'pi pi-lock-open'"
      :value="library.private ? 'Private' : 'Public'"
    />
  </div>
</template>

<style scoped>
.libraryrow {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  gap: 1rem;
  padding: 0.5rem 1rem;
  background: var(--p-card-background);
  border-radius: var(--p-card-border-radius);
  border: 1px solid var(--p-card-border);
}

.libraryrow:not(.disabled) {
  cursor: pointer;
}

.libraryrow:not(.disabled):hover {
  background: var(--p-card-hover-background);
}

.libraryrow:not(.disabled):active {
  background: var(--p-card-active-background);
}

.libraryrow.disabled {
  opacity: 0.5;
}
</style>
