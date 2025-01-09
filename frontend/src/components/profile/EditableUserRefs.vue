<script setup lang="ts">
import InputText from "primevue/inputtext";
import Button from "primevue/button";
import FloatLabel from "primevue/floatlabel";
import Message from "primevue/message";
import InputGroup from "primevue/inputgroup";
import InputGroupAddon from "primevue/inputgroupaddon";
import type { UserRefs } from "@/api/types";
import { z, ZodError } from "zod";
import { onMounted, reactive, ref } from "vue";
import { USER_REFS_EXP } from "@/utils";

const { initialValues } = defineProps<{ initialValues: UserRefs }>();

const model = defineModel<Partial<UserRefs>>();
const internalModel = ref<UserRefs>({ ...initialValues });

const reset = () => {
  internalModel.value = { ...initialValues };
};

defineExpose({ reset });

const validator = {
  orcid: z.string().url().regex(USER_REFS_EXP.orcid, "Invalid OrcID URL"),
  google_scholar: z
    .string()
    .url()
    .regex(USER_REFS_EXP.google_scholar, "Invalid Google Scholar URL"),
  researchgate: z.string().url().regex(USER_REFS_EXP.researchgate, "Invalid ResearchGate URL"),
  linkedin: z.string().url().regex(USER_REFS_EXP.linkedin, "Invalid LinkedIn URL"),
};

const errors = reactive<Record<keyof UserRefs, ZodError<string> | null>>({
  orcid: null,
  google_scholar: null,
  researchgate: null,
  linkedin: null,
});

const onChange = (field: keyof UserRefs, value?: string) => {
  if (value === "") {
    errors[field] = null;
    model.value![field] = null;
    return;
  }
  const result = validator[field].safeParse(value);
  if (result.error) {
    errors[field] = result.error;
    model.value![field] = initialValues[field];
    return;
  }
  model.value![field] = value;
};

type Field = {
  key: keyof UserRefs;
  label: string;
  placeholder: string;
};

const fields: Field[] = [
  {
    key: "orcid",
    label: "OrcID",
    placeholder: "Enter your OrcID URL...",
  },
  {
    key: "google_scholar",
    label: "Google Scholar",
    placeholder: "Enter your Google Scholar URL...",
  },
  {
    key: "researchgate",
    label: "ResearchGate",
    placeholder: "Enter your ResearchGate URL...",
  },
  {
    key: "linkedin",
    label: "LinkedIn",
    placeholder: "Enter your LinkedIn URL...",
  },
];

onMounted(() => (model.value = { ...initialValues }));
</script>

<template>
  <div class="form-container">
    <div class="form-row" v-for="field in fields" :key="field.key">
      <InputGroup>
        <FloatLabel variant="on">
          <InputText
            v-model="internalModel[field.key]"
            :invalid="errors[field.key] !== null"
            :id="field.key"
            @value-change="(v) => onChange(field.key, v)"
          />
          <label :for="field.key">{{ field.label }}</label>
        </FloatLabel>
        <InputGroupAddon>
          <Button
            as="a"
            variant="text"
            icon="pi pi-external-link"
            :href="model?.[field.key]"
            target="_blank"
            rel="noopener"
          />
        </InputGroupAddon>
      </InputGroup>
      <Message
        class="error-message"
        v-if="errors[field.key]"
        severity="error"
        size="small"
        variant="simple"
      >
        {{ errors[field.key]?.errors?.[0].message || "Invalid URL" }}
      </Message>
    </div>
  </div>
</template>

<style scoped>
.form-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-row {
  position: relative;
  display: flex;
  gap: 1rem;
}

.error-message {
  position: absolute;
  bottom: -1.5rem;
}
</style>
