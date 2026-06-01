<script setup>
import { ref } from 'vue'
import { api } from '../api.js'
import { fmtTime } from '../utils.js'

const q = ref('')
const results = ref([])
const busy = ref(false)
const msg = ref('')
const msgTone = ref('') // ok | err

async function search() {
  if (!q.value.trim()) return
  busy.value = true
  msg.value = ''
  try {
    const r = await api.search(q.value.trim())
    results.value = r.items
    if (results.value.length === 0) {
      msg.value = '没找到相关歌曲'; msgTone.value = 'err'
    }
  } catch (e) {
    msg.value = e.message; msgTone.value = 'err'
  } finally {
    busy.value = false
  }
}

async function add(s) {
  msg.value = ''
  try {
    const r = await api.enqueue(s.neid)
    msg.value = `「${s.title}」${r.msg}`; msgTone.value = 'ok'
  } catch (e) {
    msg.value = e.message; msgTone.value = 'err'
  }
}
</script>

<template>
  <div class="pix-card">
    <div class="pix-h" style="margin-bottom:12px">▼ REQUEST A SONG</div>
    <div class="row" style="gap:8px">
      <input class="pix-input" v-model="q" @keydown.enter="search" placeholder="歌名 / 歌手"/>
      <button class="pix-btn" :disabled="busy || !q" @click="search">{{ busy ? '...' : 'FIND' }}</button>
    </div>

    <div v-if="msg" class="msg" :class="msgTone">{{ msg }}</div>

    <div v-if="results.length" class="pix-scroll" style="margin-top:12px;max-height:340px;overflow-y:auto">
      <div v-for="s in results" :key="s.neid" class="s-row">
        <img v-if="s.cover_url" :src="s.cover_url" class="s-cover" referrerpolicy="no-referrer"/>
        <div v-else class="s-cover s-cover-fallback"></div>
        <div style="flex:1;min-width:0">
          <div class="s-title">{{ s.title }}</div>
          <div class="s-meta">
            <span>{{ s.artist }}</span>
            <span style="margin:0 6px;color:var(--ink-mute)">·</span>
            <span style="color:var(--ink-mute)">{{ fmtTime(s.duration) }}</span>
          </div>
        </div>
        <button class="pix-btn ghost" style="font-size:8px;padding:6px 8px" @click="add(s)">+ ADD</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.s-row {
  display: flex; align-items: center; gap: 10px;
  padding: 8px 0; border-bottom: 1px dashed #C4A785;
}
.s-row:last-child { border-bottom: none; }
.s-cover {
  width: 40px; height: 40px;
  border: 2px solid var(--ink);
  object-fit: cover; flex-shrink: 0;
}
.s-cover-fallback {
  background: linear-gradient(45deg, var(--blue) 25%, transparent 25%, transparent 50%, var(--blue) 50%, var(--blue) 75%, transparent 75%);
  background-size: 8px 8px;
  background-color: var(--bg-soft);
}
.s-title {
  font-size: 17px; line-height: 1.2;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.s-meta { font-size: 13px; margin-top: 2px; color: var(--ink-soft); }
.msg {
  margin-top: 10px; padding: 8px 10px;
  font-size: 15px;
  border: 2px dashed var(--ink);
  background: var(--bg-soft);
}
.msg.ok { border-color: var(--green); background: #F0F6E8; color: #4D6635; }
.msg.err { border-color: var(--danger); background: #FCEBEB; color: var(--danger); }
</style>
