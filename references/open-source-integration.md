# 开源 SKILL 整合说明（9 项目 → 本技能）

> 核实日期：2026-10-22。9 个项目里 **6 个真实存在**，2 个路径错误（已找到真身），1 个不存在。
> 本文回答三件事：① 各项目贡献如何映射 ② 整合后技能的结构与关键规则 ③ 四端差异。

---

# 一、核实结果与贡献映射

| # | 项目 | 状态 | 核心贡献 | 整合落点 |
|---|---|---|---|---|
| 1 | `Leonxlnx/taste-skill` ★100.6k | ✅ | 反 slop 艺术方向：客户独有素材清单、主张先行、3 方向选型、真实素材、截图修复循环 | `SKILL.md` 模式 A 七步 + `anti-slop.md` |
| 2 | `anthropics/skills` → `skills/frontend-design` ★182.8k | ✅（不在 `anthropics/frontend-design`） | 设计主管视角、**5 类 AI 套路集群**、排版禁忌清单、"结构即信息"、单一编排动效、**两遍法**（先出 design plan 再审再写码）、Chanel 减一件、文案规范 | `anti-slop.md`（新增 AI 五集群 + 8 条 tell）、`prompt-master.md`（两遍法）、`design-system-spec.md`（结构即信息） |
| 3 | `emilkowalski/skills` ★48.4k | ✅ | 动效工艺：缓动选择、**出场比入场快（~75%）**、apple-design、mobile-native（H5/APP 原生化 7 个坑）、break-ui（最坏数据测试）、animation-vocabulary、性能 | `gsap-prompts.md`（缓动/时长/性能）、`platform-matrix.md`（移动端原生化清单）、`scripts/preflight.py`（极端数据检查） |
| 4 | `educlopez/ui-craft` ★394 | ✅ | **四档阶梯**、**4 个设计旋钮**（CRAFT/MOTION/DENSITY/VARIANCE）、Top-12 工艺规则、**10 项验收条**、Nielsen×6 法则评分 + 业务影响标签、design memory | 新建 `review-rubric.md`；`design-system-spec.md` 增「设计旋钮」 |
| 5 | `NakanoSanku/OhMySkills` ★162 | ✅ | 技能打包与组合调用约定（description 触发词、目录组织） | 本技能 `description` 写法与目录结构 |
| 6 | `Owl-Listener/designer-skills` ★3k | ✅ | 111 个技能按**情境**索引、`visual-critique` 输出优先级修复清单、color-system/token/hierarchy/dark-mode 知识、认知法则（Hick/Miller）、handoff-spec/QA checklist、parallel-concepts/concept-selection | 模式 C（`redesign-mode.md`）的评分与优先级；模式 A 的三方向（parallel-concepts）；`design-md-template.md` 的 token 分层 |
| 7 | `magicuidesign/magicui` ★22.8k | ✅ | **具名动效组件词汇**：bento grid、marquee、border beam、shine border、number ticker、text reveal、dock、dot/grid pattern 等；复制即用的组件结构 | `style-library.md` 增「营销页动效配方词汇表」 |
| 8 | `kokonut-labs/kokonutui` ★2.2k | ✅（不在 `kokonutd/kokonutui`） | Tailwind + shadcn + Motion 的组件审美范式：柔和渐变、玻璃质感、克制的微交互 | `style-library.md` 玻璃/柔光风格参考、组件微交互 |
| 9 | `nomaan5541/motionsites-prompt-collection` | ❌ 404 | — | 同类内容已由 #3 + #7 覆盖 |

**结论**：不需要引入任何新依赖。9 个项目里有价值的 6 个，其贡献已全部落进本技能的规则层，且与本技能原有主张（反 slop、主张先行、令牌先行）互相印证而非冲突。

---

# 二、整合后新增的关键规则（12 条）

这 12 条是本次整合真正改变输出的部分，其他为印证补强。

## 规则 1 · 四个设计旋钮（来自 ui-craft）
提示词里先声明旋钮值，AI 才知道"多精致、多少动效、多密、多大胆"：

```
CRAFT_LEVEL      = {1-10}  精修深度（3 快出，9 像素级）     默认 7
MOTION_INTENSITY = {1-10}  动效强度（1 只 hover，10 滚动叙事）默认 5
VISUAL_DENSITY   = {1-10}  信息密度（1 编辑式留白，10 仪表盘密集）默认 5
DESIGN_VARIANCE  = {1-10}  版式胆量（1 对称安全，10 实验构图）  默认：后台 4 / 落地页 7 / 作品集 8
```

行为带（必须写进提示词）：
- `MOTION ≤3`：只做 hover，无入场/无 stagger/无滚动
- `MOTION 4-7`：标准入场 + 悬停，每屏最多 1 个滚动揭示
- `MOTION 8+`：滚动联动、页面转场、磁性光标（仍守 reduced-motion）
- `DENSITY ≤3`：宽留白，每行 1-2 项；`≥8`：仪表盘密集
- `VARIANCE ≤4`：对称栅格；`5-7`：分栏 hero + 一处破格；`≥8`：展示级，仅在用户要求时

## 规则 2 · 10 项验收条（来自 ui-craft）
任何页面交付前必须全过，否则不算完成：

```
[ ] 1  层级：3 秒能看出主信息是什么
[ ] 2  令牌：颜色/字号/圆角/间距全部来自令牌，无 magic number
[ ] 3  配色：90% 中性 + 1 个强调色；强调色每屏出现 3-5 次（Hick 定律）
[ ] 4  圆角：分级而非统一（输入 6 / 卡片 10 / 弹层 14）
[ ] 5  阴影：环境光 + 直射光双层，而非单层黑影或纯描边
[ ] 6  字体：1 个正文族（可选 1 个展示族）；>24px 标题字距 -0.02em
[ ] 7  动效：出场比入场快（~75%）；动效强度符合旋钮
[ ] 8  状态：hover/focus/active/disabled/empty/error 六态齐全
[ ] 9  无障碍：正文对比 ≥4.5:1、键盘 focus 可见、reduced-motion 降级
[ ] 10 独特性：有一个"签名细节"，且删掉任一装饰不影响理解
```

## 规则 3 · 单一签名细节（signature detail）
每个 UI 必须有一个可被记住的细节（自定义 marker、一处版式破格、独特的 hover 或转场），
且**只允许一个**。其余全部安静。对应 Anthropic 的"Chanel 法则：出门前摘掉一件配饰"。

## 规则 4 · 排版禁忌清单（来自 Anthropic）
生成页面的最常见"AI 味"排版 tell，出现即改：
- 标题里只把**一个词**改成斜体/加粗/换色
- 小标签用全大写 + 宽字距（每个标题上方都挂 eyebrow）
- 内容上方加不必要的类型标签
- 非序列内容用 01/02/03 编号（只有步骤/时间线才配编号）
- 分隔线、小圆点、等宽字体小标签构成的"模板外壳"

## 规则 5 · 5 类 AI 视觉集群（来自 Anthropic 校准）
这些"看起来对"的组合其实是模型默认值，除非 brief 明确要求，否则避开：

| 集群 | 特征 |
|---|---|
| ① 暖奶油底 + 陶土色 | 背景 ≈#F4F1EA、高对比衬线标题、强调色 ≈#D97757 |
| ② 近黑底 + 荧光点缀 | #0A0A0A + 酸绿/朱红单一强调 |
| ③ 报纸风 | 发丝线分隔、零圆角、密集多栏 |
| ④ SaaS 卡片套装 | 内容切成完全相同的圆角卡、全站同一圆角、同一层 rgba(0,0,0,.1) 阴影、渐变装饰 |
| ⑤ 模板外壳 | 每个标题上方 ALL-CAPS eyebrow、`A · B · C` 元信息、`WORD — 片段` 标签、`#0B0B0B` 假黑、小数据用等宽字体、按钮末尾加 `→` |

## 规则 6 · 结构即信息（来自 Anthropic）
边框、编号、分隔线、eyebrow 都必须编码信息，不做装饰。加任何结构元素前先问：它传递了什么信息？

## 规则 7 · 出场比入场快（来自 emilkowalski / ui-craft）
`duration(exit) ≈ 0.75 × duration(enter)`；入场用 `ease-out`（减速），退场用 `ease-in`。
AI 最常犯的错：给入场用 `ease-in`、退场比入场还慢。

## 规则 8 · 移动端原生化七项（来自 emilkowalski/mobile-native）
H5 与 APP 必须处理的七个坑，任何一条缺失都会"像网页不像应用"：
1. 粘滞 hover（移动端悬停残留）→ `@media (hover:hover)` 包裹 hover 规则
2. 点击高亮闪烁 → `-webkit-tap-highlight-color: transparent`
3. `100vh` 在移动浏览器被地址栏吃掉 → 用 `100dvh` / `svh`
4. 输入框聚焦时页面被放大 → 输入字号 ≥16px
5. 点击延迟 → 用 `pointerdown` 而非 `click` 做即时反馈
6. 安全区 → `env(safe-area-inset-*)` 全量预留
7. 滚动链与惯性 → 避免嵌套滚动，必要时 `overscroll-behavior: contain`

## 规则 9 · 用最坏数据打页面（来自 emilkowalski/break-ui）
交付前用极端数据自测：超长姓名、单字母名、超长邮箱、六位数金额、空列表、超长标签、0 条数据。
任何一处溢出/错位都算不合格。`preflight.py` 已加此项提示。

## 规则 10 · 两遍法（来自 Anthropic frontend-design）
不要一次生成到底：
1. **第一遍出计划**：4-6 个命名 hex 的色板 + 字体与角色 + ASCII 线框布局 + 一条"这页凭什么独特"的原则
2. **对照 brief 审一遍**：哪一部分像"给任何同类页面都会产出的默认值" → 改掉并说明
3. **第二遍写代码**：严格按修正后的计划

## 规则 11 · 文案也是设计（来自 Anthropic + ui-craft）
- 用用户语言命名（"管理通知" 而不是 "Webhook 配置"）
- 主动语态，CTA 说清结果："保存修改" 而不是 "提交"
- 动作名全流程一致：按钮 "发布" → 提示 "已发布"
- 报错不道歉、不含糊：说清发生了什么 + 怎么修
- 空状态是行动邀请，不是抒情
- 每个文字元素只干一件事

## 规则 12 · 有分歧时按此裁决（本技能自定）
| 冲突 | 裁决 |
|---|---|
| Anthropic："每段 fade-up 入场是 AI 默认病" vs 本技能早期"滚动揭示" | **营销页**：只允许 1 个编排好的入场序列 + 交互驱动动效，禁止逐段 fade-up；**后台**：允许分区入场（功能性，帮助定位），但 `MOTION ≤3` 时全部禁用 |
| ui-craft："不要默认蓝色" vs 本技能"三套系统都是蓝主色" | 后台蓝是**行业惯例而非默认值**：客户有品牌色必须用品牌色；无品牌色时在提示词里明示"选蓝是因为 X"，否则换色相 |
| 圆角统一 vs 分级 | 采用分级（6/10/14/20），统一圆角是 SaaS 卡片套装的 tell |
| 90% 中性 vs 品牌强色 | 营销页可放宽到 80/20，后台严守 90/10 |

---

# 三、整合后的技能结构

```
website-ui-designer/
├── SKILL.md                     # 入口：三模式 + 页面类型路由 + 旋钮 + 通用纪律
├── references/
│   ├── design-system-spec.md    # 主规范：八要素 + 九段提示词 + 意图→参数 + 旋钮
│   ├── review-rubric.md         # ★新增：10 项验收条 + 评分卡（Nielsen×6法则×业务影响）
│   ├── anti-slop.md             # ★增强：AI 五类集群 + 8 条排版 tell + 结构即信息
│   ├── open-source-integration.md # ★本文件：9 项目映射 + 12 条新规则 + 四端差异
│   ├── prompt-anatomy.md        # 5 行式风格提示词解剖（含原图存档）
│   ├── style-library.md         # 风格库 + ★动效配方词汇表（magicui/kokonutui）
│   ├── prompt-master.md         # 九段提示词骨架 + 两遍法
│   ├── gsap-prompts.md          # 动效参数库 + 正确兜底模式
│   ├── dashboard-style.md       # 工作台（数据/创作）+ 服务型工作台
│   ├── clone-mode.md            # 复刻：浏览器/截图/设计系统三路径
│   ├── redesign-mode.md         # 审计 + 定向修复
│   ├── platform-matrix.md       # ★增强：四端差异 + 移动端原生化七项
│   └── design-md-template.md    # DESIGN.md 令牌模板
├── scripts/preflight.py         # 交付前硬伤扫描（7 类 + 极端数据）
└── tests/                       # 8 个实测页（营销/后台/创作/医疗/H5）
```

**层级关系**：`SKILL.md` 是路由与纪律 → `design-system-spec.md` 是主规范 →
其余 references 是各场景的参数库 → `review-rubric.md` 是交付闸门 → `preflight.py` 是自动闸门。

---

# 四、四端适用差异

| 维度 | PC 网站 | H5 | 微信小程序 | APP |
|---|---|---|---|---|
| 旋钮默认 | CRAFT 8 / MOTION 6 / DENSITY 5 / VARIANCE 7 | CRAFT 7 / MOTION 3 / DENSITY 4 / VARIANCE 4 | CRAFT 7 / MOTION 3 / DENSITY 5 / VARIANCE 3 | CRAFT 8 / MOTION 6 / DENSITY 4 / VARIANCE 3 |
| 动效上限 | 滚动联动、光标跟随、页面转场 | 仅 hover 替代（按下反馈）+ 单次入场 ≤0.4s | 原生组件动效优先（swiper/picker），自绘动画 ≤0.3s | 跟手手势、转场、共享元素 |
| 必做项 | hover/focus 六态、键盘可达 | 移动端原生化七项、44px 热区、吸底栏 | rpx 换算、自定义导航栏预留、分包 | 安全区、平台导航模式、暗色模式 |
| 禁区 | 滚动劫持 | 粘滞 hover、100vh、<16px 输入字号 | 重 DOM 动画、大图未压缩 | 自造导航（破坏返回手势） |
| 圆角/字号基线 | 6/10/14/20 · 正文 15-17 | 12/16/999 · 正文 ≥15 | 同 H5（rpx 换算） | 10/14/20 · 正文 15-17pt |
| 图标 | SVG 2px 线性 | 同 PC，尺寸 20-22 | 单色 PNG/SVG，81px tabBar | 平台图标语言（SF Symbols / Material） |
| 交付验收 | preflight + 10 项验收条 | 加：真机 375/390/430 三档 + 安全区 | 加：开发者工具真机预览 + 包体检查 | 加：iOS/Android 双端 + 暗色 + 动态字号 |

**同一份提示词怎么跨端复用**：保留第 1-6 段（角色/令牌/布局/组件/排版/图标），只替换
第 7 段平台段与第 8 段动效段的参数，其余不动。令牌层保持同一套，保证多端品牌一致。
