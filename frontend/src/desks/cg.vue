<script setup>
/**
 * cg 的工位 —— 程序员摸鱼场示范款。
 * 复制本文件改名 `<你的昵称>.vue`，再在 _layout.json 的 slots 数组里
 * 把对应位置改成你的昵称，PR 即可。
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

const moodLabel = computed(() => {
  if (offline.value) return 'afk'
  if (inBar.value) return '泡在酒馆'
  if (sleeping.value) return '宕机休眠'
  if (coffee.value) return '续命中'
  return props.text || 'vibing'
})
</script>

<template>
  <div class="cube" :class="{ offline, me: isMe, bar: inBar, sleep: sleeping }">
    <div class="wall"></div>
    <div class="floor"></div>

    <div class="bubble" v-if="poke">{{ poke.emoji }}</div>

    <!-- 后墙：奖牌 + 挂钟 -->
    <div class="medal">
      <div class="ribbon"></div>
      <div class="coin">★</div>
    </div>
    <div class="clock">
      <span class="h"></span>
      <span class="m"></span>
    </div>

    <!-- 黑胶机：在线时旋转 -->
    <div class="vinyl">
      <div class="vinyl-disc" :class="{ play: atDesk }">
        <div class="vinyl-label"></div>
      </div>
      <div class="vinyl-arm"></div>
    </div>

    <!-- 去酒馆：屋顶冒♪ -->
    <div class="note-out" v-if="inBar">♪</div>

    <!-- 双显示器 -->
    <div class="monitors">
      <div class="screen left" :class="{ on: atDesk && !sleeping, dark: offline || inBar, sleep: sleeping }">
        <div class="cmd" v-if="atDesk && !sleeping">$ vibe_</div>
        <div class="zzz" v-if="sleeping">z</div>
      </div>
      <div class="screen right" :class="{ on: atDesk && !sleeping, dark: offline || inBar, sleep: sleeping }">
        <div class="bar1" v-if="atDesk && !sleeping"></div>
        <div class="bar2" v-if="atDesk && !sleeping"></div>
        <div class="bar3" v-if="atDesk && !sleeping"></div>
      </div>
    </div>
    <div class="keyboard"></div>

    <!-- 桌子 -->
    <div class="desk-top"></div>
    <div class="desk-leg l"></div>
    <div class="desk-leg r"></div>

    <!-- 桌上的咖啡 -->
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

    <!-- 主人 -->
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

    <!-- 地上一只小橘猫（在线时摇尾巴） -->
    <div class="cat" :class="{ active: atDesk }">
      <div class="ear l"></div>
      <div class="ear r"></div>
      <div class="cat-body"></div>
      <div class="tail"></div>
    </div>
    <!-- 地上一本书 -->
    <div class="book"></div>

    <div class="bar-tag" v-if="inBar">在酒馆</div>
    <div class="nameplate"><span>{{ nick }}</span></div>
    <div class="status">{{ moodLabel }}</div>
  </div>
</template>

<style scoped>
/* —— 复用 default 的所有基础样式 —— */
.cube {
  position: relative;
  width: 100%; height: 100%;
  border: 3px solid var(--ink);
  overflow: visible;
  image-rendering: pixelated;
  background: #FFE4B6;
}
.cube.me { box-shadow: 0 0 0 2px var(--orange-d); }
.cube.offline { filter: grayscale(0.65); opacity: 0.6; }

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
  background: #C49A6E;
  border-top: 3px solid var(--ink);
  background-image: repeating-linear-gradient(0deg, rgba(0,0,0,0.18) 0 2px, transparent 2px 14px);
}

/* 奖牌 */
.medal { position: absolute; left: 14px; top: 14px; width: 32px; height: 36px; }
.medal .ribbon {
  position: absolute; left: 4px; top: 0;
  width: 0; height: 0;
  border-left: 12px solid var(--orange-d);
  border-right: 12px solid var(--orange-d);
  border-bottom: 14px solid transparent;
}
.medal .coin {
  position: absolute; left: 4px; top: 12px;
  width: 24px; height: 24px;
  background: #E8B85A;
  border: 2px solid var(--ink);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-family: var(--font-pix);
  font-size: 11px;
  color: var(--ink);
}

.clock {
  position: absolute; right: 14px; top: 14px;
  width: 24px; height: 24px;
  background: var(--bg-card);
  border: 2px solid var(--ink);
  border-radius: 50%;
}
.clock .h, .clock .m {
  position: absolute; left: 50%; top: 50%;
  background: var(--ink); transform-origin: top center;
}
.clock .h { width: 2px; height: 6px; margin-left: -1px; transform: rotate(60deg); animation: spin 60s linear infinite; }
.clock .m { width: 2px; height: 9px; margin-left: -1px; transform: rotate(0);    animation: spin 6s  linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* 黑胶 */
.vinyl {
  position: absolute;
  left: 12px;
  bottom: calc(38% + 4px);
  width: 38px; height: 26px;
  background: #5C3A22;
  border: 2px solid var(--ink);
}
.vinyl-disc {
  position: absolute;
  left: 4px; top: 3px;
  width: 20px; height: 20px;
  border-radius: 50%;
  background: radial-gradient(circle, #1F1F1F 0 60%, #3D2E1F 61% 75%, #1F1F1F 76% 100%);
  border: 1px solid var(--ink);
}
.vinyl-disc.play { animation: vspin 4s linear infinite; }
@keyframes vspin { to { transform: rotate(360deg); } }
.vinyl-label {
  position: absolute; left: 50%; top: 50%;
  width: 6px; height: 6px;
  background: var(--orange);
  border: 1px solid var(--ink);
  border-radius: 50%;
  transform: translate(-50%, -50%);
}
.vinyl-arm {
  position: absolute;
  right: 3px; top: 2px;
  width: 12px; height: 2px;
  background: var(--ink);
  transform-origin: right center;
  transform: rotate(-30deg);
}

/* 双显示器 */
.monitors {
  position: absolute;
  left: 50%; transform: translateX(-50%);
  bottom: calc(38% + 8px);
  display: flex; gap: 3px;
}
.screen {
  width: 32px; height: 28px;
  background: #1F2F1B;
  border: 2px solid var(--ink);
  position: relative; overflow: hidden;
}
.screen.right { background: #2A1F2F; }
.screen.dark  { background: #0A1208; }
.screen.sleep { background: #15201F; }
.cmd { color: #B7E26F; font-family: var(--font-pix); font-size: 7px; padding: 5px 3px; animation: blink 1.2s steps(2) infinite; }
@keyframes blink { 50% { opacity: 0.3; } }
.zzz {
  position: absolute; right: 4px; top: 4px;
  font-family: var(--font-pix); font-size: 9px; color: #6FA88A;
  animation: zzzfade 2s ease-in-out infinite;
}
@keyframes zzzfade {
  0%, 100% { transform: translateY(0); opacity: 0.4; }
  50%      { transform: translateY(-4px); opacity: 1; }
}
.bar1, .bar2, .bar3 {
  position: absolute; bottom: 4px; width: 5px; background: var(--orange);
  animation: eq 0.8s ease-in-out infinite;
}
.bar1 { left: 4px;  height: 10px; }
.bar2 { left: 12px; height: 18px; animation-delay: 0.2s; }
.bar3 { left: 20px; height: 12px; animation-delay: 0.4s; }
@keyframes eq {
  0%, 100% { transform: scaleY(0.5); transform-origin: bottom; }
  50%      { transform: scaleY(1);   transform-origin: bottom; }
}

.keyboard {
  position: absolute;
  left: 50%; transform: translateX(-50%);
  bottom: calc(38% - 4px);
  width: 50px; height: 5px;
  background: #3D2E1F; border: 2px solid var(--ink);
  z-index: 2;
}

.desk-top {
  position: absolute;
  left: 14px; right: 14px;
  bottom: 36%;
  height: 9px;
  background: #6E3A2A; border: 2px solid var(--ink);
}
.desk-leg {
  position: absolute;
  bottom: calc(36% - 22px);
  width: 5px; height: 18px;
  background: #6E3A2A; border: 2px solid var(--ink);
}
.desk-leg.l { left: 22px; }
.desk-leg.r { right: 22px; }

/* 椅子 + 小人 */
.chair { position: absolute; left: 50%; bottom: 4px; transform: translateX(-50%); width: 36px; height: 36px; }
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
.person .head-wrap { position: relative; width: 22px; height: 22px; display: flex; align-items: center; justify-content: center; }
.headphone {
  position: absolute;
  left: -3px; right: -3px; top: -2px;
  height: 8px;
  border: 2px solid var(--ink); border-bottom: none; border-radius: 10px 10px 0 0;
}
.headphone::before, .headphone::after {
  content: ''; position: absolute; top: 4px;
  width: 4px; height: 6px; background: var(--ink);
}
.headphone::before { left: -2px; }
.headphone::after  { right: -2px; }

.zhead {
  position: absolute; left: -8px; top: -10px;
  font-family: var(--font-pix); font-size: 9px; color: var(--ink-soft);
  animation: zzzfade 2s ease-in-out infinite;
}

.person .body {
  width: 22px; height: 10px;
  background: var(--orange);
  border: 2px solid var(--ink);
  margin-top: -3px;
}
.arm-l, .arm-r {
  position: absolute; bottom: 4px;
  width: 4px; height: 6px;
  background: var(--orange); border: 2px solid var(--ink);
}
.arm-l { left: 1px; transform-origin: top center; }
.arm-r { right: 1px; transform-origin: top center; }

.person.typing  { animation: bobtype 0.5s ease-in-out infinite; }
.person.typing .arm-l { animation: type-l 0.4s ease-in-out infinite; }
.person.typing .arm-r { animation: type-r 0.4s ease-in-out infinite 0.2s; }
@keyframes bobtype {
  0%, 100% { transform: translate(-50%, 0); }
  50%      { transform: translate(-50%, -1px); }
}
@keyframes type-l { 0%,100%{transform:translateY(0) rotate(0);} 50%{transform:translateY(-2px) rotate(-12deg);} }
@keyframes type-r { 0%,100%{transform:translateY(0) rotate(0);} 50%{transform:translateY(-2px) rotate(12deg);} }

.person.sleeping { animation: slump 4s ease-in-out infinite; }
@keyframes slump { 0%,100%{transform:translate(-50%,0);} 50%{transform:translate(-50%,2px);} }

.person.sipping  { animation: sip 2.4s ease-in-out infinite; }
.person.sipping .arm-r { animation: sip-arm 2.4s ease-in-out infinite; }
@keyframes sip { 0%,60%,100%{transform:translate(-50%,0);} 30%{transform:translate(-50%,-1px);} }
@keyframes sip-arm { 0%,60%,100%{transform:translateY(0) rotate(0);} 30%{transform:translateY(-3px) rotate(20deg);} }

/* 咖啡 */
.coffee {
  position: absolute;
  left: 30px;
  bottom: calc(36% + 5px);
  width: 14px; height: 12px;
}
.coffee .cup {
  width: 14px; height: 12px;
  background: var(--bg-card); border: 2px solid var(--ink);
  border-radius: 1px 1px 4px 4px;
}
.coffee .cup::before {
  content: ''; position: absolute; right: -5px; top: 3px;
  width: 4px; height: 5px;
  border: 2px solid var(--ink); border-left: none; border-radius: 0 4px 4px 0;
}
.coffee .steam {
  position: absolute; bottom: 12px;
  width: 3px; height: 3px;
  background: rgba(255,255,255,0.85); border: 1px solid var(--ink);
  border-radius: 50%;
}
.coffee .steam.s1 { left: 3px; animation: steam 2s ease-in-out infinite; }
.coffee .steam.s2 { left: 8px; animation: steam 2s ease-in-out infinite 0.5s; }
@keyframes steam {
  0%   { transform: translateY(0)    scale(0.6); opacity: 0.9; }
  60%  { transform: translateY(-8px) scale(1);   opacity: 0.7; }
  100% { transform: translateY(-14px) scale(0.4); opacity: 0; }
}

/* 猫 + 书 */
.cat {
  position: absolute; right: 16px; bottom: 8px;
  width: 26px; height: 18px;
}
.cat .ear { position: absolute; top: -2px; width: 0; height: 0; border-left: 5px solid transparent; border-right: 5px solid transparent; border-bottom: 7px solid var(--ink); }
.cat .ear.l { left: 2px; transform: rotate(-15deg); }
.cat .ear.r { left: 14px; transform: rotate(15deg); }
.cat-body { position: absolute; bottom: 0; left: 0; width: 22px; height: 14px; background: var(--orange); border: 2px solid var(--ink); border-radius: 7px 7px 5px 5px; }
.tail {
  position: absolute; right: -4px; bottom: 4px;
  width: 10px; height: 4px;
  background: var(--orange); border: 2px solid var(--ink);
  transform-origin: left center;
}
.cat.active .tail { animation: wag 1.6s ease-in-out infinite; }
@keyframes wag {
  0%, 100% { transform: rotate(-10deg); }
  50%      { transform: rotate(20deg); }
}
.book {
  position: absolute; left: 16px; bottom: 6px;
  width: 16px; height: 5px;
  background: var(--green); border: 2px solid var(--ink);
  transform: rotate(-8deg);
}

/* 在酒馆装饰 */
.note-out {
  position: absolute; right: 50px; top: -2px;
  font-family: var(--font-pix); font-size: 14px; color: var(--orange-d);
  animation: noteup 1.6s ease-in-out infinite;
}
@keyframes noteup {
  0%   { transform: translateY(0); opacity: 0; }
  20%  { opacity: 1; }
  100% { transform: translateY(-14px); opacity: 0; }
}

.bar-tag {
  position: absolute; top: 6px; left: 50%; transform: translateX(-50%);
  font-family: var(--font-pix); font-size: 8px;
  background: var(--orange-d); color: var(--bg-card);
  padding: 2px 6px; letter-spacing: 1px; z-index: 3;
}

/* 名牌 + 状态 */
.nameplate { position: absolute; left: 0; right: 0; bottom: -3px; display: flex; justify-content: center; pointer-events: none; }
.nameplate span {
  font-family: var(--font-pix); font-size: 8px; letter-spacing: 1px;
  color: var(--bg-card); background: var(--ink); border: 2px solid var(--ink); padding: 3px 6px;
}
.status {
  position: absolute; left: 50%; top: -12px; transform: translateX(-50%);
  background: var(--bg-card); border: 2px solid var(--ink); box-shadow: 2px 2px 0 var(--ink);
  padding: 3px 8px; font-size: 13px; white-space: nowrap;
  max-width: 92%; overflow: hidden; text-overflow: ellipsis; z-index: 3;
}
.status::after {
  content: ''; position: absolute; left: 18px; bottom: -6px;
  width: 6px; height: 6px; background: var(--bg-card);
  border-right: 2px solid var(--ink); border-bottom: 2px solid var(--ink);
  transform: rotate(45deg);
}

.bubble {
  position: absolute; top: -16px; right: -8px;
  font-size: 24px; z-index: 4;
  animation: pop 0.4s ease-out, float 1.6s ease-in-out 0.4s infinite;
  pointer-events: none;
}
@keyframes pop { 0%{transform:scale(0.2);opacity:0;} 60%{transform:scale(1.3);opacity:1;} 100%{transform:scale(1);opacity:1;} }
@keyframes float { 0%,100%{transform:translateY(0);} 50%{transform:translateY(-4px);} }
</style>
