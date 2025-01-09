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

const { patch, loading } = useApi(routes.libraries.patch.removePapers);
const deletePapers = async () => {
  if (loading.value) return;
  const response = await patch<Library, { paper_ids: string[] }>({
    routeParams: [library.value._id],
    data: { paper_ids: selectedPapers.value },
  });

  if (!response?.data) return;

  library.value = response.data;
  papers.value = papers.value.filter((paper) => !selectedPapers.value.includes(paper.id));
  selectedPapers.value = [];
};

const removeButtonLabel = computed(() => {
  const count = selectedPapers.value.length;
  if (isMobile.value) return `${count}`;
  return `${count} Paper${count !== 1 ? "s" : ""}`;
});
</script>

<template>
  <Button
    icon="pi pi-trash"
    :label="removeButtonLabel"
    :disabled="selectedPapers.length === 0"
    @click="openConfirmDialog"
  />
  <ConfirmDialog
    v-if="papers.length > 0"
    ref="confirmDialog"
    title="Remove Papers"
    confirm-label="Remove"
    :loading="loading"
    @confirm="deletePapers"
  >
    Are you sure you want to remove <b>{{ selectedPapers.length }}</b> paper{{
      selectedPapers.length !== 1 ? "s" : ""
    }}
    from your library?
  </ConfirmDialog>
</template>
