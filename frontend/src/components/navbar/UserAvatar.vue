<script setup lang="ts">
import Avatar from "primevue/avatar";
import Skeleton from "primevue/skeleton";
import Button from "primevue/button";
import UserMenu from "@/components/navbar/UserMenu.vue";
import { useTemplateRef } from "vue";
import { useUserStore } from "@/stores/user-store";
import { storeToRefs } from "pinia";

const menu = useTemplateRef("menu");

const userStore = useUserStore();
const { user } = storeToRefs(userStore);

const onClick = (e: MouseEvent) => menu.value?.toggle(e);
</script>

<template>
  <div v-if="!user" class="avatar-wrapper">
    <Skeleton size="3rem" />
  </div>
  <div v-else class="avatar-wrapper">
    <Button class="avatar-button" @click="onClick">
      <Avatar :label="user.first_name.charAt(0)" size="large" />
      <UserMenu ref="menu" :user="user" />
    </Button>
  </div>
</template>

<style scoped>
.avatar-button {
  padding: 0;
  border: none;
  background-color: transparent;

  .p-avatar {
    background: var(--p-button-text-primary-hover-background);
  }
}

.avatar-button:hover {
  padding: 0 !important;
  border: none !important;
  background-color: transparent !important;

  .p-avatar {
    background: var(--p-button-text-primary-active-background);
  }
}
</style>
