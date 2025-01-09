<script setup lang="ts">
import Dialog from "primevue/dialog";
import Button from "primevue/button";
import { ref } from "vue";
import { useApi } from "@/api/use-api";
import routes from "@/api/routes";
import { signOut } from "firebase/auth";
import { useFirebaseAuth } from "vuefire";
import { useRouter } from "vue-router";

const visible = ref(false);
const auth = useFirebaseAuth()!;
const router = useRouter();

const { del, loading } = useApi(routes.users.delete.deleteUser);

const deleteAccount = async () => {
  const response = await del({ successMessage: "Account deleted successfully." });
  if (!response) return;

  await signOut(auth);
  router.push("/auth/login");
};
</script>

<template>
  <Button variant="outlined" severity="danger" label="Delete Account" @click="visible = true" />
  <Dialog
    v-model:visible="visible"
    modal
    dismissable-mask
    header="Delete Account"
    :style="{ width: '100%', maxWidth: '50rem' }"
  >
    <p style="margin-bottom: 5rem">
      Are you sure you want to delete your account? This action cannot be undone.
    </p>
    <div class="actions">
      <Button
        variant="outlined"
        severity="danger"
        :loading="loading"
        label="Delete Account"
        @click="deleteAccount"
      />
      <Button label="Cancel" @click="visible = false" />
    </div>
  </Dialog>
</template>

<style scoped>
.actions {
  display: flex;
  width: 100%;
  justify-content: flex-end;
  gap: 1rem;
}
</style>
