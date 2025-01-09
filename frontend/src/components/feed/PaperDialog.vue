<script setup lang="ts">
import Dialog from "primevue/dialog";
import Chip from "primevue/chip";
import Button from "primevue/button";
import SplitButton from "primevue/splitbutton";
import Tag from "primevue/tag";
import type { Paper } from "@/api/types";
import { getExternalLinks, PUB_TYPE_MAP } from "@/api/mappings";
import { computed, ref } from "vue";
import { useClipboard } from "@vueuse/core";
import { useToast } from "primevue";
import { useThemeStore } from "@/stores/theme-store";
import PaperThumbnail from "@/components/feed/PaperThumbnail.vue";
import PaperLikeButton from "@/components/feed/PaperLikeButton.vue";
import LibraryPickerButton from "@/components/feed/library-picker/LibraryPickerButton.vue";

const { paper, previousAvailable, nextAvailable } = defineProps<{
  paper: Paper;
  previousAvailable: boolean;
  nextAvailable: boolean;
}>();
const { breakpoints } = useThemeStore();
const isTablet = breakpoints.smaller("desktop");

const visible = ref(false);
const show = () => (visible.value = true);

const toast = useToast();
const emit = defineEmits(["previous", "next"]);

const bibtexDialogVisible = ref(false);
const bibtex = computed(() => paper.bibtex || "");
const { copy, copied } = useClipboard({ source: bibtex });
const copyBibtex = () => {
  copy(bibtex.value);
  toast.add({ severity: "success", summary: "Copied to clipboard", life: 3000 });
};

defineExpose({ show });

const pt = computed(() => ({
  root: { style: { maxWidth: "70rem", width: "100%" } },
  mask: { style: { padding: "0 2rem", zIndex: 1003 } },
  header: { style: { padding: isTablet ? "2rem 1rem 1rem 2rem" : "2rem", gap: "1rem" } },
  headeractions: { style: { alignSelf: "flex-start" } },
  content: { style: { padding: "0 2rem 0 2rem" } },
  footer: { style: { padding: "2rem", justifyContent: "space-between", gap: "1rem" } },
}));

const links = computed(() => getExternalLinks(paper));
const mobileMenuLinks = computed(() => links.value.slice(1));
const onClickMobileMenuButton = () => window.open(links.value[0].url, "_blank");
</script>

<template>
  <Dialog
    v-model:visible="visible"
    modal
    :pt="pt"
    :auto-z-index="false"
    :draggable="false"
    :dismissable-mask="true"
  >
    <template #header>
      <component :is="isTablet ? 'h3' : 'h2'">{{ paper.title }}</component>
    </template>
    <div class="content-wrapper">
      <PaperThumbnail v-if="!isTablet" class="thumbnail" :paper="paper" />
      <div class="paper-details">
        <div class="type-date">
          <Tag v-for="type in paper.publication_types" :key="type" :value="PUB_TYPE_MAP[type]" />
          <p v-if="paper.published_at" style="margin-left: auto">
            {{ new Date(paper.published_at).toLocaleDateString() }}
          </p>
        </div>
        <div class="authors">
          <Chip :class="{ 'chip-mobile': isTablet }" v-for="author in paper.authors" :key="author">
            <small style="white-space: nowrap">
              {{ author }}
            </small>
          </Chip>
        </div>
        <p class="abstract">{{ paper.abstract || "No abstract available." }}</p>
      </div>
    </div>
    <Button
      v-if="previousAvailable"
      size="large"
      rounded
      icon="pi pi-angle-left"
      class="previous-button"
      @click="emit('previous')"
    />
    <Button
      v-if="nextAvailable"
      size="large"
      rounded
      icon="pi pi-angle-right"
      class="next-button"
      @click="emit('next')"
    />
    <template #footer>
      <div v-if="!isTablet || links.length === 1" class="links">
        <Button
          as="a"
          target="_blank"
          rel="noopener noreferrer"
          v-for="link in links"
          :icon="link.icon"
          :severity="link.severity"
          :key="link.label"
          :label="link.label"
          :href="link.url"
        />
      </div>
      <SplitButton
        v-else-if="isTablet && links.length > 1"
        :model="mobileMenuLinks"
        @click="onClickMobileMenuButton"
      >
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
        <Button
          v-if="bibtex && !isTablet"
          variant="outlined"
          icon="pi pi-code"
          label="Show BibTeX"
          @click="bibtexDialogVisible = true"
        />
        <PaperLikeButton :paper="paper" />
        <LibraryPickerButton :paper="paper" />
      </div>
    </template>
  </Dialog>
  <Dialog
    v-model:visible="bibtexDialogVisible"
    header="BibTeX"
    modal
    :draggable="false"
    :dismissable-mask="true"
    :style="{ maxWidth: '40rem' }"
  >
    <pre class="bibtex">{{ bibtex }}</pre>
    <template #footer>
      <Button
        :disabled="copied"
        :icon="copied ? 'pi pi-check-circle' : 'pi pi-clipboard'"
        :label="copied ? 'Copied to Clipboard' : 'Copy to Clipboard'"
        @click="copyBibtex"
      />
    </template>
  </Dialog>
</template>

<style scoped>
.content-wrapper {
  display: flex;
  align-items: flex-start;
  gap: 2rem;
}

@media screen and (max-width: 768px) {
  .content-wrapper {
    flex-direction: column;
    gap: 1rem;
  }
}

.links {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.actions {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin-left: auto;
}

.paper-details {
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 1rem;
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

.bibtex {
  overflow-x: auto;
  font-size: 0.9rem;
  padding: 1rem;
  background-color: var(--p-secondary-color);
  border-radius: 0.5rem;
}

.previous-button {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translate(-50%, -50%);
}

.next-button {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translate(50%, -50%);
}
</style>
