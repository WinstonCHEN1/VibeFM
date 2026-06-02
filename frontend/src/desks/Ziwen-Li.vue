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
const sleeping = computed(() => /z+|睡|sleep|afk|休息/.test(txt.value))
const coffee = computed(() => /☕|咖啡|coffee|续命/.test(txt.value))
const headphone = computed(() => /🎧|listen|听歌|music|fm/.test(txt.value))

const moodLabel = computed(() => {
  if (offline.value) return 'afk'
  if (inBar.value) return '去 FM 里了'
  if (sleeping.value) return '低功耗休息'
  if (coffee.value) return '咖啡续航'
  if (headphone.value) return '听歌写代码'
  return props.text || 'vibing'
})
</script>

<template>
  <div class="cube" :class="{ offline, me: isMe, bar: inBar, sleep: sleeping }">
    <div class="wall"></div>
    <div class="floor"></div>

    <div class="bubble" v-if="poke">{{ poke.emoji }}</div>

    <div class="poster">
      <span class="poster-title">FM</span>
      <span class="poster-line a"></span>
      <span class="poster-line b"></span>
    </div>

    <div class="plant">
      <span class="leaf l"></span>
      <span class="leaf r"></span>
      <span class="pot"></span>
    </div>

    <div class="note-out" v-if="inBar">♪</div>

    <div class="desk-top"></div>
    <div class="desk-leg l"></div>
    <div class="desk-leg r"></div>

    <div class="monitor">
      <div class="screen" :class="{ on: atDesk && !sleeping, dark: offline || inBar, sleep: sleeping }">
        <template v-if="atDesk && !sleeping">
          <span class="sky"></span>
          <span class="sun"></span>
          <span class="wave w1"></span>
          <span class="wave w2"></span>
          <span class="wave w3"></span>
          <span class="equalizer e1"></span>
          <span class="equalizer e2"></span>
          <span class="equalizer e3"></span>
        </template>
        <span class="zzz" v-if="sleeping">z</span>
      </div>
      <div class="stand"></div>
      <div class="keyboard"></div>
    </div>

    <div class="coffee" v-if="coffee && atDesk">
      <div class="cup"></div>
      <div class="steam s1"></div>
      <div class="steam s2"></div>
    </div>

    <div class="chair">
      <div class="chair-back"></div>
      <div class="chair-seat"></div>
      <div class="chair-leg"></div>
    </div>

    <div class="person" v-if="atDesk" :class="{ typing: !sleeping && !coffee, sleeping, sipping: coffee }">
      <div class="head-wrap">
        <Avatar :nick="nick" size="sm"/>
        <div class="headphone" v-if="headphone"></div>
        <div class="zhead" v-if="sleeping">Z</div>
      </div>
      <div class="body"></div>
      <div class="arm-l"></div>
      <div class="arm-r"></div>
    </div>

    <div class="companion" :class="{ wait: !atDesk || sleeping }">
      <div class="hair-back"></div>
      <div class="tail left"></div>
      <div class="tail right"></div>
      <div class="face">
        <span class="eye left"></span>
        <span class="eye right"></span>
        <span class="blush left"></span>
        <span class="blush right"></span>
        <span class="mouth"></span>
      </div>
      <div class="bang"></div>
      <div class="ribbon"></div>
      <div class="dress">
        <span class="collar"></span>
        <span class="belt"></span>
      </div>
      <div class="arm a"></div>
      <div class="arm b"></div>
      <div class="leg a"></div>
      <div class="leg b"></div>
      <div class="boot a"></div>
      <div class="boot b"></div>
      <div class="heart" v-if="atDesk && !sleeping">♥</div>
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
  background: #F2D6AE;
}
.cube.me { box-shadow: 0 0 0 2px var(--orange-d); }
.cube.offline { filter: grayscale(0.65); opacity: 0.6; }

.wall {
  position: absolute;
  inset: 0;
  background-image:
    repeating-linear-gradient(0deg, rgba(61,46,31,0.06) 0 1px, transparent 1px 14px),
    repeating-linear-gradient(90deg, rgba(61,46,31,0.05) 0 1px, transparent 1px 18px);
  pointer-events: none;
}
.floor {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 38%;
  background: #B9895F;
  border-top: 3px solid var(--ink);
  background-image: repeating-linear-gradient(90deg, rgba(0,0,0,0.16) 0 2px, transparent 2px 20px);
}

.poster {
  position: absolute;
  left: 14px;
  top: 14px;
  width: 42px;
  height: 34px;
  background: var(--bg-card);
  border: 2px solid var(--ink);
  box-shadow: 2px 2px 0 rgba(61,46,31,0.15);
}
.poster-title {
  position: absolute;
  left: 7px;
  top: 5px;
  font-family: var(--font-pix);
  font-size: 8px;
  color: var(--orange-d);
}
.poster-line {
  position: absolute;
  left: 7px;
  height: 3px;
  background: var(--ink);
}
.poster-line.a { top: 18px; width: 26px; }
.poster-line.b { top: 25px; width: 18px; background: var(--green); }

.plant {
  position: absolute;
  right: 17px;
  top: 20px;
  width: 26px;
  height: 36px;
}
.pot {
  position: absolute;
  left: 8px;
  bottom: 0;
  width: 14px;
  height: 11px;
  background: var(--orange-d);
  border: 2px solid var(--ink);
}
.leaf {
  position: absolute;
  bottom: 12px;
  width: 11px;
  height: 18px;
  background: var(--green);
  border: 1px solid var(--ink);
  border-radius: 10px 10px 0 10px;
}
.leaf.l { left: 4px; transform: rotate(-24deg); }
.leaf.r { right: 2px; transform: rotate(22deg); background: var(--olive); }

.note-out {
  position: absolute;
  left: 50%;
  top: 52px;
  transform: translateX(-50%);
  font-family: var(--font-pix);
  font-size: 18px;
  color: var(--orange-d);
  animation: noteFloat 1.5s ease-in-out infinite;
}
@keyframes noteFloat {
  0%, 100% { transform: translate(-50%, 0); opacity: 0.65; }
  50% { transform: translate(-50%, -5px); opacity: 1; }
}

.desk-top {
  position: absolute;
  left: 14px;
  right: 14px;
  bottom: 36%;
  height: 9px;
  background: #6E3A2A;
  border: 2px solid var(--ink);
  z-index: 2;
}
.desk-leg {
  position: absolute;
  bottom: calc(36% - 22px);
  width: 5px;
  height: 18px;
  background: #6E3A2A;
  border: 2px solid var(--ink);
}
.desk-leg.l { left: 22px; }
.desk-leg.r { right: 22px; }

.monitor {
  position: absolute;
  left: 48%;
  bottom: calc(36% + 7px);
  transform: translateX(-50%);
  width: 62px;
  z-index: 3;
}
.screen {
  position: relative;
  width: 62px;
  height: 38px;
  background: #172331;
  border: 2px solid var(--ink);
  overflow: hidden;
  box-shadow: inset 0 0 0 1px #3A4E5F;
}
.screen.dark {
  background: #0A1208;
  box-shadow: none;
}
.screen.sleep { background: #15201F; }
.sky {
  position: absolute;
  inset: 0;
  background: linear-gradient(#87B4D6 0 45%, #F3C86B 46% 49%, #23415B 50% 100%);
}
.sun {
  position: absolute;
  right: 8px;
  top: 6px;
  width: 8px;
  height: 8px;
  background: var(--orange);
  border: 1px solid var(--ink);
  border-radius: 50%;
}
.wave {
  position: absolute;
  left: 4px;
  height: 2px;
  background: var(--bg-card);
  animation: drift 2s linear infinite;
}
.wave.w1 { top: 23px; width: 25px; }
.wave.w2 { top: 28px; width: 38px; animation-delay: 0.45s; }
.wave.w3 { top: 33px; width: 20px; animation-delay: 0.9s; }
@keyframes drift {
  0% { transform: translateX(-8px); opacity: 0.3; }
  50% { opacity: 1; }
  100% { transform: translateX(16px); opacity: 0.3; }
}
.equalizer {
  position: absolute;
  bottom: 4px;
  width: 4px;
  background: var(--orange);
  border-left: 1px solid var(--ink);
  border-right: 1px solid var(--ink);
  animation: eq 0.8s ease-in-out infinite;
}
.equalizer.e1 { right: 15px; height: 8px; }
.equalizer.e2 { right: 9px; height: 14px; animation-delay: 0.15s; }
.equalizer.e3 { right: 3px; height: 10px; animation-delay: 0.3s; }
@keyframes eq {
  0%, 100% { transform: scaleY(0.45); transform-origin: bottom; }
  50% { transform: scaleY(1); transform-origin: bottom; }
}
.zzz {
  position: absolute;
  right: 6px;
  top: 5px;
  font-family: var(--font-pix);
  font-size: 9px;
  color: #6FA88A;
  animation: zzzfade 2s ease-in-out infinite;
}
.stand { width: 18px; height: 4px; background: var(--ink); margin: 0 auto; }
.keyboard {
  width: 48px;
  height: 5px;
  background: #3D2E1F;
  border: 2px solid var(--ink);
  margin: 4px auto 0;
}

.coffee {
  position: absolute;
  right: 48px;
  bottom: calc(36% + 7px);
  width: 18px;
  height: 24px;
  z-index: 4;
}
.cup {
  position: absolute;
  left: 3px;
  bottom: 0;
  width: 12px;
  height: 11px;
  background: var(--bg-card);
  border: 2px solid var(--ink);
}
.cup::after {
  content: '';
  position: absolute;
  right: -7px;
  top: 2px;
  width: 5px;
  height: 5px;
  border: 2px solid var(--ink);
  border-left: none;
}
.steam {
  position: absolute;
  width: 2px;
  height: 8px;
  background: var(--ink-soft);
  animation: steam 1.4s ease-in-out infinite;
}
.steam.s1 { left: 5px; top: 0; }
.steam.s2 { left: 11px; top: 1px; animation-delay: 0.35s; }
@keyframes steam {
  0%, 100% { transform: translateY(0); opacity: 0.2; }
  50% { transform: translateY(-4px); opacity: 0.9; }
}

.chair {
  position: absolute;
  left: 47%;
  bottom: 4px;
  transform: translateX(-50%);
  width: 36px;
  height: 36px;
}
.chair-back,
.chair-seat {
  position: absolute;
  background: #6E3A2A;
  border: 2px solid var(--ink);
}
.chair-back { left: 6px; top: 0; width: 24px; height: 20px; }
.chair-seat { left: 0; top: 18px; width: 36px; height: 7px; }
.chair-leg {
  position: absolute;
  left: 14px;
  top: 25px;
  width: 8px;
  height: 11px;
  background: var(--ink);
}

.person {
  position: absolute;
  left: 47%;
  bottom: 18px;
  transform: translateX(-50%);
  width: 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 5;
}
.head-wrap {
  position: relative;
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.headphone {
  position: absolute;
  left: -3px;
  right: -3px;
  top: -2px;
  height: 8px;
  border: 2px solid var(--ink);
  border-bottom: none;
  border-radius: 10px 10px 0 0;
}
.headphone::before,
.headphone::after {
  content: '';
  position: absolute;
  top: 4px;
  width: 4px;
  height: 6px;
  background: var(--ink);
}
.headphone::before { left: -2px; }
.headphone::after { right: -2px; }
.zhead {
  position: absolute;
  left: -8px;
  top: -10px;
  font-family: var(--font-pix);
  font-size: 9px;
  color: var(--ink-soft);
  animation: zzzfade 2s ease-in-out infinite;
}
@keyframes zzzfade {
  0%, 100% { transform: translateY(0); opacity: 0.4; }
  50% { transform: translateY(-4px); opacity: 1; }
}
.body {
  width: 22px;
  height: 10px;
  background: var(--blue);
  border: 2px solid var(--ink);
  margin-top: -3px;
}
.arm-l,
.arm-r {
  position: absolute;
  bottom: 4px;
  width: 4px;
  height: 6px;
  background: var(--blue);
  border: 2px solid var(--ink);
}
.arm-l { left: 1px; transform-origin: top center; }
.arm-r { right: 1px; transform-origin: top center; }
.person.typing { animation: bobtype 0.5s ease-in-out infinite; }
.person.typing .arm-l { animation: type-l 0.4s ease-in-out infinite; }
.person.typing .arm-r { animation: type-r 0.4s ease-in-out infinite reverse; }
@keyframes bobtype {
  0%, 100% { transform: translate(-50%, 0); }
  50% { transform: translate(-50%, -1px); }
}
@keyframes type-l {
  0%, 100% { transform: rotate(18deg); }
  50% { transform: rotate(-10deg); }
}
@keyframes type-r {
  0%, 100% { transform: rotate(-18deg); }
  50% { transform: rotate(10deg); }
}
.person.sipping { animation: sip 1.8s ease-in-out infinite; }
@keyframes sip {
  0%, 100% { transform: translate(-50%, 0); }
  55% { transform: translate(-50%, -3px); }
}

.companion {
  position: absolute;
  right: 12px;
  bottom: 10px;
  width: 44px;
  height: 70px;
  z-index: 5;
  animation: companionBob 1.6s ease-in-out infinite;
}
.companion.wait { animation-duration: 2.6s; }
@keyframes companionBob {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-2px); }
}
.hair-back {
  position: absolute;
  left: 10px;
  top: 0;
  width: 25px;
  height: 34px;
  background: #C76083;
  border: 2px solid var(--ink);
  box-shadow:
    -3px 7px 0 #A94E71,
    3px 7px 0 #E18EAA;
}
.tail {
  position: absolute;
  top: 16px;
  width: 10px;
  height: 30px;
  background: #C76083;
  border: 2px solid var(--ink);
  z-index: 1;
}
.tail.left {
  left: 5px;
  transform: rotate(10deg);
  box-shadow: -2px 10px 0 #A94E71;
}
.tail.right {
  right: 5px;
  transform: rotate(-10deg);
  box-shadow: 2px 10px 0 #E18EAA;
}
.face {
  position: absolute;
  left: 12px;
  top: 8px;
  width: 21px;
  height: 19px;
  background: #F4C7A3;
  border: 2px solid var(--ink);
  z-index: 3;
}
.eye {
  position: absolute;
  top: 7px;
  width: 3px;
  height: 4px;
  background: var(--ink);
  animation: blinkFace 4s steps(2) infinite;
}
.eye.left { left: 4px; }
.eye.right { right: 4px; }
@keyframes blinkFace {
  0%, 90%, 100% { height: 4px; }
  94% { height: 1px; transform: translateY(2px); }
}
.blush {
  position: absolute;
  top: 12px;
  width: 4px;
  height: 2px;
  background: var(--pink);
}
.blush.left { left: 2px; }
.blush.right { right: 2px; }
.mouth {
  position: absolute;
  left: 9px;
  top: 13px;
  width: 4px;
  height: 2px;
  background: var(--ink);
}
.bang {
  position: absolute;
  left: 10px;
  top: 3px;
  width: 25px;
  height: 11px;
  background: #D77799;
  border: 2px solid var(--ink);
  border-bottom: 2px solid var(--ink);
  z-index: 4;
}
.bang::before,
.bang::after {
  content: '';
  position: absolute;
  bottom: -7px;
  width: 6px;
  height: 8px;
  background: #D77799;
  border: 2px solid var(--ink);
  border-top: none;
}
.bang::before { left: 1px; }
.bang::after { right: 2px; height: 6px; }
.ribbon {
  position: absolute;
  right: 6px;
  top: 9px;
  width: 8px;
  height: 8px;
  background: var(--orange);
  border: 2px solid var(--ink);
  z-index: 5;
  transform: rotate(45deg);
}
.dress {
  position: absolute;
  left: 11px;
  top: 31px;
  width: 23px;
  height: 26px;
  background: #78A9D4;
  border: 2px solid var(--ink);
  z-index: 3;
  clip-path: polygon(18% 0, 82% 0, 100% 100%, 0 100%);
}
.collar {
  position: absolute;
  left: 7px;
  top: 0;
  width: 9px;
  height: 7px;
  background: var(--bg-card);
  border: 2px solid var(--ink);
  border-top: none;
}
.belt {
  position: absolute;
  left: 4px;
  right: 4px;
  top: 14px;
  height: 3px;
  background: var(--orange);
  border-top: 1px solid var(--ink);
  border-bottom: 1px solid var(--ink);
}
.companion .arm {
  position: absolute;
  top: 35px;
  width: 6px;
  height: 18px;
  background: #F4C7A3;
  border: 2px solid var(--ink);
  z-index: 2;
}
.companion .arm.a {
  left: 6px;
  transform: rotate(14deg);
}
.companion .arm.b {
  right: 4px;
  transform: rotate(-22deg);
  animation: waveHand 1.8s ease-in-out infinite;
}
@keyframes waveHand {
  0%, 100% { transform: rotate(-22deg); }
  50% { transform: rotate(-42deg); }
}
.companion .leg {
  position: absolute;
  bottom: 6px;
  width: 6px;
  height: 14px;
  background: #F4C7A3;
  border: 2px solid var(--ink);
  z-index: 1;
}
.companion .leg.a { left: 14px; }
.companion .leg.b { right: 13px; }
.boot {
  position: absolute;
  bottom: 0;
  width: 10px;
  height: 7px;
  background: #4B2D25;
  border: 2px solid var(--ink);
  z-index: 4;
}
.boot.a { left: 10px; }
.boot.b { right: 9px; }
.heart {
  position: absolute;
  right: -4px;
  top: 5px;
  font-family: var(--font-pix);
  font-size: 9px;
  color: var(--orange-d);
  animation: heartPop 1.2s ease-in-out infinite;
}
@keyframes heartPop {
  0%, 100% { transform: scale(0.9); opacity: 0.55; }
  50% { transform: scale(1.15); opacity: 1; }
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
  z-index: 6;
}
.nameplate {
  position: absolute;
  left: 0;
  right: 0;
  bottom: -3px;
  display: flex;
  justify-content: center;
  z-index: 7;
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
  background: var(--bg-card);
  border: 2px solid var(--ink);
  box-shadow: 2px 2px 0 var(--ink);
  padding: 3px 8px;
  font-size: 13px;
  white-space: nowrap;
  z-index: 6;
}
.bubble {
  position: absolute;
  top: -16px;
  right: -8px;
  font-size: 24px;
  z-index: 8;
  animation: pop 0.4s ease-out, float 1.6s ease-in-out 0.4s infinite;
}
@keyframes pop {
  0% { transform: scale(0.2); opacity: 0; }
  60% { transform: scale(1.3); opacity: 1; }
  100% { transform: scale(1); }
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}
</style>
