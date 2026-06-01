<script setup>
import { ref } from 'vue'
const hide = ref(false)
</script>

<template>
  <div v-if="!hide" class="cat-mascot" @click="hide = true" title="再见">
    <div class="cat">
      <div class="ear left"></div>
      <div class="ear right"></div>
      <div class="head">
        <div class="eye left"></div>
        <div class="eye right"></div>
        <div class="nose"></div>
      </div>
      <div class="body"></div>
      <div class="tail"></div>
    </div>
    <div class="speech">♪ ♫ ♪</div>
  </div>
</template>

<style scoped>
.cat-mascot {
  position: fixed;
  right: 16px; bottom: 16px;
  z-index: 5;
  cursor: pointer;
  user-select: none;
  pointer-events: auto;
}
.cat {
  position: relative;
  width: 56px; height: 48px;
  animation: bob 2.4s ease-in-out infinite;
}
@keyframes bob {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}
.ear {
  position: absolute; top: 2px;
  width: 0; height: 0;
  border-left: 7px solid transparent;
  border-right: 7px solid transparent;
  border-bottom: 10px solid var(--ink);
}
.ear.left  { left: 6px;  transform: rotate(-15deg); }
.ear.right { right: 6px; transform: rotate(15deg); }
.head {
  position: absolute; top: 8px; left: 6px;
  width: 44px; height: 28px;
  background: var(--orange);
  border: 2px solid var(--ink);
  border-radius: 6px;
}
.eye {
  position: absolute; top: 9px;
  width: 4px; height: 6px;
  background: var(--ink);
  animation: blink 4s infinite;
}
.eye.left  { left: 10px; }
.eye.right { right: 10px; }
@keyframes blink {
  0%, 92%, 100% { transform: scaleY(1); }
  95% { transform: scaleY(0.1); }
}
.nose {
  position: absolute; top: 18px; left: 50%; transform: translateX(-50%);
  width: 4px; height: 3px;
  background: var(--orange-d);
}
.body {
  position: absolute; bottom: 0; left: 12px;
  width: 32px; height: 14px;
  background: var(--orange);
  border: 2px solid var(--ink);
  border-radius: 4px 4px 2px 2px;
}
.tail {
  position: absolute; bottom: 4px; right: 0;
  width: 14px; height: 6px;
  background: var(--orange);
  border: 2px solid var(--ink);
  border-radius: 3px;
  transform-origin: left center;
  animation: wag 1.6s ease-in-out infinite;
}
@keyframes wag {
  0%, 100% { transform: rotate(-10deg); }
  50%      { transform: rotate(20deg); }
}
.speech {
  position: absolute;
  right: 60px; bottom: 28px;
  font-family: var(--font-pix);
  font-size: 11px;
  color: var(--ink);
  background: var(--bg-card);
  border: 2px solid var(--ink);
  padding: 4px 8px;
  white-space: nowrap;
  animation: pulse 3s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 0.6; }
  50%      { opacity: 1; }
}

@media (max-width: 720px) {
  .cat-mascot { right: 8px; bottom: 8px; transform: scale(0.8); transform-origin: bottom right; }
}
</style>
