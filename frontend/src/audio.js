/**
 * 全局共享的 audio + AnalyserNode。
 *
 * - 全站只创建一个 <audio> 元素和 AudioContext，挂到 window 上
 * - NowPlaying 调 ensure() 拿到 element 来设置 src / 控制播放
 * - WaveBars 调 ensure() 拿到 analyser 来读频谱
 * - AudioContext 在用户首次交互后创建（绕过浏览器限制）
 */

let audioEl = null
let ctx = null
let analyser = null
let srcNode = null
let connected = false

function getAudioEl() {
  if (audioEl) return audioEl
  audioEl = document.createElement('audio')
  audioEl.crossOrigin = 'anonymous'
  audioEl.preload = 'auto'
  audioEl.style.display = 'none'
  document.body.appendChild(audioEl)
  return audioEl
}

export function ensureAudio() {
  return getAudioEl()
}

export function ensureAnalyser() {
  if (analyser && connected) return analyser
  const el = getAudioEl()
  try {
    if (!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)()
    if (ctx.state === 'suspended') ctx.resume().catch(() => {})
    if (!analyser) {
      analyser = ctx.createAnalyser()
      analyser.fftSize = 128
      analyser.smoothingTimeConstant = 0.75
    }
    if (!srcNode) {
      srcNode = ctx.createMediaElementSource(el)
      srcNode.connect(analyser)
      analyser.connect(ctx.destination)
      connected = true
    }
  } catch (e) {
    console.warn('audio analyser init failed:', e)
    return null
  }
  return analyser
}

export function resumeCtx() {
  if (ctx && ctx.state === 'suspended') ctx.resume().catch(() => {})
}
