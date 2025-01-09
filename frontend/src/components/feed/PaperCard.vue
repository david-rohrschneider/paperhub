<script setup lang="ts">
import Card from "primevue/card";
import Tag from "primevue/tag";
import Checkbox from "primevue/checkbox";
import type { Paper } from "@/api/types";
import PaperThumbnail from "@/components/feed/PaperThumbnail.vue";
import CitationIcon from "@/components/CitationIcon.vue";
import { useThemeStore } from "@/stores/theme-store";

const { paper, selectable = false } = defineProps<{ paper: Paper; selectable?: boolean }>();

const emit = defineEmits(["click"]);
const selectedPapers = defineModel<string[]>("selected-papers", { default: [] });

const { breakpoints } = useThemeStore();
const isMobile = breakpoints.smaller("tablet");

const authors =
  paper.authors.length > 3
    ? `${paper.authors.slice(0, 3).join(", ")} et al.`
    : paper.authors.join(", ");

const pt = {
  header: { style: { position: "relative" } },
  title: { style: { fontSize: isMobile.value ? "medium" : "1.1rem" } },
  subtitle: { style: { fontSize: isMobile.value ? "small" : "1.1rem" } },
  body: { style: { flexGrow: 1 } },
  footer: { style: { display: "flex", justifyContent: "space-between", marginTop: "auto" } },
};
</script>

<template>
  <Card :class="$style.papercard" :pt="pt" @click="emit('click')">
    <template #header>
      <PaperThumbnail :class="$style.thumbnail" :paper="paper" />
      <Checkbox
        v-if="selectable"
        v-model="selectedPapers"
        :value="paper.id"
        :class="$style.checkbox"
        :dt="{
          checkedBackground: '{zinc.900}',
          checkedHoverBackground: '{zinc.700}',
          iconCheckedColor: '{zinc.50}',
          iconCheckedHoverColor: '{zinc.50}',
        }"
        @click.stop
      />
    </template>
    <template #title>{{ paper.title }}</template>
    <template #subtitle>{{ authors }}</template>
    <template #footer>
      <div>
        <span class="pi pi-thumbs-up" />
        <span style="margin-left: 0.5rem; margin-right: 1rem">{{ paper.likes }}</span>
        <CitationIcon />
        <span style="margin-left: 0.5rem">{{ paper.citations }}</span>
      </div>
      <Tag
        v-if="paper.published_at"
        style="font-weight: normal"
        icon="pi pi-calendar"
        :value="new Date(paper.published_at).toLocaleDateString()"
        severity="secondary"
      />
    </template>
  </Card>
</template>

<style scoped module>
.papercard {
  width: 100%;
  max-width: 25rem;
  border: 1px solid var(--p-card-border);
  background: var(--p-card-background);
  cursor: pointer;
  transition: background var(--p-transition-duration);
}

.papercard:hover {
  background: var(--p-card-hover-background);
}

.papercard:active {
  box-shadow: none;
  background: var(--p-card-active-background);
}

.thumbnail {
  width: 100%;
  height: 12rem;
  border-radius: var(--p-card-border-radius) var(--p-card-border-radius) 0 0;
  border-bottom: 1px solid var(--p-card-border);
}

@media screen and (max-width: 640px) {
  .thumbnail {
    height: 10rem;
  }
}

.checkbox {
  position: absolute;
  top: 1rem;
  right: 1rem;
}
</style>
