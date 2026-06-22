<script setup>
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

const inBar = computed(() => props.online && props.location === 'bar')
const atDesk = computed(() => props.online && props.location !== 'bar')
const offline = computed(() => !props.online)
const txt = computed(() => (props.text || '').toLowerCase())
const sleeping = computed(() => /z+|睡|sleep|afk|休息|困|眠|🛌|💤/.test(txt.value))
const coffee = computed(() => /☕|咖啡|coffee|续命|energy|补魔/.test(txt.value))
const headphone = computed(() => /🎧|listen|听歌|music|fm|歌|耳机/.test(txt.value))

const moodLabel = computed(() => {
  if (offline.value) return 'offline'
  if (inBar.value) return '去听歌啦'
  if (sleeping.value) return '小睡充电'
  if (coffee.value) return '能量补给'
  if (headphone.value) return 'live mode'
  return props.text || 'ready!'
})
</script>

<template>
  <div class="cube" :class="{ offline, me: isMe, bar: inBar, sleep: sleeping }">
    <div class="wall"></div>
    <div class="floor"></div>

    <div class="bubble" v-if="poke">{{ poke.emoji }}</div>
    <div class="poke-tip" v-if="poke">
      <span>{{ poke.from || 'someone' }}</span>
      <span> poke!</span>
    </div>

    <div class="poster">
      <span class="poster-star">✦</span>
      <span class="poster-title">VIVID</span>
      <span class="poster-line a"></span>
      <span class="poster-line b"></span>
      <span class="poster-line c"></span>
    </div>

    <div class="neon-rail">
      <span class="light l1"></span>
      <span class="light l2"></span>
      <span class="light l3"></span>
      <span class="light l4"></span>
    </div>

    <div class="shelf">
      <span class="box pink"></span>
      <span class="box blue"></span>
      <span class="box green"></span>
      <span class="mini-stand"></span>
    </div>

    <div class="note-out" v-if="inBar">♪</div>

    <div class="pc-tower" :class="{ on: atDesk && !sleeping }">
      <span class="fan top"></span>
      <span class="fan bottom"></span>
      <span class="gpu"></span>
      <span class="rgb-strip"></span>
    </div>

    <div class="desk-top"></div>
    <div class="desk-leg l"></div>
    <div class="desk-leg r"></div>

    <div class="monitor-stack">
      <div class="monitor main" :class="{ on: atDesk && !sleeping, dim: offline || inBar || sleeping }">
        <template v-if="atDesk && !sleeping">
          <span class="sky"></span>
          <span class="stage-light a"></span>
          <span class="stage-light b"></span>
          <span class="beat beat1"></span>
          <span class="beat beat2"></span>
          <span class="beat beat3"></span>
          <span class="hud">LIVE</span>
        </template>
        <span class="zzz" v-if="sleeping">z</span>
      </div>
      <div class="monitor side" :class="{ on: atDesk && !sleeping, dim: offline || inBar || sleeping }">
        <template v-if="atDesk && !sleeping">
          <span class="rank">S</span>
          <span class="bar a"></span>
          <span class="bar b"></span>
          <span class="bar c"></span>
        </template>
      </div>
    </div>

    <div class="keyboard" :class="{ glow: atDesk && !sleeping }">
      <span class="key k1"></span>
      <span class="key k2"></span>
      <span class="key k3"></span>
      <span class="key k4"></span>
      <span class="key k5"></span>
    </div>
    <div class="mousepad"></div>
    <div class="mouse"></div>

    <div class="mic">
      <span class="mic-head"></span>
      <span class="mic-arm"></span>
      <span class="mic-base"></span>
    </div>

    <div class="energy" v-if="coffee && atDesk">
      <span class="can"></span>
      <span class="spark s1"></span>
      <span class="spark s2"></span>
    </div>

    <div class="chair">
      <span class="chair-back"></span>
      <span class="chair-seat"></span>
      <span class="chair-leg"></span>
    </div>

    <div class="person" v-if="atDesk" :class="{ typing: !sleeping && !coffee, sleeping, sipping: coffee }">
      <div class="head-wrap">
        <Avatar :nick="nick" size="sm"/>
        <span class="soft-bow"></span>
        <span class="headphone" v-if="headphone"></span>
        <span class="zhead" v-if="sleeping">Z</span>
      </div>
      <div class="hoodie"></div>
      <span class="sleeve left"></span>
      <span class="sleeve right"></span>
    </div>

    <div class="desk-charm">
      <span class="charm-face"></span>
      <span class="charm-spark">✦</span>
    </div>

    <div class="bar-tag" v-if="inBar">在酒馆</div>
    <div class="nameplate"><span>{{ nick }}</span></div>
    <div class="status">{{ moodLabel }}</div>
  </div>
</template>

<style scoped>
.cube {
  position: relative;
  width: 100%;
  height: 100%;
  border: 3px solid var(--ink);
  overflow: visible;
  image-rendering: pixelated;
  background: #F3D8B5;
}
.cube.me { box-shadow: 0 0 0 2px var(--orange-d); }
.cube.offline { filter: grayscale(0.58); opacity: 0.68; }

.wall {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(90deg, rgba(255,248,236,0.45) 0 8px, transparent 8px 20px),
    radial-gradient(circle, rgba(255,248,236,0.9) 0 2px, transparent 2px 100%) 8px 8px / 23px 23px,
    #F3D8B5;
  pointer-events: none;
}
.floor {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 38%;
  background: #C99668;
  border-top: 3px solid var(--ink);
  background-image:
    repeating-linear-gradient(90deg, rgba(61,46,31,0.16) 0 2px, transparent 2px 22px),
    linear-gradient(rgba(255,255,255,0.08), transparent);
}

.poster {
  position: absolute;
  left: 12px;
  top: 13px;
  width: 52px;
  height: 44px;
  background: linear-gradient(135deg, #FFF8EC 0 42%, #F4A8B8 43% 66%, #96C8D8 67% 100%);
  border: 2px solid var(--ink);
  box-shadow: 2px 2px 0 rgba(61,46,31,0.16);
  overflow: hidden;
}
.poster-star {
  position: absolute;
  right: 5px;
  top: 4px;
  font-family: var(--font-pix);
  font-size: 8px;
  color: var(--orange-d);
  animation: starPop 1.8s ease-in-out infinite;
}
.poster-title {
  position: absolute;
  left: 6px;
  top: 7px;
  font-family: var(--font-pix);
  font-size: 7px;
  color: var(--ink);
}
.poster-line {
  position: absolute;
  left: 7px;
  height: 3px;
  background: var(--ink);
}
.poster-line.a { top: 23px; width: 32px; }
.poster-line.b { top: 30px; width: 23px; background: var(--green); }
.poster-line.c { top: 36px; width: 36px; background: var(--orange); }
@keyframes starPop {
  0%, 100% { transform: scale(0.9); opacity: 0.55; }
  50% { transform: scale(1.15); opacity: 1; }
}

.neon-rail {
  position: absolute;
  left: 74px;
  top: 13px;
  width: 94px;
  height: 21px;
  border-top: 2px solid var(--ink);
  border-radius: 0 0 48px 48px;
}
.light {
  position: absolute;
  top: 4px;
  width: 9px;
  height: 9px;
  border: 1px solid var(--ink);
  transform: rotate(45deg);
  animation: neonBlink 1.7s ease-in-out infinite;
}
.light.l1 { left: 5px; background: #F4A8B8; }
.light.l2 { left: 31px; background: #96C8D8; animation-delay: 0.25s; }
.light.l3 { left: 58px; background: var(--orange); animation-delay: 0.5s; }
.light.l4 { right: 1px; background: var(--green); animation-delay: 0.75s; }
@keyframes neonBlink {
  0%, 100% { filter: brightness(0.9); }
  50% { filter: brightness(1.35); }
}

.shelf {
  position: absolute;
  left: 78px;
  top: 47px;
  width: 56px;
  height: 28px;
  border-bottom: 4px solid #6E3A2A;
  z-index: 2;
}
.box {
  position: absolute;
  bottom: 4px;
  width: 10px;
  border: 1px solid var(--ink);
}
.box.pink { left: 2px; height: 17px; background: #F4A8B8; }
.box.blue { left: 14px; height: 13px; background: #96C8D8; }
.box.green { left: 26px; height: 16px; background: var(--green); }
.mini-stand {
  position: absolute;
  right: 1px;
  bottom: 4px;
  width: 15px;
  height: 20px;
  background: var(--bg-card);
  border: 1px solid var(--ink);
  clip-path: polygon(50% 0, 90% 24%, 78% 100%, 22% 100%, 10% 24%);
}
.mini-stand::after {
  content: '';
  position: absolute;
  left: 5px;
  top: 6px;
  width: 5px;
  height: 5px;
  background: #F4A8B8;
}

.pc-tower {
  position: absolute;
  right: 13px;
  bottom: calc(36% + 2px);
  width: 30px;
  height: 54px;
  background: rgba(255,248,236,0.72);
  border: 2px solid var(--ink);
  z-index: 5;
  overflow: hidden;
}
.pc-tower::before {
  content: '';
  position: absolute;
  inset: 3px;
  border: 1px solid rgba(61,46,31,0.35);
}
.fan {
  position: absolute;
  left: 6px;
  width: 14px;
  height: 14px;
  border: 2px solid var(--ink);
  border-radius: 50%;
  background:
    linear-gradient(90deg, transparent 0 43%, var(--ink) 44% 56%, transparent 57% 100%),
    linear-gradient(0deg, transparent 0 43%, var(--ink) 44% 56%, transparent 57% 100%),
    #96C8D8;
}
.fan.top { top: 7px; }
.fan.bottom { top: 29px; background-color: #F4A8B8; }
.pc-tower.on .fan { animation: fanSpin 1.1s linear infinite; }
@keyframes fanSpin { to { transform: rotate(360deg); } }
.gpu {
  position: absolute;
  left: 4px;
  bottom: 3px;
  width: 20px;
  height: 4px;
  background: var(--ink);
}
.rgb-strip {
  position: absolute;
  right: 2px;
  top: 4px;
  width: 4px;
  height: 46px;
  background: linear-gradient(#F4A8B8, #96C8D8, var(--green), var(--orange));
}

.desk-top {
  position: absolute;
  left: 14px;
  right: 14px;
  bottom: 36%;
  height: 10px;
  background: #6E3A2A;
  border: 2px solid var(--ink);
  z-index: 4;
}
.desk-leg {
  position: absolute;
  bottom: calc(36% - 22px);
  width: 6px;
  height: 18px;
  background: #6E3A2A;
  border: 2px solid var(--ink);
}
.desk-leg.l { left: 24px; }
.desk-leg.r { right: 24px; }

.monitor-stack {
  position: absolute;
  left: 50%;
  bottom: calc(36% + 7px);
  transform: translateX(-50%);
  display: flex;
  align-items: flex-end;
  gap: 3px;
  z-index: 6;
}
.monitor {
  position: relative;
  background: #211E2C;
  border: 2px solid var(--ink);
  overflow: hidden;
}
.monitor.main { width: 54px; height: 36px; }
.monitor.side { width: 28px; height: 28px; }
.monitor.dim { background: #101318; }
.monitor.on { box-shadow: inset 0 0 0 1px rgba(255,248,236,0.5); }
.sky {
  position: absolute;
  inset: 0;
  background: linear-gradient(#704A78 0 38%, #F4A8B8 39% 58%, #2A344F 59% 100%);
}
.stage-light {
  position: absolute;
  top: -3px;
  width: 22px;
  height: 42px;
  opacity: 0.7;
  clip-path: polygon(50% 0, 100% 100%, 0 100%);
}
.stage-light.a { left: 4px; background: rgba(150,200,216,0.7); animation: sweepA 2.4s ease-in-out infinite; }
.stage-light.b { right: 3px; background: rgba(244,168,184,0.7); animation: sweepB 2.4s ease-in-out infinite; }
@keyframes sweepA {
  0%, 100% { transform: skewX(-8deg); }
  50% { transform: skewX(10deg); }
}
@keyframes sweepB {
  0%, 100% { transform: skewX(8deg); }
  50% { transform: skewX(-10deg); }
}
.beat {
  position: absolute;
  bottom: 4px;
  width: 4px;
  background: var(--orange);
  border-left: 1px solid var(--ink);
  border-right: 1px solid var(--ink);
  animation: beat 0.72s ease-in-out infinite;
}
.beat1 { left: 7px; height: 8px; }
.beat2 { left: 15px; height: 14px; animation-delay: 0.14s; }
.beat3 { left: 23px; height: 10px; animation-delay: 0.28s; }
@keyframes beat {
  0%, 100% { transform: scaleY(0.5); transform-origin: bottom; }
  50% { transform: scaleY(1); transform-origin: bottom; }
}
.hud {
  position: absolute;
  right: 3px;
  top: 4px;
  font-family: var(--font-pix);
  font-size: 6px;
  color: var(--bg-card);
}
.rank {
  position: absolute;
  left: 6px;
  top: 4px;
  font-family: var(--font-pix);
  font-size: 12px;
  color: #F4A8B8;
}
.bar {
  position: absolute;
  left: 5px;
  height: 3px;
  background: var(--bg-card);
}
.bar.a { bottom: 5px; width: 18px; }
.bar.b { bottom: 10px; width: 12px; background: #96C8D8; }
.bar.c { bottom: 15px; width: 16px; background: var(--green); }
.zzz {
  position: absolute;
  right: 5px;
  top: 5px;
  font-family: var(--font-pix);
  font-size: 9px;
  color: var(--olive);
  animation: zfloat 2s ease-in-out infinite;
}

.keyboard {
  position: absolute;
  left: 48%;
  bottom: calc(36% - 4px);
  transform: translateX(-50%);
  width: 58px;
  height: 8px;
  background: #2A1F2D;
  border: 2px solid var(--ink);
  z-index: 7;
  display: flex;
  gap: 3px;
  align-items: center;
  justify-content: center;
}
.key {
  width: 6px;
  height: 3px;
  border: 1px solid var(--ink);
  background: var(--bg-card);
}
.keyboard.glow .k1 { background: #F4A8B8; }
.keyboard.glow .k2 { background: #96C8D8; }
.keyboard.glow .k3 { background: var(--green); }
.keyboard.glow .k4 { background: var(--orange); }
.keyboard.glow .k5 { background: var(--bg-card); }
.mousepad {
  position: absolute;
  right: 43px;
  bottom: calc(36% - 2px);
  width: 20px;
  height: 10px;
  background: #47314B;
  border: 2px solid var(--ink);
  z-index: 6;
}
.mouse {
  position: absolute;
  right: 48px;
  bottom: calc(36% + 1px);
  width: 8px;
  height: 6px;
  background: #FFF8EC;
  border: 1px solid var(--ink);
  border-radius: 5px 5px 2px 2px;
  z-index: 7;
}

.mic {
  position: absolute;
  left: 30px;
  bottom: calc(36% + 3px);
  width: 21px;
  height: 35px;
  z-index: 6;
}
.mic-head {
  position: absolute;
  left: 0;
  top: 0;
  width: 12px;
  height: 15px;
  background: #2A1F2D;
  border: 2px solid var(--ink);
  border-radius: 6px 6px 4px 4px;
}
.mic-head::after {
  content: '';
  position: absolute;
  left: 3px;
  top: 3px;
  width: 4px;
  height: 7px;
  background: #96C8D8;
}
.mic-arm {
  position: absolute;
  left: 9px;
  top: 13px;
  width: 3px;
  height: 17px;
  background: var(--ink);
  transform: rotate(-18deg);
}
.mic-base {
  position: absolute;
  left: 7px;
  bottom: 0;
  width: 13px;
  height: 4px;
  background: var(--ink);
}

.energy {
  position: absolute;
  left: 52px;
  bottom: calc(36% + 6px);
  width: 16px;
  height: 24px;
  z-index: 8;
}
.can {
  position: absolute;
  left: 3px;
  bottom: 0;
  width: 11px;
  height: 18px;
  background: linear-gradient(#96C8D8 0 46%, #F4A8B8 47% 100%);
  border: 2px solid var(--ink);
}
.can::after {
  content: '';
  position: absolute;
  left: 3px;
  top: 6px;
  width: 4px;
  height: 4px;
  background: var(--bg-card);
}
.spark {
  position: absolute;
  font-family: var(--font-pix);
  font-size: 7px;
  color: var(--orange-d);
  animation: sparkUp 1.4s ease-in-out infinite;
}
.spark::before { content: '✦'; }
.spark.s1 { left: 0; top: 2px; }
.spark.s2 { right: 0; top: 0; animation-delay: 0.35s; }
@keyframes sparkUp {
  0%, 100% { transform: translateY(0); opacity: 0.35; }
  50% { transform: translateY(-5px); opacity: 1; }
}

.chair {
  position: absolute;
  left: 50%;
  bottom: 4px;
  transform: translateX(-50%);
  width: 40px;
  height: 36px;
  z-index: 3;
}
.chair-back,
.chair-seat {
  position: absolute;
  background: #47314B;
  border: 2px solid var(--ink);
}
.chair-back {
  left: 7px;
  top: 0;
  width: 26px;
  height: 20px;
  border-top-color: #96C8D8;
}
.chair-seat {
  left: 2px;
  top: 18px;
  width: 36px;
  height: 8px;
  border-top-color: #F4A8B8;
}
.chair-leg {
  position: absolute;
  left: 17px;
  top: 25px;
  width: 7px;
  height: 11px;
  background: var(--ink);
}

.person {
  position: absolute;
  left: 50%;
  bottom: 19px;
  transform: translateX(-50%);
  width: 34px;
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 9;
}
.head-wrap {
  position: relative;
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.soft-bow {
  position: absolute;
  right: -8px;
  top: -5px;
  width: 15px;
  height: 10px;
}
.soft-bow::before,
.soft-bow::after {
  content: '';
  position: absolute;
  top: 2px;
  width: 8px;
  height: 7px;
  background: #F4A8B8;
  border: 1px solid var(--ink);
}
.soft-bow::before { left: 0; transform: skewY(-18deg); }
.soft-bow::after { right: 0; transform: skewY(18deg); }
.headphone {
  position: absolute;
  left: -4px;
  right: -4px;
  top: -3px;
  height: 9px;
  border: 2px solid var(--ink);
  border-bottom: none;
  border-radius: 10px 10px 0 0;
}
.headphone::before,
.headphone::after {
  content: '';
  position: absolute;
  top: 5px;
  width: 4px;
  height: 7px;
  background: #96C8D8;
  border: 1px solid var(--ink);
}
.headphone::before { left: -2px; }
.headphone::after { right: -2px; }
.zhead {
  position: absolute;
  left: -9px;
  top: -11px;
  font-family: var(--font-pix);
  font-size: 9px;
  color: var(--ink-soft);
  animation: zfloat 2s ease-in-out infinite;
}
@keyframes zfloat {
  0%, 100% { transform: translateY(0); opacity: 0.45; }
  50% { transform: translateY(-5px); opacity: 1; }
}
.hoodie {
  width: 24px;
  height: 12px;
  background: linear-gradient(90deg, #96C8D8 0 50%, #F4A8B8 51% 100%);
  border: 2px solid var(--ink);
  margin-top: -3px;
}
.sleeve {
  position: absolute;
  bottom: 3px;
  width: 5px;
  height: 8px;
  background: #96C8D8;
  border: 2px solid var(--ink);
}
.sleeve.left { left: 2px; transform-origin: top center; }
.sleeve.right { right: 2px; transform-origin: top center; background: #F4A8B8; }
.person.typing { animation: playerBob 0.55s ease-in-out infinite; }
.person.typing .sleeve.left { animation: tapLeft 0.42s ease-in-out infinite; }
.person.typing .sleeve.right { animation: tapRight 0.42s ease-in-out infinite 0.16s; }
@keyframes playerBob {
  0%, 100% { transform: translate(-50%, 0); }
  50% { transform: translate(-50%, -1px); }
}
@keyframes tapLeft {
  0%, 100% { transform: rotate(8deg); }
  50% { transform: rotate(-12deg) translateY(-2px); }
}
@keyframes tapRight {
  0%, 100% { transform: rotate(-8deg); }
  50% { transform: rotate(12deg) translateY(-2px); }
}
.person.sleeping { animation: sleepyBob 3s ease-in-out infinite; }
@keyframes sleepyBob {
  0%, 100% { transform: translate(-50%, 0); }
  50% { transform: translate(-50%, 2px); }
}
.person.sipping { animation: sip 2s ease-in-out infinite; }
.person.sipping .sleeve.right { animation: sipArm 2s ease-in-out infinite; }
@keyframes sip {
  0%, 100% { transform: translate(-50%, 0); }
  45% { transform: translate(-50%, -2px); }
}
@keyframes sipArm {
  0%, 100% { transform: rotate(-8deg); }
  45% { transform: rotate(24deg) translateY(-4px); }
}

.desk-charm {
  position: absolute;
  left: 14px;
  bottom: 7px;
  width: 28px;
  height: 30px;
  z-index: 5;
  animation: charmBob 2.2s ease-in-out infinite;
}
.charm-face {
  position: absolute;
  left: 4px;
  bottom: 0;
  width: 21px;
  height: 22px;
  background: var(--bg-card);
  border: 2px solid var(--ink);
  border-radius: 5px;
}
.charm-face::before,
.charm-face::after {
  content: '';
  position: absolute;
  top: 8px;
  width: 3px;
  height: 3px;
  background: var(--ink);
}
.charm-face::before { left: 5px; }
.charm-face::after { right: 5px; }
.charm-spark {
  position: absolute;
  right: -2px;
  top: 1px;
  color: var(--orange-d);
  font-family: var(--font-pix);
  font-size: 7px;
}
@keyframes charmBob {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-2px); }
}

.note-out {
  position: absolute;
  left: 54%;
  top: 39px;
  font-family: var(--font-pix);
  font-size: 17px;
  color: var(--orange-d);
  z-index: 12;
  animation: noteFloat 1.5s ease-in-out infinite;
}
@keyframes noteFloat {
  0%, 100% { transform: translateY(0); opacity: 0.62; }
  50% { transform: translateY(-6px); opacity: 1; }
}

.bar-tag {
  position: absolute;
  top: 6px;
  left: 50%;
  transform: translateX(-50%);
  font-family: var(--font-pix);
  font-size: 8px;
  background: var(--orange-d);
  color: var(--bg-card);
  padding: 2px 6px;
  letter-spacing: 1px;
  z-index: 13;
}
.nameplate {
  position: absolute;
  left: 0;
  right: 0;
  bottom: -3px;
  display: flex;
  justify-content: center;
  pointer-events: none;
  z-index: 14;
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
  left: 50%;
  top: -12px;
  transform: translateX(-50%);
  max-width: 92%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  background: var(--bg-card);
  border: 2px solid var(--ink);
  box-shadow: 2px 2px 0 var(--ink);
  padding: 3px 8px;
  font-size: 13px;
  z-index: 14;
}
.status::after {
  content: '';
  position: absolute;
  left: 18px;
  bottom: -6px;
  width: 6px;
  height: 6px;
  background: var(--bg-card);
  border-right: 2px solid var(--ink);
  border-bottom: 2px solid var(--ink);
  transform: rotate(45deg);
}
.bubble {
  position: absolute;
  top: -16px;
  right: -8px;
  font-size: 24px;
  z-index: 16;
  pointer-events: none;
  animation: pop 0.4s ease-out, float 1.6s ease-in-out 0.4s infinite;
}
.poke-tip {
  position: absolute;
  left: 50%;
  top: -28px;
  transform: translateX(-50%);
  background: #F4A8B8;
  border: 2px solid var(--ink);
  box-shadow: 2px 2px 0 var(--ink);
  font-size: 11px;
  padding: 2px 6px;
  white-space: nowrap;
  z-index: 15;
  animation: pop 0.3s ease-out;
}
@keyframes pop {
  0% { transform: scale(0.2); opacity: 0; }
  60% { transform: scale(1.25); opacity: 1; }
  100% { transform: scale(1); opacity: 1; }
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}
</style>
