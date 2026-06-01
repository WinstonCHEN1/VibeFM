<script setup>
import { ref } from 'vue'
import { api } from '../api.js'
import { fmtTime } from '../utils.js'

const tab = ref('song')           // song | user | playlist
const q = ref('')
const busy = ref(false)
const msg = ref('')
const msgTone = ref('')

const songs = ref([])
const users = ref([])
const playlists = ref([])

const pickedUser = ref(null)      // {uid, nickname, avatar}
const userPlaylists = ref([])
const openPid = ref(null)         // 当前展开查看的歌单 ID
const openTracks = ref([])
const loadingTracks = ref(false)

function reset() {
  songs.value = []
  users.value = []
  playlists.value = []
  pickedUser.value = null
  userPlaylists.value = []
  openPid.value = null
  openTracks.value = []
  msg.value = ''
}

function switchTab(t) {
  tab.value = t
  reset()
}

async function doSearch() {
  if (!q.value.trim()) return
  busy.value = true
  msg.value = ''
  reset()
  try {
    if (tab.value === 'song') {
      const r = await api.search(q.value.trim())
      songs.value = r.items
      if (!songs.value.length) { msg.value = '没找到相关歌曲'; msgTone.value = 'err' }
    } else if (tab.value === 'user') {
      const r = await api.searchUsers(q.value.trim())
      users.value = r.items
      if (!users.value.length) { msg.value = '没找到这个用户'; msgTone.value = 'err' }
    } else if (tab.value === 'playlist') {
      const r = await api.searchPlaylists(q.value.trim())
      playlists.value = r.items
      if (!playlists.value.length) { msg.value = '没找到相关歌单'; msgTone.value = 'err' }
    }
  } catch (e) {
    msg.value = e.message; msgTone.value = 'err'
  } finally {
    busy.value = false
  }
}

async function pickUser(u) {
  pickedUser.value = u
  busy.value = true
  msg.value = ''
  userPlaylists.value = []
  try {
    const r = await api.userPlaylists(u.uid)
    userPlaylists.value = r.items
    if (!userPlaylists.value.length) {
      msg.value = '这个用户没有公开歌单'; msgTone.value = 'err'
    }
  } catch (e) {
    msg.value = e.message; msgTone.value = 'err'
  } finally {
    busy.value = false
  }
}

function backToUserList() {
  pickedUser.value = null
  userPlaylists.value = []
  openPid.value = null
  openTracks.value = []
}

async function openPlaylist(p) {
  if (openPid.value === p.id) {
    openPid.value = null
    openTracks.value = []
    return
  }
  openPid.value = p.id
  openTracks.value = []
  loadingTracks.value = true
  msg.value = ''
  try {
    const r = await api.playlistTracks(p.id)
    openTracks.value = r.items
  } catch (e) {
    msg.value = e.message; msgTone.value = 'err'
    openPid.value = null
  } finally {
    loadingTracks.value = false
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

function fmtCount(n) {
  if (!n) return '0'
  if (n >= 100000000) return (n / 100000000).toFixed(1) + '亿'
  if (n >= 10000) return (n / 10000).toFixed(1) + '万'
  return String(n)
}
</script>

<template>
  <div class="pix-card">
    <div class="row" style="margin-bottom:12px;flex-wrap:wrap;gap:6px">
      <div class="pix-h">▼ FIND MUSIC</div>
      <div class="tab-row">
        <button class="tab" :class="{ active: tab === 'song' }" @click="switchTab('song')">SONG</button>
        <button class="tab" :class="{ active: tab === 'user' }" @click="switchTab('user')">USER</button>
        <button class="tab" :class="{ active: tab === 'playlist' }" @click="switchTab('playlist')">LIST</button>
      </div>
    </div>

    <div class="row" style="gap:8px">
      <input class="pix-input" v-model="q" @keydown.enter="doSearch"
             :placeholder="tab === 'song' ? '歌名 / 歌手' : tab === 'user' ? '网易云用户昵称' : '歌单关键词，比如 夏天'"/>
      <button class="pix-btn" :disabled="busy || !q" @click="doSearch">{{ busy ? '...' : 'FIND' }}</button>
    </div>

    <div v-if="msg" class="msg" :class="msgTone">{{ msg }}</div>

    <div v-if="tab === 'song' && songs.length" class="pix-scroll list">
      <div v-for="s in songs" :key="s.neid" class="row item">
        <img v-if="s.cover_url" :src="s.cover_url" class="thumb" referrerpolicy="no-referrer"/>
        <div v-else class="thumb thumb-fb"></div>
        <div style="flex:1;min-width:0">
          <div class="ttl">{{ s.title }}</div>
          <div class="meta">{{ s.artist }} · {{ fmtTime(s.duration) }}</div>
        </div>
        <button class="pix-btn ghost mini" @click="add(s)">+ ADD</button>
      </div>
    </div>

    <div v-if="tab === 'user'">
      <div v-if="!pickedUser && users.length" class="pix-scroll list">
        <div v-for="u in users" :key="u.uid" class="row item user-row" @click="pickUser(u)">
          <img v-if="u.avatar" :src="u.avatar" class="thumb avatar-thumb" referrerpolicy="no-referrer"/>
          <div v-else class="thumb avatar-thumb thumb-fb"></div>
          <div style="flex:1;min-width:0">
            <div class="ttl">{{ u.nickname }}</div>
            <div class="meta">{{ u.signature || 'UID: ' + u.uid }}</div>
          </div>
          <span class="pix-tag">►</span>
        </div>
      </div>

      <div v-if="pickedUser">
        <div class="row pinned">
          <button class="pix-btn ghost mini" @click="backToUserList">‹ BACK</button>
          <img v-if="pickedUser.avatar" :src="pickedUser.avatar" class="thumb avatar-thumb sm" referrerpolicy="no-referrer"/>
          <div style="flex:1;min-width:0">
            <div class="ttl">{{ pickedUser.nickname }}</div>
            <div class="meta">{{ userPlaylists.length }} 个歌单</div>
          </div>
        </div>
        <div class="pix-scroll list">
          <template v-for="p in userPlaylists" :key="p.id">
            <div class="row item playlist-row" @click="openPlaylist(p)">
              <img v-if="p.cover" :src="p.cover" class="thumb" referrerpolicy="no-referrer"/>
              <div v-else class="thumb thumb-fb"></div>
              <div style="flex:1;min-width:0">
                <div class="ttl">{{ p.name }}</div>
                <div class="meta">{{ p.track_count }} 首 · {{ fmtCount(p.play_count) }} 播放</div>
              </div>
              <span class="pix-tag">{{ openPid === p.id ? '▼' : '▸' }}</span>
            </div>
            <div v-if="openPid === p.id" class="sub-tracks">
              <div v-if="loadingTracks" class="muted" style="padding:10px;font-size:14px">loading tracks...</div>
              <div v-for="t in openTracks" :key="t.neid" class="row item sub">
                <img v-if="t.cover_url" :src="t.cover_url" class="thumb sm" referrerpolicy="no-referrer"/>
                <div v-else class="thumb sm thumb-fb"></div>
                <div style="flex:1;min-width:0">
                  <div class="ttl">{{ t.title }}</div>
                  <div class="meta">{{ t.artist }} · {{ fmtTime(t.duration) }}</div>
                </div>
                <button class="pix-btn ghost mini" @click="add(t)">+ ADD</button>
              </div>
            </div>
          </template>
        </div>
      </div>
    </div>

    <div v-if="tab === 'playlist' && playlists.length" class="pix-scroll list">
      <template v-for="p in playlists" :key="p.id">
        <div class="row item playlist-row" @click="openPlaylist(p)">
          <img v-if="p.cover" :src="p.cover" class="thumb" referrerpolicy="no-referrer"/>
          <div v-else class="thumb thumb-fb"></div>
          <div style="flex:1;min-width:0">
            <div class="ttl">{{ p.name }}</div>
            <div class="meta">{{ p.creator }} · {{ p.track_count }} 首 · {{ fmtCount(p.play_count) }} 播放</div>
          </div>
          <span class="pix-tag">{{ openPid === p.id ? '▼' : '▸' }}</span>
        </div>
        <div v-if="openPid === p.id" class="sub-tracks">
          <div v-if="loadingTracks" class="muted" style="padding:10px;font-size:14px">loading tracks...</div>
          <div v-for="t in openTracks" :key="t.neid" class="row item sub">
            <img v-if="t.cover_url" :src="t.cover_url" class="thumb sm" referrerpolicy="no-referrer"/>
            <div v-else class="thumb sm thumb-fb"></div>
            <div style="flex:1;min-width:0">
              <div class="ttl">{{ t.title }}</div>
              <div class="meta">{{ t.artist }} · {{ fmtTime(t.duration) }}</div>
            </div>
            <button class="pix-btn ghost mini" @click="add(t)">+ ADD</button>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.tab-row { display: flex; gap: 4px; margin-left: auto; }
.tab {
  font-family: var(--font-pix);
  font-size: 8px;
  background: var(--bg-card);
  color: var(--ink);
  border: 2px solid var(--ink);
  padding: 6px 8px;
  letter-spacing: 1px;
  cursor: pointer;
}
.tab.active {
  background: var(--orange);
  box-shadow: 2px 2px 0 var(--ink);
}
.list {
  margin-top: 12px;
  max-height: 380px;
  overflow-y: auto;
}
.item {
  gap: 10px;
  padding: 8px 0;
  border-bottom: 1px dashed #C4A785;
}
.item:last-child { border-bottom: none; }
.user-row, .playlist-row { cursor: pointer; }
.user-row:hover, .playlist-row:hover { background: var(--bg-soft); }
.thumb {
  width: 40px; height: 40px;
  border: 2px solid var(--ink);
  object-fit: cover;
  flex-shrink: 0;
  background: var(--bg-soft);
}
.thumb.sm { width: 32px; height: 32px; }
.thumb.thumb-fb {
  background: linear-gradient(45deg, var(--blue) 25%, transparent 25%, transparent 50%, var(--blue) 50%, var(--blue) 75%, transparent 75%);
  background-size: 8px 8px;
  background-color: var(--bg-soft);
}
.avatar-thumb { border-radius: 50%; }
.ttl {
  font-size: 16px; line-height: 1.2;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.meta { font-size: 13px; margin-top: 2px; color: var(--ink-soft); }
.pix-btn.mini { font-size: 8px; padding: 6px 8px; }
.pinned {
  gap: 10px;
  padding: 10px;
  margin: 12px 0 0;
  background: var(--bg-soft);
  border: 2px dashed var(--ink);
}
.pinned .ttl { font-size: 17px; font-weight: bold; }
.sub-tracks {
  background: var(--bg-soft);
  border: 1px dashed var(--ink-mute);
  padding: 4px 10px;
  margin-bottom: 6px;
  max-height: 280px;
  overflow-y: auto;
}
.sub-tracks .item { padding: 6px 0; border-bottom-color: rgba(168, 107, 61, 0.4); }
.msg {
  margin-top: 10px; padding: 8px 10px; font-size: 15px;
  border: 2px dashed var(--ink); background: var(--bg-soft);
}
.msg.ok  { border-color: var(--green); background: #F0F6E8; color: #4D6635; }
.msg.err { border-color: var(--danger); background: #FCEBEB; color: var(--danger); }
</style>
