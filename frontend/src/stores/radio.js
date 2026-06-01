import { defineStore } from 'pinia'
import { auth, api } from '../api.js'

export const useRadioStore = defineStore('radio', {
  state: () => ({
    current: null,
    queue: [],
    online: 0,
    onlineList: [],
    chats: [],
    serverOffsetMs: 0,
    ws: null,
    connected: false,
    needUnlock: false,
  }),
  getters: {
    isPlaying: (s) => !!s.current,
  },
  actions: {
    initSocket() {
      if (!auth.token || this.ws) return
      const proto = location.protocol === 'https:' ? 'wss' : 'ws'
      const ws = new WebSocket(`${proto}://${location.host}/ws?token=${auth.token}`)
      ws.onopen = () => { this.connected = true }
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
        this.serverOffsetMs = msg.data.server_time - Date.now()
        this._emit('songChange', msg.data.current)
      } else if (msg.type === 'song_change') {
        this._emit('songChange', msg.data)
      } else if (msg.type === 'queue_update') {
        this.queue = msg.data
      } else if (msg.type === 'online') {
        if (typeof msg.data === 'number') {
          this.online = msg.data
        } else {
          this.online = msg.data.count
          this.onlineList = msg.data.list || []
        }
      } else if (msg.type === 'chat') {
        this.chats.push(msg.data)
        if (this.chats.length > 100) this.chats.splice(0, this.chats.length - 100)
      }
    },
    _emit(name, data) {
      window.dispatchEvent(new CustomEvent('fm:' + name, { detail: data }))
    },
    sendChat(content) {
      if (!this.ws || !content) return
      this.ws.send(JSON.stringify({ type: 'chat', content }))
    },
    async refreshState() {
      try {
        const s = await api.state()
        this.queue = s.queue
        this.online = s.online
        this.serverOffsetMs = s.server_time - Date.now()
        this._emit('songChange', s.current)
      } catch (e) { /* ignore */ }
    }
  }
})
