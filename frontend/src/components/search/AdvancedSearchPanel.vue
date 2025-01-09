<script setup lang="ts">
import Panel from "primevue/panel";
import InputGroup from "primevue/inputgroup";
import InputGroupAddon from "primevue/inputgroupaddon";
import InputText from "primevue/inputtext";
import Button from "primevue/button";
import MultiSelect from "primevue/multiselect";
import FloatLabel from "primevue/floatlabel";
import ToggleButton from "primevue/togglebutton";
import DatePicker from "primevue/datepicker";
import InputNumber from "primevue/inputnumber";
import { z } from "zod";
import { computed, ref } from "vue";
import type { PaperSearchBody, PublicationType, UserField } from "@/api/types";
import { PUB_TYPE_MAP, PUB_TYPE_OPTIONS, USER_FIELD_MAP, USER_FIELD_OPTIONS } from "@/api/mappings";
import { useThemeStore } from "@/stores/theme-store";

const { breakpoints } = useThemeStore();
const isMobile = breakpoints.smaller("tablet");

const emit = defineEmits<{
  submit: [values: PaperSearchBody];
}>();

type FormValues = Omit<PaperSearchBody, "publication_date_start" | "publication_date_end"> & {
  publication_date_range?: [Date, Date | null];
};

const initialValues: FormValues = {
  query: "",
  publication_types: [],
  open_access_pdf: undefined,
  fields_of_study: [],
  publication_date_range: undefined,
  min_citation_count: undefined,
};

const formValues = ref<FormValues>(JSON.parse(JSON.stringify(initialValues)));

const resolver = z.object({
  query: z.string().min(1),
  publication_types: z.optional(
    z.array(z.enum(Object.keys(PUB_TYPE_MAP) as [PublicationType, ...PublicationType[]])),
  ),
  open_access_pdf: z.optional(z.boolean()),
  fields_of_study: z.optional(
    z.array(z.enum(Object.keys(USER_FIELD_MAP) as [UserField, ...UserField[]])),
  ),
  publication_date_range: z.optional(z.array(z.date().nullable()).length(2)),
  min_citation_count: z.optional(z.number().int().min(0)),
});

const isValid = computed(() => resolver.safeParse(formValues.value).success);
const isPristine = computed(
  () => JSON.stringify(formValues.value) === JSON.stringify(initialValues),
);

const submit = () => {
  const v = formValues.value;
  const returnValues: PaperSearchBody = { query: v.query };

  if (v.publication_types?.length) {
    returnValues.publication_types = v.publication_types;
  }

  if (v.open_access_pdf !== undefined) {
    returnValues.open_access_pdf = v.open_access_pdf;
  }

  if (v.fields_of_study?.length) {
    returnValues.fields_of_study = v.fields_of_study;
  }

  if (v.publication_date_range?.[0]) {
    returnValues.publication_date_start = v.publication_date_range[0].toISOString();
  }

  if (v.publication_date_range?.[1]) {
    returnValues.publication_date_end = v.publication_date_range[1].toISOString();
  }

  if (v.min_citation_count !== undefined) {
    returnValues.min_citation_count = v.min_citation_count;
  }

  emit("submit", returnValues);
};

const pt = {
  root: { style: { width: "100%" } },
};
</script>

<template>
  <div class="advanced-search-panel">
    <InputGroup style="margin-right: 1rem">
      <InputText
        :size="isMobile ? undefined : 'large'"
        v-model="formValues.query"
        fluid
        placeholder="Search for any paper..."
      />
      <InputGroupAddon>
        <Button
          :size="isMobile ? undefined : 'large'"
          icon="pi pi-search"
          :label="isMobile ? undefined : 'Search'"
          :disabled="!isValid"
          @click="submit"
        />
      </InputGroupAddon>
    </InputGroup>

    <Panel toggleable collapsed :pt="pt">
      <template #header>
        <component :is="isMobile ? 'h4' : 'h3'">Filters</component>
      </template>

      <div class="filters">
        <FloatLabel variant="on">
          <MultiSelect
            v-model="formValues.publication_types"
            :options="PUB_TYPE_OPTIONS"
            :max-selected-labels="3"
            option-label="label"
            option-value="value"
            placeholder="."
            filter
            fluid
          />
          <label for="publication_types">Publication Types</label>
        </FloatLabel>

        <ToggleButton
          v-model="formValues.open_access_pdf"
          onLabel="Only Open Access"
          offLabel="Allow Closed Access"
        />

        <FloatLabel variant="on">
          <MultiSelect
            v-model="formValues.fields_of_study"
            :options="USER_FIELD_OPTIONS"
            :max-selected-labels="3"
            option-label="label"
            option-value="value"
            placeholder="."
            filter
            fluid
          />
          <label for="fields_of_study">Fields of Study</label>
        </FloatLabel>

        <FloatLabel variant="on">
          <DatePicker
            v-model="formValues.publication_date_range"
            selection-mode="range"
            show-icon
            fluid
            icon-display="input"
            :maxDate="new Date()"
            :manualInput="false"
          />
          <label for="publication_date_range">Publication Date</label>
        </FloatLabel>

        <FloatLabel variant="on">
          <InputNumber
            v-model="formValues.min_citation_count"
            buttonLayout="horizontal"
            :min="0"
            showButtons
            fluid
          >
            <template #incrementicon>
              <i class="pi pi-plus" />
            </template>
            <template #decrementicon>
              <i class="pi pi-minus" />
            </template>
          </InputNumber>
          <label for="min_citation_count">Min Citations</label>
        </FloatLabel>

        <Button
          severity="secondary"
          label="Reset"
          icon="pi pi-refresh"
          @click="formValues = JSON.parse(JSON.stringify(initialValues))"
          :disabled="isPristine"
        />
      </div>
    </Panel>
  </div>
</template>

<style scoped>
.advanced-search-panel {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 40rem;
  gap: 1rem;
}

.filters {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(15rem, 1fr));
  gap: 1rem;
}
</style>
