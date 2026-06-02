<script setup>
/**
 * 默认工位 —— 像素贴图小屋。
 *
 * Props（所有自定义工位都必须接受）：
 *   nick    : 工位主人的昵称
 *   text    : 自填状态文本
 *   online  : 是否在线
 *   location: 'floor' | 'bar' | ''
 *   isMe    : 是否是自己的工位
 *   poke    : { emoji } 收到的戳一下气泡
 *
 * 动效：
 *   - 离线          → 灰掉，椅子空，电脑黑屏
 *   - 在工区(floor) → 小人坐着敲键盘，屏幕滚字
 *   - 在酒馆(bar)   → 椅子空着，屋顶冒一个 ♪，门口出现一个去酒馆的脚印
 *   - 自填带 ☕     → 桌上放一杯咖啡，小人偶尔抿一口
 *   - 自填带 z/zZz/睡 → 屏幕息屏，小人头上 Z
 *   - 自填带 🎧/listening → 头上戴耳机
 */
import { computed } from 'vue'
import Avatar from '../components/Avatar.vue'

const props = defineProps({
  nick:     { type: String, default: '' },
  text:     { type: String, default: '' },
  online:   { type: Boolean, default: false },
  location: { type: String, default: '' },
  isMe:     { type: Boolean, default: false },
  poke:     { type: Object, default: null },
})

const inBar    = computed(() => props.online && props.location === 'bar')
const atDesk   = computed(() => props.online && props.location !== 'bar')
const offline  = computed(() => !props.online)

const txt = computed(() => (props.text || '').toLowerCase())
const sleeping = computed(() => /z+|睡|sleep|afk|🛌|💤/.test(txt.value))
const coffee   = computed(() => /☕|咖啡|coffee|续命/.test(txt.value))
const headphone = computed(() => /🎧|listen|听歌|music/.test(txt.value))
const empty    = computed(() => !props.nick)

const moodLabel = computed(() => {
  if (empty.value) return '空位 · 等待入驻'
  if (offline.value) return 'afk'
  if (inBar.value) return '在酒馆里'
  if (sleeping.value) return '休息中'
  if (coffee.value) return '咖啡 break'
  return props.text || 'vibing'
})
</script>

<template>
  <div class="cube" :class="{ offline, me: isMe, bar: inBar, sleep: sleeping, empty }">
    <!-- 后墙地砖 -->
    <div class="wall"></div>
    <div class="floor"></div>

    <!-- 戳一下 -->
    <div class="bubble" v-if="poke">{{ poke.emoji }}</div>

    <!-- 空位提示 -->
    <div v-if="empty" class="vacancy">
      <div class="vacancy-tag">VACANT</div>
      <div class="vacancy-tip">等一个像素工友</div>
    </div>

    <template v-else>
      <!-- 后墙：海报 + 挂钟（只是装饰） -->
      <div class="poster">
        <span class="ps a"></span>
        <span class="ps b"></span>
        <span class="ps c"></span>
      </div>
      <div class="clock">
        <span class="h"></span>
        <span class="m"></span>
      </div>

      <!-- 去酒馆了：屋顶冒♪ + 椅子空 -->
      <div class="note-out" v-if="inBar">♪</div>

      <!-- 台灯：在线 / 在桌 时点亮 -->
      <div class="lamp">
        <div class="shade"></div>
        <div class="arm"></div>
        <div class="base"></div>
        <div class="light" v-if="atDesk && !sleeping"></div>
      </div>

      <!-- 桌面 + 桌腿 -->
      <div class="desk-top"></div>
      <div class="desk-leg l"></div>
      <div class="desk-leg r"></div>

      <!-- 显示器 -->
      <div class="monitor">
        <div class="screen" :class="{ on: atDesk && !sleeping, sleep: sleeping, dark: offline || inBar }">
          <div class="line a"></div>
          <div class="line b"></div>
          <div class="line c"></div>
          <div class="zzz" v-if="sleeping">z</div>
        </div>
        <div class="stand"></div>
        <div class="keyboard"></div>
      </div>

      <!-- 桌上的咖啡杯（带☕ 状态时出现） -->
      <div class="coffee" v-if="coffee && atDesk">
        <div class="cup"></div>
        <div class="steam s1"></div>
        <div class="steam s2"></div>
      </div>

      <!-- 椅子 -->
      <div class="chair">
        <div class="chair-back"></div>
        <div class="chair-seat"></div>
        <div class="chair-leg"></div>
      </div>

      <!-- 小人：在桌时坐着，去酒馆时不出现 -->
      <div class="person"
           v-if="atDesk"
           :class="{ typing: !sleeping && !coffee, sleeping, sipping: coffee }">
        <div class="head-wrap">
          <Avatar :nick="nick" size="sm"/>
          <div class="headphone" v-if="headphone"></div>
          <div class="zhead" v-if="sleeping">Z</div>
        </div>
        <div class="body"></div>
        <div class="arm-l"></div>
        <div class="arm-r"></div>
      </div>

      <!-- 离开椅子去酒馆的脚印（仅 in bar） -->
      <div class="bar-tag" v-if="inBar">在酒馆</div>

      <!-- 名牌 -->
      <div class="nameplate"><span>{{ nick }}</span></div>

      <!-- 状态气泡 -->
      <div class="status">{{ moodLabel }}</div>
    </template>
  </div>
</template>

<style scoped>
.cube {
  position: relative;
  width: 100%; height: 100%;
  border: 3px solid var(--ink);
  overflow: visible;
  image-rendering: pixelated;
  background: #E9C9A0;
}
.cube.me { box-shadow: 0 0 0 2px var(--orange-d); }
.cube.offline { filter: grayscale(0.65); opacity: 0.6; }
.cube.empty   { background: var(--bg-soft); }

.wall {
  position: absolute; inset: 0;
  background-image:
    repeating-linear-gradient(0deg, rgba(0,0,0,0.05) 0 1px, transparent 1px 14px),
    repeating-linear-gradient(90deg, rgba(0,0,0,0.04) 0 1px, transparent 1px 18px);
  pointer-events: none;
}
.floor {
  position: absolute; left: 0; right: 0; bottom: 0;
  height: 38%;
  background: #B98856;
  border-top: 3px solid var(--ink);
  background-image: repeating-linear-gradient(0deg, rgba(0,0,0,0.18) 0 2px, transparent 2px 14px);
}

/* ========== 空位 ========== */
.vacancy {
  position: absolute; inset: 0;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  gap: 6px;
  color: var(--ink-mute);
}
.vacancy-tag {
  font-family: var(--font-pix);
  font-size: 11px;
  letter-spacing: 2px;
  background: var(--bg-card);
  border: 2px dashed var(--ink-mute);
  padding: 4px 8px;
}
.vacancy-tip { font-size: 14px; color: var(--ink-soft); }

/* ========== 装饰：海报 + 钟 ========== */
.poster {
  position: absolute;
  left: 14px; top: 14px;
  width: 42px; height: 32px;
  background: var(--bg-card);
  border: 2px solid var(--ink);
  display: flex; flex-direction: column; gap: 3px;
  padding: 5px 4px;
}
.poster .ps { display: block; height: 4px; }
.poster .ps.a { background: var(--orange-d); }
.poster .ps.b { background: var(--green); width: 70%; }
.poster .ps.c { background: var(--blue);  width: 50%; }

.clock {
  position: absolute;
  right: 14px; top: 14px;
  width: 22px; height: 22px;
  background: var(--bg-card);
  border: 2px solid var(--ink);
  border-radius: 50%;
}
.clock .h, .clock .m {
  position: absolute; left: 50%; top: 50%;
  background: var(--ink); transform-origin: top center;
}
.clock .h { width: 2px; height: 5px; margin-left: -1px; transform: rotate(60deg); animation: spin 60s linear infinite; }
.clock .m { width: 2px; height: 8px; margin-left: -1px; transform: rotate(0);    animation: spin 6s  linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* ========== 台灯 ========== */
.lamp {
  position: absolute;
  right: 14px; top: 44px;
  width: 26px; height: 42px;
}
.lamp .shade { position: absolute; left: 0; top: 0; width: 26px; height: 12px; background: var(--orange); border: 2px solid var(--ink); border-radius: 9px 9px 1px 1px; }
.lamp .arm   { position: absolute; left: 11px; top: 12px; width: 4px; height: 18px; background: var(--ink); }
.lamp .base  { position: absolute; left: 4px; top: 30px; width: 18px; height: 6px; background: #6E3A2A; border: 2px solid var(--ink); }
.lamp .light {
  position: absolute; left: -10px; top: 10px;
  width: 46px; height: 28px;
  background: radial-gradient(ellipse at 50% 0%, rgba(255,211,122,0.7), transparent 70%);
  pointer-events: none;
  animation: flick 2.6s ease-in-out infinite;
}
@keyframes flick {
  0%, 100% { opacity: 0.85; }
  45%      { opacity: 1; }
  50%      { opacity: 0.6; }
  55%      { opacity: 1; }
}

/* ========== 桌子 + 显示器 ========== */
.desk-top {
  position: absolute;
  left: 14px; right: 14px;
  bottom: 36%;
  height: 9px;
  background: #6E3A2A;
  border: 2px solid var(--ink);
}
.desk-leg {
  position: absolute;
  bottom: calc(36% - 22px);
  width: 5px; height: 18px;
  background: #6E3A2A;
  border: 2px solid var(--ink);
}
.desk-leg.l { left: 22px; }
.desk-leg.r { right: 22px; }

.monitor {
  position: absolute;
  left: 50%;
  bottom: calc(36% + 7px);
  transform: translateX(-50%);
  width: 60px;
}
.screen {
  position: relative;
  width: 60px; height: 38px;
  background: #1F2F1B;
  border: 2px solid var(--ink);
  box-shadow: inset 0 0 0 1px #3A5236;
  overflow: hidden;
}
.screen.dark  { background: #0A1208; box-shadow: none; }
.screen.sleep { background: #15201F; }

.screen .line {
  position: absolute;
  height: 2px; background: #B7E26F;
  transform: scaleX(0); transform-origin: left;
}
.screen.on .line.a { top: 8px;  left: 5px; width: 26px; animation: typing 2.8s steps(8) infinite; }
.screen.on .line.b { top: 16px; left: 5px; width: 38px; animation: typing 2.8s steps(8) infinite 0.3s; }
.screen.on .line.c { top: 24px; left: 5px; width: 18px; animation: typing 2.8s steps(8) infinite 0.6s; }
@keyframes typing {
  0%, 25% { transform: scaleX(0); }
  60%, 90% { transform: scaleX(1); }
  100%    { transform: scaleX(1); }
}
.zzz {
  position: absolute; right: 6px; top: 4px;
  font-family: var(--font-pix);
  font-size: 9px;
  color: #6FA88A;
  animation: zzz 2s ease-in-out infinite;
}
@keyframes zzz {
  0%, 100% { transform: translateY(0); opacity: 0.4; }
  50%      { transform: translateY(-4px); opacity: 1; }
}

.stand    { width: 18px; height: 4px; background: var(--ink); margin: 0 auto; }
.keyboard { width: 46px; height: 5px; background: #3D2E1F; border: 2px solid var(--ink); margin: 4px auto 0; }

/* ========== 椅子 + 小人 ========== */
.chair {
  position: absolute;
  left: 50%; bottom: 4px; transform: translateX(-50%);
  width: 36px; height: 36px;
}
.chair-back { position: absolute; left: 6px; top: 0;  width: 24px; height: 20px; background: #6E3A2A; border: 2px solid var(--ink); }
.chair-seat { position: absolute; left: 0;  top: 18px; width: 36px; height: 7px;  background: #6E3A2A; border: 2px solid var(--ink); }
.chair-leg  { position: absolute; left: 14px; top: 25px; width: 8px; height: 11px; background: var(--ink); }

.person {
  position: absolute;
  left: 50%; bottom: 18px;
  transform: translateX(-50%);
  width: 30px;
  display: flex; flex-direction: column; align-items: center;
  z-index: 2;
}
.person .head-wrap {
  position: relative;
  width: 22px; height: 22px;
  display: flex; align-items: center; justify-content: center;
}
.headphone {
  position: absolute;
  left: -3px; right: -3px; top: -2px;
  height: 8px;
  border: 2px solid var(--ink);
  border-bottom: none;
  border-radius: 10px 10px 0 0;
  background: transparent;
}
.headphone::before, .headphone::after {
  content: '';
  position: absolute; top: 4px;
  width: 4px; height: 6px;
  background: var(--ink);
}
.headphone::before { left: -2px; }
.headphone::after  { right: -2px; }

.zhead {
  position: absolute;
  left: -8px; top: -10px;
  font-family: var(--font-pix);
  font-size: 9px;
  color: var(--ink-soft);
  animation: zzz 2s ease-in-out infinite;
}

.person .body {
  width: 22px; height: 10px;
  background: var(--blue);
  border: 2px solid var(--ink);
  margin-top: -3px;
}

/* 胳膊：典型动效目标 */
.arm-l, .arm-r {
  position: absolute;
  bottom: 4px;
  width: 4px; height: 6px;
  background: var(--blue);
  border: 2px solid var(--ink);
}
.arm-l { left: 1px;  transform-origin: top center; }
.arm-r { right: 1px; transform-origin: top center; }

.person.typing  { animation: bobtype 0.5s ease-in-out infinite; }
.person.typing .arm-l { animation: type-l 0.4s ease-in-out infinite; }
.person.typing .arm-r { animation: type-r 0.4s ease-in-out infinite 0.2s; }
@keyframes bobtype {
  0%, 100% { transform: translate(-50%, 0); }
  50%      { transform: translate(-50%, -1px); }
}
@keyframes type-l {
  0%, 100% { transform: translateY(0) rotate(0); }
  50%      { transform: translateY(-2px) rotate(-12deg); }
}
@keyframes type-r {
  0%, 100% { transform: translateY(0) rotate(0); }
  50%      { transform: translateY(-2px) rotate(12deg); }
}

.person.sleeping { animation: slump 4s ease-in-out infinite; }
@keyframes slump {
  0%, 100% { transform: translate(-50%, 0); }
  50%      { transform: translate(-50%, 2px); }
}

.person.sipping  { animation: sip 2.4s ease-in-out infinite; }
.person.sipping .arm-r { animation: sip-arm 2.4s ease-in-out infinite; }
@keyframes sip {
  0%, 60%, 100% { transform: translate(-50%, 0); }
  30%           { transform: translate(-50%, -1px); }
}
@keyframes sip-arm {
  0%, 60%, 100% { transform: translateY(0) rotate(0); }
  30%           { transform: translateY(-3px) rotate(20deg); }
}

/* ========== 咖啡 ========== */
.coffee {
  position: absolute;
  left: 24px;
  bottom: calc(36% + 5px);
  width: 14px; height: 12px;
}
.coffee .cup {
  width: 14px; height: 12px;
  background: var(--bg-card);
  border: 2px solid var(--ink);
  border-radius: 1px 1px 4px 4px;
}
.coffee .cup::before {
  content: '';
  position: absolute;
  right: -5px; top: 3px;
  width: 4px; height: 5px;
  border: 2px solid var(--ink);
  border-left: none;
  border-radius: 0 4px 4px 0;
}
.coffee .steam {
  position: absolute;
  bottom: 12px;
  width: 3px; height: 3px;
  background: rgba(255,255,255,0.85);
  border: 1px solid var(--ink);
  border-radius: 50%;
}
.coffee .steam.s1 { left: 3px; animation: steam 2s ease-in-out infinite; }
.coffee .steam.s2 { left: 8px; animation: steam 2s ease-in-out infinite 0.5s; }
@keyframes steam {
  0%   { transform: translateY(0) scale(0.6); opacity: 0.9; }
  60%  { transform: translateY(-8px) scale(1); opacity: 0.7; }
  100% { transform: translateY(-14px) scale(0.4); opacity: 0; }
}

/* ========== 在酒馆 ========== */
.note-out {
  position: absolute;
  right: 50px; top: -2px;
  font-family: var(--font-pix);
  font-size: 14px;
  color: var(--orange-d);
  animation: noteup 1.6s ease-in-out infinite;
}
@keyframes noteup {
  0%   { transform: translateY(0); opacity: 0; }
  20%  { opacity: 1; }
  100% { transform: translateY(-14px); opacity: 0; }
}

.bar-tag {
  position: absolute;
  top: 6px; left: 50%;
  transform: translateX(-50%);
  font-family: var(--font-pix);
  font-size: 8px;
  background: var(--orange-d);
  color: var(--bg-card);
  padding: 2px 6px;
  letter-spacing: 1px;
  z-index: 3;
}

/* ========== 名牌 + 状态 ========== */
.nameplate {
  position: absolute;
  left: 0; right: 0; bottom: -3px;
  display: flex; justify-content: center;
  pointer-events: none;
}
.nameplate span {
  font-family: var(--font-pix);
  font-size: 8px;
  letter-spacing: 1px;
  color: var(--bg-card);
  background: var(--ink);
  border: 2px solid var(--ink);
  padding: 3px 6px;
}

.status {
  position: absolute;
  left: 50%; top: -12px;
  transform: translateX(-50%);
  background: var(--bg-card);
  border: 2px solid var(--ink);
  box-shadow: 2px 2px 0 var(--ink);
  padding: 3px 8px;
  font-size: 13px;
  white-space: nowrap;
  max-width: 92%;
  overflow: hidden; text-overflow: ellipsis;
  z-index: 3;
}
.status::after {
  content: '';
  position: absolute;
  left: 18px; bottom: -6px;
  width: 6px; height: 6px;
  background: var(--bg-card);
  border-right: 2px solid var(--ink);
  border-bottom: 2px solid var(--ink);
  transform: rotate(45deg);
}

.bubble {
  position: absolute;
  top: -16px; right: -8px;
  font-size: 24px;
  z-index: 4;
  animation: pop 0.4s ease-out, float 1.6s ease-in-out 0.4s infinite;
  pointer-events: none;
}
@keyframes pop {
  0%   { transform: scale(0.2); opacity: 0; }
  60%  { transform: scale(1.3); opacity: 1; }
  100% { transform: scale(1.0); opacity: 1; }
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50%      { transform: translateY(-4px); }
}
</style>
