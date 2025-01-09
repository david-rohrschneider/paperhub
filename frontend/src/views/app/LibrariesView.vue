<script setup lang="ts">
import routes from "@/api/routes";
import type { Library, Paginated } from "@/api/types";
import { useApi } from "@/api/use-api";
import LibraryRow from "@/components/libraries/LibraryRow.vue";
import { onMounted, ref, useTemplateRef } from "vue";
import Button from "primevue/button";
import ProgressSpinner from "primevue/progressspinner";
import { useThemeStore } from "@/stores/theme-store";
import { useRouter } from "vue-router";
import CreateLibraryDialog from "@/components/libraries/CreateLibraryDialog.vue";
import PageHeader from "@/components/PageHeader.vue";

const { get, loading } = useApi(routes.libraries.get.userLibraries);
const LIMIT = 20;
const page = ref(-1);

const libraries = ref<Library[]>([]);
const total = ref(0);

const { breakpoints } = useThemeStore();
const isMobile = breakpoints.smaller("tablet");

const router = useRouter();
const handleClick = (library: Library) => {
  router.push(`/libraries/${library._id}`);
};

const createLibraryDialog = useTemplateRef("createLibraryDialog");
const handleClickCreate = () => createLibraryDialog.value?.show();

const fetchLibraries = async () => {
  if (loading.value) return;
  page.value++;

  const params = { limit: LIMIT, offset: page.value * LIMIT };
  const response = await get<Paginated<Library>>({ config: { params } });

  if (!response?.data) return;
  libraries.value.push(...response.data.data);
  total.value = response.data.total;
};

onMounted(fetchLibraries);
</script>

<template>
  <PageHeader title="Libraries" :subtitle="`Showing ${libraries.length} of ${total} Libraries`">
    <template #right>
      <Button
        v-if="!isMobile"
        @click="handleClickCreate"
        icon="pi pi-plus"
        label="Create Library"
      />
    </template>
  </PageHeader>

  <div class="libraries-list">
    <LibraryRow
      v-for="library in libraries"
      :key="library._id"
      :library="library"
      @click="() => handleClick(library)"
    />
    <ProgressSpinner
      v-if="loading"
      style="width: 50px; height: 50px"
      strokeWidth="8"
      fill="transparent"
      animationDuration=".5s"
    />
    <Button
      v-else-if="libraries.length > 0 && libraries.length < total"
      @click="fetchLibraries"
      label="Load More"
    />
  </div>

  <CreateLibraryDialog ref="createLibraryDialog" />
  <Button
    v-if="isMobile"
    class="mobile-create-button"
    @click="handleClickCreate"
    icon="pi pi-plus"
  />
</template>

<style scoped>
.libraries-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  align-self: center;
  width: 100%;
  gap: 1rem;
}

.mobile-create-button {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
}
</style>
