<script setup lang="ts">
import routes from "@/api/routes";
import type { Paper, Library, Paginated } from "@/api/types";
import { useApi } from "@/api/use-api";
import { computed, onMounted, ref, useTemplateRef } from "vue";
import Tag from "primevue/tag";
import PaperFeed from "@/components/feed/PaperFeed.vue";
import Divider from "primevue/divider";
import ProgressSpinner from "primevue/progressspinner";
import Button from "primevue/button";
import { useThemeStore } from "@/stores/theme-store";
import RemovePapersButton from "@/components/libraries/RemovePapersButton.vue";
import ClearLibraryButton from "@/components/libraries/ClearLibraryButton.vue";
import MobileEditDial from "@/components/libraries/MobileEditDial.vue";
import LayoutSelect from "@/components/feed/LayoutSelect.vue";
import LibraryOptionsButton from "@/components/libraries/LibraryOptionsButton.vue";
import ToggleButton from "primevue/togglebutton";
import LibrarySettingsDialog from "@/components/libraries/LibrarySettingsDialog.vue";
import ConfirmDialog from "@/components/ConfirmDialog.vue";
import { useShare } from "@vueuse/core";
import { useCurrentUser } from "vuefire";
import { useRouter } from "vue-router";
import PageHeader from "@/components/PageHeader.vue";

const { libraryId, publicLibrary = false } = defineProps<{
  libraryId: string;
  publicLibrary?: boolean;
}>();

const { breakpoints } = useThemeStore();
const isMobile = breakpoints.smaller("tablet");

const libraryRoute = computed(() =>
  publicLibrary ? routes.libraries.get.publicLibrary : routes.libraries.get.userLibrary,
);
const { get, loading } = useApi(libraryRoute.value);
const library = ref<Library | null>(null);

const fetchLibrary = async () => {
  if (loading.value) return;
  const response = await get<Library>({ routeParams: [libraryId] });

  if (!response?.data) return;
  library.value = response.data;
};

const numPapersString = computed(() => {
  if (!library.value) return "";
  if (library.value.num_papers === 1) return "1 Paper";
  return `${library.value.num_papers} Papers`;
});

const layout = ref<"list" | "grid">("list");
const papers = ref<Paper[]>([]);
const LIMIT = 20;
const page = ref(-1);

const papersRoute = computed(() =>
  publicLibrary ? routes.libraries.get.publicLibraryPapers : routes.libraries.get.userLibraryPapers,
);

const { get: getPapers, loading: loadingPapers } = useApi(papersRoute.value);

const fetchPapers = async () => {
  if (loadingPapers.value) return;
  page.value++;

  const params = { offset: page.value * LIMIT, limit: LIMIT };
  const response = await getPapers<Paginated<Paper>>({
    routeParams: [libraryId],
    config: { params },
  });

  if (!response?.data) return;
  papers.value.push(...response.data.data);
};

const editing = ref(false);
const selectedPapers = ref<string[]>([]);
const settingsDialog = useTemplateRef("settingsDialog");

const toggleEditing = () => {
  editing.value = !editing.value;
  selectedPapers.value = [];
};

const handleClickSettings = () => settingsDialog.value?.show();

const firebaseUser = useCurrentUser();
const isUserLibrary = computed(() => firebaseUser.value?.uid === library.value?.user_id);

const { share, isSupported } = useShare();
const handleClickShare = () => {
  if (!isSupported.value) return;
  if (!library.value) return;
  if (library.value.private) return;

  const url = location.href.includes("?public") ? location.href : `${location.href}?public=true`;

  share({
    title: import.meta.env.VITE_APP_TITLE,
    text: `Check out my Library: ${library.value!.title}`,
    url,
  }).catch((error) => error);
};

const confirmDeleteDialog = useTemplateRef("confirmDeleteDialog");
const handleClickDelete = () => confirmDeleteDialog.value?.show();

const router = useRouter();
const { del, loading: loadingDelete } = useApi(routes.libraries.delete.deleteLibrary);
const deleteLibrary = async () => {
  if (!library.value) return;
  if (loadingDelete.value) return;
  await del({ routeParams: [library.value._id], successMessage: "Library deleted" });
  router.push("/libraries");
};

onMounted(() => {
  library.value = null;
  papers.value = [];
  page.value = -1;
  selectedPapers.value = [];
  editing.value = false;
  fetchLibrary();
  fetchPapers();
});
</script>

<template>
  <PageHeader
    style="flex-wrap: wrap"
    v-if="library"
    :title="library.title"
    :subtitle="`Showing ${papers.length} of ${library.num_papers} papers`"
  >
    <template #right>
      <div class="tags">
        <Tag
          :icon="library.private ? 'pi pi-lock' : 'pi pi-lock-open'"
          :value="library.private ? 'Private' : 'Public'"
        />
        <Tag icon="pi pi-book" :value="numPapersString" />
        <Tag v-if="library.default" style="margin-right: auto" value="Default" />

        <Button
          v-if="!isMobile && !library.private"
          variant="text"
          @click="handleClickShare"
          icon="pi pi-share-alt"
        />

        <LibraryOptionsButton
          v-if="!library.default && isUserLibrary && !isMobile"
          @settings="handleClickSettings"
          @delete="handleClickDelete"
        />
      </div>
    </template>
  </PageHeader>

  <Divider :style="{ margin: 0 }" />

  <div v-if="library && library.num_papers > 0" class="papers-header">
    <ToggleButton
      v-if="!isMobile && isUserLibrary"
      @value-change="toggleEditing"
      off-icon="pi pi-pencil"
      on-icon="pi pi-times"
      onLabel="Stop Editing"
      offLabel="Edit Papers"
    />

    <div class="papers-header-actions" v-if="editing">
      <RemovePapersButton
        v-model:papers="papers"
        v-model:selected-papers="selectedPapers"
        v-model:library="library"
      />
      <ClearLibraryButton
        v-model:papers="papers"
        v-model:selected-papers="selectedPapers"
        v-model:library="library"
      />
    </div>

    <p v-else></p>

    <LayoutSelect :style="{ height: '3rem', marginLeft: 'auto' }" v-model="layout" />
  </div>

  <PaperFeed
    v-if="library"
    :layout="layout"
    :papers="papers"
    :loading="loadingPapers"
    :more-available="papers.length < library.num_papers"
    :selectable="editing"
    v-model:selected-papers="selectedPapers"
    @load-more="fetchPapers"
  />

  <p v-if="library && !loadingPapers && papers.length === 0">No papers in this library</p>

  <MobileEditDial
    v-if="library && isMobile"
    :can-edit-papers="isUserLibrary && library.num_papers > 0"
    :can-edit-settings="!library.default && isUserLibrary"
    :is-private="library.private"
    @edit="toggleEditing"
    @settings="handleClickSettings"
    @delete="handleClickDelete"
    @share="handleClickShare"
  />
  <LibrarySettingsDialog
    v-if="library && !library.default && isUserLibrary"
    ref="settingsDialog"
    v-model="library"
  />
  <ConfirmDialog
    v-if="library && !library.default && isUserLibrary"
    ref="confirmDeleteDialog"
    title="Delete Library"
    confirm-label="Delete"
    :loading="loadingDelete"
    @confirm="deleteLibrary"
  >
    Are you sure you want to delete <b>{{ library.title }}</b
    >?
  </ConfirmDialog>
  <ProgressSpinner
    v-if="!library"
    style="width: 50px; height: 50px"
    strokeWidth="8"
    fill="transparent"
    animationDuration=".5s"
  />
</template>

<style scoped>
.library-header {
  display: flex;
  align-items: center;
  width: 100%;
  gap: 1rem;
  flex-wrap: wrap;
}

.tags {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.papers-header {
  display: flex;
  align-items: center;
  width: 100%;
  gap: 1rem;
}

.papers-header-actions {
  display: flex;
  gap: 1rem;
}
</style>
