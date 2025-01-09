<script setup lang="ts">
import type { Paper } from "@/api/types";
import thumbnailFallback from "@/assets/images/thumbnail-fallback.jpg";
import iconLocked from "@/assets/images/icon-locked.svg";
import iconFallback from "@/assets/images/icon-fallback.svg";

const { paper } = defineProps<{ paper: Paper }>();

const thumbnailUrl = paper.thumbnail_url || thumbnailFallback;
const iconUrl = !paper.open_pdf_url ? iconLocked : !paper.thumbnail_url ? iconFallback : null;
</script>

<template>
  <div class="container">
    <img class="thumbnail" :src="thumbnailUrl" alt="Thumbnail" />
    <img v-if="iconUrl" :src="iconUrl" alt="Thumbnail Icon" class="thumbnail-icon" />
  </div>
</template>

<style scoped>
.container {
  position: relative;
  overflow: hidden;
  display: inline-block;
}

.thumbnail {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: top;
}

.thumbnail-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 5rem;
  height: 5rem;
}
</style>
