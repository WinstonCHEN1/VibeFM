import { reactive } from 'vue'

const TOKEN_KEY = 'fm_token'
const NICK_KEY  = 'fm_nick'

export const auth = reactive({
  token: localStorage.getItem(TOKEN_KEY) || '',
  nickname: localStorage.getItem(NICK_KEY) || '',
  set(token, nickname) {
    this.token = token
    this.nickname = nickname
    localStorage.setItem(TOKEN_KEY, token)
    localStorage.setItem(NICK_KEY, nickname)
  },
  clear() {
    this.token = ''
    this.nickname = ''
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(NICK_KEY)
  }
})

async function request(path, opts = {}) {
  const headers = { 'Content-Type': 'application/json', ...(opts.headers || {}) }
  if (auth.token) headers['Authorization'] = `Bearer ${auth.token}`
  const res = await fetch(path, { ...opts, headers })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || `HTTP ${res.status}`)
  }
  return res.json()
}

export const api = {
  login: (invite_code, nickname) =>
    request('/api/auth/login', { method: 'POST', body: JSON.stringify({ invite_code, nickname }) }),
  state: () => request('/api/state'),
  search: (q) => request(`/api/search?q=${encodeURIComponent(q)}`),
  enqueue: (neid) => request('/api/queue', { method: 'POST', body: JSON.stringify({ neid }) }),
  skip: () => request('/api/skip', { method: 'POST' }),
  lyric: (neid) => request(`/api/lyric/${neid}`),
  searchUsers: (q) => request(`/api/playlist/search-users?q=${encodeURIComponent(q)}`),
  searchPlaylists: (q) => request(`/api/playlist/search?q=${encodeURIComponent(q)}`),
  userPlaylists: (uid) => request(`/api/playlist/by-user/${uid}`),
  playlistTracks: (pid) => request(`/api/playlist/${pid}/tracks`),
}
