<script setup lang="ts">
import Button from "primevue/button";
import Drawer from "primevue/drawer";
import Avatar from "primevue/avatar";
import Skeleton from "primevue/skeleton";
import Divider from "primevue/divider";
import { ref } from "vue";
import { useUserStore } from "@/stores/user-store";
import { storeToRefs } from "pinia";
import MobileMenuLink from "./MobileMenuLink.vue";
import navbarLinks from "@/components/navbar/navbar-links";
import { useFirebaseAuth } from "vuefire";
import { signOut } from "firebase/auth";
import { useRouter } from "vue-router";

const open = ref(false);

const userStore = useUserStore();
const { user } = storeToRefs(userStore);

const auth = useFirebaseAuth()!;
const router = useRouter();
const logout = async () => {
  open.value = false;
  await signOut(auth);
  router.push("/auth/login");
};
</script>

<template>
  <Button variant="text" icon="pi pi-bars" @click="open = true" />
  <Drawer
    v-model:visible="open"
    position="right"
    :pt="{ root: { style: { transition: 'transform 0.2s' } } }"
  >
    <template #header>
      <div class="header">
        <Skeleton v-if="!user" size="3rem" />
        <Avatar v-else :label="user.first_name.charAt(0)" size="large" />
      </div>
    </template>
    <div class="content-wrapper">
      <div v-if="user">
        <h2>{{ user.first_name }} {{ user.last_name }}</h2>
        <small>{{ user.email }}</small>
      </div>
      <Divider />
      <div class="links-wrapper">
        <MobileMenuLink
          v-for="link in navbarLinks"
          :key="link.label"
          :icon="link.icon"
          :to="link.to"
          :label="link.label"
          @click="open = false"
        />
        <MobileMenuLink icon="pi pi-user" to="/profile" label="Profile" @click="open = false" />
        <MobileMenuLink icon="pi pi-thumbs-up" to="/likes" label="My Likes" @click="open = false" />
        <Button
          class="logout-button"
          icon="pi pi-sign-out"
          label="Logout"
          severity="secondary"
          @click="logout"
        />
      </div>
    </div>
  </Drawer>
</template>

<style scoped>
.header {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.content-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.links-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  flex-grow: 1;
}

.logout-button {
  margin-top: auto;
}
</style>
