<script setup lang="ts">
import { PUB_TYPE_MAP } from "@/api/mappings";
import type { Paper } from "@/api/types";
import PaperThumbnail from "@/components/feed/PaperThumbnail.vue";
import { useThemeStore } from "@/stores/theme-store";
import Tag from "primevue/tag";
import Card from "primevue/card";
import Checkbox from "primevue/checkbox";
import CitationIcon from "@/components/CitationIcon.vue";

const { paper, selectable = false } = defineProps<{ paper: Paper; selectable?: boolean }>();

const emit = defineEmits(["click", "delete"]);
const selectedPapers = defineModel<string[]>("selected-papers", { default: [] });

const { breakpoints } = useThemeStore();
const isTablet = breakpoints.smaller("desktop");
const isMobile = breakpoints.smaller("tablet");

const authors =
  paper.authors.length > 3
    ? `${paper.authors.slice(0, 3).join(", ")} et al.`
    : paper.authors.join(", ");

const pt = {
  body: { style: { padding: 0 } },
  content: { style: { display: "flex", gap: "1rem" } },
};
</script>

<template>
  <div :class="$style['paper-row']">
    <Checkbox v-if="selectable" :value="paper.id" v-model="selectedPapers" />
    <Card :class="$style.paperrowcard" :pt="pt" @click="emit('click')">
      <template #content>
        <PaperThumbnail v-if="!isMobile" :class="$style.thumbnail" :paper="paper" />
        <div :class="$style['paper-details']">
          <component :is="isMobile ? 'h4' : 'h3'">
            {{ paper.title }}
          </component>
          <component :is="isMobile ? 'small' : 'p'" :class="$style.subtitle">
            {{ authors }}
          </component>
          <div v-if="!isTablet" :class="$style.tags">
            <Tag v-for="type in paper.publication_types" :key="type" :value="PUB_TYPE_MAP[type]" />
          </div>
          <div :class="$style.footer">
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
          </div>
        </div>
      </template>
    </Card>
  </div>
</template>

<style scoped module>
.paper-row {
  display: flex;
  width: 100%;
  gap: 1rem;
  align-items: center;
}

.paperrowcard {
  width: 100%;
  border-radius: var(--p-card-border-radius);
  border: 1px solid var(--p-card-border);
  background: var(--p-card-background);
  cursor: pointer;
  transition: background var(--p-transition-duration);
}

.paperrowcard:hover {
  background: var(--p-card-hover-background);
}

.paperrowcard:active {
  background: var(--p-card-active-background);
}

.thumbnail {
  border-radius: var(--p-card-border-radius) 0 0 var(--p-card-border-radius);
  border-right: 1px solid var(--p-card-border);
  width: 10rem;
  flex-shrink: 0;
}

@media screen and (max-width: 900px) {
  .thumbnail {
    width: 10rem;
  }
}

@media screen and (max-width: 640px) {
  .thumbnail {
    display: none;
  }
}

.paper-details {
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 1rem;
  padding: 1rem;
}

.subtitle {
  color: var(--p-text-muted-color);
}

.tags {
  display: flex;
  gap: 0.5rem;
}

.footer {
  display: flex;
  margin-top: auto;
  justify-content: space-between;
}
</style>
