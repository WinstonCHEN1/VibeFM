<script setup>
import { ref } from 'vue'
import { auth, api } from '../api.js'
import { useRadioStore } from '../stores/radio.js'

const inviteCode = ref('')
const nickname = ref('')
const err = ref('')
const busy = ref(false)
const radio = useRadioStore()

async function submit() {
  err.value = ''
  busy.value = true
  try {
    const r = await api.login(inviteCode.value.trim(), nickname.value.trim())
    auth.set(r.token, r.nickname)
    radio.initSocket()
  } catch (e) {
    err.value = e.message
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div style="min-height:100%;display:flex;align-items:center;justify-content:center;padding:24px;position:relative">
    <div class="dot-bg" style="position:absolute;inset:0;pointer-events:none"></div>

    <div style="position:relative;width:100%;max-width:420px">
      <div style="text-align:center;margin-bottom:18px">
        <div class="floaty" style="display:inline-block;font-family:var(--font-pix);font-size:28px;letter-spacing:4px">
          <span style="color:var(--orange-d)">V</span><span style="color:var(--ink)">I</span><span style="color:var(--green)">B</span><span style="color:var(--ink)">E</span>
          <span style="margin:0 8px;color:var(--ink)">·</span>
          <span style="color:var(--orange)">F</span><span style="color:var(--ink)">M</span>
        </div>
        <div class="muted" style="margin-top:6px;font-size:16px">cg's tiny radio for friends</div>
      </div>

      <div class="pix-card">
        <div class="pix-h" style="margin-bottom:14px">▼ ENTER THE STATION</div>

        <label class="pix-h sm muted" style="display:block;margin-bottom:6px">INVITE CODE</label>
        <input class="pix-input" v-model="inviteCode" placeholder="letmein" @keydown.enter="submit"/>

        <label class="pix-h sm muted" style="display:block;margin:14px 0 6px">NICKNAME</label>
        <input class="pix-input" v-model="nickname" maxlength="24" placeholder="how should we call you?" @keydown.enter="submit"/>

        <button class="pix-btn" style="width:100%;margin-top:18px;padding:12px"
                :disabled="busy || !inviteCode || !nickname" @click="submit">
          {{ busy ? 'CONNECTING...' : '► PRESS START' }}
        </button>

        <div v-if="err" style="margin-top:12px;padding:8px;background:#FCEBEB;border:2px dashed var(--danger);color:var(--danger);font-size:15px">
          ! {{ err }}
        </div>
      </div>

      <div class="muted" style="text-align:center;margin-top:16px;font-size:14px">
        音乐由网易云解析 · 仅限好友圈使用
      </div>
    </div>
  </div>
</template>
