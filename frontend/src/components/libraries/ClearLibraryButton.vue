<script setup lang="ts">
import routes from "@/api/routes";
import type { Library, Paper } from "@/api/types";
import { useApi } from "@/api/use-api";
import { useThemeStore } from "@/stores/theme-store";
import { computed, useTemplateRef } from "vue";
import Button from "primevue/button";
import ConfirmDialog from "@/components/ConfirmDialog.vue";

const selectedPapers = defineModel<string[]>("selectedPapers", { required: true });
const library = defineModel<Library>("library", { required: true });
const papers = defineModel<Paper[]>("papers", { required: true });

const { breakpoints } = useThemeStore();
const isMobile = breakpoints.smaller("tablet");

const confirmDialog = useTemplateRef("confirmDialog");
const openConfirmDialog = () => confirmDialog.value?.show();

const { patch, loading } = useApi(routes.libraries.patch.clearLibrary);
const clearLibrary = async () => {
  if (loading.value) return;
  const response = await patch<Library>({
    routeParams: [library.value._id],
    data: null,
  });

  if (!response?.data) return;

  library.value = response.data;
  papers.value = [];
  selectedPapers.value = [];
};

const clearButtonLabel = computed(() => {
  if (isMobile.value) return "Clear";
  return "Clear Library";
});
</script>

<template>
  <Button :label="clearButtonLabel" @click="openConfirmDialog" />
  <ConfirmDialog
    ref="confirmDialog"
    title="Clear Library"
    confirm-label="Clear"
    :loading="loading"
    @confirm="clearLibrary"
  >
    Are you sure you want to remove <b>all</b> papers from your library?
  </ConfirmDialog>
</template>
