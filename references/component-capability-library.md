# 组件能力库（Component Capability Library）

> 抓取核实：2026-10-26。四个站点均可访问，组件清单来自实际页面，非推测。
> 定位：**语义 → 原语**的映射层。`component-library.md` 管"怎么接进工程"，本文件管"这个需求该用哪种交互原语"。

---

## 抓取状态

| 来源 | 状态 | 实测规模 | 关键事实 |
|---|---|---|---|
| **shadcn/ui** | ✅ 已知 + 本次沿用 | 50+ 基础组件 | 源码复制进仓库，Radix 行为 + Tailwind 样式 |
| **Beautiful UI** | ✅ 抓取成功 | **21 个 AI 原语**（编号 01-21） | 面向前端"AI 原生界面"，每个原语带状态机（如 Thinking 有 Steps/Reasoning/Search/Coding 四态） |
| **beUI** | ✅ 抓取成功 | **71 个组件**（含 React Native 版） | Motion + Tailwind，**通过 shadcn registry 分发**（`bunx shadcn add @beui/timeline`） |
| **Rare UI** | ✅ 抓取成功 | **27 个**单文件组件 | 同样走 shadcn CLI（`npx shadcn@latest add swamimalode07/rare-ui/fluid-orb`）+ MCP |
| **Transitions.dev** | ✅ 抓取成功 | **43+ 过渡**，分 Essential / AI Agents / Effects / Texts / Pro | 提供 library + studio + builder，可导出实现 |

> 抓取成功也不代表可以照抄：**视觉一律重绘，只取交互语义与运动语言**。

---

# A. 组件能力矩阵

| 来源 | 能力域 | 触发场景 | 提取内容（只取这些） |
|---|---|---|---|
| **shadcn/ui** | 基座：可访问的行为原语 + 可组合样式 | 任何需要按钮/弹窗/表格/表单/图表/侧栏/Toast 的地方 | 组件 API（variant/size）、Radix 的焦点与键盘行为、`data-state` 约定、CSS 变量主题接口 |
| **Beautiful UI** | AI 交互原语（21 个） | AI 输出、推理过程、执行前确认、工具调用、长任务、批量编辑、知识引用 | **状态机与时序**：如 Thinking 的展开/折叠、Streaming 的逐字与来源挂载、Approval 的 1/3 步进、Task Rows 的 running/failed/completed |
| **beUI** | 精致交互层（71 个，Motion 驱动） | 需要"有质感的动效组件"：Dock、命令面板、Morphing Modal、Bottom Sheet、Tabs、Tilt Card、数字滚动 | **运动语言**：spring 参数、shared layout 过渡、morph 高度、惯性拖拽、键盘可玩性 |
| **Rare UI** | 去模板化视觉（27 个） | 页面需要一个"记忆点"，但不想靠装饰堆料 | **一个非常规维度**：非常规几何（Fluid Orb）、物理感（Gravity Letters）、非标准控件（Duration Picker）、Folder 式层叠 |
| **Transitions.dev** | 过渡与微交互（43+） | 页面/视图切换、状态切换、数字变化、通知、菜单展开 | **过渡类型学**：shared axis、origin-aware、card resize、number pop-in、text swap；以及时长/缓动规格 |

## 检索顺序（不可颠倒）

```
① shadcn/ui 拿基座      —— 先解决"能不能用、能不能键盘操作"
② BeUI / Rare UI 定风格 —— 再决定"它长什么样、动起来什么手感"
③ Transitions 加质感    —— 补"状态之间怎么过去"
④ Beautiful UI 补 AI 原语 —— 只在涉及 AI 输出/推理/确认时启用
```

**为什么是这个顺序**：基座决定可访问性与工程成本（最贵、最难改）；风格是皮肤（中等）；过渡是连接件（便宜）；AI 原语是场景特化（只有 AI 场景才需要）。
**反例**：先挑一个 Fluid Orb，再想"这页是干什么的"——这就是从 L5 反推 L2，必然跑偏。

---

# B. 五个来源的可执行能力（能力域 + 触发场景 + 落地规则）

## B1. shadcn/ui —— 基座

**能力域**：Button / Dialog / Sheet / Table / Form / Select / Tabs / Toast / Chart / Sidebar / Command 等 50+。
**触发场景**：任何"必须有键盘操作、焦点管理、ARIA"的地方；表单校验；表格排序筛选；命令面板。

**落地规则**
1. `npx shadcn@latest init` + `add <component>`，源码落进 `components/ui/`，**从此归你维护**
2. 只消费语义令牌：`--background/--foreground/--primary/--ring` 映射到本技能 12 令牌（见 `templates/shadcn-theme.css`）
3. **四件必改**：圆角分级 / 半透明边框 / 两级阴影 / 5 档字阶（否则就是"默认 shadcn 脸"）
4. 行为**不要重造**：焦点捕获、Esc、方向键、滚动锁由 Radix 负责；改样式别删 `data-state`
5. 只用 `variant` / `size` 扩展，不在页面里 `!important`
6. 升级用 diff，不删了重装

## B2. Beautiful UI —— AI 原生原语（21 个）

**能力域**（实测清单）：
```
01 Loading State（像素网格 + 计时）  02 Thinking（可展开 trace：Steps/Reasoning/Search/Coding）
03 Streaming Text（流式 + 内联来源 + 后续追问）  04 Approval Card（1/3 步进、Skip/Continue）
05 Tool Chips（工具调用压缩为 chip）  06 Task Rows（running/failed/completed + 进度）
07 Chat（分栏对话 + 推理回复 + 输入区）  08 Prompt Bar（@来源 / 命令 / 模型选择 / 语音）
09 Recommendation Card（置信度 + 备选 + Accept）  10 Context Cards（检索片段 + 来源文件）
11 Diff Table（逐行 toggle 的变更表）  12 Records Table（CRM 式：标签/排序/关系强度）
13 Filter Table（状态 chip 重排活数据）  14 Sidebar Nav（折叠 + 滑动高亮）
15 Search（实时过滤 + 空状态）  16 Flowchart（点阵画布 + 条件分支）
17 Insight Cards（分页洞察 + 可 scrub 图表）  18 Code Block（行号 + 统一 diff）
19 Fine-tune Card（设计属性检查器）  20 Selection Actions（划词交给 Agent 改写）
21 Agent Screen（观看/教学/录制 Agent 屏幕）
```

**触发场景**：任何"AI 在替用户做事"的界面——生成中、思考中、流式输出、将要执行、已执行、需要人确认。

**落地规则（关键：抽象语义，不搬视觉）**
1. **先抽状态机**：每个原语先写清 `idle → running → success/failed` 的状态与转移，再画
2. 用**自己的令牌**重绘：主色、圆角、字体、间距全部来自项目（不要把它的像素网格与配色搬过来）
3. **保留交互语义**：Thinking 必须可展开/折叠；Streaming 必须能中断；Approval 必须能 Skip；Diff 必须能逐行切换
4. **保留可访问性**：`aria-live` 播报流式文本、进度用 `role="progressbar"`、trace 用 `aria-expanded`
5. **性能**：流式文本用增量 DOM（不要整段重渲染）；trace 折叠时不挂载子节点
6. **不照抄的视觉**：像素方块 loader、彩色 timeline 圆点、玻璃卡片——这些是它的品牌，不是你的

## B3. beUI —— 精致交互层（71 个）

**能力域**：Button（spring/stateful/magnetic/metallic）、Morphing Modal、Animated Toast Stack、Action Swap、Dock、Tabs（pill/segment/underline + layoutId 指示器）、Dynamic Island、Command Palette、Expandable Action Bar/Tabs、Tilt Card、Bottom Sheet、Switch、Tooltip、Text Animation、Number Animation、Bouncy Accordion、Range Slider、Theme Toggle（View Transition 揭示）、Drawer、Swipeable List、Bloom Menu、Card Dealer、Sankey Chart、Timeline…（React Native 版 71 个）

**触发场景**：需要"手感"的地方——导航高亮滑动、弹层形变、数字滚动、拖拽抽屉、Tab 切换、命令面板。

**落地规则**
1. 分发方式是 **shadcn registry**：`bunx shadcn add @beui/<name>`，同样落进你的仓库 → 同样要审
2. **只取运动语言**：spring 的 stiffness/damping、`layoutId` 共享过渡、morph 高度、拖拽惯性、按压缩放
3. 与 `motion-decision-table` 对齐：它的默认时长往往偏"展示型"，按功能五类重新定档（100/150/200/≤300）
4. **玻璃 / 大圆角 / 磁吸** 属于它的风格，不是通用规范：产品界面慎用，品牌页一页最多 1 处
5. 必须保留它的降级：`reduced-motion` 下取消形变与惯性，只留状态变化
6. RN 版（Reanimated）只在真原生/RN 项目用；Taro/小程序 WebView 用 CSS 近似

## B4. Rare UI —— 去模板化视觉（27 个）

**能力域**：Folder（层叠文件夹）、Duration Picker、Fluid Orb（流体球）、Gravity Letters（重力字）、OTP Input，以及另外 22 个单文件组件；支持 shadcn CLI 与 **MCP** 安装。

**触发场景**：页面已经很规整，需要一个"记忆点"；或产品本身就是创意/工具型，需要摆脱卡片感。

**落地规则**
1. **一页只用 1 个**（与"记忆点唯一"同源）；用两个就变成马戏团
2. **必须服务信息**：Fluid Orb 做"系统负载/生成进度"可以；做纯装饰不行
3. 抽象的是"非常规维度"，不是它的霓虹/发光/3D 外观：可以是几何（球/层叠）、物理（重力/流体）、非标准控件（时长选择器）
4. 性能红线：流体/重力类用 `transform` + `requestAnimationFrame` 或 CSS，禁止每帧改布局
5. 必须有 reduced-motion 终态（冻结为静态图形）
6. **降级策略（若站点不可用）**：至少在一个维度做非常规处理——破除"默认卡片 + 阴影 + 圆角"三件套
   （例：改用细线分区、整幅图片承载内容、非对称栅格、或一个物理感动效）

## B5. Transitions.dev —— 过渡与微交互（43+）

**能力域**：分类为 Essential / AI Agents / Effects / Texts / Pro；实测条目含 Card resize（卡片形变）、Number pop-in（数字模糊翻转）、Notification badge（对角弹入）、Text states swap（文本模糊切换）、Menu dropdown（origin-aware 展开）等 43+。

**触发场景**：视图/页面切换、状态切换、数字更新、通知出现、菜单展开、文本替换。

**落地规则**
1. **抽象成"过渡类型 + 时长 + 缓动"**，用 CSS / View Transitions / Motion 自己实现，**不引它的运行时**
2. 类型对应：
   - **shared axis**（同轴位移）→ 层级切换（列表→详情、上一步→下一步）
   - **origin-aware**（从触发点展开）→ 菜单、气泡、下拉
   - **card resize / morph** → 卡片展开为详情
   - **number pop-in / text swap** → 数值更新、状态文案替换
3. 时长：微交互 120-200ms ease-out；页面级 200-300ms shared axis；数字/文本 180-260ms
4. **骨架屏无缝衔接**：加载完成时骨架与真实内容的位置、尺寸必须一致，用 crossfade 150ms 而不是"骨架消失→内容出现"
5. 禁止：过渡期间改变布局（CLS）、超过 400ms 的页面过渡、`linear`
6. **降级策略（若站点不可用）**：用上述通用规则即可——shared axis 页面过渡、120-200ms ease-out 微交互、骨架屏无缝、reduced-motion 全降

---

# C. 语义 → 组件映射表

> 用法：先按"用户要什么"找到语义，再按"首选原语 → 来源"取用；第三列是**降级路径**（原语不可用/不合适时）。

| 需求语义 | 首选原语 | 来源 | 降级路径 |
|---|---|---|---|
| AI 加载中 | Loading State（带耗时） | Beautiful UI | 三点脉冲 + 文案"正在处理" |
| AI 推理过程 | Thinking（可展开 trace） | Beautiful UI | 折叠的"查看步骤"列表 |
| 流式回答 | Streaming Text（内联来源 + 追问） | Beautiful UI | 逐段追加 + 光标 |
| 执行前确认 | Approval Card（选项 + Skip） | Beautiful UI | 二次确认弹窗（shadcn Dialog） |
| 工具调用 | Tool Chips | Beautiful UI | 一行等宽文本 + 状态点 |
| 长任务进度 | Task Rows（running/failed/completed） | Beautiful UI | 进度条 + 列表（shadcn） |
| AI 对话 | Chat（推理回复 + 输入区） | Beautiful UI | 普通消息流 + 输入框 |
| 输入指令 | Prompt Bar（@来源 / 命令 / 模型） | Beautiful UI | 普通输入框 + 快捷标签 |
| 建议下一步 | Recommendation Card（置信度 + 备选） | Beautiful UI | 一条 inline 建议 + 两个按钮 |
| 知识来源 | Context Cards（片段 + 文件名） | Beautiful UI | 脚注编号 + 链接 |
| 批量编辑 | Diff Table（逐行 toggle） | Beautiful UI | 变更列表 + 复选框 |
| CRM 列表 | Records Table（标签/关系强度） | Beautiful UI | 表格 + 徽章（shadcn Table） |
| 状态筛选 | Filter Table（状态 chip） | Beautiful UI | Tabs / Select 过滤 |
| 搜索 | Search（实时 + 空态） | Beautiful UI | 输入框 + 结果列表 |
| 流程/编排 | Flowchart（点阵画布） | Beautiful UI | 步骤条 / 有序列表 |
| 数据洞察 | Insight Cards（可 scrub 图表） | Beautiful UI | KPI 卡 + 折线（shadcn Chart） |
| 代码/补丁 | Code Block（行号 + diff） | Beautiful UI | `<pre>` + 等宽字体 |
| 参数微调 | Fine-tune Card（属性检查器） | Beautiful UI | 表单控件组 |
| 划词操作 | Selection Actions | Beautiful UI | 悬浮工具条 |
| 观察 Agent 操作 | Agent Screen | Beautiful UI | 日志流 + 截图 |
| 表单 / 弹窗 / 表格 / 按钮基座 | Button / Dialog / Table / Form / Toast | **shadcn/ui** | 原生元素 + 自写 ARIA |
| 命令面板（⌘K） | Command Palette | beUI（+ shadcn Command） | Dialog + 输入 + 列表 |
| Tab 切换（滑动指示器） | Tabs（layoutId） | beUI | 下划线 Tab + CSS 过渡 |
| 移动端底部操作 | Bottom Sheet（snap 点） | beUI | 固定底部抽屉 |
| 数值变化 | Number Animation / Number pop-in | beUI / Transitions | 直接替换数字 |
| 导航 / 页面切换 | shared axis | **Transitions** | 交叉淡入 150-200ms |
| 菜单/气泡展开 | origin-aware dropdown | **Transitions** | 淡入 + 缩放 0.98 |
| 卡片展开为详情 | card resize / morph | **Transitions** | 同页展开（grid-rows） |
| 通知出现 | Notification badge / Toast Stack | beUI / Transitions | 右上角 Toast |
| 去模板化视觉 | Fluid Orb / Gravity Letters / Folder | **Rare UI** | 一个非常规维度（几何/物理/非标准控件） |
| 空状态 | Empty State（插图 + 一个动作） | shadcn（组合） | 文案 + 主按钮 |
| 错误恢复 | Alert + 重试按钮 | shadcn | 行内错误文案 |

---

# D. 检索流程与质量闸门

## D1. 七步检索流程

```
① 解析需求      用户要完成什么？谁是用户？在哪一步卡住？
② 识别 UI 语义  判定属于哪类：基座控件 / 数据展示 / AI 过程 / 状态过渡 / 记忆点
③ 查能力矩阵    按语义找到候选原语（可能 2-3 个）
④ 取 shadcn 基座 先确保可访问与工程可行（Button/Dialog/Table/Form…）
⑤ 定风格        BeUI 的运动语言 / Rare UI 的一个非常规维度
⑥ 加质感        Transitions 的过渡类型 + 时长；必要时补 Beautiful UI 原语
⑦ 输出          代码 + 「原语说明」+ 降级方案
```

**输出模板（每次必附）**
```markdown
原语：Thinking（可展开 trace） · 来源：Beautiful UI 02
抽象了什么：三段状态机（收集 → 推理 → 工具调用）+ 折叠/展开语义
用本项目重绘：令牌 --color-surface / --radius-card；时长 220ms ease-out
保留交互：aria-expanded、Esc 折叠、折叠时不挂载子树
降级：无 JS 时显示静态步骤列表
```

## D2. 质量闸门（五条，逐条过）

```
[ ] 1 AI 交互是否用了对的原语？（生成中≠加载中；推理≠流式；确认≠弹窗）
[ ] 2 基座是否可访问？（键盘可达、ARIA 正确、focus 可见、Esc 可退）
[ ] 3 动效是否有明确时长与缓动，且 reduced-motion 有终态？
[ ] 4 是否避免了模板味？（无默认卡片+阴影+圆角三件套、无照抄的原站配色）
[ ] 5 是否标注了原语来源与降级方案？
```

**任一条为"否" → 不交付。** 第 1 条是最常见的错误：把"AI 在推理"做成一个 spinner，
用户不知道它在干什么，只知道它在转。

## D3. 与现有架构的接法

| 层 | 谁负责 |
|---|---|
| L4 系统 · 工程接入 | `component-library.md`（shadcn 四件必改、variant 纪律、升级策略） |
| L4/L5 之间 · 语义选型 | **本文件**（哪个需求用哪种原语） |
| L5 表现 · 时长与降级 | `motion-decision-table.md`（五类）+ `motion-spec.md`（参数） |
| L6 交付 · 验收 | `audit_all.py` + 六段设计依据 + 本文件的五条闸门 |

**冲突裁决**：工程问题看 component-library；语义问题看本文件；时长看 motion-decision-table。
三者不一致时，以"可访问性 > 语义正确 > 视觉还原"为序。

## D4. 不做什么

- 不把五个站点的视觉风格当成"设计语言"——它们各自有品牌，你只需要语义
- 不在一个页面同时用 BeUI 的磁吸 + Rare UI 的流体球 + Transitions 的花式过渡（三件套 = 新的廉价）
- 不为"用了 AI 原语"而硬加 AI 功能；没有 AI 过程的页面，一个 AI 原语都不要加
- 不引第三方运行时来实现过渡（Transitions 的价值在类型学，不在包）
