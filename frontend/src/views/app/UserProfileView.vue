<script setup lang="ts">
import { useUserStore } from "@/stores/user-store";
import { storeToRefs } from "pinia";
import Avatar from "primevue/avatar";
import Button from "primevue/button";
import Divider from "primevue/divider";
import { USER_TITLE_OPTIONS } from "@/api/mappings";
import EditableText from "@/components/EditableText.vue";
import { computed, nextTick, ref, useTemplateRef } from "vue";
import EditableSelect from "@/components/EditableSelect.vue";
import { hasChanged } from "@/utils";
import type { User } from "@/api/types";
import { useApi } from "@/api/use-api";
import routes from "@/api/routes";
import EditableUserRefs from "@/components/profile/EditableUserRefs.vue";
import { useThemeStore } from "@/stores/theme-store";
import EditableUserFields from "@/components/profile/EditableUserFields.vue";
import DeleteAccountButton from "@/components/profile/DeleteAccountButton.vue";

const userStore = useUserStore();
const { user } = storeToRefs(userStore);

const themeStore = useThemeStore();
const { isMobile } = storeToRefs(themeStore);

const updateData = ref<Partial<User>>({});

const dirty = computed(() => {
  if (!user.value) return false;
  return hasChanged(user.value, updateData.value);
});

const refsEl = useTemplateRef("refsEl");

const reset = () => {
  updateData.value = { title: user.value?.title, refs: { ...user.value!.refs } };
  refsEl.value?.reset();
};

const { loading, patch } = useApi(routes.users.patch.updateUser);

const save = async () => {
  if (!dirty.value) return;

  const response = await patch<User, Partial<User>>({
    data: updateData.value,
    successMessage: "User updated successfully",
  });

  if (!response?.data) return;
  user.value = response.data;
  nextTick(() => reset());
};
</script>

<template>
  <div v-if="user" class="user-profile">
    <div :class="isMobile ? 'avatar-wrapper-mobile' : 'avatar-wrapper'">
      <Avatar class="big-avatar" :label="user.first_name.charAt(0)" size="xlarge" />
      <div class="user-info">
        <EditableSelect
          tag="h4"
          :initial-option="user.title"
          :options="USER_TITLE_OPTIONS"
          v-model="updateData.title"
          fallback-text="No title set"
          placeholder="Select your Title..."
        />
        <div class="name-wrapper" :class="{ 'name-wrapper-mobile': isMobile }">
          <EditableText
            tag="h1"
            :initial-text="user.first_name"
            :max-width="isMobile ? '20rem' : undefined"
            v-model="updateData.first_name"
          />
          <EditableText
            tag="h1"
            :initial-text="user.last_name"
            :max-width="isMobile ? '20rem' : undefined"
            v-model="updateData.last_name"
          />
        </div>
        <EditableText
          tag="h3"
          :initial-text="user.affiliation"
          :max-width="isMobile ? '20rem' : undefined"
          fallback-text="No affiliation set"
          placeholder="Enter your Affiliation..."
          allow-empty
          v-model="updateData.affiliation"
        />
      </div>
    </div>
    <Divider v-if="isMobile" />
    <h2 style="margin-bottom: 1rem">Fields of Study</h2>
    <EditableUserFields :initial-values="user.fields" v-model="updateData.fields" />
    <Divider />
    <h2 style="margin-bottom: 1rem">Bio</h2>
    <EditableText
      tag="p"
      fallback-text="No bio set"
      placeholder="Enter your Bio..."
      :initial-text="user.bio"
      allow-empty
      v-model="updateData.bio"
      text-area
    />
    <Divider />
    <h2 style="margin-bottom: 1rem">References</h2>
    <EditableUserRefs ref="refsEl" :initial-values="user.refs" v-model="updateData.refs" />
    <div class="delete-account">
      <DeleteAccountButton />
    </div>
  </div>
  <div v-if="dirty" class="action-buttons">
    <Button label="Reset" icon="pi pi-undo" @click="reset" />
    <Button label="Save" icon="pi pi-save" :loading="loading" @click="save" />
  </div>
</template>

<style scoped>
.user-profile {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 40rem;
}

.avatar-wrapper {
  display: flex;
  gap: 2rem;
}

.avatar-wrapper-mobile {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.name-wrapper {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-bottom: 0.5rem;
}

.big-avatar {
  width: 7rem;
  height: 7rem;
  font-size: 5rem;
  margin-bottom: 1rem;
}

.action-buttons {
  position: fixed;
  bottom: 3rem;
  right: 3rem;
  display: flex;
  gap: 1rem;
}

.refs-container {
  display: grid;
  grid-template-columns: auto auto;
}

.delete-account {
  margin-top: 2rem;
  width: 100%;
}
</style>
