<script setup>
import { computed } from 'vue'
import { useRadioStore } from '../stores/radio.js'
import { auth } from '../api.js'
import Avatar from './Avatar.vue'

const radio = useRadioStore()

const list = computed(() => {
  const arr = [...(radio.onlineList || [])]
  // 自己置顶，方便看到"我在场"
  arr.sort((a, b) => {
    if (a === auth.nickname) return -1
    if (b === auth.nickname) return 1
    return 0
  })
  return arr
})
</script>

<template>
  <div class="pix-card tight">
    <div class="row" style="margin-bottom:10px">
      <div class="pix-h">▼ WHO'S TUNED IN</div>
      <span class="pix-tag" style="margin-left:8px">{{ radio.online }}</span>
      <span class="dot live"></span>
    </div>

    <div v-if="list.length === 0" class="muted" style="font-size:14px;padding:6px 0">
      还没人进来…
    </div>

    <div v-else class="audience">
      <div v-for="n in list" :key="n" class="aud-item" :class="{ me: n === auth.nickname }">
        <Avatar :nick="n"/>
        <div class="aud-name">{{ n }}</div>
        <span v-if="n === auth.nickname" class="me-tag">YOU</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.audience {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(96px, 1fr));
  gap: 8px;
}
.aud-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 6px 4px;
  background: var(--bg-soft);
  border: 2px solid transparent;
  position: relative;
}
.aud-item.me {
  border-color: var(--ink);
  background: var(--bg-card);
}
.aud-name {
  font-size: 14px;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.me-tag {
  position: absolute;
  top: -8px; right: -4px;
  font-family: var(--font-pix);
  font-size: 7px;
  background: var(--orange-d);
  color: var(--bg-card);
  padding: 2px 4px;
  border: 1px solid var(--ink);
  letter-spacing: 1px;
}
.dot {
  width: 6px; height: 6px;
  background: var(--green);
  border: 1px solid var(--ink);
  margin-left: auto;
  animation: blink-live 1.4s ease-in-out infinite;
}
@keyframes blink-live {
  0%, 100% { opacity: 1; }
  50%      { opacity: 0.4; }
}
</style>
