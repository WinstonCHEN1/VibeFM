<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { auth, api } from '../api.js'
import { useRadioStore } from '../stores/radio.js'
import { deskOf, buildSlots, grid } from '../desks/_registry.js'
import { playSong, stopSong } from '../audio.js'
import Avatar from '../components/Avatar.vue'
import LobbyChat from '../components/LobbyChat.vue'
import WallBoard from '../components/WallBoard.vue'

const radio = useRadioStore()
const router = useRouter()
const draftStatus = ref(radio.statusText || '')
const wallTarget = ref('')
const needUnlock = ref(false)

onMounted(() => {
  if (auth.token) radio.initSocket()
  radio.setLocation('floor')
  // 如果之前打开了 LISTEN 且当前已有歌，进 floor 自动续上
  if (radio.listening && radio.current) {
    playSong(radio.current, {
      serverOffsetMs: radio.serverOffsetMs,
      onNeedUnlock: v => { needUnlock.value = v },
    })
  }
  window.addEventListener('fm:songChange', onSongEvent)
})
onUnmounted(() => {
  window.removeEventListener('fm:songChange', onSongEvent)
})

function onSongEvent(e) {
  if (!radio.listening) return
  const song = e.detail
  if (!song) { stopSong(); return }
  playSong(song, {
    serverOffsetMs: radio.serverOffsetMs,
    onNeedUnlock: v => { needUnlock.value = v },
  })
}

function toggleListen() {
  if (radio.listening) {
    radio.setListening(false)
    stopSong()
    needUnlock.value = false
    return
  }
  radio.setListening(true)
  if (radio.current) {
    playSong(radio.current, {
      serverOffsetMs: radio.serverOffsetMs,
      onNeedUnlock: v => { needUnlock.value = v },
    })
  } else {
    // OFF AIR：戳一下后端让它播下一首（兜底歌单），然后等 song_change 事件到达
    api.skip().catch(() => {})
  }
}

function logout() {
  radio.closeSocket()
  stopSong()
  auth.clear()
}
function saveStatus() { radio.setStatusText(draftStatus.value || '') }
function enterBar() { router.push('/fm') }

function openWall(nick) {
  if (!nick) return
  wallTarget.value = nick
}
function closeWall() { wallTarget.value = '' }

// 当前工位上要显示的气泡（按"被戳人"索引，全场可见）
const pokeFor = computed(() => {
  const map = {}
  for (const p of radio.pokes) map[p.to] = p
  return map
})

// "应当出现在 floor 上的人"：所有在线 + 自己
const visibleNicks = computed(() => {
  const set = new Set()
  for (const n of radio.onlineList) set.add(n)
  if (auth.nickname) set.add(auth.nickname)
  return [...set]
})

const slots = computed(() => buildSlots(visibleNicks.value))

function presenceOf(nick) { return radio.presence[nick] || {} }
function isOnline(nick)   { return radio.onlineList.includes(nick) || nick === auth.nickname }

const inBarCount = computed(() =>
  Object.values(radio.presence).filter(p => p.location === 'bar').length
)
const onlineDetails = computed(() => {
  const list = []
  for (const n of radio.onlineList) {
    list.push({
      nick: n,
      location: presenceOf(n).location || 'floor',
      text: presenceOf(n).text || '',
      listening: !!presenceOf(n).listening,
    })
  }
  return list
})
</script>

<template>
  <div class="page">
    <div class="dot-bg page-bg"></div>

    <div class="container">
      <!-- 顶部：左 ONLINE / 中 BAR(进 FM) / 右 ME -->
      <header class="topbar">
        <div class="online-card pix-card tight">
          <div class="online-head">
            <span class="dot-on"></span>
            <span class="pix-h sm">ONLINE</span>
            <span class="muted" style="margin-left:auto;font-size:13px">
              {{ radio.onlineList.length }} · 酒馆 {{ inBarCount }}
            </span>
          </div>
          <div class="online-list pix-scroll">
            <div v-if="!onlineDetails.length" class="muted" style="font-size:14px;padding:4px 0">
              空荡荡的工区…
            </div>
            <div v-for="o in onlineDetails" :key="o.nick" class="online-row">
              <Avatar :nick="o.nick" size="sm"/>
              <span class="who">{{ o.nick }}</span>
              <span v-if="o.listening" class="listening-mark" title="正在听歌">♪</span>
              <span v-if="o.location === 'bar'" class="pix-tag warn" style="font-size:7px">BAR</span>
              <span v-else class="muted small">{{ o.text || 'vibing' }}</span>
            </div>
          </div>
        </div>

        <!-- 中间：FM 收音机方框 -->
        <button class="bar-box" @click="enterBar" :title="radio.current ? radio.current.name : '安静中'">
          <div class="bar-box-inner">
            <div class="bar-screen">
              <span class="bar-screen-dot"></span>
              <span class="bar-screen-text" v-if="radio.current">
                <span class="bar-screen-title">{{ radio.current.title || radio.current.name }}</span>
                <span class="bar-screen-artist" v-if="radio.current.artist"> · {{ radio.current.artist }}</span>
              </span>
              <span class="bar-screen-text muted" v-else>OFF AIR</span>
            </div>
            <div class="bar-knobs">
              <span class="knob"></span>
              <span class="knob"></span>
              <span class="speaker"></span>
              <span class="bar-door">
                <span class="door-knob"></span>
              </span>
            </div>
            <div class="bar-label">FM · THE BAR →</div>
          </div>
        </button>

        <div class="me-card pix-card tight">
          <div class="logo">
            <span style="color:var(--orange-d)">V</span><span>I</span><span style="color:var(--green)">B</span><span>E</span>
            <span style="margin:0 4px">·</span>
            <span style="color:var(--orange)">L</span><span>O</span><span>U</span><span>N</span><span>G</span><span>E</span>
            <span class="logo-tip">想在大厅听歌？点 LISTENING ♪</span>
          </div>
          <div class="me-row">
            <Avatar :nick="auth.nickname" size="sm"/>
            <span style="font-size:15px">{{ auth.nickname }}</span>
            <button
              class="pix-btn listen-btn"
              :class="{ on: radio.listening }"
              style="font-size:8px;padding:6px 8px;margin-left:auto"
              @click="toggleListen"
              :title="radio.listening ? '停止收听' : '在工区也跟着酒馆一起听'"
            >
              <span class="dot"></span>
              {{ radio.listening ? 'LISTENING' : 'LISTEN' }}
            </button>
            <button class="pix-btn ghost" style="font-size:8px;padding:6px 8px" @click="logout">EXIT</button>
          </div>
          <div class="status-input">
            <input
              class="pix-input"
              v-model="draftStatus"
              maxlength="20"
              placeholder="此刻在做什么？(≤20字)"
              @keydown.enter="saveStatus"
            />
            <button class="pix-btn" style="font-size:8px;padding:8px 10px" @click="saveStatus">SAVE</button>
          </div>
          <div v-if="needUnlock && radio.listening" class="unlock-hint" @click="toggleListen">
            浏览器拦了自动播放 · 点 LISTENING 重试
          </div>
        </div>
      </header>

      <!-- 工区：6 格固定 slot，居中 -->
      <section class="floor-card pix-card">
        <div class="stage-wrap">
          <div
            class="stage"
            :style="{
              width:  grid.cols * grid.cellW + (grid.cols - 1) * grid.gap + 'px',
              height: grid.rows * grid.cellH + (grid.rows - 1) * grid.gap + 'px',
              gap: grid.gap + 'px',
              gridTemplateColumns: 'repeat(' + grid.cols + ', ' + grid.cellW + 'px)',
              gridTemplateRows:    'repeat(' + grid.rows + ', ' + grid.cellH + 'px)',
            }"
          >
            <div
              v-for="(s, i) in slots"
              :key="i"
              class="slot"
              :class="{ vacant: !s.occupied, poked: !!pokeFor[s.nick] }"
              @click="openWall(s.nick)"
            >
              <component
                :is="deskOf(s.nick)"
                :nick="s.nick"
                :text="presenceOf(s.nick).text || ''"
                :online="isOnline(s.nick)"
                :location="presenceOf(s.nick).location || ''"
                :is-me="s.nick === auth.nickname"
                :poke="pokeFor[s.nick] || null"
              />
            </div>
          </div>
        </div>
      </section>

      <!-- 大厅聊天 -->
      <LobbyChat/>

      <footer class="footer muted">
        ╱╱ vibe lounge ╱ never goes off air ╱╱
      </footer>

      <!-- 被戳 toast -->
      <div class="toasts" v-if="radio.pokeToasts.length">
        <div v-for="t in radio.pokeToasts" :key="t.id" class="toast">
          <span class="toast-emoji">{{ t.emoji }}</span>
          <span class="toast-from">{{ t.from }}</span>
          <span> 戳了你！</span>
        </div>
      </div>
    </div>

    <WallBoard v-if="wallTarget" :target="wallTarget" @close="closeWall"/>
  </div>
</template>

<style scoped>
.page { min-height: 100%; position: relative; }
.page-bg { position: fixed; inset: 0; pointer-events: none; z-index: 0; }
.container {
  position: relative; z-index: 1;
  max-width: 1100px; margin: 0 auto;
  padding: 14px 16px 28px;
  display: flex; flex-direction: column; gap: 12px;
}

/* —— 顶部三栏 —— */
.topbar {
  display: grid;
  grid-template-columns: 260px 220px minmax(0, 1fr);
  gap: 12px;
  align-items: stretch;
}
.online-card { padding: 8px 10px; }
.online-head {
  display: flex; align-items: center; gap: 6px;
  margin-bottom: 4px;
}
.dot-on {
  width: 9px; height: 9px;
  background: var(--green);
  border: 2px solid var(--ink);
  display: inline-block;
}
.online-list {
  max-height: 110px;
  overflow-y: auto;
  display: flex; flex-direction: column; gap: 2px;
  padding-right: 4px;
}
.online-row {
  display: flex; align-items: center; gap: 8px;
  padding: 2px 0;
  font-size: 14px;
}
.online-row .who { font-family: var(--font-body); }
.online-row .small {
  font-size: 12px;
  margin-left: auto;
  max-width: 130px;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.listening-mark {
  font-family: var(--font-pix);
  font-size: 10px;
  color: var(--orange-d);
  animation: listen-pulse-mark 1.4s ease-in-out infinite;
}
@keyframes listen-pulse-mark {
  0%, 100% { transform: translateY(0); opacity: 0.7; }
  50%      { transform: translateY(-2px); opacity: 1; }
}

/* —— FM 方框（中间，最简单的收音机外观） —— */
.bar-box {
  background: var(--ink);
  color: var(--bg-card);
  border: 3px solid var(--ink);
  box-shadow: 4px 4px 0 var(--orange-d);
  padding: 10px 12px;
  cursor: pointer;
  font-family: var(--font-body);
  text-align: left;
  transition: transform 0.06s, box-shadow 0.06s;
}
.bar-box:hover  { box-shadow: 6px 6px 0 var(--orange-d); }
.bar-box:active { transform: translate(2px, 2px); box-shadow: 2px 2px 0 var(--orange-d); }

.bar-box-inner {
  display: flex; flex-direction: column; gap: 6px;
}
.bar-screen {
  background: #2A1F12;
  border: 2px solid var(--orange-d);
  padding: 4px 8px;
  font-family: var(--font-pix);
  font-size: 9px;
  color: var(--orange);
  letter-spacing: 1px;
  display: flex; align-items: center; gap: 6px;
  overflow: hidden;
}
.bar-screen-dot {
  width: 6px; height: 6px;
  background: var(--orange);
  border-radius: 50%;
  flex-shrink: 0;
  animation: pulse 1.4s ease-in-out infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 0.4; box-shadow: 0 0 0 0 rgba(232,148,90,0); }
  50%      { opacity: 1;   box-shadow: 0 0 6px 2px rgba(232,148,90,0.6); }
}
.bar-screen-text {
  flex: 1;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.bar-screen-title { color: var(--orange); }
.bar-screen-artist { color: var(--olive); }
.bar-knobs {
  display: flex; align-items: center; gap: 6px;
}
.knob {
  width: 12px; height: 12px;
  border-radius: 50%;
  background: var(--orange-d);
  border: 2px solid var(--bg-card);
  flex-shrink: 0;
}
.knob:nth-child(2) { background: var(--orange); }
.speaker {
  flex: 1; height: 12px;
  background-image: repeating-linear-gradient(
    90deg,
    var(--bg-card) 0 2px,
    transparent 2px 5px
  );
}
.bar-door {
  position: relative;
  width: 14px; height: 18px;
  background: #6E3A2A;
  border: 2px solid var(--bg-card);
  flex-shrink: 0;
  background-image: repeating-linear-gradient(
    90deg,
    rgba(0,0,0,0.35) 0 1px,
    transparent 1px 4px
  );
}
.door-knob {
  position: absolute;
  right: 2px; top: 50%;
  width: 3px; height: 3px;
  background: #FFD37A;
  border-radius: 50%;
  transform: translateY(-50%);
}
.bar-box:hover .bar-door { animation: door-open 0.6s ease-in-out; }
@keyframes door-open {
  0%, 100% { transform: perspective(40px) rotateY(0); }
  50%      { transform: perspective(40px) rotateY(-30deg); }
}
.bar-label {
  font-family: var(--font-pix);
  font-size: 9px;
  letter-spacing: 2px;
  color: var(--orange);
  text-align: center;
}

/* —— 我的卡 —— */
.me-card { padding: 8px 10px; display: flex; flex-direction: column; gap: 6px; }
.logo {
  font-family: var(--font-pix);
  font-size: 14px;
  letter-spacing: 2px;
  display: flex; align-items: baseline; gap: 6px; flex-wrap: wrap;
}
.logo-tip {
  font-family: var(--font-body);
  font-size: 12px;
  letter-spacing: 0;
  color: var(--ink-mute);
  white-space: nowrap;
}
.me-row { display: flex; align-items: center; gap: 8px; }
.status-input { display: flex; gap: 6px; }
.status-input .pix-input { flex: 1; }

.listen-btn {
  background: var(--bg-card);
  display: inline-flex; align-items: center; gap: 4px;
}
.listen-btn .dot {
  width: 6px; height: 6px;
  background: var(--ink-mute);
  border: 1px solid var(--ink);
  display: inline-block;
}
.listen-btn.on { background: var(--green); }
.listen-btn.on .dot {
  background: var(--orange-d);
  animation: listen-pulse 1.4s ease-in-out infinite;
}
@keyframes listen-pulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(212,115,62,0); }
  50%      { box-shadow: 0 0 6px 2px rgba(212,115,62,0.7); }
}
.unlock-hint {
  font-size: 12px; color: var(--orange-d);
  background: var(--bg-soft);
  border: 2px dashed var(--orange-d);
  padding: 3px 6px;
  cursor: pointer;
  text-align: center;
}

/* —— Floor 卡片 + 网格 —— */
.floor-card { padding: 10px; position: relative; }
.stage-wrap {
  /* 用 block + overflow-x，避免 flex 居中导致窄屏无法左滑 */
  display: block;
  overflow-x: auto;
  overflow-y: hidden;
  -webkit-overflow-scrolling: touch;
  background: #C99B6E;
  border: 3px solid var(--ink);
  padding: 18px;
  box-shadow: inset 0 0 0 4px #B98856, inset 0 0 0 6px var(--ink);
  background-image:
    repeating-linear-gradient(0deg,  rgba(61,46,31,0.18) 0 2px, transparent 2px 56px),
    repeating-linear-gradient(90deg, rgba(61,46,31,0.10) 0 2px, transparent 2px 84px),
    repeating-linear-gradient(0deg,  transparent 0 28px, rgba(255,255,255,0.04) 28px 56px);
}
.stage {
  display: grid;
  position: relative;
  margin: 0 auto;     /* 容器够宽时居中；不够宽时贴左，左右都能滚 */
}
.slot {
  position: relative;
  cursor: pointer;
  transition: transform 0.08s;
}
.slot:hover:not(.vacant) { transform: translate(-2px, -2px); }
.slot.vacant { cursor: default; }
.slot.poked {
  animation: poke-glow 1.4s ease-in-out infinite;
}
@keyframes poke-glow {
  0%, 100% { filter: drop-shadow(0 0 0 transparent); }
  50%      { filter: drop-shadow(0 0 8px rgba(232,148,90,0.95)); }
}

.footer { text-align: center; font-size: 13px; letter-spacing: 1px; }

.toasts {
  position: fixed;
  right: 18px; bottom: 18px;
  display: flex; flex-direction: column; gap: 8px;
  z-index: 60;
}
.toast {
  background: var(--orange);
  border: 3px solid var(--ink);
  box-shadow: 4px 4px 0 var(--ink);
  padding: 6px 12px;
  font-size: 14px;
  display: flex; align-items: center; gap: 6px;
  animation: toastin 0.3s ease-out;
}
.toast-emoji { font-size: 20px; }
.toast-from { font-weight: bold; }
@keyframes toastin {
  from { transform: translateX(40px); opacity: 0; }
  to   { transform: translateX(0);    opacity: 1; }
}

@media (max-width: 980px) {
  .topbar { grid-template-columns: 1fr; }
  .stage-wrap { padding: 12px; }
}
@media (max-width: 600px) {
  .container { padding: 10px 10px 24px; }
  .stage-wrap { padding: 10px; }
}
</style>
