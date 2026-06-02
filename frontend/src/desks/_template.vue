<script setup>
/**
 * 工位模板。复制本文件改名 `<你的昵称>.vue`，再到 _layout.json 的 slots 里
 * 把对应位置改成你的昵称。详细规则见 desks/README.md。
 *
 * 已经预接好状态钩子：
 *   atDesk   = 在线 + 不在酒馆
 *   inBar    = 在线 + 在酒馆
 *   offline  = 不在线
 *   sleeping = 自填带 z / 睡 / sleep / afk
 *   coffee   = 自填带 ☕ / 咖啡 / coffee / 续命
 *   headphone= 自填带 🎧 / listen / 听歌
 * 你的工位会自动用得到这些 class，自由发挥。
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
const txt      = computed(() => (props.text || '').toLowerCase())
const sleeping = computed(() => /z+|睡|sleep|afk/.test(txt.value))
const coffee   = computed(() => /☕|咖啡|coffee|续命/.test(txt.value))
</script>

<template>
  <div class="cube" :class="{ offline, me: isMe, bar: inBar, sleep: sleeping }">
    <div class="wall"></div>
    <div class="floor"></div>

    <div class="bubble" v-if="poke">{{ poke.emoji }}</div>

    <!-- ⬇⬇ 你的房间装饰 ⬇⬇ -->
    <!-- 比如：海报、植物、涂鸦… -->
    <!-- ⬆⬆ -->

    <!-- 桌椅显示器（建议保留） -->
    <div class="desk-top"></div>
    <div class="monitor">
      <div class="screen" :class="{ on: atDesk && !sleeping, dark: offline || inBar }"></div>
    </div>
    <div class="chair"></div>

    <!-- 主人 -->
    <div class="person"
         v-if="atDesk"
         :class="{ typing: !sleeping && !coffee, sleeping, sipping: coffee }">
      <Avatar :nick="nick" size="sm"/>
      <div class="body"></div>
    </div>

    <div class="bar-tag" v-if="inBar">在酒馆</div>
    <div class="nameplate"><span>{{ nick }}</span></div>
    <div class="status">{{ text || (offline ? 'afk' : 'vibing') }}</div>
  </div>
</template>

<style scoped>
.cube { position: relative; width: 100%; height: 100%; border: 3px solid var(--ink); overflow: visible; background: #E9C9A0; }
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
  height: 38%; background: #B98856; border-top: 3px solid var(--ink);
  background-image: repeating-linear-gradient(0deg, rgba(0,0,0,0.18) 0 2px, transparent 2px 14px);
}

.desk-top {
  position: absolute; left: 14px; right: 14px; bottom: 36%;
  height: 9px; background: #6E3A2A; border: 2px solid var(--ink);
}
.monitor { position: absolute; left: 50%; bottom: calc(36% + 7px); transform: translateX(-50%); }
.screen { width: 60px; height: 38px; background: #1F2F1B; border: 2px solid var(--ink); }
.screen.dark { background: #0A1208; }

.chair {
  position: absolute; left: 50%; bottom: 4px; transform: translateX(-50%);
  width: 36px; height: 30px;
  background: #6E3A2A; border: 2px solid var(--ink);
}

.person {
  position: absolute; left: 50%; bottom: 18px; transform: translateX(-50%);
  display: flex; flex-direction: column; align-items: center; z-index: 2;
}
.person .body {
  width: 22px; height: 10px; background: var(--blue); border: 2px solid var(--ink); margin-top: -3px;
}
.person.typing { animation: bob 0.5s ease-in-out infinite; }
@keyframes bob { 0%,100%{transform:translate(-50%,0);} 50%{transform:translate(-50%,-1px);} }

.bar-tag {
  position: absolute; top: 6px; left: 50%; transform: translateX(-50%);
  font-family: var(--font-pix); font-size: 8px; background: var(--orange-d); color: var(--bg-card);
  padding: 2px 6px; letter-spacing: 1px; z-index: 3;
}
.nameplate { position: absolute; left: 0; right: 0; bottom: -3px; display: flex; justify-content: center; }
.nameplate span {
  font-family: var(--font-pix); font-size: 8px; letter-spacing: 1px;
  color: var(--bg-card); background: var(--ink); border: 2px solid var(--ink); padding: 3px 6px;
}
.status {
  position: absolute; left: 50%; top: -12px; transform: translateX(-50%);
  background: var(--bg-card); border: 2px solid var(--ink); box-shadow: 2px 2px 0 var(--ink);
  padding: 3px 8px; font-size: 13px; white-space: nowrap; z-index: 3;
}
.bubble {
  position: absolute; top: -16px; right: -8px; font-size: 24px;
  z-index: 4; animation: pop 0.4s ease-out, float 1.6s ease-in-out 0.4s infinite;
}
@keyframes pop { 0%{transform:scale(0.2);opacity:0;} 60%{transform:scale(1.3);opacity:1;} 100%{transform:scale(1);} }
@keyframes float { 0%,100%{transform:translateY(0);} 50%{transform:translateY(-4px);} }
</style>
