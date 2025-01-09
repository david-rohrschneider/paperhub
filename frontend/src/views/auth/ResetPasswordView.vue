<script setup lang="ts">
import { Form, type FormSubmitEvent } from "@primevue/forms";
import Button from "primevue/button";
import InputGroup from "primevue/inputgroup";
import InputGroupAddon from "primevue/inputgroupaddon";
import Message from "primevue/message";
import FloatLabel from "primevue/floatlabel";
import Password from "primevue/password";
import { zodResolver } from "@primevue/forms/resolvers/zod";
import { confirmPasswordReset } from "firebase/auth";
import { useToast } from "primevue";
import { onBeforeMount, ref } from "vue";
import { useRouter } from "vue-router";
import { useFirebaseAuth } from "vuefire";
import { z } from "zod";

const { email, oobCode } = defineProps<{ email?: string; oobCode?: string }>();

const router = useRouter();
const auth = useFirebaseAuth()!;
const toast = useToast();
const loading = ref(false);

const initialValues = ref({
  password: "",
  repeat_password: "",
});

const resolver = zodResolver(
  z.object({
    password: z
      .string()
      .min(8)
      .max(50)
      .refine((value) => /[a-z]/.test(value), "Must have a lowercase letter.")
      .refine((value) => /[A-Z]/.test(value), "Must have an uppercase letter."),
    repeat_password: z.string().min(1),
  }),
);

const onFormSubmit = async (event: FormSubmitEvent) => {
  const v = event.values;

  if (!v.password || !v.repeat_password) return;
  if (v.password !== v.repeat_password) return;

  loading.value = true;

  try {
    await confirmPasswordReset(auth, oobCode!, v.password);
    toast.add({
      severity: "success",
      summary: "Success",
      detail: "Password Reset successful. You can now login with your new password!",
      life: 5000,
    });
    router.push("/auth/login");
  } catch {
    toast.add({
      severity: "error",
      summary: "Error",
      detail: "Password Reset failed. Please try requesting a new password reset email.",
      life: 5000,
    });
  } finally {
    loading.value = false;
  }
};

onBeforeMount(() => {
  if (!email || !oobCode) {
    router.push("/auth/login");
  }
});
</script>

<template>
  <Message>
    Enter a new password for your account with email: <b>{{ email }}</b>
  </Message>
  <Form
    class="form"
    :initial-values="initialValues"
    :resolver="resolver"
    validate-on-blur
    validate-on-submit
    :validate-on-value-update="false"
    @submit="onFormSubmit"
    v-slot="$form"
  >
    <InputGroup>
      <InputGroupAddon>
        <i class="pi pi-lock"></i>
      </InputGroupAddon>
      <FloatLabel variant="on">
        <Password name="password" :feedback="false" toggle-mask />
        <label for="password">Password</label>
      </FloatLabel>
    </InputGroup>
    <Message v-if="$form.password?.invalid" severity="error" size="small" variant="simple">
      {{ $form.password.error.message }}
    </Message>

    <InputGroup>
      <InputGroupAddon>
        <i class="pi pi-lock"></i>
      </InputGroupAddon>
      <FloatLabel variant="on">
        <Password name="repeat_password" :feedback="false" toggle-mask />
        <label for="repeat_password">Repeat Password</label>
      </FloatLabel>
    </InputGroup>
    <Message
      v-if="
        $form.repeat_password?.invalid || $form.repeat_password?.dirty
          ? $form.repeat_password?.value !== $form.password?.value
          : false
      "
      severity="error"
      size="small"
      variant="simple"
    >
      {{ $form.repeat_password?.error?.message || "Passwords do not match" }}
    </Message>

    <Button
      :disabled="
        !$form.valid ||
        $form.password?.pristine ||
        $form.repeat_password?.pristine ||
        $form.repeat_password?.value !== $form.password?.value
      "
      :loading="loading"
      fluid
      label="Reset Password"
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
