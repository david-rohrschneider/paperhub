<script setup lang="ts">
import PaperFeed from "@/components/feed/PaperFeed.vue";
import { onBeforeUnmount, onMounted, ref } from "vue";
import { useApi } from "@/api/use-api";
import routes from "@/api/routes";
import type { Paper } from "@/api/types";
import LayoutSelect from "@/components/feed/LayoutSelect.vue";
import PageHeader from "@/components/PageHeader.vue";

const layout = ref<"list" | "grid">("grid");

const { get, loading, abort } = useApi(routes.papers.get.userFeed);

const papers = ref<Paper[]>([]);

const LIMIT = 20;
const page = ref(-1);

const fetchPapers = async () => {
  page.value++;
  const params = { offset: page.value * LIMIT, limit: LIMIT };
  const response = await get<Paper[]>({ config: { params } });
  if (!response?.data) return;
  papers.value.push(...response.data);
};

onMounted(fetchPapers);
onBeforeUnmount(abort);
</script>

<template>
  <PageHeader title="My Feed" :subtitle="`Showing ${papers.length} Papers`">
    <template #right>
      <LayoutSelect v-model="layout" />
    </template>
  </PageHeader>
  <PaperFeed
    :layout="layout"
    :papers="papers"
    :loading="loading"
    :moreAvailable="true"
    @load-more="fetchPapers"
  />
</template>
