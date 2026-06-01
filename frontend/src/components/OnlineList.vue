<script setup>
import { ref } from 'vue'
import { useRadioStore } from '../stores/radio.js'
import Avatar from './Avatar.vue'

const radio = useRadioStore()
const open = ref(false)
</script>

<template>
  <div style="position:relative">
    <button class="pix-btn ghost" style="font-size:9px;padding:6px 10px" @click="open = !open">
      <span class="online-dot"></span>
      ONLINE {{ radio.online }}
    </button>
    <div v-if="open && radio.onlineList.length" class="dropdown pix-card tight">
      <div class="pix-h sm" style="margin-bottom:8px">IN THE STATION</div>
      <div v-for="n in radio.onlineList" :key="n" class="row" style="gap:8px;padding:4px 0;font-size:15px">
        <Avatar :nick="n" size="sm"/>
        <span>{{ n }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.online-dot {
  display: inline-block; width: 8px; height: 8px;
  background: var(--green); border: 1px solid var(--ink);
  vertical-align: middle; margin-right: 6px;
}
.dropdown {
  position: absolute; right: 0; top: 100%; margin-top: 8px;
  min-width: 180px; max-height: 280px; overflow-y: auto;
  z-index: 10;
}
</style>
