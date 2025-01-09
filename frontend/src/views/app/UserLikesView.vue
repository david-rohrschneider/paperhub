<script setup lang="ts">
import routes from "@/api/routes";
import type { Paginated, Paper } from "@/api/types";
import { useApi } from "@/api/use-api";
import { useThemeStore } from "@/stores/theme-store";
import { onBeforeUnmount, onMounted, ref } from "vue";
import LayoutSelect from "@/components/feed/LayoutSelect.vue";
import PaperFeed from "@/components/feed/PaperFeed.vue";
import PageHeader from "@/components/PageHeader.vue";

const { breakpoints } = useThemeStore();
const isMobile = breakpoints.smaller("tablet");

const papers = ref<Paper[]>([]);
const total = ref(0);

const layout = ref<"list" | "grid">("list");

const LIMIT = 20;
const page = ref(-1);

const { get, loading, abort } = useApi(routes.likes.get.userLikes);

const loadMore = async () => {
  if (loading.value) return;
  page.value++;

  const params = { limit: LIMIT, offset: page.value * LIMIT };
  const response = await get<Paginated<Paper>>({ config: { params } });

  if (!response?.data) return;

  papers.value.push(...response.data.data);
  total.value = response.data.total;
};

onMounted(loadMore);
onBeforeUnmount(abort);
</script>

<template>
  <PageHeader
    title="My Likes"
    :subtitle="`${isMobile ? '' : 'Showing'} ${papers.length} of ${total} papers`"
  >
    <template #right><LayoutSelect v-if="papers.length > 0" v-model="layout" /></template>
  </PageHeader>

  <p v-if="!loading && papers.length === 0">No papers liked yet</p>

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
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  width: 100%;
}
</style>
