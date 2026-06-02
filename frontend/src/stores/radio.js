import { defineStore } from 'pinia'
import { auth, api } from '../api.js'

const STATUS_KEY = 'fm_status_text'

export const useRadioStore = defineStore('radio', {
  state: () => ({
    current: null,
    queue: [],
    online: 0,
    onlineList: [],
    presence: {},               // { nick: { location, text, last_seen } }
    statusText: localStorage.getItem(STATUS_KEY) || '',
    location: 'floor',          // 当前自己在哪个路由
    chats: [],
    serverOffsetMs: 0,
    frozen: false,
    ws: null,
    connected: false,
    needUnlock: false,
    pokes: [],                  // 收到的戳一下：{ id, from, emoji, t }
    walls: {},                  // 工位留言：{ [target]: [{nick, content, ts}, ...] }
  }),
  getters: {
    isPlaying: (s) => !!s.current,
    onFloorList: (s) => Object.entries(s.presence)
      .filter(([, p]) => p.location === 'floor')
      .map(([nick]) => nick),
    inBarList: (s) => Object.entries(s.presence)
      .filter(([, p]) => p.location === 'bar')
      .map(([nick]) => nick),
  },
  actions: {
    initSocket() {
      if (!auth.token || this.ws) return
      const proto = location.protocol === 'https:' ? 'wss' : 'ws'
      const ws = new WebSocket(`${proto}://${location.host}/ws?token=${auth.token}`)
      ws.onopen = () => {
        this.connected = true
        // 连接成功后立刻同步一次本地状态
        this._sendPresence()
      }
      ws.onmessage = (ev) => this._handle(JSON.parse(ev.data))
      ws.onclose = () => {
        this.connected = false
        this.ws = null
        if (auth.token) setTimeout(() => this.initSocket(), 2000)
      }
      this.ws = ws
    },
    closeSocket() {
      if (this.ws) { this.ws.close(); this.ws = null }
    },
    _handle(msg) {
      if (msg.type === 'state') {
        this.online = msg.data.online
        this.queue = msg.data.queue
        this.onlineList = msg.data.online_list || []
        this.presence = msg.data.presence || {}
        this.serverOffsetMs = msg.data.server_time - Date.now()
        this.frozen = !!msg.data.frozen
        const history = (msg.data.chat_history || []).map(c => ({ ...c, history: true }))
        this.chats = history
        this._emit('songChange', msg.data.current)
      } else if (msg.type === 'song_change') {
        this.frozen = false
        this._emit('songChange', msg.data)
      } else if (msg.type === 'queue_update') {
        this.queue = msg.data
      } else if (msg.type === 'online') {
        if (typeof msg.data === 'number') {
          this.online = msg.data
        } else {
          this.online = msg.data.count
          this.onlineList = msg.data.list || []
          if (msg.data.presence) this.presence = msg.data.presence
        }
      } else if (msg.type === 'presence') {
        const { nick, ...rest } = msg.data
        if (nick) this.presence = { ...this.presence, [nick]: rest }
      } else if (msg.type === 'chat') {
        this.chats.push({ ...msg.data, history: false })
        if (this.chats.length > 200) this.chats.splice(0, this.chats.length - 200)
      } else if (msg.type === 'poke') {
        const id = Math.random().toString(36).slice(2)
        const item = { id, from: msg.data.from, emoji: msg.data.emoji || '👋', t: Date.now() }
        this.pokes.push(item)
        // 5 秒后自动消失
        setTimeout(() => {
          this.pokes = this.pokes.filter(p => p.id !== id)
        }, 5000)
      } else if (msg.type === 'wall_post') {
        const m = msg.data
        if (!m || !m.target) return
        const list = this.walls[m.target] ? [...this.walls[m.target]] : []
        list.push(m)
        if (list.length > 20) list.splice(0, list.length - 20)
        this.walls = { ...this.walls, [m.target]: list }
      }
    },
    _emit(name, data) {
      window.dispatchEvent(new CustomEvent('fm:' + name, { detail: data }))
    },
    _sendPresence() {
      if (!this.ws || this.ws.readyState !== 1) return
      this.ws.send(JSON.stringify({
        type: 'presence',
        location: this.location,
        text: this.statusText,
      }))
    },
    setLocation(loc) {
      if (loc !== 'floor' && loc !== 'bar') return
      this.location = loc
      this._sendPresence()
    },
    setStatusText(text) {
      const t = (text || '').slice(0, 20)
      this.statusText = t
      localStorage.setItem(STATUS_KEY, t)
      this._sendPresence()
    },
    poke(target, emoji = '👋') {
      if (!this.ws || !target || target === auth.nickname) return
      this.ws.send(JSON.stringify({ type: 'poke', to: target, emoji }))
    },
    sendChat(content) {
      if (!this.ws || !content) return
      this.ws.send(JSON.stringify({ type: 'chat', content }))
    },
    wallPost(target, content) {
      if (!this.ws || !target || !content) return
      this.ws.send(JSON.stringify({ type: 'wall_post', to: target, content }))
    },
    async loadWall(target) {
      if (!target) return
      try {
        const res = await fetch(`/api/wall/${encodeURIComponent(target)}`)
        const data = await res.json()
        this.walls = { ...this.walls, [target]: data.items || [] }
      } catch (e) { /* ignore */ }
    },
    async refreshState() {
      try {
        const s = await api.state()
        this.queue = s.queue
        this.online = s.online
        if (s.presence) this.presence = s.presence
        this.serverOffsetMs = s.server_time - Date.now()
        this._emit('songChange', s.current)
      } catch (e) { /* ignore */ }
    }
  }
})
