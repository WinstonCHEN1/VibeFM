<script setup>
import { ref, nextTick, watch } from 'vue'
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

watch(() => radio.chats.length, async () => {
  await nextTick()
  if (listRef.value) listRef.value.scrollTop = listRef.value.scrollHeight
})
</script>

<template>
  <div class="pix-card">
    <div class="pix-h" style="margin-bottom:10px">▼ CHAT</div>
    <div ref="listRef" class="pix-scroll chat-list">
      <div v-if="radio.chats.length === 0" class="muted" style="text-align:center;padding:20px 0">
        说点什么吧～
      </div>
      <div v-for="(c, i) in radio.chats" :key="i" class="chat-line">
        <span :style="{ color: pickColor(c.nick).bg, fontWeight:'bold' }">{{ c.nick }}</span>
        <span style="color:var(--ink-mute)"> &gt; </span>
        <span>{{ c.content }}</span>
      </div>
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
</style>
