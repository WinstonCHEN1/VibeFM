<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ensureAnalyser } from '../audio.js'

const props = defineProps({
  bars: { type: Number, default: 24 },
  height: { type: Number, default: 36 }
})

const canvasRef = ref(null)
let raf = 0
let analyser = null

function paint() {
  raf = requestAnimationFrame(paint)
  const canvas = canvasRef.value
  if (!canvas) return
  if (!analyser) {
    analyser = ensureAnalyser()
    if (!analyser) return
  }
  const w = canvas.width
  const h = canvas.height
  const ctx = canvas.getContext('2d')
  ctx.clearRect(0, 0, w, h)

  const buf = new Uint8Array(analyser.frequencyBinCount)
  analyser.getByteFrequencyData(buf)

  const N = props.bars
  const gap = 2
  const barW = Math.floor((w - (N + 1) * gap) / N)
  const blockH = 4
  const blocks = Math.floor(h / blockH)

  // 取对数采样：低频粗、高频细
  for (let i = 0; i < N; i++) {
    const lo = Math.floor(Math.pow(i / N, 1.4) * buf.length)
    const hi = Math.floor(Math.pow((i + 1) / N, 1.4) * buf.length)
    let sum = 0, cnt = 0
    for (let k = Math.max(0, lo); k < Math.min(buf.length, Math.max(hi, lo + 1)); k++) {
      sum += buf[k]; cnt++
    }
    const v = cnt ? sum / cnt / 255 : 0
    const litBlocks = Math.max(0, Math.round(v * blocks))
    const x = gap + i * (barW + gap)
    for (let b = 0; b < blocks; b++) {
      const y = h - (b + 1) * blockH + 1
      const lit = b < litBlocks
      // 颜色分段：底部橙、中部深橙、顶部 1~2 块红
      let color
      if (!lit) color = '#EFE2CD'
      else if (b >= blocks - 2) color = '#C45A4A'
      else if (b >= blocks - 5) color = '#D4733E'
      else color = '#E8945A'
      ctx.fillStyle = color
      ctx.fillRect(x, y, barW, blockH - 1)
    }
  }
}

function resize() {
  const canvas = canvasRef.value
  if (!canvas) return
  const dpr = Math.min(2, window.devicePixelRatio || 1)
  const cssW = canvas.clientWidth
  const cssH = props.height
  canvas.width = cssW * dpr
  canvas.height = cssH * dpr
  canvas.style.height = cssH + 'px'
  const ctx = canvas.getContext('2d')
  ctx.imageSmoothingEnabled = false
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
}

onMounted(() => {
  resize()
  window.addEventListener('resize', resize)
  raf = requestAnimationFrame(paint)
})
onUnmounted(() => {
  window.removeEventListener('resize', resize)
  cancelAnimationFrame(raf)
})
</script>

<template>
  <canvas ref="canvasRef" class="wave-canvas" :style="{ height: height + 'px' }"/>
</template>

<style scoped>
.wave-canvas {
  display: block;
  width: 100%;
  background: var(--bg-card);
  border: 2px solid var(--ink);
  image-rendering: pixelated;
}
</style>
