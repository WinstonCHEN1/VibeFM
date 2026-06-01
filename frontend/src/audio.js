/**
 * 全局共享的 audio 元素。
 * 全站只创建一个，挂在 document.body。
 */

let audioEl = null

export function ensureAudio() {
  if (audioEl) return audioEl
  audioEl = document.createElement('audio')
  audioEl.crossOrigin = 'anonymous'
  audioEl.preload = 'auto'
  audioEl.style.display = 'none'
  document.body.appendChild(audioEl)
  return audioEl
}

// 兼容旧调用，已经不再使用 analyser
export function ensureAnalyser() { return null }
export function resumeCtx() {}
