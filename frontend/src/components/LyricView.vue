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
  // 不立刻清空 lines —— 让旧歌词留着，直到新歌词到位再替换
  // 这样切歌瞬间 UI 不会闪空白
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      const r = await api.lyric(neid)
      // 若服务端返回空但本地之前有歌词，且不是同一首 → 直接判定无歌词
      const parsed = parseLRC(r.lrc || '', r.tlyric || '')
      lines.value = parsed
      lineEls.value = []
      activeIdx.value = -1
      noLyric.value = parsed.length === 0
      // 拿到了（哪怕是空）就退出，但若 error 字段存在就继续重试
      if (!r.error) {
        loading.value = false
        return
      }
    } catch (e) {
      // 网络错，继续重试
    }
    await sleep(400 * (attempt + 1))
  }
  // 重试都失败：保留旧歌词，仅清 loading
  loading.value = false
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)) }

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
      <button v-if="!loading && radio.current" class="pix-btn ghost mini" style="margin-left:auto"
              @click="loadFor(radio.current.neid)" title="重新拉取歌词">↻</button>
    </div>

    <div v-if="!hasLines && !loading" class="muted no-ly">
      <span v-if="noLyric">这首没有歌词哦～</span>
      <span v-else>没拉到歌词，<a href="#" @click.prevent="radio.current && loadFor(radio.current.neid)" style="color:var(--orange-d)">重试</a></span>
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
.pix-btn.mini { font-size: 9px; padding: 4px 6px; box-shadow: 2px 2px 0 var(--ink); }
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
