<script setup>
import { ref, nextTick, watch, computed } from 'vue'
import { useRadioStore } from '../stores/radio.js'
import { pickColor } from '../utils.js'

const radio = useRadioStore()
const input = ref('')
const listRef = ref(null)

function send() {
  const v = input.value.trim()
  if (!v) return
  radio.sendChat(v.slice(0, 200))
  input.value = ''
}

// 找到最后一条 history 消息的索引——后面紧接着画"以下是新消息"分隔线
const lastHistoryIdx = computed(() => {
  let idx = -1
  for (let i = 0; i < radio.chats.length; i++) {
    if (radio.chats[i].history) idx = i
    else break
  }
  return idx
})

const hasHistory = computed(() => lastHistoryIdx.value >= 0)
const hasNew = computed(() => radio.chats.some(c => !c.history))

function fmtClock(ts) {
  if (!ts) return ''
  const d = new Date(ts)
  const hh = String(d.getHours()).padStart(2, '0')
  const mm = String(d.getMinutes()).padStart(2, '0')
  return `${hh}:${mm}`
}

watch(() => radio.chats.length, async () => {
  await nextTick()
  if (listRef.value) listRef.value.scrollTop = listRef.value.scrollHeight
}, { immediate: true })
</script>

<template>
  <div class="pix-card">
    <div class="pix-h" style="margin-bottom:10px">▼ CHAT</div>
    <div ref="listRef" class="pix-scroll chat-list">
      <div v-if="radio.chats.length === 0" class="muted" style="text-align:center;padding:20px 0">
        说点什么吧～
      </div>

      <div v-if="hasHistory" class="divider top">
        <span class="line"></span>
        <span class="text">最近历史 ({{ lastHistoryIdx + 1 }})</span>
        <span class="line"></span>
      </div>

      <template v-for="(c, i) in radio.chats" :key="i">
        <div class="chat-line" :class="{ historic: c.history }">
          <span class="time muted">{{ fmtClock(c.ts) }}</span>
          <span class="nick" :style="{ color: pickColor(c.nick).bg }">{{ c.nick }}</span>
          <span style="color:var(--ink-mute)"> &gt; </span>
          <span>{{ c.content }}</span>
        </div>
        <div v-if="hasHistory && hasNew && i === lastHistoryIdx" class="divider mid">
          <span class="line"></span>
          <span class="text">新消息</span>
          <span class="line"></span>
        </div>
      </template>
    </div>
    <div class="row" style="gap:8px;margin-top:10px">
      <input class="pix-input" v-model="input" maxlength="200"
             @keydown.enter="send" placeholder="press ENTER to send..."/>
      <button class="pix-btn" :disabled="!input.trim()" @click="send">SEND</button>
    </div>
  </div>
</template>

<style scoped>
.chat-list {
  height: 220px;
  overflow-y: auto;
  padding: 10px 12px;
  background: var(--bg-soft);
  border: 2px solid var(--ink);
  font-size: 17px; line-height: 1.5;
}
.chat-line { word-break: break-word; }
.chat-line .time {
  font-family: var(--font-pix);
  font-size: 9px;
  margin-right: 6px;
}
.chat-line .nick { font-weight: bold; }
.chat-line.historic { opacity: 0.62; }
.divider {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 8px 0;
  font-family: var(--font-pix);
  font-size: 8px;
  letter-spacing: 1px;
  color: var(--ink-mute);
}
.divider .line {
  flex: 1; height: 0;
  border-top: 1px dashed var(--ink-mute);
}
.divider .text { white-space: nowrap; }
.divider.mid { color: var(--orange-d); }
.divider.mid .line { border-top-color: var(--orange-d); }
</style>
