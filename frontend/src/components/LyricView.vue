<script setup>
import { ref, watch, computed, onMounted, onUnmounted } from 'vue'
import { useRadioStore } from '../stores/radio.js'
import { api } from '../api.js'
import { parseLRC, findActiveLyric } from '../utils.js'

const radio = useRadioStore()

const lines = ref([])
const activeIdx = ref(-1)
const loading = ref(false)
const noLyric = ref(false)
const listRef = ref(null)

let pollTimer = null
let lastNeid = null

async function loadFor(neid) {
  if (!neid) { lines.value = []; noLyric.value = true; return }
  loading.value = true
  noLyric.value = false
  lines.value = []
  activeIdx.value = -1
  try {
    const r = await api.lyric(neid)
    const parsed = parseLRC(r.lrc || '', r.tlyric || '')
    lines.value = parsed
    noLyric.value = parsed.length === 0
  } catch (e) {
    noLyric.value = true
  } finally {
    loading.value = false
  }
}

function tick() {
  if (!radio.current || lines.value.length === 0) return
  const startedClient = radio.current.started_at - radio.serverOffsetMs
  const cur = (Date.now() - startedClient) / 1000
  const idx = findActiveLyric(lines.value, cur)
  if (idx !== activeIdx.value) {
    activeIdx.value = idx
    scrollToActive()
  }
}

function scrollToActive() {
  const el = listRef.value
  if (!el) return
  const node = el.querySelector(`[data-idx="${activeIdx.value}"]`)
  if (!node) return
  const offset = node.offsetTop - el.clientHeight / 2 + node.clientHeight / 2
  el.scrollTo({ top: Math.max(0, offset), behavior: 'smooth' })
}

watch(() => radio.current?.neid, (neid) => {
  if (neid !== lastNeid) {
    lastNeid = neid
    loadFor(neid)
  }
}, { immediate: true })

onMounted(() => {
  pollTimer = setInterval(tick, 250)
})
onUnmounted(() => {
  clearInterval(pollTimer)
})

const hasLines = computed(() => lines.value.length > 0)
</script>

<template>
  <div class="pix-card lyric-card">
    <div class="row" style="margin-bottom:8px">
      <div class="pix-h">▼ LYRICS</div>
      <span v-if="loading" class="muted" style="margin-left:8px;font-size:13px">loading...</span>
    </div>

    <div v-if="!hasLines && !loading" class="muted no-ly">
      <span v-if="noLyric">这首没有歌词哦～</span>
      <span v-else>等一下，找歌词中</span>
    </div>

    <div v-else ref="listRef" class="ly-scroll pix-scroll">
      <div v-for="(ln, i) in lines" :key="i" :data-idx="i"
           class="ly-line"
           :class="{ active: i === activeIdx, prev: i < activeIdx, next: i > activeIdx }">
        <div class="ly-text">{{ ln.text }}</div>
        <div v-if="ln.tr" class="ly-tr">{{ ln.tr }}</div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.lyric-card { display: flex; flex-direction: column; }
.no-ly {
  text-align: center;
  padding: 30px 0;
  font-size: 16px;
}
.ly-scroll {
  height: 220px;
  overflow-y: auto;
  padding: 24px 12px;
  background: var(--bg-soft);
  border: 2px solid var(--ink);
  scroll-behavior: smooth;
}
.ly-line {
  text-align: center;
  padding: 6px 0;
  transition: opacity 0.3s, transform 0.3s, color 0.3s;
}
.ly-text {
  font-size: 17px;
  line-height: 1.3;
  color: var(--ink-mute);
  word-break: break-word;
}
.ly-tr {
  font-size: 14px;
  color: var(--ink-mute);
  margin-top: 2px;
  opacity: 0.7;
}
.ly-line.prev { opacity: 0.45; }
.ly-line.next { opacity: 0.65; }
.ly-line.active .ly-text {
  color: var(--ink);
  font-size: 19px;
  font-weight: bold;
  letter-spacing: 1px;
}
.ly-line.active .ly-tr {
  color: var(--ink-soft);
  opacity: 1;
}
@media (max-width: 720px) {
  .ly-scroll { height: 180px; padding: 20px 8px; }
  .ly-text { font-size: 16px; }
  .ly-line.active .ly-text { font-size: 18px; }
}
</style>
