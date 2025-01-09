<script setup lang="ts">
import Button from "primevue/button";
import ProgressSpinner from "primevue/progressspinner";
import type { Paper } from "@/api/types";
import PaperCard from "@/components/feed/PaperCard.vue";
import PaperRow from "@/components/feed/PaperRow.vue";
import PaperDialog from "@/components/feed/PaperDialog.vue";
import PaperCardDialogMobile from "@/components/feed/PaperSheet.vue";
import { ref, useTemplateRef } from "vue";
import { useThemeStore } from "@/stores/theme-store";
import { storeToRefs } from "pinia";

const {
  layout,
  papers,
  loading,
  moreAvailable,
  selectable = false,
} = defineProps<{
  layout: "list" | "grid";
  papers: Paper[];
  loading: boolean;
  moreAvailable: boolean;
  selectable?: boolean;
}>();

const emit = defineEmits(["load-more"]);
const selectedPapers = defineModel<string[]>("selected-papers", { default: [] });

const themeStore = useThemeStore();
const { isMobile } = storeToRefs(themeStore);

const dialogPaperIndex = ref(0);

const dialog = useTemplateRef("dialog");

const handleClick = (index: number) => {
  if (!selectable) {
    dialogPaperIndex.value = index;
    dialog.value?.show();
    return;
  }

  const paperId = papers[index].id;
  const idx = selectedPapers.value.indexOf(paperId);

  if (idx === -1) {
    selectedPapers.value.push(paperId);
    return;
  }

  selectedPapers.value.splice(idx, 1);
};
</script>

<template>
  <div v-if="layout === 'grid'" class="paper-feed-grid">
    <PaperCard
      v-for="(paper, index) in papers"
      :key="paper.id"
      :paper="paper"
      :selectable="selectable"
      v-model:selected-papers="selectedPapers"
      @click="handleClick(index)"
    />
    <div v-if="loading" class="load-more">
      <ProgressSpinner
        style="width: 50px; height: 50px"
        strokeWidth="8"
        fill="transparent"
        animationDuration=".5s"
      />
    </div>
    <div v-else-if="moreAvailable" class="load-more">
      <Button @click="emit('load-more')" label="Load More" />
    </div>
  </div>

  <div v-else class="paper-feed-list">
    <PaperRow
      v-for="(paper, index) in papers"
      :key="paper.id"
      :paper="paper"
      :selectable="selectable"
      v-model:selected-papers="selectedPapers"
      @click="handleClick(index)"
    />
    <div v-if="loading" class="load-more">
      <ProgressSpinner
        style="width: 50px; height: 50px"
        strokeWidth="8"
        fill="transparent"
        animationDuration=".5s"
      />
    </div>
    <div v-else-if="moreAvailable" class="load-more">
      <Button @click="emit('load-more')" label="Load More" />
    </div>
  </div>

  <PaperDialog
    v-if="!isMobile && papers.length > 0"
    ref="dialog"
    :paper="papers[dialogPaperIndex]"
    :previousAvailable="dialogPaperIndex > 0"
    :nextAvailable="dialogPaperIndex < papers.length - 1"
    @previous="dialogPaperIndex--"
    @next="dialogPaperIndex++"
  />
  <PaperCardDialogMobile
    v-else-if="isMobile && papers.length > 0"
    ref="dialog"
    :paper="papers[dialogPaperIndex]"
  />
</template>

<style scoped>
.paper-feed-grid {
  width: 100%;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.paper-feed-list {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.load-more {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
