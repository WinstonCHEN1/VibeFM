# Vibe Lounge · Desks

每一页 Floor 上有 **6 个固定工位**（3×2 网格）。
默认是 `_default.vue`（标准小屋），但你可以提 PR 给自己（或者你朋友）画一个独一无二的工位。

## 怎么提 PR

1. **复制模板**

   ```bash
   cp frontend/src/desks/_template.vue frontend/src/desks/<你的昵称>.vue
   ```

   - 文件名必须**完全等于**你登录时填的 nickname（区分大小写）。
   - 中文 / emoji 的 nickname 也支持，文件名直接用就行。

2. **改造你的工位**

   随便折腾内部的 div / SVG / CSS。模板里已经把状态钩子写好（`atDesk` / `inBar` / `offline` / `sleeping` / `coffee` / `headphone`），你可以根据它们切换样式或动效。

3. **占座**

   编辑 `frontend/src/desks/_layout.json`，把 `slots` 数组里**对应位置**改成你的昵称：

   ```json
   "slots": [
     "cg",     // 左上
     "alice",
     "bob",
     "",       // 左下，空位
     "yuki",
     ""
   ]
   ```

   `slots` 是按行优先排列的固定槽位（顺序就是它在网格里的位置）。

4. **提 PR**

   PR 里贴一张截图，让大家围观一下你的小窝。

## 工位规则

- **尺寸**：必须 `width: 100%; height: 100%;` 撑满父容器（默认 196×184）。不要写死 px。
- **必须接受 props**（直接复制模板就行）：
  - `nick` 工位主人的昵称
  - `text` 自填状态文本
  - `online` 是否在线
  - `location` `'floor' | 'bar' | ''`
  - `isMe` 是否是当前查看者自己
  - `poke` `{ emoji }` 别人戳你时的临时气泡

- **状态动效约定**（不强制，但默认工位提供这些识别规则给你参考）：
  | 自填关键词 | 触发 |
  |------------|-----|
  | `z` `zZ` `睡` `sleep` `afk` `🛌` `💤` | 屏幕息屏 + 头顶冒 Z |
  | `☕` `咖啡` `coffee` `续命` | 桌上多一杯咖啡 |
  | `🎧` `听歌` `listen` `music` | 戴上耳机 |

  你想加自己的关键词随便加。

- **风格**：保持现有像素风 + 米色调。可用的 CSS 变量：
  `--bg / --bg-card / --bg-soft / --ink / --ink-soft / --orange / --green / --blue / --pink / --olive / --font-pix / --font-body`。

- **只能动自己那一格**：不要改别人的 `.vue`、不要动 `_default.vue` / `_registry.js` / `_template.vue`。
- **静态 only**：不准在 `<script setup>` 里 fetch、setInterval、写全局副作用。CSS 动画随便用。
- **没外链**：不要 `import` 任何包，不要引用外部图片 / 字体 / iframe。

## 第二页？

后面会扩展 `slots` 长度到 12（即 6+6），分页切换。提 PR 时如果第一页满了，加一页就行。

## 文件清单

```
desks/
├── README.md         ← 你正在看
├── _registry.js      ← 自动收集所有工位（不要改）
├── _layout.json      ← 工位坐标（slots 数组）
├── _default.vue      ← 默认工位
├── _template.vue     ← 复制这个开始你的工位
├── cg.vue            ← 一个示例（双显示器+黑胶+橘猫）
└── <你的昵称>.vue
```

PR 不严格，只玩自己那格 :)
