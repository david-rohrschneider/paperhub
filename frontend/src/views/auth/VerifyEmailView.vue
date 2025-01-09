<script setup lang="ts">
import routes from "@/api/routes";
import { useApi } from "@/api/use-api";
import Message from "primevue/message";
import Button from "primevue/button";
import InputText from "primevue/inputtext";
import InputGroup from "primevue/inputgroup";
import InputGroupAddon from "primevue/inputgroupaddon";
import FloatLabel from "primevue/floatlabel";
import { Form, type FormSubmitEvent } from "@primevue/forms";
import { ref } from "vue";
import { zodResolver } from "@primevue/forms/resolvers/zod";
import { z } from "zod";

const disabled = ref(false);

const initialValues = ref({
  email: "",
});

const resolver = zodResolver(
  z.object({
    email: z.string().email(),
  }),
);

const { post, loading } = useApi(routes.users.post.requestVerificationEmail, true);
const onFormSubmit = async (event: FormSubmitEvent) => {
  if (loading.value) return;
  if (!event.values?.email) return;

  const data = { email: event.values.email };
  await post({ data, successMessage: "Verification email sent successfully." });

  disabled.value = true;
  setTimeout(() => (disabled.value = false), 10_000);
};
</script>

<template>
  <Message severity="secondary">
    Your account has been created successfully. To sign in, please verify your email address by
    clicking the link in the email we sent you. If you did not receive an email, you can request a
    new verification email below.
  </Message>
  <Form
    class="form"
    :initial-values="initialValues"
    :resolver="resolver"
    validate-on-blur
    validate-on-submit
    @submit="onFormSubmit"
    v-slot="$form"
  >
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

    <Button
      :disabled="!$form.valid || $form.email?.pristine"
      :loading="loading"
      fluid
      label="Submit"
      type="submit"
    />
  </Form>
</template>

<style scoped>
.form {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 20rem;
  gap: 1rem;
}
</style>
