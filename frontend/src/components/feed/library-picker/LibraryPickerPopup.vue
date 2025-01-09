<script setup lang="ts">
import routes from "@/api/routes";
import type { Paper, Library, Paginated } from "@/api/types";
import { useApi } from "@/api/use-api";
import Popover from "primevue/popover";
import { ref, useTemplateRef } from "vue";
import LibraryPickerRow from "@/components/feed/library-picker/LibraryPickerRow.vue";
import Button from "primevue/button";
import ProgressSpinner from "primevue/progressspinner";

const { paper } = defineProps<{ paper: Paper }>();

const menu = useTemplateRef("menu");
const toggle = (e: Event) => menu.value?.toggle(e);

defineExpose({ toggle });
const emit = defineEmits<{
  add: [libraryId: string, event: MouseEvent];
}>();

const { get, loading } = useApi(routes.libraries.get.userLibraries);
const LIMIT = 20;
const page = ref(-1);

const libraries = ref<Library[]>([]);
const total = ref(0);

const fetchLibraries = async () => {
  if (loading.value) return;
  page.value++;

  const params = { limit: LIMIT, offset: page.value * LIMIT, contains_paper: paper.id };
  const response = await get<Paginated<Library>>({ config: { params } });

  if (!response?.data) return;
  libraries.value.push(...response.data.data);
  total.value = response.data.total;
};

const clickLibraryRow = (e: MouseEvent, library: Library) => {
  if (library.contains_paper) return;
  emit("add", library._id, e);
};

const onShow = () => {
  page.value = -1;
  libraries.value = [];
  total.value = 0;
  fetchLibraries();
};
</script>

<template>
  <Popover
    :pt="{ content: { style: { padding: '1.5rem' } } }"
    ref="menu"
    :style="{ width: '100%', maxWidth: '30rem', zIndex: 1004 }"
    @show="onShow"
  >
    <h2 style="margin-bottom: 2rem">Add to Library</h2>
    <div class="libraries-list">
      <LibraryPickerRow
        v-for="library in libraries"
        :key="library._id"
        :library="library"
        @click="(e) => clickLibraryRow(e, library)"
      />
      <div class="load-more">
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
    </div>
  </Popover>
</template>

<style scoped>
.libraries-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  height: 15rem;
  overflow-y: auto;
}

.load-more {
  display: flex;
  width: 100%;
  justify-content: center;
}
</style>
