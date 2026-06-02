<script setup>
/**
 * 替代原 ChatPanel：在 FM 页里展示自己工位的留言板。
 * 大厅聊天已经搬到 Floor。
 */
import { ref, watch, nextTick, computed, onMounted } from 'vue'
import { auth } from '../api.js'
import { useRadioStore } from '../stores/radio.js'
import { pickColor } from '../utils.js'

const radio = useRadioStore()
const input = ref('')
const listRef = ref(null)
const me = computed(() => auth.nickname)
const messages = computed(() => radio.walls[me.value] || [])

function send() {
  const v = input.value.trim()
  if (!v || !me.value) return
  radio.wallPost(me.value, v.slice(0, 140))
  input.value = ''
}
function fmtClock(ts) {
  if (!ts) return ''
  const d = new Date(ts)
  return `${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}`
}

onMounted(() => { if (me.value) radio.loadWall(me.value) })

watch(() => messages.value.length, async () => {
  await nextTick()
  if (listRef.value) listRef.value.scrollTop = listRef.value.scrollHeight
}, { immediate: true })
</script>

<template>
  <div class="pix-card">
    <div class="head">
      <span class="pix-h">▼ MY WALL</span>
      <span class="muted" style="font-size:12px">回 floor 看大厅聊天</span>
    </div>
    <div ref="listRef" class="pix-scroll wall-list">
      <div v-if="!messages.length" class="muted" style="text-align:center;padding:24px 0;font-size:14px">
        还没人给你留言，去大厅勾搭一下吧
      </div>
      <div v-for="(m, i) in messages" :key="i" class="line">
        <span class="time muted">{{ fmtClock(m.ts) }}</span>
        <span class="nick" :style="{ color: pickColor(m.nick).bg }">{{ m.nick }}</span>
        <span style="color:var(--ink-mute)"> &gt; </span>
        <span>{{ m.content }}</span>
      </div>
    </div>
    <div class="row" style="gap:8px;margin-top:10px">
      <input
        class="pix-input"
        v-model="input"
        maxlength="140"
        @keydown.enter="send"
        placeholder="给自己留张便签…"
      />
      <button class="pix-btn" :disabled="!input.trim()" @click="send">POST</button>
    </div>
  </div>
</template>

<style scoped>
.head {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 8px;
}
.wall-list {
  height: 220px;
  overflow-y: auto;
  padding: 10px 12px;
  background: var(--bg-soft);
  border: 2px solid var(--ink);
  font-size: 16px; line-height: 1.5;
}
.line { word-break: break-word; padding: 2px 0; }
.line .time { font-family: var(--font-pix); font-size: 9px; margin-right: 6px; }
.line .nick { font-weight: bold; }
</style>
