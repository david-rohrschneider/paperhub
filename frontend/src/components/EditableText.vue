<script setup lang="ts">
import { computed, ref, useTemplateRef, watchEffect } from "vue";

const {
  tag,
  initialText,
  fallbackText,
  placeholder,
  maxWidth,
  textArea = false,
  allowEmpty = false,
} = defineProps<{
  tag: "p" | "h1" | "h2" | "h3" | "h4" | "h5" | "h6";
  initialText?: string;
  fallbackText?: string;
  placeholder?: string;
  maxWidth?: string;
  textArea?: boolean;
  allowEmpty?: boolean;
}>();

const emit = defineEmits<{
  (e: "submit", text?: string): void;
}>();

const model = defineModel<string>();
const isEditing = ref(false);
const inputEl = useTemplateRef("inputEl");

const edit = () => {
  if (model.value === undefined) model.value = initialText || "";
  isEditing.value = true;
};

const submit = () => {
  isEditing.value = false;
  if (!allowEmpty && model.value === "") {
    model.value = initialText;
  }
  if (model.value === initialText) return;
  emit("submit", model.value);
};

const reset = () => {
  model.value = initialText;
  isEditing.value = false;
};

defineExpose({ reset });

watchEffect(() => inputEl.value?.focus());

const displayText = computed(() => {
  if (model.value === "") return fallbackText;
  if (model.value !== undefined) return model.value;
  return initialText || fallbackText;
});
</script>

<template>
  <component
    style="cursor: pointer"
    :style="{ maxWidth }"
    :class="{ 'text-limited': maxWidth }"
    :is="tag"
    @click="edit"
  >
    <span v-if="!isEditing" v-tooltip.top="'Click to edit'">
      {{ displayText }}
    </span>
    <input
      v-else-if="!textArea"
      ref="inputEl"
      class="invisible-input"
      type="text"
      :placeholder="placeholder"
      v-model="model"
      @blur="submit"
      @keydown.enter="submit"
      @keydown.esc="reset"
      v-autowidth="{ maxWidth }"
    />
    <textarea
      v-else
      ref="inputEl"
      class="invisible-input"
      rows="5"
      v-model="model"
      :placeholder="placeholder"
      @blur="submit"
      @keydown.esc="reset"
    />
  </component>
</template>

<style scoped>
.text-limited {
  overflow: hidden;
  text-overflow: ellipsis;
}

.invisible-input {
  display: block;
  font: inherit;
  font-size: inherit;
  margin: 0;
  padding: 0;
  border: none;
  outline: none;
  background: transparent;
}

textarea {
  width: 100%;
  resize: none;
}
</style>
