<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { auth } from '../api.js'
import { useRadioStore } from '../stores/radio.js'
import { deskOf, buildSlots, grid } from '../desks/_registry.js'
import Avatar from '../components/Avatar.vue'
import LobbyChat from '../components/LobbyChat.vue'
import WallBoard from '../components/WallBoard.vue'

const radio = useRadioStore()
const router = useRouter()
const draftStatus = ref(radio.statusText || '')
const wallTarget = ref('')

onMounted(() => {
  if (auth.token) radio.initSocket()
  radio.setLocation('floor')
})

function logout() {
  radio.closeSocket()
  auth.clear()
}
function saveStatus() { radio.setStatusText(draftStatus.value || '') }
function enterBar() { router.push('/fm') }

function openWall(nick) {
  if (!nick) return
  wallTarget.value = nick
}
function closeWall() { wallTarget.value = '' }

// 最近收到的戳一下，按发送方索引（显示在他的工位上方）
const pokeFor = computed(() => {
  const map = {}
  for (const p of radio.pokes) map[p.from] = p
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
              <span class="bar-screen-text">{{ radio.current ? radio.current.name : 'OFF AIR' }}</span>
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
          </div>
          <div class="me-row">
            <Avatar :nick="auth.nickname" size="sm"/>
            <span style="font-size:15px">{{ auth.nickname }}</span>
            <button class="pix-btn ghost" style="font-size:8px;padding:6px 8px;margin-left:auto" @click="logout">EXIT</button>
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
              :class="{ vacant: !s.occupied }"
              @click="openWall(s.nick)"
            >
              <component
                :is="deskOf(s.nick)"
                :nick="s.nick"
                :text="presenceOf(s.nick).text || ''"
                :online="isOnline(s.nick)"
                :location="presenceOf(s.nick).location || ''"
                :is-me="s.nick === auth.nickname"
                :poke="s.nick === auth.nickname ? null : (pokeFor[s.nick] || null)"
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
}
.me-row { display: flex; align-items: center; gap: 8px; }
.status-input { display: flex; gap: 6px; }
.status-input .pix-input { flex: 1; }

/* —— Floor 卡片 + 网格 —— */
.floor-card { padding: 10px; position: relative; }
.stage-wrap {
  display: flex; justify-content: center;
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
}
.slot {
  position: relative;
  cursor: pointer;
  transition: transform 0.08s;
}
.slot:hover:not(.vacant) { transform: translate(-2px, -2px); }
.slot.vacant { cursor: default; }

.footer { text-align: center; font-size: 13px; letter-spacing: 1px; }

@media (max-width: 980px) {
  .topbar { grid-template-columns: 1fr; }
  .stage-wrap { padding: 14px; overflow-x: auto; }
}
</style>
