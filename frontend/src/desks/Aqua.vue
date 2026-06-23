<script setup>
/**
 * Aqua 的工位 —— 可爱官方玉桂狗（Cinnamoroll）风格主题。
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

const inBar     = computed(() => props.online && props.location === 'bar')
const atDesk    = computed(() => props.online && props.location !== 'bar')
const offline   = computed(() => !props.online)
const txt       = computed(() => (props.text || '').toLowerCase())
const sleeping  = computed(() => /z+|睡|sleep|afk|休息|🛌|💤/.test(txt.value))
const coffee    = computed(() => /☕|咖啡|coffee|续命/.test(txt.value))
const headphone = computed(() => /🎧|listen|听歌|music|fm/.test(txt.value))

const moodLabel = computed(() => {
  if (offline.value) return 'afk'
  if (inBar.value) return '去酒馆散步'
  if (sleeping.value) return '呼呼大睡中'
  if (coffee.value) return '玉桂狗下午茶'
  if (headphone.value) return '沉浸音乐中'
  return props.text || 'vibing'
})
</script>

<template>
  <div class="cube" :class="{ offline, me: isMe, bar: inBar, sleep: sleeping }">
    <!-- 后墙：梦幻星空天蓝色 + 地板：温暖奶油白 -->
    <div class="wall"></div>
    <div class="floor"></div>

    <!-- 戳一下气泡 -->
    <div class="bubble" v-if="poke">{{ poke.emoji }}</div>
    <div class="poke-tip" v-if="poke">
      <span class="poke-from">{{ poke.from }}</span>
      <span> 戳了 </span>
      <span class="poke-to">{{ isMe ? '你' : (poke.to || nick) }}</span>
    </div>

    <!-- 背景装饰：像素风星星挂件 -->
    <div class="garland">
      <span class="garland-star s1"></span>
      <span class="garland-star s2"></span>
      <span class="garland-star s3"></span>
    </div>

    <!-- 后墙：漂浮的白云 -->
    <div class="cloud-decor c1">
      <svg viewBox="0 0 36 20" width="36" height="20">
        <path d="M 6,12 A 6,6 0 0,1 12,6 A 8,8 0 0,1 24,4 A 8,8 0 0,1 32,10 A 6,6 0 0,1 36,16 A 4,4 0 0,1 32,20 L 6,20 A 5,5 0 0,1 6,12 Z" fill="#FFFFFF" stroke="var(--ink)" stroke-width="2" />
      </svg>
    </div>
    <div class="cloud-decor c2">
      <svg viewBox="0 0 36 20" width="24" height="14">
        <path d="M 6,12 A 6,6 0 0,1 12,6 A 8,8 0 0,1 24,4 A 8,8 0 0,1 32,10 A 6,6 0 0,1 36,16 A 4,4 0 0,1 32,20 L 6,20 A 5,5 0 0,1 6,12 Z" fill="#FFFFFF" stroke="var(--ink)" stroke-width="2" />
      </svg>
    </div>

    <!-- 挂在墙上的可爱官方玉桂狗海报 (使用透明背景切图，干净无黑边) -->
    <div class="poster"></div>

    <!-- 挂在右侧墙上的肉桂卷饰品 -->
    <div class="wall-decor-cinnamon-roll"></div>

    <!-- 在酒馆里的音符漂浮 -->
    <div class="note-out" v-if="inBar">♪</div>

    <!-- 地板装饰：左侧白云地毯 -->
    <svg class="cloud-rug" viewBox="0 0 50 20" width="50" height="20">
      <path d="M 8,15 Q 4,15 4,11 Q 4,7 10,7 Q 12,3 18,3 Q 26,3 28,6 Q 32,2 38,2 Q 44,2 45,7 Q 48,7 48,11 Q 48,15 42,15 Z" fill="#FFF" stroke="var(--ink)" stroke-width="2" />
    </svg>

    <!-- 桌子（白色桌面 + 粉色桌腿） -->
    <div class="desk-top"></div>
    <div class="desk-leg l"></div>
    <div class="desk-leg r"></div>

    <!-- 显示器（带玉桂狗耳朵的白色显示器） -->
    <div class="monitor">
      <div class="screen" :class="{ on: atDesk && !sleeping, dark: offline || inBar, sleep: sleeping }">
        <template v-if="atDesk && !sleeping">
          <div class="sky-bg"></div>
          <!-- 滚动像素白云 -->
          <div class="scroll-cloud"></div>
          <!-- 听歌时的音量条 -->
          <div class="bars" v-if="headphone">
            <span class="bar b1"></span>
            <span class="bar b2"></span>
          </div>
        </template>
        <span class="zzz" v-if="sleeping">z</span>
      </div>
      <div class="stand"></div>
      <div class="keyboard"></div>
    </div>

    <!-- 玉桂狗马克杯（带☕ 状态时出现） -->
    <div class="coffee" v-if="coffee && atDesk">
      <div class="cup">
        <span class="cup-eye l"></span>
        <span class="cup-eye r"></span>
        <span class="cup-mouth"></span>
      </div>
      <!-- 心形蒸汽 -->
      <div class="steam s1">♥</div>
      <div class="steam s2">♥</div>
    </div>

    <!-- 椅子（玉桂狗大耳朵椅背 + 粉色坐垫） -->
    <div class="chair">
      <div class="chair-back"></div>
      <div class="chair-seat"></div>
      <div class="chair-leg"></div>
    </div>

    <!-- 主人（在桌前） -->
    <div class="person"
         v-if="atDesk"
         :class="{ typing: !sleeping && !coffee, sleeping, sipping: coffee }">
      <div class="head-wrap">
        <Avatar :nick="nick" size="sm"/>
        <!-- 听歌时戴上可爱白蓝耳机 -->
        <div class="headphone" v-if="headphone"></div>
        <div class="zhead" v-if="sleeping">Z</div>
      </div>
      <div class="body"></div>
      <div class="arm-l"></div>
      <div class="arm-r"></div>
    </div>

    <!-- 右侧玉桂狗萌宠伴侣（在线时会开心摇摆，戴耳机/睡觉时状态同步） -->
    <div class="cinnamoroll-companion" :class="{ inactive: !atDesk, sleep: sleeping }">
      <!-- 官方玉桂狗切图 -->
      <div class="cinnamoroll-sprite"></div>

      <!-- 睡觉状态的睡帽叠加 -->
      <svg v-if="sleeping" class="c-sleep-cap-overlay" viewBox="0 0 32 16" width="28" height="14">
        <path d="M 12,12 C 10,5 24,1 28,6 C 30,8 26,12 21,12" fill="#BBD6EC" stroke="var(--ink)" stroke-width="1.5" />
        <circle cx="29" cy="6" r="2.5" fill="#FFFFFF" stroke="var(--ink)" stroke-width="1.5" />
      </svg>

      <!-- 听歌状态的耳机叠加 -->
      <svg v-if="headphone" class="c-headphone-overlay" viewBox="0 0 40 24" width="40" height="24">
        <path d="M 11,14 C 11,5 29,5 29,14" fill="none" stroke="var(--ink)" stroke-width="2.5" stroke-linecap="round" />
        <ellipse cx="10" cy="14" rx="3.5" ry="5.5" fill="#FFB3C6" stroke="var(--ink)" stroke-width="1.5" />
        <ellipse cx="30" cy="14" rx="3.5" ry="5.5" fill="#FFB3C6" stroke="var(--ink)" stroke-width="1.5" />
      </svg>

      <!-- 睡觉状态的呼呼泡泡 -->
      <span class="sleep-bubble" v-if="sleeping">💤</span>
      <!-- 在线活跃时的闪烁爱心 -->
      <span class="sparkle" v-if="atDesk && !sleeping">✦</span>
    </div>

    <!-- 底部名牌与状态 -->
    <div class="bar-tag" v-if="inBar">在酒馆</div>
    <div class="nameplate"><span>{{ nick }}</span></div>
    <div class="status">{{ moodLabel }}</div>
  </div>
</template>

<style scoped>
/* ========== 基础风格：梦幻天蓝 + 奶油白 ========== */
.cube {
  position: relative;
  width: 100%; height: 100%;
  border: 3px solid var(--ink);
  overflow: visible;
  image-rendering: pixelated;
  background: #EBF3FE; /* 浅天蓝 */
}
.cube.me { box-shadow: 0 0 0 2px var(--pink); }
.cube.offline { filter: grayscale(0.65); opacity: 0.6; }

.wall {
  position: absolute; inset: 0;
  background-image:
    repeating-linear-gradient(0deg, rgba(255,255,255,0.4) 0 1px, transparent 1px 14px),
    repeating-linear-gradient(90deg, rgba(255,255,255,0.4) 0 1px, transparent 1px 18px);
  pointer-events: none;
}
.floor {
  position: absolute; left: 0; right: 0; bottom: 0;
  height: 38%;
  background: #FFFBF2; /* 奶油白 */
  border-top: 3px solid var(--ink);
  background-image: repeating-linear-gradient(90deg, rgba(0,0,0,0.06) 0 2px, transparent 2px 20px);
}

/* ========== 星星挂件 ========== */
.garland {
  position: absolute;
  top: 6px; left: 8px; right: 8px;
  height: 10px;
  border-bottom: 2px dashed rgba(0, 0, 0, 0.1);
  border-radius: 0 0 50% 50%;
  pointer-events: none;
}
.garland-star {
  position: absolute;
  width: 5px; height: 5px;
  border: 1px solid var(--ink);
  transform: rotate(45deg);
}
.garland-star.s1 { left: 25%; top: 3px; background: #FFD6E0; }  /* 粉星 */
.garland-star.s2 { left: 50%; top: 6px; background: #FFF9DB; }  /* 黄星 */
.garland-star.s3 { left: 75%; top: 3px; background: #C6E2FF; }  /* 蓝星 */

/* ========== 漂浮的云朵 ========== */
.cloud-decor {
  position: absolute;
  pointer-events: none;
  filter: drop-shadow(1px 1px 0 rgba(0,0,0,0.05));
}
.cloud-decor.c1 { left: 50px; top: 10px; animation: floatCloud 8s ease-in-out infinite alternate; }
.cloud-decor.c2 { right: 48px; top: 12px; animation: floatCloud 6s ease-in-out infinite alternate-reverse; }
@keyframes floatCloud {
  0% { transform: translateX(0); }
  100% { transform: translateX(4px); }
}

/* ========== 墙上可爱的玉桂狗海报 ========== */
.poster {
  position: absolute;
  left: 10px; top: 26px;
  width: 46px; height: 35px;
  background-image: url('./cinnamoroll_poster.png');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  filter: drop-shadow(2px 2px 0 rgba(0,0,0,0.08));
  image-rendering: auto; /* 重置为默认平滑缩放，防止高分辨率缩小时产生像素锯齿 */
}

/* ========== 墙上可爱的肉桂卷饰品 ========== */
.wall-decor-cinnamon-roll {
  position: absolute;
  right: 18px; top: 22px;
  width: 19px; height: 31px;
  background-image: url('./cinnamon_roll_decor.png');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  filter: drop-shadow(2px 2px 0 rgba(0,0,0,0.06));
  image-rendering: auto; /* 重置为默认平滑缩放，防止高分辨率缩小时产生像素锯齿 */
}

/* ========== 地毯 ========== */
.cloud-rug {
  position: absolute;
  left: 10px; bottom: 8px;
  pointer-events: none;
  z-index: 1;
}

/* ========== 白色木桌与粉色桌腿 ========== */
.desk-top {
  position: absolute;
  left: 14px; right: 14px;
  bottom: 36%;
  height: 9px;
  background: #FFFFFF;
  border: 2px solid var(--ink);
  z-index: 2;
}
.desk-leg {
  position: absolute;
  bottom: calc(36% - 22px);
  width: 5px; height: 18px;
  background: #FFD6E0; /* 樱花粉桌腿 */
  border: 2px solid var(--ink);
}
.desk-leg.l { left: 22px; }
.desk-leg.r { right: 22px; }

/* ========== 带耳朵的白色显示器 ========== */
.monitor {
  position: absolute;
  left: 48%;
  bottom: calc(36% + 7px);
  transform: translateX(-50%);
  width: 60px;
  z-index: 3;
}
.monitor::before, .monitor::after {
  content: '';
  position: absolute;
  top: -3px;
  width: 8px; height: 16px;
  background: #FFFFFF;
  border: 2px solid var(--ink);
  border-radius: 4px;
  z-index: -1; /* 渲染在显示器壳体背后，避免遮挡屏幕 */
}
.monitor::before { left: -4px; transform: rotate(-25deg); }
.monitor::after { right: -4px; transform: rotate(25deg); }

.screen {
  position: relative;
  width: 60px; height: 38px;
  background: #FFFFFF;
  border: 2px solid var(--ink);
  box-shadow: inset 0 0 0 1px #EBF3FE;
  overflow: hidden;
}
.screen.dark { background: #0F1626; box-shadow: none; }
.screen.sleep { background: #1C2333; }
.sky-bg {
  position: absolute; inset: 0;
  background: linear-gradient(#C6E2FF 0 50%, #E8F1FC 50% 100%);
}
.scroll-cloud {
  position: absolute;
  left: 10px; top: 12px;
  width: 18px; height: 10px;
  background: #FFF;
  border-radius: 5px;
  box-shadow: 20px -4px 0 -1px #FFF;
  animation: scrollC 6s linear infinite;
}
@keyframes scrollC {
  0% { transform: translateX(-35px); }
  100% { transform: translateX(55px); }
}
.bars {
  position: absolute;
  right: 4px; bottom: 4px;
  display: flex; gap: 2px;
}
.bar {
  width: 3px; background: #FFB3C6;
  animation: eqBar 0.8s ease-in-out infinite;
}
.bar.b1 { height: 10px; }
.bar.b2 { height: 14px; animation-delay: 0.2s; }
@keyframes eqBar {
  0%, 100% { transform: scaleY(0.4); transform-origin: bottom; }
  50% { transform: scaleY(1); transform-origin: bottom; }
}

.stand { width: 16px; height: 4px; background: var(--ink); margin: 0 auto; }
.keyboard {
  width: 44px; height: 5px;
  background: #FFFFFF; border: 2px solid var(--ink);
  margin: 4px auto 0;
}

/* ========== 可爱咖啡杯 ========== */
.coffee {
  position: absolute;
  left: 20px;
  bottom: calc(36% + 6px);
  width: 14px; height: 12px;
  z-index: 4;
}
.cup {
  position: relative;
  width: 14px; height: 12px;
  background: #FFFFFF;
  border: 2px solid var(--ink);
  border-radius: 2px;
}
.cup::before {
  content: '';
  position: absolute;
  right: -5px; top: 2px;
  width: 4px; height: 5px;
  border: 2px solid var(--ink);
  border-left: none;
  border-radius: 0 3px 3px 0;
}
.cup-eye {
  position: absolute;
  top: 3px;
  width: 1.5px; height: 2px;
  background: #4B9CD3;
}
.cup-eye.l { left: 3px; }
.cup-eye.r { right: 3px; }
.cup-mouth {
  position: absolute;
  left: 50%; top: 6px; transform: translateX(-50%);
  width: 3px; height: 1.5px;
  border-bottom: 1px solid var(--ink);
  border-radius: 0 0 1.5px 1.5px;
}
.steam {
  position: absolute;
  font-size: 8px; color: #FFB3C6;
  animation: steamHeart 1.8s ease-in-out infinite;
}
.steam.s1 { left: 1px; top: -10px; }
.steam.s2 { left: 7px; top: -8px; animation-delay: 0.4s; }
@keyframes steamHeart {
  0% { transform: translateY(0) scale(0.6); opacity: 0.2; }
  50% { transform: translateY(-4px) scale(1) rotate(15deg); opacity: 0.95; }
  100% { transform: translateY(-10px) scale(0.5); opacity: 0; }
}

/* ========== 椅子 (大耳椅背) ========== */
.chair {
  position: absolute;
  left: 48%; bottom: 4px;
  transform: translateX(-50%);
  width: 36px; height: 36px;
}
.chair-back {
  position: absolute;
  left: 5px; top: 0;
  width: 26px; height: 18px;
  background: #FFFFFF;
  border: 2px solid var(--ink);
  border-radius: 8px;
}
.chair-back::before, .chair-back::after {
  content: '';
  position: absolute;
  top: 3px;
  width: 7px; height: 13px;
  background: #FFFFFF;
  border: 2px solid var(--ink);
  border-radius: 3px;
}
.chair-back::before { left: -6px; transform: rotate(-15deg); }
.chair-back::after { right: -6px; transform: rotate(15deg); }

.chair-seat {
  position: absolute;
  left: 0; top: 17px;
  width: 36px; height: 7px;
  background: #FFD6E0; /* 樱花粉坐垫 */
  border: 2px solid var(--ink);
  border-radius: 2px;
}
.chair-leg {
  position: absolute;
  left: 14px; top: 24px;
  width: 8px; height: 12px;
  background: var(--ink);
}

/* ========== 主人 (坐在椅子上) ========== */
.person {
  position: absolute;
  left: 48%; bottom: 18px;
  transform: translateX(-50%);
  width: 30px;
  display: flex; flex-direction: column; align-items: center;
  z-index: 5;
}
.head-wrap {
  position: relative;
  width: 22px; height: 22px;
  display: flex; align-items: center; justify-content: center;
}
/* 听歌时的可爱耳机 */
.headphone {
  position: absolute;
  left: -3px; right: -3px; top: -2px;
  height: 8px;
  border: 2px solid var(--ink);
  border-bottom: none;
  border-radius: 10px 10px 0 0;
}
.headphone::before, .headphone::after {
  content: '';
  position: absolute; top: 4px;
  width: 4px; height: 6px;
  background: #FFB3C6; /* 粉色耳罩 */
  border: 1.5px solid var(--ink);
  border-radius: 2px;
}
.headphone::before { left: -3px; }
.headphone::after  { right: -3px; }

.zhead {
  position: absolute;
  left: -8px; top: -10px;
  font-family: var(--font-pix);
  font-size: 9px;
  color: var(--ink-soft);
  animation: zzz 2s ease-in-out infinite;
}
@keyframes zzz {
  0%, 100% { transform: translateY(0); opacity: 0.4; }
  50% { transform: translateY(-4px); opacity: 1; }
}

.body {
  width: 22px; height: 10px;
  background: #C6E2FF; /* 天蓝色衣服 */
  border: 2px solid var(--ink);
  margin-top: -3px;
}
.arm-l, .arm-r {
  position: absolute; bottom: 4px;
  width: 4px; height: 6px;
  background: #C6E2FF;
  border: 2px solid var(--ink);
}
.arm-l { left: 1px; transform-origin: top center; }
.arm-r { right: 1px; transform-origin: top center; }

/* 动作动画 */
.person.typing { animation: bobtype 0.5s ease-in-out infinite; }
.person.typing .arm-l { animation: type-l 0.4s ease-in-out infinite; }
.person.typing .arm-r { animation: type-r 0.4s ease-in-out infinite reverse; }
@keyframes bobtype {
  0%, 100% { transform: translate(-50%, 0); }
  50% { transform: translate(-50%, -1px); }
}
@keyframes type-l {
  0%, 100% { transform: rotate(20deg); }
  50% { transform: rotate(-8deg); }
}
@keyframes type-r {
  0%, 100% { transform: rotate(-20deg); }
  50% { transform: rotate(8deg); }
}

.person.sleeping { animation: slump 4s ease-in-out infinite; }
@keyframes slump {
  0%, 100% { transform: translate(-50%, 0); }
  50% { transform: translate(-50%, 2px); }
}
.person.sipping { animation: sip 2s ease-in-out infinite; }
.person.sipping .arm-r { animation: sip-arm 2s ease-in-out infinite; }
@keyframes sip {
  0%, 100% { transform: translate(-50%, 0); }
  50% { transform: translate(-50%, -2px); }
}
@keyframes sip-arm {
  0%, 100% { transform: translateY(0) rotate(0); }
  50% { transform: translateY(-3px) rotate(22deg); }
}

/* ========== 玉桂狗伴侣 (在线/离线/睡觉/听歌动效) ========== */
.cinnamoroll-companion {
  position: absolute;
  right: 6px; bottom: 8px;
  width: 51px; height: 34px; /* 精准缩小至 85%（即 51x34） */
  z-index: 5;
  pointer-events: none;
}
.cinnamoroll-companion:not(.inactive) {
  animation: happyWobble 2s ease-in-out infinite;
}
.cinnamoroll-companion.inactive {
  filter: grayscale(0.5);
  opacity: 0.75;
}
.cinnamoroll-companion.sleep {
  animation: companionSleep 4s ease-in-out infinite;
}

/* 伴侣切图 */
.cinnamoroll-sprite {
  width: 100%; height: 100%;
  background-image: url('./cinnamoroll.png');
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center bottom;
  filter: drop-shadow(2px 2px 0 rgba(0,0,0,0.06));
  image-rendering: auto; /* 重置为默认平滑缩放，防止高分辨率缩小时产生像素锯齿 */
}

/* 伴侣叠加装扮定位 (同步调整为 51x34 下的最佳对齐尺寸) */
.c-sleep-cap-overlay {
  position: absolute;
  top: -9px;
  left: 10px;
  pointer-events: none;
  filter: drop-shadow(1px 1px 0 rgba(0,0,0,0.05));
  animation: capWobble 2s ease-in-out infinite;
}
.c-headphone-overlay {
  position: absolute;
  top: -1px;
  left: 5px;
  pointer-events: none;
  filter: drop-shadow(1px 1px 0 rgba(0,0,0,0.05));
  animation: headphoneWobble 2s ease-in-out infinite;
}

@keyframes capWobble {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50% { transform: translateY(0.5px) rotate(1deg); }
}
@keyframes headphoneWobble {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(0.5px) scale(0.98); }
}

/* 伴侣动作 */
@keyframes happyWobble {
  0%, 100% { transform: translateY(0) rotate(0); }
  50% { transform: translateY(-2px) rotate(1deg); }
}
@keyframes companionSleep {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(1px); }
}

.sleep-bubble {
  position: absolute;
  left: 6px; top: -12px;
  font-size: 8px;
  animation: floatBubble 2.2s linear infinite;
}
@keyframes floatBubble {
  0% { transform: translate(0, 0) scale(0.6); opacity: 0; }
  15% { opacity: 0.9; }
  60% { transform: translate(-3px, -8px) scale(1); opacity: 0.7; }
  100% { transform: translate(-6px, -16px) scale(0.5); opacity: 0; }
}

.sparkle {
  position: absolute;
  right: -2px; top: -8px;
  font-family: var(--font-pix);
  font-size: 9px;
  color: #FFF9DB;
  animation: sparklePop 1.5s ease-in-out infinite;
}
@keyframes sparklePop {
  0%, 100% { transform: scale(0.7) rotate(0deg); opacity: 0.4; }
  50% { transform: scale(1.1) rotate(45deg); opacity: 1; }
}

/* ========== 酒馆装饰 ========== */
.note-out {
  position: absolute;
  right: 50px; top: -2px;
  font-family: var(--font-pix);
  font-size: 14px;
  color: var(--pink);
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
  background: var(--pink); color: #FFF;
  padding: 2px 6px; letter-spacing: 1px; z-index: 6;
}

/* ========== 名牌与状态 ========== */
.nameplate { position: absolute; left: 0; right: 0; bottom: -3px; display: flex; justify-content: center; pointer-events: none; z-index: 7; }
.nameplate span {
  font-family: var(--font-pix); font-size: 8px; letter-spacing: 1px;
  color: #FFF; background: var(--ink); border: 2px solid var(--ink); padding: 3px 6px;
}

.status {
  position: absolute; left: 50%; top: -12px; transform: translateX(-50%);
  background: #FFF; border: 2px solid var(--ink); box-shadow: 2px 2px 0 var(--ink);
  padding: 3px 8px; font-size: 13px; white-space: nowrap;
  max-width: 92%; overflow: hidden; text-overflow: ellipsis; z-index: 6;
}
.status::after {
  content: ''; position: absolute; left: 18px; bottom: -6px;
  width: 6px; height: 6px; background: #FFF;
  border-right: 2px solid var(--ink); border-bottom: 2px solid var(--ink);
  transform: rotate(45deg);
}

.bubble {
  position: absolute; top: -16px; right: -8px;
  font-size: 24px; z-index: 8;
  animation: pop 0.4s ease-out, float 1.6s ease-in-out 0.4s infinite;
  pointer-events: none;
}
.poke-tip {
  position: absolute; left: 50%; top: -28px; transform: translateX(-50%);
  background: #FFD6E0; border: 2px solid var(--ink); box-shadow: 2px 2px 0 var(--ink);
  font-size: 11px; padding: 2px 6px; white-space: nowrap; z-index: 8;
  animation: pop 0.3s ease-out;
}
.poke-tip .poke-from { font-weight: bold; }
.poke-tip .poke-to   { color: var(--ink); font-weight: bold; }

@keyframes pop {
  0% { transform: scale(0.2); opacity: 0; }
  60% { transform: scale(1.3); opacity: 1; }
  100% { transform: scale(1); opacity: 1; }
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50%      { transform: translateY(-4px); }
}
</style>
