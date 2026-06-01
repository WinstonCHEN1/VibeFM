<script setup>
import { onMounted, onUnmounted } from 'vue'
import { auth } from './api.js'
import { useRadioStore } from './stores/radio.js'
import LoginCard from './components/LoginCard.vue'
import NowPlaying from './components/NowPlaying.vue'
import LyricView from './components/LyricView.vue'
import Queue from './components/Queue.vue'
import BrowsePanel from './components/BrowsePanel.vue'
import ChatPanel from './components/ChatPanel.vue'
import OnlineList from './components/OnlineList.vue'
import AudiencePanel from './components/AudiencePanel.vue'
import CatMascot from './components/CatMascot.vue'
import Avatar from './components/Avatar.vue'

const radio = useRadioStore()

function logout() {
  radio.closeSocket()
  auth.clear()
}

onMounted(() => { if (auth.token) radio.initSocket() })
onUnmounted(() => { radio.closeSocket() })
</script>

<template>
  <LoginCard v-if="!auth.token"/>

  <div v-else class="page">
    <div class="dot-bg page-bg"></div>

    <div class="container">
      <header class="topbar">
        <div class="row" style="gap:10px">
          <div class="logo floaty">
            <span style="color:var(--orange-d)">V</span><span>I</span><span style="color:var(--green)">B</span><span>E</span>
            <span style="margin:0 4px">·</span>
            <span style="color:var(--orange)">F</span><span>M</span>
          </div>
          <span class="by-cg muted">by cg</span>
        </div>
        <div class="row" style="gap:10px">
          <OnlineList/>
          <div class="row" style="gap:6px">
            <Avatar :nick="auth.nickname" size="sm"/>
            <span style="font-size:15px">{{ auth.nickname }}</span>
          </div>
          <button class="pix-btn ghost" style="font-size:8px;padding:6px 8px" @click="logout">EXIT</button>
        </div>
      </header>

      <section class="main-grid">
        <div class="col-left">
          <NowPlaying/>
          <LyricView/>
          <BrowsePanel/>
        </div>
        <div class="col-right">
          <Queue/>
          <AudiencePanel/>
          <ChatPanel/>
        </div>
      </section>

      <footer class="footer muted">
        ╱╱ powered by friendship ╱ never goes off air ╱╱
      </footer>
    </div>

    <CatMascot/>
  </div>
</template>

<style scoped>
.page { min-height: 100%; position: relative; }
.page-bg { position: fixed; inset: 0; pointer-events: none; z-index: 0; }
.container {
  position: relative; z-index: 1;
  max-width: 1180px; margin: 0 auto;
  padding: 24px 18px 40px;
}
.topbar {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 18px;
  flex-wrap: wrap; gap: 10px;
}
.logo {
  font-family: var(--font-pix);
  font-size: 18px;
  letter-spacing: 3px;
}
.by-cg {
  font-family: var(--font-pix);
  font-size: 9px;
  letter-spacing: 2px;
  margin-left: 4px;
  margin-top: 6px;
}
.main-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.7fr) minmax(0, 1fr);
  gap: 18px;
}
.col-left, .col-right {
  display: flex; flex-direction: column; gap: 18px;
  min-width: 0;
}
.footer {
  text-align: center;
  margin-top: 30px;
  font-size: 14px;
  letter-spacing: 1px;
}

@media (max-width: 860px) {
  .main-grid { grid-template-columns: 1fr; }
  .container { padding: 16px 12px 32px; }
  .logo { font-size: 16px; }
}
</style>
