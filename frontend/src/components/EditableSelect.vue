<script setup lang="ts" generic="T extends string | number">
import { computed, nextTick, onMounted, ref, watch } from "vue";
import Select, { type SelectMethods } from "primevue/select";
import Button from "primevue/button";

type Option = { label: string; value: T };

const { tag, initialOption, options, fallbackText, placeholder } = defineProps<{
  tag: "p" | "h1" | "h2" | "h3" | "h4" | "h5" | "h6";
  initialOption?: T;
  fallbackText: string;
  placeholder?: string;
  options: Option[];
}>();

const emit = defineEmits<{
  (e: "submit", optionValue?: T): void;
}>();

const selectInput = ref<SelectMethods | null>(null);
const model = defineModel<T>();
const displayText = computed(() => {
  if (!model.value) return fallbackText;
  return options.find((o) => o.value === model.value)?.label;
});
const isEditing = ref(false);

const edit = () => {
  isEditing.value = true;
};

const submit = (option?: Option) => {
  isEditing.value = false;
  model.value = option?.value;
  if (option?.value === initialOption) return;
  emit("submit", option?.value);
};

const reset = () => {
  model.value = initialOption;
  isEditing.value = false;
};

const clear = () => {
  model.value = undefined;
  emit("submit");
  selectInput.value?.hide();
};

const onHide = () => (isEditing.value = false);

defineExpose({ reset });
onMounted(() => (model.value = initialOption));

watch(selectInput, (newValue) => {
  if (newValue) nextTick(() => newValue.show(true));
});

const selectDt = {
  paddingX: 0,
  paddingY: 0,
  background: "transparent",
};
</script>

<template>
  <component style="cursor: pointer" :is="tag" @click="edit">
    <span v-if="!isEditing" v-tooltip.top="'Click to edit'">
      {{ displayText }}
    </span>
    <div v-else class="select-wrapper">
      <Select
        class="invisible-select"
        ref="selectInput"
        option-label="label"
        :placeholder="placeholder"
        :dt="selectDt"
        :default-value="options.find((o) => o.value === model)"
        :options="options"
        @value-change="submit"
        @hide="onHide"
      >
        <template #footer>
          <div class="footer-wrapper">
            <Button fluid label="Clear" icon="pi pi-trash" severity="secondary" @click="clear" />
          </div>
        </template>
      </Select>
    </div>
  </component>
</template>

<style scoped>
.select-wrapper {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.invisible-select {
  font: inherit;
  font-size: inherit;
  border: none;
}

.footer-wrapper {
  padding: 0 var(--p-select-list-padding) var(--p-select-list-padding) var(--p-select-list-padding);
}
</style>
