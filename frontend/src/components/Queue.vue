<script setup>
import { useRadioStore } from '../stores/radio.js'
import Avatar from './Avatar.vue'

const radio = useRadioStore()
</script>

<template>
  <div class="pix-card">
    <div class="row" style="margin-bottom:12px">
      <div class="pix-h">▼ QUEUE</div>
      <span class="pix-tag" style="margin-left:8px">{{ radio.queue.length }}</span>
    </div>

    <div v-if="radio.queue.length === 0" style="padding:14px 0;font-size:15px" class="muted">
      暂时没人点歌<br/>电台正在放兜底曲
    </div>

    <div v-else class="pix-scroll" style="max-height:380px;overflow-y:auto">
      <div v-for="(q, i) in radio.queue" :key="q.neid + '-' + i" class="q-row">
        <span class="q-num">{{ String(i + 1).padStart(2, '0') }}</span>
        <Avatar :nick="q.requester_nick" size="sm"/>
        <div style="flex:1;min-width:0">
          <div class="q-title">{{ q.title }}</div>
          <div class="q-meta">
            <span style="color:var(--ink-soft)">{{ q.artist }}</span>
            <span class="dot-sep">·</span>
            <span style="color:var(--ink-mute)">{{ q.requester_nick }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.q-row {
  display: flex; align-items: center; gap: 10px;
  padding: 8px 0;
  border-bottom: 1px dashed #C4A785;
}
.q-row:last-child { border-bottom: none; }
.q-num {
  font-family: var(--font-pix);
  font-size: 9px; color: var(--ink-mute); width: 22px;
}
.q-title {
  font-size: 17px; line-height: 1.2;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.q-meta { font-size: 13px; margin-top: 2px; }
.dot-sep { margin: 0 6px; color: var(--ink-mute); }
</style>
