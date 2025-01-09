<script setup lang="ts">
import Button from "primevue/button";
import type { Paper } from "@/api/types";
import { useApi } from "@/api/use-api";
import routes from "@/api/routes";
import { computed, ref } from "vue";

const { paper } = defineProps<{ paper: Paper }>();
const { post, loading: loadingLike } = useApi(routes.likes.post.createLike);
const { del, loading: loadingDelete } = useApi(routes.likes.delete.deleteLikeByPaper);

const liked = ref(false);
const likes = computed(() => (liked.value ? paper.likes + 1 : paper.likes));

const like = async () => {
  const response = await post({ routeParams: [paper.id], data: null, successMessage: "Liked!" });
  if (!response) return;
  liked.value = true;
};

const unlike = async () => {
  const response = await del({ routeParams: [paper.id], successMessage: "Unliked!" });
  if (!response) return;
  liked.value = false;
};

const handleClick = async () => {
  if (liked.value) {
    await unlike();
    return;
  }

  await like();
};
</script>

<template>
  <Button
    icon="pi pi-thumbs-up"
    :variant="liked ? undefined : 'outlined'"
    :label="`${likes}`"
    :loading="loadingLike || loadingDelete"
    @click="handleClick"
  />
</template>
