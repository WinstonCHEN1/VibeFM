<script setup>
import { computed, ref, watch, nextTick } from 'vue'
import { auth } from '../api.js'
import { useRadioStore } from '../stores/radio.js'
import { pickColor } from '../utils.js'
import Avatar from './Avatar.vue'

const props = defineProps({
  target: { type: String, required: true },
})
const emit = defineEmits(['close'])

const radio = useRadioStore()
const input = ref('')
const listRef = ref(null)

const POKE_EMOJIS = ['👋', '☕', '🍻', '🎵', '🔥', '✨']

const messages = computed(() => radio.walls[props.target] || [])
const presence = computed(() => radio.presence[props.target] || {})
const online = computed(() =>
  radio.onlineList.includes(props.target) || props.target === auth.nickname
)
const isMe = computed(() => props.target === auth.nickname)

function send() {
  const v = input.value.trim()
  if (!v) return
  radio.wallPost(props.target, v.slice(0, 140))
  input.value = ''
}
function poke(e) {
  if (isMe.value) return
  radio.poke(props.target, e)
}
function fmtClock(ts) {
  if (!ts) return ''
  const d = new Date(ts)
  return `${String(d.getHours()).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}`
}
function close() { emit('close') }

watch(() => messages.value.length, async () => {
  await nextTick()
  if (listRef.value) listRef.value.scrollTop = listRef.value.scrollHeight
}, { immediate: true })

radio.loadWall(props.target)
</script>

<template>
  <div class="wall-mask" @click.self="close">
    <div class="wall-card pix-card">
      <div class="wall-head">
        <Avatar :nick="target" size="lg"/>
        <div style="flex:1;min-width:0">
          <div class="pix-h">{{ target }} 的工位</div>
          <div class="muted" style="font-size:13px;margin-top:2px">
            <span class="dot" :class="{ off: !online, bar: presence.location === 'bar' }"></span>
            <span v-if="!online">离线</span>
            <span v-else-if="presence.location === 'bar'">在酒馆</span>
            <span v-else>在工位 · {{ presence.text || 'vibing' }}</span>
          </div>
        </div>
        <button class="pix-btn ghost" style="font-size:8px;padding:6px 8px" @click="close">CLOSE</button>
      </div>

      <div v-if="!isMe" class="poke-bar">
        <span class="muted" style="font-size:13px">戳一下 →</span>
        <button v-for="e in POKE_EMOJIS" :key="e" class="poke-btn" @click="poke(e)">{{ e }}</button>
      </div>

      <div class="pix-h sm" style="margin:14px 0 6px">▼ MESSAGES · {{ messages.length }}/20</div>
      <div ref="listRef" class="wall-list pix-scroll">
        <div v-if="!messages.length" class="muted" style="text-align:center;padding:18px 0;font-size:14px">
          还没人留言，做第一个吧～
        </div>
        <div v-for="(m, i) in messages" :key="i" class="wall-line">
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
          :placeholder="isMe ? '给自己留张便签…' : `给 ${target} 留个言…`"
        />
        <button class="pix-btn" :disabled="!input.trim()" @click="send">POST</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.wall-mask {
  position: fixed; inset: 0;
  background: rgba(61,46,31,0.45);
  display: flex; align-items: center; justify-content: center;
  z-index: 50;
  padding: 20px;
  animation: fade 0.15s ease-out;
}
@keyframes fade { from { opacity: 0; } to { opacity: 1; } }
.wall-card {
  width: 460px; max-width: 100%;
  max-height: 80vh;
  display: flex; flex-direction: column;
}
.wall-head {
  display: flex; align-items: center; gap: 10px;
  padding-bottom: 10px;
  border-bottom: 2px solid var(--ink);
}
.dot {
  display: inline-block; width: 8px; height: 8px;
  background: var(--green); border: 1px solid var(--ink);
  vertical-align: middle; margin-right: 4px;
}
.dot.off { background: var(--bg-soft); }
.dot.bar { background: var(--orange-d); }

.poke-bar {
  display: flex; align-items: center; gap: 6px;
  margin-top: 12px;
  padding: 8px 10px;
  background: var(--bg-soft);
  border: 2px solid var(--ink);
}
.poke-btn {
  font-size: 18px;
  background: var(--bg-card);
  border: 2px solid var(--ink);
  box-shadow: 2px 2px 0 var(--ink);
  padding: 2px 6px;
  cursor: pointer;
  transition: transform 0.05s;
}
.poke-btn:hover  { background: var(--bg); }
.poke-btn:active { transform: translate(1px, 1px); box-shadow: 1px 1px 0 var(--ink); }

.wall-list {
  flex: 1;
  overflow-y: auto;
  background: var(--bg-soft);
  border: 2px solid var(--ink);
  padding: 10px 12px;
  font-size: 16px; line-height: 1.5;
  min-height: 180px;
  max-height: 50vh;
}
.wall-line { word-break: break-word; padding: 2px 0; }
.wall-line .time { font-family: var(--font-pix); font-size: 9px; margin-right: 6px; }
.wall-line .nick { font-weight: bold; }
</style>
