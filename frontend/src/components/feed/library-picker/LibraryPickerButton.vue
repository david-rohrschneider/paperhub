<script setup lang="ts">
import Button from "primevue/button";
import { useThemeStore } from "@/stores/theme-store";
import { useApi } from "@/api/use-api";
import routes from "@/api/routes";
import LibraryPickerPopup from "@/components/feed/library-picker/LibraryPickerPopup.vue";
import { useTemplateRef } from "vue";
import type { Paper } from "@/api/types";

const { paper } = defineProps<{ paper: Paper }>();

const { breakpoints } = useThemeStore();
const isTablet = breakpoints.smaller("desktop");

const dialog = useTemplateRef("dialog");

const { post, loading } = useApi(routes.libraries.post.addPapers);
const add = async (libraryId: string, event: MouseEvent) => {
  if (loading.value) return;
  dialog.value?.toggle(event);
  await post({
    routeParams: [libraryId],
    data: { paper_ids: [paper.id] },
    successMessage: "Paper added to library",
  });
};
</script>

<template>
  <Button
    variant="outlined"
    icon="pi pi-bookmark"
    :label="isTablet ? undefined : 'Add to Library'"
    :loading="loading"
    @click="dialog?.toggle"
  />
  <LibraryPickerPopup ref="dialog" :paper="paper" @add="add" />
</template>
