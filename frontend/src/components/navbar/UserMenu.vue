<script setup lang="ts">
import { ref, useTemplateRef } from "vue";
import Menu from "primevue/menu";
import type { User } from "@/api/types";
import type { MenuItem } from "primevue/menuitem";
import { signOut } from "firebase/auth";
import { useRouter } from "vue-router";
import { useFirebaseAuth } from "vuefire";

const { user } = defineProps<{
  user: User;
}>();

const menu = useTemplateRef("menu");
const auth = useFirebaseAuth()!;
const router = useRouter();

const logout = async () => {
  await signOut(auth);
  router.push("/auth/login");
};

const items = ref<MenuItem[]>([
  {
    label: () => `${user.first_name} ${user.last_name}`,
    items: [
      {
        label: "Profile",
        icon: "pi pi-user",
        command: () => router.push("/profile"),
      },
      {
        label: "My Likes",
        icon: "pi pi-thumbs-up",
        command: () => router.push("/likes"),
      },
      {
        label: "Logout",
        icon: "pi pi-sign-out",
        command: logout,
      },
    ],
  },
]);

defineExpose({
  toggle: (e: MouseEvent) => menu.value?.toggle(e),
});

const dt = {
  listPadding: "1rem",
  itemPadding: "0.5rem 1rem",
};
</script>

<template>
  <Menu ref="menu" :model="items" :dt="dt" popup />
</template>
