<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRadioStore } from '../stores/radio.js'
import { api } from '../api.js'
import { fmtTime, pickColor } from '../utils.js'
import { ensureAudio, ensureAnalyser, resumeCtx } from '../audio.js'
import Avatar from './Avatar.vue'

const radio = useRadioStore()
const playProgress = ref(0)
const isPaused = ref(true)
const volume = ref(parseFloat(localStorage.getItem('fm_vol') || '0.8'))
const muted = ref(localStorage.getItem('fm_mute') === '1')
let progressTimer = null

const audio = ensureAudio()

function applyVolume() {
  audio.volume = volume.value
  audio.muted = muted.value
}

function onVolumeChange() {
  applyVolume()
  localStorage.setItem('fm_vol', String(volume.value))
  if (muted.value && volume.value > 0) {
    muted.value = false
    localStorage.setItem('fm_mute', '0')
  }
}

function toggleMute() {
  muted.value = !muted.value
  localStorage.setItem('fm_mute', muted.value ? '1' : '0')
  applyVolume()
}

function applySong(song) {
  if (!song) return
  audio.src = song.url
  applyVolume()
  const startedClient = song.started_at - radio.serverOffsetMs
  const offsetSec = Math.max(0, (Date.now() - startedClient) / 1000)
  try { audio.currentTime = offsetSec } catch (_) {}
  audio.play().then(() => {
    isPaused.value = false
    radio.needUnlock = false
    ensureAnalyser()
    resumeCtx()
  }).catch(() => {
    radio.needUnlock = true
    isPaused.value = true
  })
}

function onSongEvent(e) { applySong(e.detail); radio.current = e.detail }

function tick() {
  if (radio.current) {
    playProgress.value = audio.currentTime
    isPaused.value = audio.paused
  }
}

function unlock() {
  audio.play().then(() => {
    radio.needUnlock = false
    isPaused.value = false
    ensureAnalyser()
    resumeCtx()
  }).catch(()=>{})
}

async function doSkip() {
  try { await api.skip() } catch (e) { /* TODO toast */ }
}

const progressPct = computed(() => {
  if (!radio.current || !radio.current.duration) return 0
  return Math.min(100, (playProgress.value / radio.current.duration) * 100)
})

const requesterColor = computed(() => pickColor(radio.current?.requester_nick))

onMounted(() => {
  window.addEventListener('fm:songChange', onSongEvent)
  progressTimer = setInterval(tick, 500)
  radio.refreshState()
})
onUnmounted(() => {
  window.removeEventListener('fm:songChange', onSongEvent)
  clearInterval(progressTimer)
})
</script>

<template>
  <div class="pix-card now-playing">
    <div v-if="radio.current" class="np-grid">
      <div class="np-cover-wrap">
        <div class="cover-frame" :class="{ 'paused': isPaused }">
          <img v-if="radio.current.cover_url" :src="radio.current.cover_url" class="cover-img spin" :class="{ paused: isPaused }" referrerpolicy="no-referrer"/>
          <div v-else class="cover-fallback spin" :class="{ paused: isPaused }"></div>
          <div class="cover-hole"></div>
        </div>
      </div>

      <div class="np-info">
        <div class="row" style="gap:8px;flex-wrap:wrap">
          <span class="pix-tag warn">▶ NOW PLAYING</span>
          <span v-if="radio.current.requester_nick" class="row" style="gap:6px;font-size:14px" :style="{ color: requesterColor.bg }">
            <span style="color:var(--ink-mute)">requested by</span>
            <Avatar :nick="radio.current.requester_nick" size="sm"/>
            <span style="color:var(--ink)">{{ radio.current.requester_nick }}</span>
          </span>
        </div>
        <div class="np-title">{{ radio.current.title }}</div>
        <div class="np-artist">{{ radio.current.artist }}</div>

        <div style="margin-top:14px">
          <div class="bar-track">
            <div class="bar-fill" :style="{ width: progressPct + '%' }"></div>
          </div>
          <div class="row" style="justify-content:space-between;font-size:14px;margin-top:4px;color:var(--ink-soft)">
            <span>{{ fmtTime(playProgress) }}</span>
            <span>{{ fmtTime(radio.current.duration) }}</span>
          </div>
        </div>
      </div>
    </div>

    <div v-else style="padding:24px;text-align:center" class="muted">
      <div class="pix-h sm">▒ NO SIGNAL ▒</div>
      <div style="margin-top:8px;font-size:15px">电台准备中… 点首歌让它转起来</div>
    </div>

    <div v-if="radio.needUnlock" style="margin-top:12px;padding:10px;background:#FAEEDA;border:2px dashed var(--ink)">
      <span class="pix-h sm">! AUTOPLAY BLOCKED</span>
      <span style="margin-left:10px">浏览器拦截了自动播放，</span>
      <button class="pix-btn ghost" style="font-size:8px;padding:6px 8px;margin-left:6px" @click="unlock">CLICK TO PLAY</button>
    </div>

    <div class="row controls-row">
      <button class="pix-btn ghost" @click="doSkip">≫ SKIP</button>
      <div class="vol-row">
        <button class="vol-icon-btn" @click="toggleMute" :title="muted ? '取消静音' : '静音'">
          <span v-if="muted || volume === 0">×</span>
          <span v-else-if="volume < 0.34">▎</span>
          <span v-else-if="volume < 0.67">▍</span>
          <span v-else>▌</span>
        </button>
        <input type="range" min="0" max="1" step="0.01" v-model.number="volume"
               @input="onVolumeChange" class="vol-slider"
               :class="{ muted: muted }"/>
        <span class="vol-num">{{ muted ? '--' : Math.round(volume * 100) }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.np-grid {
  display: grid;
  grid-template-columns: 140px 1fr;
  gap: 18px;
  align-items: flex-start;
}
.np-cover-wrap { display: flex; justify-content: center; }
.cover-frame {
  width: 140px; height: 140px;
  background: var(--ink);
  border: 3px solid var(--ink);
  border-radius: 50%;
  position: relative;
  overflow: hidden;
}
.cover-img, .cover-fallback {
  width: 100%; height: 100%;
  border-radius: 50%;
  object-fit: cover;
  display: block;
}
.cover-fallback {
  background: linear-gradient(45deg, var(--orange) 25%, var(--orange-d) 25%, var(--orange-d) 50%, var(--orange) 50%, var(--orange) 75%, var(--orange-d) 75%);
  background-size: 16px 16px;
}
.cover-hole {
  position: absolute;
  left: 50%; top: 50%;
  transform: translate(-50%, -50%);
  width: 28px; height: 28px;
  background: var(--bg-card);
  border: 2px solid var(--ink);
  border-radius: 50%;
}
.cover-hole::after {
  content: ''; position: absolute; left: 50%; top: 50%;
  transform: translate(-50%, -50%);
  width: 6px; height: 6px;
  background: var(--ink); border-radius: 50%;
}
.np-info { min-width: 0; }
.np-title {
  font-size: 26px; line-height: 1.15; margin-top: 10px;
  font-weight: bold; word-break: break-word;
}
.np-artist { font-size: 18px; color: var(--ink-soft); margin-top: 2px; }

.controls-row {
  margin-top: 14px;
  gap: 12px;
  flex-wrap: wrap;
  align-items: center;
}
.vol-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
}
.vol-icon-btn {
  font-family: var(--font-pix);
  font-size: 14px;
  width: 30px; height: 30px;
  background: var(--bg-card);
  border: 2px solid var(--ink);
  box-shadow: 2px 2px 0 var(--ink);
  color: var(--ink);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  cursor: pointer;
}
.vol-icon-btn:active { transform: translate(1px, 1px); box-shadow: 1px 1px 0 var(--ink); }
.vol-slider {
  -webkit-appearance: none; appearance: none;
  width: 130px; height: 14px;
  background: var(--bg-card);
  border: 2px solid var(--ink);
  outline: none; cursor: pointer;
  padding: 0;
}
.vol-slider.muted { opacity: 0.45; }
.vol-slider::-webkit-slider-thumb {
  -webkit-appearance: none; appearance: none;
  width: 14px; height: 18px;
  background: var(--orange);
  border: 2px solid var(--ink);
  cursor: pointer;
}
.vol-slider::-moz-range-thumb {
  width: 14px; height: 18px;
  background: var(--orange);
  border: 2px solid var(--ink);
  cursor: pointer;
}
.vol-num {
  font-family: var(--font-pix);
  font-size: 9px;
  width: 28px;
  text-align: right;
  color: var(--ink-soft);
}

@media (max-width: 720px) {
  .np-grid { grid-template-columns: 1fr; gap: 12px; text-align: center; }
  .np-info { text-align: left; }
  .cover-frame { width: 120px; height: 120px; }
  .vol-row { margin-left: 0; flex: 1 1 100%; }
  .vol-slider { flex: 1; width: auto; }
}
</style>
