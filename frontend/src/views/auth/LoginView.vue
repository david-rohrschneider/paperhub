<script setup lang="ts">
import { ref } from "vue";
import InputGroup from "primevue/inputgroup";
import InputText from "primevue/inputtext";
import InputGroupAddon from "primevue/inputgroupaddon";
import Password from "primevue/password";
import Button from "primevue/button";
import Divider from "primevue/divider";
import { Form, type FormSubmitEvent } from "@primevue/forms";
import { z } from "zod";
import { zodResolver } from "@primevue/forms/resolvers/zod";
import { signInWithEmailAndPassword } from "firebase/auth";
import { useRouter } from "vue-router";
import { useFirebaseAuth } from "vuefire";
import { useToast } from "primevue/usetoast";

const initialValues = ref({
  email: "",
  password: "",
});

const resolver = zodResolver(
  z.object({
    email: z.string().email(),
    password: z.string().min(1),
  }),
);

const loading = ref(false);
const router = useRouter();
const auth = useFirebaseAuth()!;
const toast = useToast();

const onFormSubmit = async (e: FormSubmitEvent) => {
  if (!e.valid) return;

  loading.value = true;

  try {
    await signInWithEmailAndPassword(auth, e.values.email, e.values.password);
    router.push("/");
  } catch {
    toast.add({
      severity: "error",
      summary: "Error",
      detail: "Invalid email or password",
      life: 3000,
    });
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="login-page">
    <Form
      class="form"
      :initial-values="initialValues"
      :resolver="resolver"
      @submit="onFormSubmit"
      v-slot="$form"
    >
      <InputGroup>
        <InputGroupAddon>
          <i class="pi pi-at"></i>
        </InputGroupAddon>
        <InputText name="email" placeholder="E-Mail" />
      </InputGroup>

      <InputGroup>
        <InputGroupAddon>
          <i class="pi pi-lock"></i>
        </InputGroupAddon>
        <Password name="password" :feedback="false" toggle-mask placeholder="Password" />
      </InputGroup>

      <Button
        :disabled="!$form.valid || $form.email?.pristine || $form.password?.pristine"
        :loading="loading"
        fluid
        label="Login"
        type="submit"
      />
    </Form>

    <Divider style="margin: 0" />
    <Button as="router-link" fluid severity="secondary" label="Register" to="/auth/register" />
  </div>
</template>

<style scoped>
.login-page {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
  max-width: 20rem;
  align-self: center;
}

.form {
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 1rem;
}
</style>
