<script setup lang="ts">
import Chip from "primevue/chip";
import Button from "primevue/button";
import Popover from "primevue/popover";
import { USER_FIELD_MAP, USER_FIELD_OPTIONS } from "@/api/mappings";
import type { UserField } from "@/api/types";
import { computed, nextTick, useTemplateRef } from "vue";

const { initialValues } = defineProps<{ initialValues: UserField[] }>();

const model = defineModel<UserField[]>();
const menu = useTemplateRef("menu");

const onAdd = async (field: UserField) => {
  if (!model.value) model.value = [...initialValues];
  await nextTick(() => model.value?.push(field));
  menu.value?.alignOverlay();
};

const onRemove = (index: number) => {
  if (!model.value) model.value = [...initialValues];
  nextTick(() => model.value?.splice(index, 1));
};

const items = computed(() => {
  const valuesToCheck = model.value || initialValues;
  return USER_FIELD_OPTIONS.filter((field) => !valuesToCheck.includes(field.value));
});

const showMenu = (e: MouseEvent) => menu.value?.show(e);
</script>

<template>
  <div class="editable-user-fields">
    <Chip
      v-for="(field, index) in model || initialValues"
      :key="field"
      :label="USER_FIELD_MAP[field]"
      :pt="{
        root: { style: { fontSize: 'small', borderRadius: '3rem' } },
      }"
      removable
      @remove="onRemove(index)"
    />
    <Button rounded severity="secondary" size="small" icon="pi pi-plus" @click="showMenu" />
    <Popover ref="menu">
      <div class="options-container">
        <Button
          size="small"
          severity="secondary"
          v-for="item in items"
          :key="item.value"
          :label="item.label"
          @click="onAdd(item.value)"
        />
      </div>
    </Popover>
  </div>
</template>

<style scoped>
.editable-user-fields {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.options-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  max-height: 15rem;
  max-width: 30rem;
  overflow-y: auto;
}
</style>
