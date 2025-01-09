import Aura from "@primevue/themes/aura";
import { definePreset } from "@primevue/themes";

import primitive from "@/prime-vue-theme/primitive";
import semantic from "@/prime-vue-theme/semantic";
import components from "@/prime-vue-theme/components";

const presetExtension = {
  primitive,
  semantic,
  components,
};

const preset = definePreset(Aura, presetExtension);

export const DARK_MODE_CLASS = "dark-mode";

const options = { darkModeSelector: `.${DARK_MODE_CLASS}` };

export default { theme: { preset, options } };
