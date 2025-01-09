<script setup lang="ts">
import { onKeyStroke, useElementSize, useSwipe } from "@vueuse/core";
import { computed, nextTick, ref, useTemplateRef } from "vue";

const {
  overlay = true,
  maxWidth = 640,
  initialHeight,
  transitionDuration = 0.5,
  overlayClickClose = true,
  canSwipe = true,
} = defineProps<{
  overlay?: boolean;
  maxWidth?: number;
  initialHeight?: number;
  transitionDuration?: number;
  overlayClickClose?: boolean;
  canSwipe?: boolean;
}>();

const showSheet = ref(false);
const translateValue = ref(100);

const headerEl = useTemplateRef("bottomSheetHeader");
const { height: headerHeight } = useElementSize(headerEl);

const mainEl = useTemplateRef("bottomSheetMain");

const footerEl = useTemplateRef("bottomSheetFooter");
const { height: footerHeight } = useElementSize(footerEl);

const areaEl = useTemplateRef("bottomSheetDraggableArea");

const sheetHeight = ref(0);
const midHeight = ref(0);
const MAX_HEIGHT = window.innerHeight * 0.95;
const MAX_MID_HEIGHT = window.innerHeight * 0.6;
const startHeight = ref(0);

const initHeights = () => {
  if (initialHeight && initialHeight < MAX_HEIGHT) {
    midHeight.value = initialHeight;
    sheetHeight.value = initialHeight;
    return;
  }

  const elemHeight = headerHeight.value + mainEl.value!.scrollHeight + footerHeight.value;

  if (elemHeight > MAX_MID_HEIGHT) {
    midHeight.value = MAX_MID_HEIGHT;
    sheetHeight.value = MAX_MID_HEIGHT;
    return;
  }

  midHeight.value = elemHeight;
  sheetHeight.value = elemHeight;
};

const open = async () => {
  await nextTick();

  initHeights();

  translateValue.value = 0;
  document.documentElement.style.overflowY = "hidden";
  document.documentElement.style.overscrollBehavior = "none";
  showSheet.value = true;
};

const close = async () => {
  showSheet.value = false;
  translateValue.value = 100;
  setTimeout(() => {
    document.documentElement.style.overflowY = "auto";
    document.documentElement.style.overscrollBehavior = "";
  }, transitionDuration * 1000);
};

const clickOnOverlayHandler = () => {
  if (!overlayClickClose) return;
  close();
};

onKeyStroke("Escape", close, { dedupe: true });

const transitionDurationString = computed(() => `${transitionDuration}s`);
const heightString = computed(() => `${sheetHeight.value}px`);
const translateValueString = computed(() => `${translateValue.value}%`);
const maxWidthString = computed(() => `${maxWidth}px`);

const swipeStartHandler = () => {
  startHeight.value = sheetHeight.value;
};

const offsetToPercent = (offset: number) => (offset / sheetHeight.value) * 100;
const swipeHandler = (deltaY: number) => {
  if (!canSwipe) return;

  // swipe up and sheet is already at max height
  if (deltaY > 0 && sheetHeight.value >= MAX_HEIGHT) return;

  const currentHeight = startHeight.value + deltaY;

  if (currentHeight <= midHeight.value) {
    const offsetFromMid = midHeight.value - currentHeight;
    translateValue.value = offsetToPercent(offsetFromMid);
    return;
  }

  sheetHeight.value = currentHeight;
};

const swipeEndHandler = (deltaY: number) => {
  if (!canSwipe) return;

  const currentHeight = startHeight.value + deltaY;

  // sheet is between mid and max height
  if (currentHeight >= midHeight.value) {
    const offsetFromMid = currentHeight - midHeight.value;

    // sheet is closer to max height
    if (offsetFromMid > (MAX_HEIGHT - midHeight.value) / 2) {
      sheetHeight.value = MAX_HEIGHT;
      return;
    }

    // sheet is closer to mid height
    sheetHeight.value = midHeight.value;
    return;
  }

  // sheet is between bottom and mid height
  if (currentHeight < midHeight.value / 2) {
    close();
    return;
  }

  translateValue.value = 0;
};

const { isSwiping, lengthY } = useSwipe(areaEl, {
  threshold: 10,
  onSwipeStart: swipeStartHandler,
  onSwipe: () => swipeHandler(lengthY.value),
  onSwipeEnd: () => swipeEndHandler(lengthY.value),
});

const sheetContentClasses = computed(() => {
  return [
    "bottom-sheet__content",
    {
      "bottom-sheet__content--fullscreen": sheetHeight.value >= window.innerHeight,
      "bottom-sheet__content--dragging": isSwiping.value,
    },
  ];
});

defineExpose({ open, close });
</script>

<template>
  <Teleport to="body">
    <div class="bottom-sheet" ref="bottomSheet" :aria-hidden="!showSheet" role="dialog">
      <transition>
        <div
          @click="clickOnOverlayHandler"
          class="bottom-sheet__overlay"
          v-show="overlay && showSheet"
        />
      </transition>
      <div ref="bottomSheetContent" :class="sheetContentClasses">
        <header ref="bottomSheetHeader" class="bottom-sheet__header">
          <div class="bottom-sheet__draggable-area" ref="bottomSheetDraggableArea">
            <div class="bottom-sheet__draggable-thumb" />
          </div>
        </header>
        <main ref="bottomSheetMain" class="bottom-sheet__main">
          <slot />
        </main>
        <footer ref="bottomSheetFooter" class="bottom-sheet__footer">
          <slot name="footer" />
        </footer>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.bottom-sheet {
  z-index: 1002;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;

  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  transition: visibility v-bind("transitionDurationString");
}

.bottom-sheet * {
  box-sizing: border-box;
}

.bottom-sheet[aria-hidden="false"] {
  visibility: visible;
}

.bottom-sheet[aria-hidden="true"] {
  visibility: hidden;
  pointer-events: none;
}

.bottom-sheet__overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: -1;
  background: var(--p-overlay-modal-color);
  opacity: 0.3;
}

.bottom-sheet__content {
  display: flex;
  flex-direction: column;
  border-radius: 16px 16px 0 0;
  background: var(--p-overlay-modal-background);
  overflow-y: hidden;
  transform: translate3d(0, v-bind("translateValueString"), 0);
  max-width: v-bind("maxWidthString");
  width: 100%;
  height: v-bind("heightString");
  pointer-events: all;
}

.bottom-sheet__content--fullscreen {
  border-radius: 0;
}

.bottom-sheet__content:not(.bottom-sheet__content--dragging) {
  transition: v-bind("transitionDurationString") ease;
}

.bottom-sheet__draggable-area {
  width: 100%;
  margin: auto;
  padding: 16px;
  cursor: grab;
}

.bottom-sheet__draggable-thumb {
  width: 40px;
  height: 4px;
  background: var(--p-primary-color);
  border-radius: 8px;
  margin: 0 auto;
}

.bottom-sheet__main {
  display: block;
  overflow-y: scroll;
  -webkit-overflow-scrolling: touch;
  touch-action: auto !important;
}

.bottom-sheet__footer {
  display: flex;
  justify-content: center;
  margin-top: auto;
}

.v-enter-active,
.v-leave-active {
  transition: opacity v-bind("transitionDurationString") ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
