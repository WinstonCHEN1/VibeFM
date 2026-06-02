/**
 * 全局共享的 audio 元素 + 播放助手。
 * 全站只创建一个 audio，Floor 大厅和 FM 页都用它。
 */

let audioEl = null
let unlockerAttached = false
let needUnlockCb = null
let currentSig = ''

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

/**
 * 在 song 上同步播放当前曲目；如果是同一首歌（neid + started_at 不变）什么都不做。
 * options: { serverOffsetMs, volume, muted, onNeedUnlock(true|false) }
 */
export function playSong(song, options = {}) {
  const a = ensureAudio()
  if (!song) {
    currentSig = ''
    a.pause()
    a.removeAttribute('src')
    a.load()
    return
  }
  const sig = `${song.neid}-${song.started_at}`
  if (sig === currentSig) {
    // 同首同次，重新尝试播一次（可能用户先暂停再开）
    if (a.paused) a.play().catch(() => {})
    return
  }
  currentSig = sig
  a.src = song.url
  a.volume = options.volume ?? a.volume ?? 0.8
  a.muted  = !!options.muted
  const startedClient = song.started_at - (options.serverOffsetMs || 0)
  const offsetSec = Math.max(0, (Date.now() - startedClient) / 1000)
  try { a.currentTime = offsetSec } catch (_) {}
  a.play().then(() => {
    options.onNeedUnlock && options.onNeedUnlock(false)
  }).catch(() => {
    // 自动播放被拦：静音重试 + 等用户首次交互再开声
    a.muted = true
    a.play().catch(() => {})
    options.onNeedUnlock && options.onNeedUnlock(true)
    if (!unlockerAttached) {
      unlockerAttached = true
      needUnlockCb = options.onNeedUnlock || null
      const handler = () => {
        a.muted = !!options.muted
        a.play().catch(() => {})
        needUnlockCb && needUnlockCb(false)
        unlockerAttached = false
        window.removeEventListener('pointerdown', handler)
        window.removeEventListener('keydown', handler)
        window.removeEventListener('touchstart', handler)
      }
      window.addEventListener('pointerdown', handler, { once: true, passive: true })
      window.addEventListener('keydown', handler, { once: true, passive: true })
      window.addEventListener('touchstart', handler, { once: true, passive: true })
    }
  })
}

export function stopSong() {
  const a = ensureAudio()
  currentSig = ''
  a.pause()
  a.removeAttribute('src')
  a.load()
}

export function setAudioVolume(v) {
  const a = ensureAudio()
  a.volume = v
}
export function setAudioMuted(m) {
  const a = ensureAudio()
  a.muted = m
}
