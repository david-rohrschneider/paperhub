<script setup lang="ts">
import Dialog from "primevue/dialog";
import Button from "primevue/button";
import InputText from "primevue/inputtext";
import Message from "primevue/message";
import FloatLabel from "primevue/floatlabel";
import SelectButton from "primevue/selectbutton";
import { Form } from "@primevue/forms";
import { reactive, ref } from "vue";
import type { CreateLibraryBody, Library } from "@/api/types";
import { useApi } from "@/api/use-api";
import routes from "@/api/routes";
import type { FormSubmitEvent } from "@primevue/forms";
import { zodResolver } from "@primevue/forms/resolvers/zod";
import { z } from "zod";
import { useRouter } from "vue-router";

const visible = ref(false);

const initialValues = reactive({ title: "", private: true });

const resolver = ref(
  zodResolver(
    z.object({
      title: z
        .string()
        .min(1, "Title is required")
        .max(60, "Title must be less than 60 characters"),
      private: z.boolean(),
    }),
  ),
);

const privateOptions = [
  { label: "Public", value: false, icon: "pi pi-lock-open" },
  { label: "Private", value: true, icon: "pi pi-lock" },
];

defineExpose({
  show: () => (visible.value = true),
});

const router = useRouter();

const { post, loading } = useApi(routes.libraries.post.createLibrary);

const createLibrary = async (e: FormSubmitEvent) => {
  if (loading.value) return;

  const response = await post<Library, CreateLibraryBody>({
    data: { title: e.values.title, private: e.values.private },
    successMessage: "Library created successfully",
  });

  if (!response?.data) return;

  visible.value = false;
  router.push(`/libraries/${response.data._id}`);
};
</script>

<template>
  <Dialog
    v-model:visible="visible"
    modal
    dismissable-mask
    header="Create New Library"
    :style="{ width: '100%', maxWidth: '30rem' }"
  >
    <Form
      v-slot="$form"
      :initialValues="initialValues"
      :resolver="resolver"
      validateOnValueUpdate
      @submit="createLibrary"
      class="form"
    >
      <div class="form-field">
        <FloatLabel variant="on">
          <InputText name="title" type="text" fluid />
          <label for="title">Library Title</label>
        </FloatLabel>
        <Message v-if="$form.title?.invalid" severity="error" size="small" variant="simple">
          {{ $form.title.error.message }}
        </Message>
      </div>

      <SelectButton
        name="private"
        :options="privateOptions"
        option-label="label"
        option-value="value"
      >
        <template #option="slotProps">
          <span style="display: flex; align-items: center; gap: 0.5rem">
            <i :class="slotProps.option.icon" />
            {{ slotProps.option.label }}
          </span>
        </template>
      </SelectButton>

      <div class="actions">
        <Button severity="secondary" label="Cancel" @click="visible = false" />
        <Button
          :disabled="!$form.valid || $form.title?.pristine"
          :loading="loading"
          type="submit"
          label="Create Library"
        />
      </div>
    </Form>
  </Dialog>
</template>

<style scoped>
.form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.actions {
  display: flex;
  width: 100%;
  align-items: center;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}
</style>
