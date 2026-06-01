const PALETTE = [
  { bg: '#E8945A', name: 'orange' },
  { bg: '#9FB7D4', name: 'blue' },
  { bg: '#A8C49F', name: 'olive' },
  { bg: '#D49F9F', name: 'pink' },
  { bg: '#C9B96B', name: 'mustard' },
  { bg: '#B49DD4', name: 'lilac' },
]

function hashStr(s) {
  let h = 0
  for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0
  return Math.abs(h)
}

export function pickColor(nick) {
  if (!nick) return PALETTE[0]
  return PALETTE[hashStr(nick) % PALETTE.length]
}

export function initial(nick) {
  if (!nick) return '?'
  const cleaned = nick.trim()
  if (!cleaned) return '?'
  const code = cleaned.codePointAt(0)
  if (code > 0x4e00) return cleaned[0]   // 中文取首字
  return cleaned[0].toUpperCase()
}

export function fmtTime(sec) {
  if (!sec || isNaN(sec)) return '00:00'
  const m = Math.floor(sec / 60), s = Math.floor(sec % 60)
  return `${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`
}

export function parseLRC(lrc, tlyric = '') {
  if (!lrc) return []
  const re = /\[(\d{1,2}):(\d{1,2})(?:[.:](\d{1,3}))?\]/g
  const lines = []
  const collect = (raw, into) => {
    let m, last = 0
    const stamps = []
    re.lastIndex = 0
    while ((m = re.exec(raw)) !== null) {
      const min = parseInt(m[1], 10)
      const sec = parseInt(m[2], 10)
      const ms = m[3] ? parseInt(m[3].padEnd(3, '0'), 10) : 0
      stamps.push(min * 60 + sec + ms / 1000)
      last = re.lastIndex
    }
    const text = raw.slice(last).trim()
    if (!text || stamps.length === 0) return
    for (const t of stamps) into.push({ t, text })
  }
  for (const raw of lrc.split('\n')) collect(raw, lines)

  if (tlyric) {
    const tarr = []
    for (const raw of tlyric.split('\n')) collect(raw, tarr)
    const tmap = new Map()
    for (const x of tarr) tmap.set(x.t.toFixed(2), x.text)
    for (const ln of lines) {
      const tx = tmap.get(ln.t.toFixed(2))
      if (tx) ln.tr = tx
    }
  }
  lines.sort((a, b) => a.t - b.t)
  return lines
}

export function findActiveLyric(lines, currentSec) {
  if (!lines || lines.length === 0) return -1
  let lo = 0, hi = lines.length - 1, ans = -1
  while (lo <= hi) {
    const mid = (lo + hi) >> 1
    if (lines[mid].t <= currentSec) { ans = mid; lo = mid + 1 }
    else { hi = mid - 1 }
  }
  return ans
}
