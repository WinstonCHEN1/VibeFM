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
