<script setup lang="ts">
import routes from "@/api/routes";
import type { Paginated, Paper, PaperSearchBody } from "@/api/types";
import { useApi } from "@/api/use-api";
import AdvancedSearchPanel from "@/components/search/AdvancedSearchPanel.vue";
import LayoutSelect from "@/components/feed/LayoutSelect.vue";
import PaperFeed from "@/components/feed/PaperFeed.vue";
import { ref } from "vue";
import { useThemeStore } from "@/stores/theme-store";

const { breakpoints } = useThemeStore();
const isMobile = breakpoints.smaller("tablet");

const layout = ref<"list" | "grid">("list");
const papers = ref<Paper[]>([]);
const total = ref(0);
const { post, loading } = useApi(routes.papers.post.search);

const LIMIT = 20;
const page = ref(0);
const lastRequestBody = ref<PaperSearchBody | null>(null);

const submit = async (body: PaperSearchBody) => {
  if (loading.value) return;

  lastRequestBody.value = body;
  page.value = 0;
  papers.value = [];
  total.value = 0;

  const params = { limit: LIMIT, offset: page.value * LIMIT };
  const response = await post<Paginated<Paper>, PaperSearchBody>({
    data: body,
    config: { params },
  });

  if (!response?.data) return;
  papers.value = response.data.data;
  total.value = response.data.total;
};

const loadMore = async () => {
  if (loading.value || !lastRequestBody.value) return;
  page.value++;

  const params = { limit: LIMIT, offset: page.value * LIMIT };
  const response = await post<Paginated<Paper>, PaperSearchBody>({
    data: lastRequestBody.value,
    config: { params },
  });

  if (!response?.data) return;
  papers.value.push(...response.data.data);
};
</script>

<template>
  <AdvancedSearchPanel @submit="submit" />

  <div v-if="papers.length > 0" class="papers-header">
    <p>{{ isMobile ? "" : "Showing" }} {{ papers.length }} of {{ total }} results</p>
    <LayoutSelect v-model="layout" />
  </div>

  <p v-else-if="!loading && lastRequestBody">No papers found</p>

  <PaperFeed
    :layout="layout"
    :papers="papers"
    :loading="loading"
    :more-available="papers.length < total"
    @load-more="loadMore"
  />
</template>

<style scoped>
.papers-header {
  display: flex;
  gap: 1rem;
  align-items: center;
  width: 100%;
  justify-content: space-between;
}
</style>
