<script setup>
import { onMounted, onUnmounted } from 'vue'
import { auth } from './api.js'
import { useRadioStore } from './stores/radio.js'
import LoginCard from './components/LoginCard.vue'

const radio = useRadioStore()

onMounted(() => { if (auth.token) radio.initSocket() })
onUnmounted(() => { radio.closeSocket() })
</script>

<template>
  <LoginCard v-if="!auth.token"/>
  <router-view v-else/>
</template>
