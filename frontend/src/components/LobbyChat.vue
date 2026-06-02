<script setup>
import { ref, nextTick, watch, computed, onMounted, onUnmounted } from 'vue'
import { useRadioStore } from '../stores/radio.js'
import { pickColor } from '../utils.js'

const radio = useRadioStore()
const input = ref('')
const listRef = ref(null)
const flash = ref(false)
let flashTimer = null

function send() {
  const v = input.value.trim()
  if (!v) return
  radio.sendChat(v.slice(0, 200))
  input.value = ''
  radio.clearChatUnread()
}

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
  return `${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}`
}

// 新消息：滚到底 + 卡片闪一下 + 进 floor 时清未读
watch(() => radio.chats.length, async (n, o) => {
  await nextTick()
  if (listRef.value) listRef.value.scrollTop = listRef.value.scrollHeight
  if (n > o) {
    flash.value = true
    clearTimeout(flashTimer)
    flashTimer = setTimeout(() => { flash.value = false }, 1200)
  }
}, { immediate: true })

onMounted(() => radio.clearChatUnread())
onUnmounted(() => {
  radio.clearChatUnread()
  clearTimeout(flashTimer)
})
</script>

<template>
  <div class="lobby-chat pix-card" :class="{ flash }">
    <div class="head">
      <span class="pix-h">▼ LOBBY CHAT</span>
      <span class="head-r">
        <span v-if="radio.chatUnread" class="unread-pill">+{{ radio.chatUnread }}</span>
        <span class="muted" style="font-size:12px">最近 20 条 · 全场可见</span>
      </span>
    </div>
    <div ref="listRef" class="chat-list pix-scroll" @scroll="radio.clearChatUnread()">
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
             @keydown.enter="send"
             @focus="radio.clearChatUnread()"
             placeholder="press ENTER to send..."/>
      <button class="pix-btn" :disabled="!input.trim()" @click="send">SEND</button>
    </div>
  </div>
</template>

<style scoped>
.lobby-chat { display: flex; flex-direction: column; transition: box-shadow 0.3s; }
.lobby-chat.flash { animation: chatFlash 1.2s ease-out; }
@keyframes chatFlash {
  0%   { box-shadow: 4px 4px 0 var(--ink), 0 0 0 0 rgba(232,148,90,0); }
  20%  { box-shadow: 4px 4px 0 var(--ink), 0 0 14px 3px rgba(232,148,90,0.85); }
  100% { box-shadow: 4px 4px 0 var(--ink), 0 0 0 0 rgba(232,148,90,0); }
}
.head {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 8px;
}
.head-r { display: flex; align-items: center; gap: 8px; }
.unread-pill {
  font-family: var(--font-pix);
  font-size: 8px;
  background: var(--orange-d);
  color: var(--bg-card);
  border: 2px solid var(--ink);
  padding: 2px 5px;
  letter-spacing: 1px;
  animation: pulse-pill 1.4s ease-in-out infinite;
}
@keyframes pulse-pill {
  0%, 100% { transform: scale(1); }
  50%      { transform: scale(1.08); }
}
.chat-list {
  height: 200px;
  overflow-y: auto;
  padding: 10px 12px;
  background: var(--bg-soft);
  border: 2px solid var(--ink);
  font-size: 17px; line-height: 1.5;
}
.chat-line { word-break: break-word; }
.chat-line .time { font-family: var(--font-pix); font-size: 9px; margin-right: 6px; }
.chat-line .nick { font-weight: bold; }
.chat-line.historic { opacity: 0.62; }
.divider {
  display: flex; align-items: center; gap: 8px; margin: 8px 0;
  font-family: var(--font-pix); font-size: 8px; letter-spacing: 1px;
  color: var(--ink-mute);
}
.divider .line { flex: 1; height: 0; border-top: 1px dashed var(--ink-mute); }
.divider .text { white-space: nowrap; }
.divider.mid { color: var(--orange-d); }
.divider.mid .line { border-top-color: var(--orange-d); }
</style>
