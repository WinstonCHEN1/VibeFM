<script setup>
import { computed } from 'vue'
import { pickColor, initial } from '../utils.js'

const props = defineProps({
  nick: String,
  size: { type: String, default: '' }
})
const c = computed(() => pickColor(props.nick))
const text = computed(() => initial(props.nick))
</script>

<template>
  <span class="pix-avatar" :class="size" :style="{ background: c.bg }">{{ text }}</span>
</template>
