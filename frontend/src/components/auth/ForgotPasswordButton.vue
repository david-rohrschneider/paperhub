<script setup lang="ts">
import routes from "@/api/routes";
import { useApi } from "@/api/use-api";
import type { FormSubmitEvent } from "@primevue/forms";
import { zodResolver } from "@primevue/forms/resolvers/zod";
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import InputGroup from "primevue/inputgroup";
import InputGroupAddon from "primevue/inputgroupaddon";
import InputText from "primevue/inputtext";
import Message from "primevue/message";
import { Form } from "@primevue/forms";
import { ref } from "vue";
import { z } from "zod";

const visible = ref(false);

const initialValues = ref({
  email: "",
});

const resolver = zodResolver(
  z.object({
    email: z.string().email(),
  }),
);

const { post, loading } = useApi(routes.users.post.requestPasswordResetEmail, true);

const onFormSubmit = async (event: FormSubmitEvent) => {
  if (loading.value) return;
  const v = event.values;
  if (!v.email) return;

  await post({ data: v, successMessage: "Password reset email sent." });
};
</script>

<template>
  <Button style="padding: 0" variant="link" label="Forgot Password?" />
  <Dialog
    v-model:visible="visible"
    modal
    dismissable-mask
    header="Reset Password"
    :style="{ width: '100%', maxWidth: '25rem' }"
  >
    <Form
      class="form"
      :initial-values="initialValues"
      :resolver="resolver"
      validate-on-blur
      validate-on-submit
      @submit="onFormSubmit"
      v-slot="$form"
    >
      <p>
        If you forgot your password and want to set a new one, please enter your email below and
        request a password reset link.
      </p>

      <InputGroup>
        <InputGroupAddon>
          <i class="pi pi-at"></i>
        </InputGroupAddon>
        <FloatLabel variant="on">
          <InputText name="email" />
          <label for="email">E-Mail</label>
        </FloatLabel>
      </InputGroup>
      <Message v-if="$form.email?.invalid" severity="error" size="small" variant="simple">
        {{ $form.email.error.message }}
      </Message>

      <div class="actions">
        <Button label="Cancel" severity="secondary" @click="visible = false" />
        <Button
          :disabled="!$form.valid || $form.email?.pristine"
          :loading="loading"
          fluid
          label="Submit"
          type="submit"
        />
      </div>
    </Form>
  </Dialog>
</template>

<style scoped>
.form {
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 1rem;
}

.actions {
  display: flex;
  width: 100%;
  gap: 1rem;
  justify-content: flex-end;
}
</style>
