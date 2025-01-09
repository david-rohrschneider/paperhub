<script setup lang="ts">
import Dialog from "primevue/dialog";
import Button from "primevue/button";
import { ref } from "vue";

const {
  title,
  confirmLabel,
  loading,
  hideCancel = false,
} = defineProps<{
  title: string;
  confirmLabel: string;
  loading?: boolean;
  hideCancel?: boolean;
}>();

const emit = defineEmits(["confirm"]);

const visible = ref(false);

defineExpose({
  show: () => (visible.value = true),
});

const handleClick = () => {
  emit("confirm");
  visible.value = false;
};
</script>

<template>
  <Dialog
    v-model:visible="visible"
    modal
    dismissable-mask
    :header="title"
    :style="{ width: '100%', maxWidth: '50rem' }"
  >
    <p style="margin-bottom: 5rem">
      <slot />
    </p>
    <div class="actions">
      <Button v-if="!hideCancel" label="Cancel" severity="secondary" @click="visible = false" />
      <Button :loading="loading" :label="confirmLabel" @click="handleClick" />
    </div>
  </Dialog>
</template>

<style scoped>
.actions {
  display: flex;
  width: 100%;
  align-items: center;
  justify-content: flex-end;
  gap: 1rem;
}
</style>
