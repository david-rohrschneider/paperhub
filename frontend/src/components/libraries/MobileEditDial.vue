<script setup lang="ts">
import { computed, ref } from "vue";
import SpeedDial from "primevue/speeddial";
import Button from "primevue/button";
import Tag from "primevue/tag";

const { isPrivate, canEditPapers, canEditSettings } = defineProps<{
  isPrivate: boolean;
  canEditPapers: boolean;
  canEditSettings: boolean;
}>();
const emit = defineEmits(["edit", "settings", "delete", "share"]);

const items = computed(() => {
  const actions = [];

  if (canEditPapers) {
    actions.push({
      label: "Edit Papers",
      icon: "pi pi-pencil",
      command: () => emit("edit"),
    });
  }

  if (canEditSettings) {
    actions.push({
      label: "Settings",
      icon: "pi pi-cog",
      command: () => emit("settings"),
    });

    actions.push({
      label: "Delete Library",
      icon: "pi pi-trash",
      command: () => emit("delete"),
    });
  }

  if (!isPrivate) {
    actions.push({
      label: "Share",
      icon: "pi pi-share-alt",
      command: () => emit("share"),
    });
  }

  return actions;
});

const maskVisible = ref(false);

const callbackWithMask = (event: Event, cb: (e: Event) => void, mask: boolean) => {
  maskVisible.value = mask;
  cb(event);
};
</script>

<template>
  <Transition name="mask">
    <div class="mask" v-if="maskVisible" @click="maskVisible = false" />
  </Transition>
  <SpeedDial
    v-if="items.length > 0"
    :model="items"
    :style="{ position: 'fixed', right: '2rem', bottom: '2rem', zIndex: 1002 }"
    direction="up"
  >
    <template #button="{ toggleCallback }">
      <Button
        icon="pi pi-ellipsis-v"
        @click="(e) => callbackWithMask(e, toggleCallback, !maskVisible)"
      />
    </template>
    <template #item="{ item, toggleCallback }">
      <div style="position: relative">
        <Tag severity="secondary" class="item-label" :value="item.label" />
        <Button
          @click="(e) => callbackWithMask(e, toggleCallback, false)"
          :icon="item.icon"
          rounded
          severity="secondary"
        />
      </div>
    </template>
  </SpeedDial>
</template>

<style scoped>
.mask {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: var(--p-mask-background);
  z-index: 1001;
}

.item-label {
  position: absolute;
  white-space: nowrap;
  top: 50%;
  left: -0.5rem;
  transform: translate(-100%, -50%);
}

.mask-enter-active,
.mask-leave-active {
  transition: opacity var(--p-transition-duration);
}

.mask-enter-from,
.mask-leave-to {
  opacity: 0;
}
</style>
