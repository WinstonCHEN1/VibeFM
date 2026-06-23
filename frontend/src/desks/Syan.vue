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
const coffee = computed(() => /☕|咖啡|coffee|续命|energy|补魔|奶茶/.test(txt.value))
const headphone = computed(() => /🎧|listen|听歌|music|fm|歌|耳机|live/.test(txt.value))

const moodLabel = computed(() => {
  if (offline.value) return 'soft off'
  if (inBar.value) return 'drink off'
  if (sleeping.value) return '已安眠'
  if (coffee.value) return '瑞幸黑金鹿'
  if (headphone.value) return 'live ready'
  return props.text || 'pink setup'
})
</script>

<template>
  <div class="cube" :class="{ offline, me: isMe, bar: inBar, sleep: sleeping }">
    <div class="wall"></div>
    <div class="floor"></div>
    <div class="rug"></div>

    <div class="bubble" v-if="poke">{{ poke.emoji }}</div>
    <div class="poke-tip" v-if="poke">
      <span>{{ poke.from || 'someone' }}</span>
      <span> poke!</span>
    </div>

    <div class="poster-card">
      <span class="poster-title">VIVID</span>
      <span class="poster-chip">STAGE</span>
      <span class="poster-line a"></span>
      <span class="poster-line b"></span>
      <span class="poster-star">✦</span>
    </div>

    <div class="light-string">
      <span class="cord"></span>
      <span class="bulb b1"></span>
      <span class="bulb b2"></span>
      <span class="bulb b3"></span>
      <span class="bulb b4"></span>
    </div>

    <div class="shelf">
      <span class="mini-box a"></span>
      <span class="mini-box b"></span>
      <span class="mini-box c"></span>
      <span class="standee"></span>
    </div>

    <div class="pc-tower" :class="{ on: atDesk && !sleeping }">
      <span class="glass"></span>
      <span class="fan top"></span>
      <span class="fan bottom"></span>
      <span class="gpu"></span>
      <span class="rgb-strip"></span>
    </div>

    <div class="desk-leg l"></div>
    <div class="desk-leg r"></div>
    <div class="desk-top"></div>
    <div class="desk-front"></div>
    <div class="desk-shine"></div>

    <div class="monitor-stack">
      <div class="monitor main" :class="{ on: atDesk && !sleeping, dim: offline || inBar || sleeping }">
        <template v-if="atDesk && !sleeping">
          <span class="screen-bg"></span>
          <span class="stage-beam left"></span>
          <span class="stage-beam right"></span>
          <span class="eq e1"></span>
          <span class="eq e2"></span>
          <span class="eq e3"></span>
          <span class="screen-label">LIVE</span>
        </template>
        <span class="zzz" v-if="sleeping">z</span>
      </div>
      <div class="monitor side" :class="{ on: atDesk && !sleeping, dim: offline || inBar || sleeping }">
        <template v-if="atDesk && !sleeping">
          <span class="side-rank">S</span>
          <span class="side-line a"></span>
          <span class="side-line b"></span>
          <span class="side-line c"></span>
        </template>
      </div>
    </div>

    <div class="monitor-stand"></div>
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

    <div class="sweet-drink" v-if="coffee && atDesk">
      <span class="cup"></span>
      <span class="straw"></span>
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
        <span class="hair-bow"></span>
        <span class="headphone" v-if="headphone"></span>
        <span class="zhead" v-if="sleeping">Z</span>
      </div>
      <div class="hoodie"></div>
      <span class="sleeve left"></span>
      <span class="sleeve right"></span>
    </div>

    <div class="plush">
      <span class="plush-head"></span>
      <span class="plush-body"></span>
      <span class="plush-spark">✦</span>
    </div>

    <img class="khn-standee" src="./khn.webp" alt="" aria-hidden="true" />

    <div class="note-out" v-if="inBar">♪</div>
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
  background: #F8D8D7;
}
.cube.me { box-shadow: 0 0 0 2px var(--orange-d); }
.cube.offline { filter: grayscale(0.55); opacity: 0.68; }

.wall {
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle, rgba(255,248,236,0.95) 0 2px, transparent 2px 100%) 9px 8px / 22px 22px,
    repeating-linear-gradient(90deg, rgba(255,248,236,0.34) 0 8px, transparent 8px 18px),
    #F8D8D7;
  pointer-events: none;
}
.wall::after {
  content: '';
  position: absolute;
  inset: 0;
  background:
    linear-gradient(45deg, transparent 0 45%, rgba(255,248,236,0.24) 45% 55%, transparent 55% 100%) 0 0 / 28px 28px;
}
.floor {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 38%;
  background: #D9A077;
  border-top: 3px solid var(--ink);
  background-image:
    repeating-linear-gradient(90deg, rgba(61,46,31,0.15) 0 2px, transparent 2px 22px),
    linear-gradient(rgba(255,255,255,0.12), transparent);
}
.rug {
  position: absolute;
  left: 48px;
  right: 48px;
  bottom: 3px;
  height: 22px;
  background: #F5B9C8;
  border: 2px solid var(--ink);
  border-radius: 10px 10px 2px 2px;
  z-index: 1;
}
.rug::after {
  content: '';
  position: absolute;
  left: 8px;
  right: 8px;
  top: 7px;
  height: 3px;
  background: rgba(255,248,236,0.75);
}


.poster-card {
  position: absolute;
  left: 14px;
  top: 14px;
  width: 50px;
  height: 42px;
  background: linear-gradient(135deg, #FFF8EC 0 38%, #F6B8C6 39% 68%, #B7DCE6 69% 100%);
  border: 2px solid var(--ink);
  box-shadow: 2px 2px 0 rgba(61,46,31,0.14);
  z-index: 3;
}
.poster-title {
  position: absolute;
  left: 6px;
  top: 6px;
  font-family: var(--font-pix);
  font-size: 7px;
  color: var(--ink);
}
.poster-chip {
  position: absolute;
  right: 5px;
  top: 17px;
  font-family: var(--font-pix);
  font-size: 5px;
  color: var(--bg-card);
  background: #7B617A;
  border: 1px solid var(--ink);
  padding: 2px 3px;
}
.poster-line {
  position: absolute;
  left: 7px;
  height: 3px;
  background: var(--ink);
}
.poster-line.a { top: 24px; width: 20px; }
.poster-line.b { top: 31px; width: 34px; background: #96C8D8; }
.poster-star {
  position: absolute;
  right: 5px;
  bottom: 4px;
  font-family: var(--font-pix);
  font-size: 7px;
  color: var(--orange-d);
  animation: starPop 1.7s ease-in-out infinite;
}
@keyframes starPop {
  0%, 100% { transform: scale(0.9); opacity: 0.55; }
  50% { transform: scale(1.18); opacity: 1; }
}

.light-string {
  position: absolute;
  right: 11px;
  top: 13px;
  width: 76px;
  height: 30px;
  z-index: 4;
}
.cord {
  position: absolute;
  left: 0;
  right: 0;
  top: 3px;
  height: 18px;
  border-top: 2px solid var(--ink);
  border-radius: 0 0 40px 40px;
}
.bulb {
  position: absolute;
  top: 10px;
  width: 9px;
  height: 9px;
  border: 1px solid var(--ink);
  transform: rotate(45deg);
  animation: bulbTwinkle 1.5s ease-in-out infinite;
}
.bulb.b1 { left: 5px; background: #F6B8C6; }
.bulb.b2 { left: 25px; background: #B7DCE6; animation-delay: 0.18s; }
.bulb.b3 { left: 47px; background: #FFF1A8; animation-delay: 0.36s; }
.bulb.b4 { right: 2px; background: #BFE2C3; animation-delay: 0.54s; }
@keyframes bulbTwinkle {
  0%, 100% { filter: brightness(0.95); }
  50% { filter: brightness(1.28); }
}

.shelf {
  position: absolute;
  right: 17px;
  top: 49px;
  width: 55px;
  height: 29px;
  border-bottom: 4px solid #7A4C39;
  z-index: 3;
}
.mini-box {
  position: absolute;
  bottom: 4px;
  width: 9px;
  border: 1px solid var(--ink);
}
.mini-box.a { left: 3px; height: 15px; background: #F6B8C6; }
.mini-box.b { left: 14px; height: 19px; background: #FFF1A8; }
.mini-box.c { left: 25px; height: 13px; background: #B7DCE6; }
.standee {
  position: absolute;
  right: 2px;
  bottom: 4px;
  width: 14px;
  height: 21px;
  background: #FFF8EC;
  border: 1px solid var(--ink);
  clip-path: polygon(50% 0, 90% 28%, 78% 100%, 22% 100%, 10% 28%);
}
.standee::after {
  content: '';
  position: absolute;
  left: 4px;
  top: 7px;
  width: 6px;
  height: 6px;
  background: #F6B8C6;
}

.pc-tower {
  position: absolute;
  right: 13px;
  bottom: calc(36% + 1px);
  width: 30px;
  height: 56px;
  background: #FFF8EC;
  border: 2px solid var(--ink);
  z-index: 7;
  overflow: hidden;
}
.glass {
  position: absolute;
  inset: 4px;
  background: rgba(183,220,230,0.22);
  border: 1px solid rgba(61,46,31,0.35);
}
.fan {
  position: absolute;
  left: 7px;
  width: 13px;
  height: 13px;
  border: 2px solid var(--ink);
  border-radius: 50%;
  background:
    linear-gradient(90deg, transparent 0 42%, var(--ink) 43% 57%, transparent 58% 100%),
    linear-gradient(0deg, transparent 0 42%, var(--ink) 43% 57%, transparent 58% 100%),
    #F6B8C6;
}
.fan.top { top: 8px; }
.fan.bottom { top: 30px; background-color: #B7DCE6; }
.pc-tower.on .fan { animation: fanSpin 1.05s linear infinite; }
@keyframes fanSpin { to { transform: rotate(360deg); } }
.gpu {
  position: absolute;
  left: 5px;
  bottom: 4px;
  width: 19px;
  height: 4px;
  background: var(--ink);
}
.rgb-strip {
  position: absolute;
  right: 2px;
  top: 5px;
  width: 4px;
  height: 47px;
  background: linear-gradient(#F6B8C6, #B7DCE6, #FFF1A8, #BFE2C3);
}

.desk-top {
  position: absolute;
  left: 14px;
  right: 14px;
  bottom: 36%;
  height: 11px;
  background: #8A5541;
  border: 2px solid var(--ink);
  z-index: 6;
}
.desk-top::after {
  content: '';
  position: absolute;
  left: 7px;
  right: 7px;
  top: 2px;
  height: 2px;
  background: rgba(255,248,236,0.35);
}
.desk-front {
  position: absolute;
  left: 18px;
  right: 18px;
  bottom: calc(36% - 12px);
  height: 14px;
  background: #A76850;
  border-left: 2px solid var(--ink);
  border-right: 2px solid var(--ink);
  border-bottom: 2px solid var(--ink);
  z-index: 5;
}
.desk-shine {
  position: absolute;
  left: 28px;
  right: 28px;
  bottom: calc(36% - 4px);
  height: 2px;
  background: rgba(255,248,236,0.35);
  z-index: 6;
}
.desk-leg {
  position: absolute;
  bottom: calc(36% - 37px);
  width: 7px;
  height: 38px;
  background: #8A5541;
  border: 2px solid var(--ink);
  z-index: 4;
}
.desk-leg.l { left: 23px; }
.desk-leg.r { right: 23px; }

.monitor-stack {
  position: absolute;
  left: 51%;
  bottom: calc(36% + 8px);
  transform: translateX(-50%);
  display: flex;
  align-items: flex-end;
  gap: 3px;
  z-index: 8;
}
.monitor {
  position: relative;
  background: #241A30;
  border: 2px solid var(--ink);
  overflow: hidden;
}
.monitor.main { width: 55px; height: 36px; }
.monitor.side { width: 28px; height: 28px; }
.monitor.dim { background: #121018; }
.monitor.on { box-shadow: inset 0 0 0 1px rgba(255,248,236,0.5); }
.screen-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(#8B5C89 0 34%, #F6B8C6 35% 58%, #3B456C 59% 100%);
}
.stage-beam {
  position: absolute;
  top: -4px;
  width: 24px;
  height: 42px;
  opacity: 0.72;
  clip-path: polygon(50% 0, 100% 100%, 0 100%);
}
.stage-beam.left { left: 4px; background: rgba(183,220,230,0.72); animation: sweepLeft 2.3s ease-in-out infinite; }
.stage-beam.right { right: 3px; background: rgba(246,184,198,0.78); animation: sweepRight 2.3s ease-in-out infinite; }
@keyframes sweepLeft {
  0%, 100% { transform: skewX(-8deg); }
  50% { transform: skewX(10deg); }
}
@keyframes sweepRight {
  0%, 100% { transform: skewX(8deg); }
  50% { transform: skewX(-10deg); }
}
.eq {
  position: absolute;
  bottom: 4px;
  width: 4px;
  background: #FFF1A8;
  border-left: 1px solid var(--ink);
  border-right: 1px solid var(--ink);
  animation: eqPulse 0.72s ease-in-out infinite;
}
.eq.e1 { left: 7px; height: 8px; }
.eq.e2 { left: 15px; height: 14px; animation-delay: 0.14s; }
.eq.e3 { left: 23px; height: 10px; animation-delay: 0.28s; }
@keyframes eqPulse {
  0%, 100% { transform: scaleY(0.5); transform-origin: bottom; }
  50% { transform: scaleY(1); transform-origin: bottom; }
}
.screen-label {
  position: absolute;
  right: 3px;
  top: 4px;
  font-family: var(--font-pix);
  font-size: 6px;
  color: var(--bg-card);
}
.side-rank {
  position: absolute;
  left: 6px;
  top: 4px;
  font-family: var(--font-pix);
  font-size: 12px;
  color: #F6B8C6;
}
.side-line {
  position: absolute;
  left: 5px;
  height: 3px;
  background: var(--bg-card);
}
.side-line.a { bottom: 5px; width: 18px; }
.side-line.b { bottom: 10px; width: 12px; background: #B7DCE6; }
.side-line.c { bottom: 15px; width: 16px; background: #BFE2C3; }
.zzz {
  position: absolute;
  right: 5px;
  top: 5px;
  font-family: var(--font-pix);
  font-size: 9px;
  color: var(--olive);
  animation: zfloat 2s ease-in-out infinite;
}
.monitor-stand {
  position: absolute;
  left: 50%;
  bottom: calc(36% + 3px);
  width: 22px;
  height: 7px;
  transform: translateX(-50%);
  background: var(--ink);
  z-index: 7;
}

.keyboard {
  position: absolute;
  left: 48%;
  bottom: calc(36% - 3px);
  transform: translateX(-50%);
  width: 59px;
  height: 8px;
  background: #2A1F2D;
  border: 2px solid var(--ink);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 3px;
  z-index: 9;
}
.key {
  width: 6px;
  height: 3px;
  border: 1px solid var(--ink);
  background: var(--bg-card);
}
.keyboard.glow .k1 { background: #F6B8C6; }
.keyboard.glow .k2 { background: #B7DCE6; }
.keyboard.glow .k3 { background: #FFF1A8; }
.keyboard.glow .k4 { background: #BFE2C3; }
.keyboard.glow .k5 { background: #FFF8EC; }
.mousepad {
  position: absolute;
  right: 42px;
  bottom: calc(36% - 1px);
  width: 21px;
  height: 10px;
  background: #6F496A;
  border: 2px solid var(--ink);
  z-index: 8;
}
.mouse {
  position: absolute;
  right: 48px;
  bottom: calc(36% + 2px);
  width: 8px;
  height: 6px;
  background: #FFF8EC;
  border: 1px solid var(--ink);
  border-radius: 5px 5px 2px 2px;
  z-index: 9;
}

.mic {
  position: absolute;
  left: 31px;
  bottom: calc(36% + 3px);
  width: 21px;
  height: 34px;
  z-index: 8;
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
  background: #F6B8C6;
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

.sweet-drink {
  position: absolute;
  left: 53px;
  bottom: calc(36% + 5px);
  width: 17px;
  height: 25px;
  z-index: 10;
}
.cup {
  position: absolute;
  left: 3px;
  bottom: 0;
  width: 12px;
  height: 17px;
  background: linear-gradient(#FFF8EC 0 35%, #F6B8C6 36% 100%);
  border: 2px solid var(--ink);
}
.cup::after {
  content: '';
  position: absolute;
  left: 3px;
  bottom: 3px;
  width: 4px;
  height: 4px;
  background: #B7DCE6;
}
.straw {
  position: absolute;
  left: 9px;
  top: 0;
  width: 2px;
  height: 13px;
  background: var(--ink);
  transform: rotate(14deg);
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
  bottom: 5px;
  transform: translateX(-50%);
  width: 42px;
  height: 37px;
  z-index: 3;
}
.chair-back,
.chair-seat {
  position: absolute;
  background: #7B617A;
  border: 2px solid var(--ink);
}
.chair-back {
  left: 7px;
  top: 0;
  width: 28px;
  height: 20px;
  border-top-color: #F6B8C6;
}
.chair-back::after {
  content: '';
  position: absolute;
  left: 5px;
  right: 5px;
  top: 5px;
  height: 3px;
  background: rgba(255,248,236,0.38);
}
.chair-seat {
  left: 2px;
  top: 18px;
  width: 38px;
  height: 8px;
  border-top-color: #B7DCE6;
}
.chair-leg {
  position: absolute;
  left: 18px;
  top: 25px;
  width: 7px;
  height: 12px;
  background: var(--ink);
}

.person {
  position: absolute;
  left: 50%;
  bottom: 20px;
  transform: translateX(-50%);
  width: 34px;
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 11;
}
.head-wrap {
  position: relative;
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.hair-bow {
  position: absolute;
  right: -8px;
  top: -5px;
  width: 15px;
  height: 10px;
}
.hair-bow::before,
.hair-bow::after {
  content: '';
  position: absolute;
  top: 2px;
  width: 8px;
  height: 7px;
  background: #F6B8C6;
  border: 1px solid var(--ink);
}
.hair-bow::before { left: 0; transform: skewY(-18deg); }
.hair-bow::after { right: 0; transform: skewY(18deg); }
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
  background: #F6B8C6;
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
  background: linear-gradient(90deg, #F6B8C6 0 50%, #B7DCE6 51% 100%);
  border: 2px solid var(--ink);
  margin-top: -3px;
}
.sleeve {
  position: absolute;
  bottom: 3px;
  width: 5px;
  height: 8px;
  background: #F6B8C6;
  border: 2px solid var(--ink);
}
.sleeve.left { left: 2px; transform-origin: top center; }
.sleeve.right { right: 2px; transform-origin: top center; background: #B7DCE6; }
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

.plush {
  position: absolute;
  left: 13px;
  bottom: 7px;
  width: 29px;
  height: 31px;
  z-index: 5;
  animation: plushBob 2.2s ease-in-out infinite;
}
.plush-head {
  position: absolute;
  left: 5px;
  top: 0;
  width: 18px;
  height: 17px;
  background: #FFF8EC;
  border: 2px solid var(--ink);
  border-radius: 5px;
}
.plush-head::before,
.plush-head::after {
  content: '';
  position: absolute;
  top: 7px;
  width: 3px;
  height: 3px;
  background: var(--ink);
}
.plush-head::before { left: 4px; }
.plush-head::after { right: 4px; }
.plush-body {
  position: absolute;
  left: 3px;
  bottom: 0;
  width: 23px;
  height: 16px;
  background: #F6B8C6;
  border: 2px solid var(--ink);
  border-radius: 4px 4px 7px 7px;
}
.plush-spark {
  position: absolute;
  right: -2px;
  top: 1px;
  color: var(--orange-d);
  font-family: var(--font-pix);
  font-size: 7px;
}
@keyframes plushBob {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-2px); }
}

.khn-standee {
  position: absolute;
  right: 1px;
  bottom: 3px;
  width: 56px;
  height: auto;
  z-index: 12;
  pointer-events: none;
  image-rendering: auto;
  filter: drop-shadow(2px 2px 0 rgba(61,46,31,0.38));
}

.note-out {
  position: absolute;
  left: 54%;
  top: 40px;
  font-family: var(--font-pix);
  font-size: 17px;
  color: var(--orange-d);
  z-index: 13;
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
  z-index: 14;
}
.nameplate {
  position: absolute;
  left: 0;
  right: 0;
  bottom: -3px;
  display: flex;
  justify-content: center;
  pointer-events: none;
  z-index: 15;
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
  z-index: 15;
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
  z-index: 17;
  pointer-events: none;
  animation: pop 0.4s ease-out, float 1.6s ease-in-out 0.4s infinite;
}
.poke-tip {
  position: absolute;
  left: 50%;
  top: -28px;
  transform: translateX(-50%);
  background: #F6B8C6;
  border: 2px solid var(--ink);
  box-shadow: 2px 2px 0 var(--ink);
  font-size: 11px;
  padding: 2px 6px;
  white-space: nowrap;
  z-index: 16;
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
