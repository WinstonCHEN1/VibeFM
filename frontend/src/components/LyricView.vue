<script setup>
import { ref, watch, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRadioStore } from '../stores/radio.js'
import { api } from '../api.js'
import { parseLRC, findActiveLyric } from '../utils.js'

const radio = useRadioStore()

const lines = ref([])
const activeIdx = ref(-1)
const loading = ref(false)
const noLyric = ref(false)
const listRef = ref(null)
const lineEls = ref([])

let pollTimer = null
let lastNeid = null

function setLineEl(el, idx) {
  if (el) lineEls.value[idx] = el
}

async function loadFor(neid) {
  if (!neid) { lines.value = []; noLyric.value = true; return }
  loading.value = true
  noLyric.value = false
  lines.value = []
  lineEls.value = []
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
  }
}

function scrollToActive() {
  const list = listRef.value
  const node = lineEls.value[activeIdx.value]
  if (!list || !node) return
  const target = node.offsetTop - list.clientHeight / 2 + node.clientHeight / 2
  list.scrollTo({ top: Math.max(0, target), behavior: 'smooth' })
}

// 数据加载完 / 当前行变化时，等 DOM 渲染好再滚
watch(activeIdx, async () => {
  await nextTick()
  scrollToActive()
})

// 歌词加载完成（但还没有 active 行）时，先把视图顶到第 0 行
watch(lines, async (val) => {
  if (val.length === 0) return
  await nextTick()
  if (listRef.value) listRef.value.scrollTop = 0
  // 立刻算一次 active
  tick()
})

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
      <div class="ly-spacer"></div>
      <div v-for="(ln, i) in lines"
           :key="i"
           :ref="el => setLineEl(el, i)"
           class="ly-line"
           :class="{ active: i === activeIdx, prev: i < activeIdx, next: i > activeIdx }">
        <div class="ly-text">{{ ln.text }}</div>
        <div v-if="ln.tr" class="ly-tr">{{ ln.tr }}</div>
      </div>
      <div class="ly-spacer"></div>
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
  padding: 0 12px;
  background: var(--bg-soft);
  border: 2px solid var(--ink);
}
.ly-spacer { height: 90px; }
.ly-line {
  text-align: center;
  padding: 8px 0;
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
.ly-line.prev { opacity: 0.4; }
.ly-line.next { opacity: 0.55; }
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
  .ly-scroll { height: 180px; }
  .ly-spacer { height: 70px; }
  .ly-text { font-size: 16px; }
  .ly-line.active .ly-text { font-size: 18px; }
}
</style>
