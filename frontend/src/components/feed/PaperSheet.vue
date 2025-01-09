<script setup lang="ts">
import Chip from "primevue/chip";
import Button from "primevue/button";
import SplitButton from "primevue/splitbutton";
import Tag from "primevue/tag";
import type { Paper } from "@/api/types";
import { getExternalLinks, PUB_TYPE_MAP } from "@/api/mappings";
import { computed, useTemplateRef } from "vue";
import BottomSheet from "@/components/BottomSheet.vue";
import PaperLikeButton from "@/components/feed/PaperLikeButton.vue";
import LibraryPickerButton from "@/components/feed/library-picker/LibraryPickerButton.vue";

const { paper } = defineProps<{ paper: Paper }>();

const sheet = useTemplateRef("sheet");
const show = () => sheet.value?.open();

defineExpose({ show });

const links = computed(() => getExternalLinks(paper));
const menuItems = computed(() => links.value.slice(1));
const onClickMenuButton = () => window.open(links.value[0].url, "_blank");
</script>

<template>
  <BottomSheet ref="sheet" :transition-duration="0.3">
    <div class="content-wrapper">
      <h3>{{ paper.title }}</h3>
      <div class="type-date">
        <Tag v-for="type in paper.publication_types" :key="type" :value="PUB_TYPE_MAP[type]" />
        <p v-if="paper.published_at" style="margin-left: auto">
          {{ new Date(paper.published_at).toLocaleDateString() }}
        </p>
      </div>
      <div class="authors">
        <Chip class="chip-mobile" v-for="author in paper.authors" :key="author">
          <small style="white-space: nowrap">
            {{ author }}
          </small>
        </Chip>
      </div>
      <p class="abstract">{{ paper.abstract || "No abstract available." }}</p>
    </div>

    <template #footer>
      <div class="footer">
        <Button
          v-if="links.length === 1"
          as="a"
          target="_blank"
          rel="noopener noreferrer"
          :icon="links[0].icon"
          :severity="links[0].severity"
          :key="links[0].label"
          :label="links[0].label"
          :href="links[0].url"
        />
        <SplitButton v-else-if="links.length > 1" :model="menuItems" @click="onClickMenuButton">
          <span :class="links[0].icon" />
          <span>{{ links[0].label }}</span>
          <template #item="{ item, props }">
            <a
              as="a"
              target="_blank"
              rel="noopener noreferrer"
              v-bind="props.action"
              :href="item.url"
            >
              <span :class="item.icon" />
              <span>{{ item.label }}</span>
            </a>
          </template>
        </SplitButton>

        <div class="actions">
          <PaperLikeButton :paper="paper" />
          <LibraryPickerButton :paper="paper" />
        </div>
      </div>
    </template>
  </BottomSheet>
</template>

<style scoped>
.content-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 0 1rem 1rem 1rem;
}

.footer {
  display: flex;
  width: 100%;
  padding: 1rem;
  align-items: center;
  justify-content: space-between;
}

.actions {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-left: auto;
}

.type-date {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.thumbnail {
  width: 20rem;
  border-radius: var(--p-card-border-radius);
  border: 1px solid var(--p-inputtext-border-color);
}

.authors {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.chip-mobile {
  font-size: 0.8rem;
  padding: 0.25rem 0.5rem;
}

.abstract {
  text-align: justify;
  color: var(--p-dialog-maintext-color);
}
</style>
