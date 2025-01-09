<script setup lang="ts">
import { ref } from "vue";
import InputGroup from "primevue/inputgroup";
import InputText from "primevue/inputtext";
import InputGroupAddon from "primevue/inputgroupaddon";
import Password from "primevue/password";
import Button from "primevue/button";
import Divider from "primevue/divider";
import Select from "primevue/select";
import FloatLabel from "primevue/floatlabel";
import Panel from "primevue/panel";
import DatePicker from "primevue/datepicker";
import Textarea from "primevue/textarea";
import Message from "primevue/message";
import { Form, FormField, type FormSubmitEvent } from "@primevue/forms";
import { z } from "zod";
import { zodResolver } from "@primevue/forms/resolvers/zod";
import { useRouter } from "vue-router";
import EditableUserFields from "@/components/profile/EditableUserFields.vue";
import { USER_FIELD_MAP, USER_TITLE_OPTIONS } from "@/api/mappings";
import type { User, CreateUserBody, UserField } from "@/api/types";
import { USER_REFS_EXP } from "@/utils";
import { useThemeStore } from "@/stores/theme-store";
import { useApi } from "@/api/use-api";
import routes from "@/api/routes";

const { breakpoints } = useThemeStore();
const isMobile = breakpoints.smaller("tablet");

const initialValues = ref({
  title: null,
  first_name: "",
  last_name: "",
  email: "",
  password: "",
  repeat_password: "",
  affiliation: "",
  bday: null,
  bio: "",
  fields: [],
  orcid: "",
  google_scholar: "",
  researchgate: "",
  linkedin: "",
});

const resolver = zodResolver(
  z.object({
    title: z.string().nullable(),
    first_name: z.string().min(1).max(50),
    last_name: z.string().min(1).max(50),
    email: z.string().email(),
    password: z
      .string()
      .min(8)
      .max(50)
      .refine((value) => /[a-z]/.test(value), "Must have a lowercase letter.")
      .refine((value) => /[A-Z]/.test(value), "Must have an uppercase letter."),
    repeat_password: z.string().min(1),
    affiliation: z.string().min(1).max(100).optional().or(z.literal("")),
    bday: z
      .date()
      .max(new Date(new Date().setFullYear(new Date().getFullYear() - 18)))
      .nullable(),
    bio: z.string().min(1).max(500).optional().or(z.literal("")),
    fields: z.array(z.enum(Object.keys(USER_FIELD_MAP) as [UserField, ...UserField[]])),
    orcid: z
      .string()
      .url()
      .regex(USER_REFS_EXP.orcid, "Invalid OrcID URL")
      .optional()
      .or(z.literal("")),
    google_scholar: z
      .string()
      .url()
      .regex(USER_REFS_EXP.google_scholar, "Invalid Google Scholar URL")
      .optional()
      .or(z.literal("")),
    researchgate: z
      .string()
      .url()
      .regex(USER_REFS_EXP.researchgate, "Invalid ResearchGate URL")
      .optional()
      .or(z.literal("")),
    linkedin: z
      .string()
      .url()
      .regex(USER_REFS_EXP.linkedin, "Invalid LinkedIn URL")
      .optional()
      .or(z.literal("")),
  }),
);

const { post, loading } = useApi(routes.users.post.createUser, true);
const router = useRouter();

const onFormSubmit = async (e: FormSubmitEvent) => {
  if (!e.valid) return;

  const values = Object.fromEntries(Object.entries(e.values).filter(([, value]) => value));
  const body: CreateUserBody = {
    title: values.title,
    first_name: values.first_name,
    last_name: values.last_name,
    email: values.email,
    password: values.password,
    affiliation: values.affiliation,
    bio: values.bio,
    fields: values.fields,
    refs: {
      orcid: values.orcid,
      google_scholar: values.google_scholar,
      researchgate: values.researchgate,
      linkedin: values.linkedin,
    },
    bday: values.bday?.toISOString(),
  };

  const response = await post<User, CreateUserBody>({
    data: body,
    successMessage: "User created successfully.",
  });

  if (!response?.data) return;
  router.push("/auth/verify-email");
};
</script>

<template>
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
    <div class="form-groups" :class="{ 'form-groups-mobile': isMobile }">
      <div class="form-group">
        <InputGroup>
          <InputGroupAddon>
            <i class="pi pi-graduation-cap"></i>
          </InputGroupAddon>
          <FloatLabel variant="on">
            <Select
              name="title"
              :options="USER_TITLE_OPTIONS"
              option-label="label"
              option-value="value"
              show-clear
            />
            <label for="title">Title</label>
          </FloatLabel>
        </InputGroup>

        <InputGroup>
          <InputGroupAddon>
            <i class="pi pi-id-card"></i>
          </InputGroupAddon>
          <FloatLabel variant="on">
            <InputText name="first_name" />
            <label for="first_name">First Name</label>
          </FloatLabel>
          <FloatLabel variant="on">
            <InputText name="last_name" />
            <label for="last_name">Last Name</label>
          </FloatLabel>
        </InputGroup>
        <Message v-if="$form.first_name?.invalid" severity="error" size="small" variant="simple">
          {{ $form.first_name.error.message }}
        </Message>
        <Message v-if="$form.last_name?.invalid" severity="error" size="small" variant="simple">
          {{ $form.last_name.error.message }}
        </Message>

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
      </div>

      <Divider v-if="isMobile" style="margin: 0" />

      <div class="form-group">
        <InputGroup>
          <InputGroupAddon>
            <i class="pi pi-building"></i>
          </InputGroupAddon>
          <FloatLabel variant="on">
            <InputText name="affiliation" />
            <label for="affiliation">Affiliation</label>
          </FloatLabel>
        </InputGroup>
        <Message v-if="$form.affiliation?.invalid" severity="error" size="small" variant="simple">
          {{ $form.affiliation.error.message }}
        </Message>

        <InputGroup>
          <InputGroupAddon>
            <i class="pi pi-calendar"></i>
          </InputGroupAddon>
          <FloatLabel variant="on">
            <DatePicker
              name="bday"
              fluid
              :max-date="new Date(new Date().setFullYear(new Date().getFullYear() - 18))"
            />
            <label for="bday">Birthday</label>
          </FloatLabel>
        </InputGroup>
        <Message v-if="$form.bday?.invalid" severity="error" size="small" variant="simple">
          {{ $form.bday.error.message }}
        </Message>

        <InputGroup>
          <InputGroupAddon>
            <i class="pi pi-user"></i>
          </InputGroupAddon>
          <FloatLabel variant="on">
            <Textarea name="bio" auto-resize style="resize: none; width: 100%; min-height: 100%" />
            <label for="bio">Short Biography</label>
          </FloatLabel>
        </InputGroup>
        <Message v-if="$form.bio?.invalid" severity="error" size="small" variant="simple">
          {{ $form.bio.error.message }}
        </Message>

        <div class="fields">
          <label for="fields">Fields of Study</label>
          <FormField v-slot="$field" name="fields">
            <EditableUserFields :initial-values="[]" v-model="$field.value" />
          </FormField>
        </div>

        <Panel
          header="References"
          toggleable
          collapsed
          :pt="{
            header: { style: { padding: '0.5rem 1rem' } },
            title: {
              style: { fontSize: '1rem', fontWeight: 'normal', color: 'var(--p-text-muted-color)' },
            },
            content: { style: { display: 'flex', flexDirection: 'column', gap: '0.5rem' } },
          }"
        >
          <InputGroup>
            <InputGroupAddon>
              <i class="pi pi-globe"></i>
            </InputGroupAddon>
            <FloatLabel variant="on">
              <InputText name="orcid" />
              <label for="orcid">OrcID</label>
            </FloatLabel>
          </InputGroup>
          <Message v-if="$form.orcid?.invalid" severity="error" size="small" variant="simple">
            {{ $form.orcid.error.message }}
          </Message>

          <InputGroup>
            <InputGroupAddon>
              <i class="pi pi-google"></i>
            </InputGroupAddon>
            <FloatLabel variant="on">
              <InputText name="google_scholar" />
              <label for="google_scholar">Google Scholar</label>
            </FloatLabel>
          </InputGroup>
          <Message
            v-if="$form.google_scholar?.invalid"
            severity="error"
            size="small"
            variant="simple"
          >
            {{ $form.google_scholar.error.message }}
          </Message>

          <InputGroup>
            <InputGroupAddon>
              <i class="pi pi-globe"></i>
            </InputGroupAddon>
            <FloatLabel variant="on">
              <InputText name="researchgate" />
              <label for="researchgate">ResearchGate</label>
            </FloatLabel>
          </InputGroup>
          <Message
            v-if="$form.researchgate?.invalid"
            severity="error"
            size="small"
            variant="simple"
          >
            {{ $form.researchgate.error.message }}
          </Message>

          <InputGroup>
            <InputGroupAddon>
              <i class="pi pi-linkedin"></i>
            </InputGroupAddon>
            <FloatLabel variant="on">
              <InputText name="linkedin" />
              <label for="linkedin">LinkedIn</label>
            </FloatLabel>
          </InputGroup>
          <Message v-if="$form.linkedin?.invalid" severity="error" size="small" variant="simple">
            {{ $form.linkedin.error.message }}
          </Message>
        </Panel>
      </div>
    </div>
    <Button
      :disabled="
        !$form.valid ||
        $form.first_name?.pristine ||
        $form.last_name?.pristine ||
        $form.email?.pristine ||
        $form.password?.pristine ||
        $form.repeat_password?.pristine ||
        $form.repeat_password?.value !== $form.password?.value
      "
      :loading="loading"
      fluid
      label="Register"
      type="submit"
    />
  </Form>
  <Divider style="margin: 0" />
  <Button as="router-link" fluid severity="secondary" label="Login" to="/auth/login" />
</template>

<style scoped>
.form {
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 1rem;
}

.form-groups {
  display: flex;
  gap: 1rem;
  width: 100%;
}

.form-groups-mobile {
  flex-direction: column;
  max-height: 60vh;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
}

.fields {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem;
  border-radius: var(--p-form-field-border-radius);
  border: 1px solid var(--p-inputtext-border-color);
  background: var(--p-inputtext-background);
  font-size: 1rem;
  color: var(--p-text-muted-color);
}

.refs {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 0.5rem;
  border-radius: var(--p-form-field-border-radius);
  border: 1px solid var(--p-inputtext-border-color);
  font-size: 1rem;
  color: var(--p-text-muted-color);
}
</style>
