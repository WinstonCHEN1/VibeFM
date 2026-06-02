/**
 * 工位注册表（v2 — 固定 slot 版）。
 *
 * 思路：
 *  - 总览页放 6 个固定 slot（3×2 网格），后续可扩展第二页同样布局
 *  - `_layout.json.slots` 是一个长度 = cols*rows 的数组，每个元素是占座者的 nickname
 *    （空字符串表示这个位子空着）
 *  - 任何人没在 slots 里但又上线了 → 自动顶到第一个空位（不会挤掉别人）
 *  - 工位长相由 `<nickname>.vue` 决定，没自定义就回落到 `_default.vue`
 *
 *  自定义工位文件名规则：必须等于 nickname（区分大小写）。
 */
import DefaultDesk from './_default.vue'
import layout from './_layout.json'

const modules = import.meta.glob('./*.vue', { eager: true })

const customDesks = {}
for (const path in modules) {
  const m = path.match(/\.\/([^/_][^/]*)\.vue$/)
  if (!m) continue
  customDesks[m[1]] = modules[path].default
}

export function deskOf(nick) {
  return customDesks[nick] || DefaultDesk
}

export const grid = layout._grid || { cols: 3, rows: 2, cellW: 196, cellH: 184, gap: 16 }

/**
 * 给定"目前应该出现在 floor 上"的昵称列表（在线 + 自己），返回 slot 数组。
 * - 已在 slots 占座的留在原位
 * - 没占座但在线的，依次塞进第一个空 slot
 * - 离线人员仍占住自己的固定 slot（visible 但灰）
 *
 * 返回：[{ nick, col, row, occupied }] 长度恒等于 cols*rows
 */
export function buildSlots(visibleNicks) {
  const total = grid.cols * grid.rows
  const slots = (layout.slots || []).slice(0, total)
  while (slots.length < total) slots.push('')

  const declared = new Set(slots.filter(Boolean))
  const extras = visibleNicks.filter(n => n && !declared.has(n))

  const out = []
  let extraIdx = 0
  for (let i = 0; i < total; i++) {
    let nick = slots[i]
    if (!nick && extraIdx < extras.length) {
      nick = extras[extraIdx++]
    }
    out.push({
      nick: nick || '',
      col: i % grid.cols,
      row: Math.floor(i / grid.cols),
      occupied: !!nick,
    })
  }
  return out
}
