# SKILL 架构与调用规范（Governance）

> 版本 2.3.0 起，本文件是**唯一的能力地图**。遇到"该看哪份文件""两份文件说法冲突"时，先看这里。
> 其余 28 份参考文件都是"实现层"，不参与仲裁。

---

## 0. 一句话结论

**七层结构，每层只有一个负责人；跨层冲突时，下层永远服从上层。**
层内冲突时，看 `SSOT`（Single Source of Truth）标记；标 `冻结` 的文件只作历史样例，不再参与决策。

---

## 1. 七层全景

```
L0 宪法层    SKILL.md（原则/红线/自检） + skill-architecture.md（本文件）
L1 输入层    design-intake（澄清/迭代） · terminology-layer（说法翻译） · rag-retrieval（检索）
L2 方向层    brand-direction（旋钮/五轴/昂贵感/骨架） · brand-spec-library（品牌与行业）
L3 结构层    workbench-blueprint（工作台五部件/数据地板） · dashboard-style（行业细节）
L4 系统层    token-architecture（令牌） · typography-system（字体） · component-library（组件）
L5 表现层    component-capability-library（语义原语） · motion-decision-table（决策） · motion-spec（参数） · visual-interaction-spec（可读性/交互态）
L6 交付层    review-rubric（评分） · audit_contrast / preflight（机器闸门） · examples（范式）
```

**流动方向不可逆**：L0 约束 L2，L2 决定 L3，L3 消费 L4，L4 供 L5 使用，L6 只验收不决策。
**禁止**：从 L5 反推 L2（"先挑个酷动效再想这页要说什么"）——这是最常见的顺序错误。

---

## 2. 职责表（每份文件只干一件事）

| 文件 | 唯一职责 | 输入 | 输出 | 明确不负责 | 状态 |
|---|---|---|---|---|---|
| **SKILL.md** | 角色、工作流、五模块硬规则（A-E）、红线、优先级、交付契约、清单 | 任何需求 | 决策与约束 | 具体实现代码 | **SSOT·宪法** |
| **skill-architecture.md** | 能力地图、优先级、冲突裁决 | 层内冲突 | 调用顺序 | 设计本身 | **SSOT·治理** |
| design-intake | 三问澄清、方案卡、反馈归类、迭代上限 | 用户原话 | 需求卡 + 方案卡 + 迭代记录 | 视觉判断 | SSOT |
| terminology-layer | 症状 → 术语，成对坑 | 用户描述 | 1-3 条术语 + 改写需求 | 设计方案 | SSOT |
| rag-retrieval | 生成前检索依据 | 查询 | 注入块（必须遵守/禁止/依据） | 判断依据对不对 | SSOT |
| brand-direction | 方向：三旋钮、五轴、昂贵感、四种骨架、廉价清单 | 需求卡 | 方向 + 骨架 + 材质 | 具体色值/组件 | SSOT |
| brand-spec-library | 品牌规范与行业默认的取用 | 行业/品牌 | 四件事 + 禁忌 + 令牌映射 | 品牌创意 | SSOT |
| workbench-blueprint | 工作台五部件、数据地板、时刻 | 工作台需求 | 规格（不是页面） | 视觉风格 | SSOT |
| dashboard-style | 行业工作台细节（KPI/表格/图表） | 工作台规格 | 组件参数 | 钩子与数据地板 | 参考 |
| token-architecture | 三层令牌、oklch、多端换算、迁移 | 品牌色 | 令牌文件 | 组件长什么样 | **SSOT·令牌** |
| typography-system | 字族关系、字阶、中文、性能 | 方向 | 字体方案 | 排版布局 | **SSOT·字体** |
| component-library | 组件库选型与接入纪律 | 技术栈 | 接入方案 + 主题映射 | 页面结构 | **SSOT·组件** |
| component-capability-library | 语义 → 原语映射（shadcn/Beautiful UI/beUI/Rare UI/Transitions） | 需求语义 | 原语 + 抽取内容 + 降级 | 工程接入 | **SSOT·语义原语** |
| motion-decision-table | 动效**要不要做**、做哪类、多久 | 模块清单 | 动效决策表 | 具体库参数 | **SSOT·动效决策** |
| motion-spec | 动效**怎么做**（库/弹簧/呼吸/性能） | 决策表 | 参数与代码 | 该不该做 | **SSOT·动效参数** |
| visual-interaction-spec | 对比度、视觉焦点、8 态、成功动画 | 页面 | 硬指标 + 验收 | 方向与骨架 | **SSOT·可读性** |
| diagnosis-protocol | 七项扫描、灰度测试、处方、优先级 | 现状 | 诊断报告 | 设计方案 | **SSOT·诊断** |
| review-rubric | 评分卡、三段清单、最坏数据 | 产物 | 分数 + 必改项 | 设计决策 | **SSOT·评分** |
| platform-matrix | 四端差异与移动端六条 | 平台 | 适配参数 | 视觉风格 | SSOT·平台 |
| design-md-template | DESIGN.md 的文档格式 | 令牌 | 文件骨架 | 令牌内容 | 格式 |
| examples/* | 范式（六段依据、验证案例） | — | 参照物 | 规则来源 | 参考 |
| anti-patterns | 20 条红线（判定/损害/替代/例外） | — | 禁令 | 正面方案 | **SSOT·禁令** |
| learning-loop / inspiration-sources | 个人能力与素材获取 | — | 方法/清单 | 决策 | 参考 |
| open-source-integration | 方法论来源与历史记录 | — | 溯源 | 决策 | 存档 |

### 2.1 已冻结（保留但不再作为依据）

| 文件 | 冻结原因 | 现由谁接管 |
|---|---|---|
| `anti-slop.md` | 与 `anti-patterns.md` 重复，且条目更旧 | **anti-patterns**（20 条） |
| `style-library.md` | 6 种风格模板会造成"选模板"而非"组合方向" | **brand-direction** 五轴 |
| `gsap-prompts.md` | 只是实现片段，容易被误当成"动效该怎么做"的决策依据 | **motion-decision-table**（决策）+ **motion-spec**（参数） |
| `redesign-mode.md` | 与 `diagnosis-protocol` 重叠且无优先级算法 | **diagnosis-protocol** |
| `prompt-anatomy.md` | 5 行式解剖已被 brand-direction 的五轴 + 六段契约取代 | **brand-direction** + **SKILL.md §7** |
| `prompt-master.md` | 九段式提示词仍是有效交付格式，但不再是"设计方法" | 保留为**输出格式**，不作决策依据 |
| `clone-mode.md` | 复刻流程仍有效，但"照着抄"违反 brand-direction 的反同质化 | 保留为**输入路径**，必须先过五轴改造 |
| `design-system-spec.md` | 数值库仍有用，但令牌结构以 token-architecture 为准 | **token-architecture**（结构）+ 本文件（数值） |

> 冻结 ≠ 删除。历史项目仍在用，删了会让老交付无法追溯；但它们不得再作为新决策的依据。

---

## 3. 12 组重叠与裁决

| # | 重叠 | 冲突表现 | 裁决 |
|---|---|---|---|
| 0 | component-capability-library vs component-library | 都谈 shadcn，一个谈"该用哪种原语"、一个谈"怎么接进工程" | **语义选型看 capability，工程接入看 component-library**；两者都受 motion-decision-table 的时长约束 |
| 1 | anti-slop vs anti-patterns | 两套禁令，条目数不同 | anti-patterns 为准（20 条）；anti-slop 冻结 |
| 2 | motion-spec vs motion-decision-table | 一个讲参数、一个讲时机，常被混用 | **先决策后参数**：先查 decision-table 定"哪类/多久"，再查 motion-spec 定"用什么库/弹簧" |
| 3 | gsap-prompts vs motion-spec | gsap 片段暗示"动效=GSAP" | 库选型以 motion-spec 的决策树为准；GSAP 只是五种引擎之一 |
| 4 | visual-interaction-spec vs brand-direction | 都谈"好看"，一个给硬指标、一个给方向 | 方向由 brand-direction 定；对比度/8 态由 visual-interaction-spec 一票否决 |
| 5 | token-architecture vs design-system-spec | 都列令牌与字号 | 结构/命名/换算看 token-architecture；具体数值区间看 design-system-spec |
| 6 | workbench-blueprint vs dashboard-style | 都谈工作台 | 钩子/数据地板/顺序 → blueprint；KPI 卡/表格/图表细节 → dashboard-style |
| 7 | diagnosis-protocol vs redesign-mode | 都做"审现有页面" | 一律走 diagnosis-protocol 的七项扫描与优先级公式 |
| 8 | brand-direction vs style-library | 一个组合、一个选模板 | 选模板 = 同质化来源，冻结 style-library |
| 9 | design-intake vs workbench-blueprint | 都要"先问清楚" | intake 负责通用三问；blueprint 只补工作台特有的"时刻/数据地板" |
| 10 | terminology-layer vs 文案规范 | 一个翻译术语、一个写文案 | 术语解决"叫什么"，文案解决"怎么说"；不互相替代 |
| 11 | platform-matrix vs component-library | 都涉及"多端" | 单位/安全区/导航 → platform-matrix；组件在多端如何复用 → component-library |
| 12 | motion 五类 vs 3.10 硬规则 | 时长档位两处出现 | 以 motion-decision-table 的五类为准；3.10 是摘要 |

**通用裁决规则（按顺序）**
1. 宪法（SKILL.md）优先于一切
2. 层内 SSOT 优先于参考
3. 更具体的范围优先（"医疗工作台" > "全部后台"）
4. 可测量的优先（4.5:1 > "看起来更舒服"）
5. 仍冲突 → 记录到交付说明，由人裁定，**不许静默选一个**

---

## 4. 调用优先级（P0-P6）

```
P0 宪法闸门     灰度测试是否通过？对比度/触控/焦点是否达标？
                不通过 → 停，先修结构或换令牌，不进入美化
P1 输入          design-intake 三问 → 需求卡
                 用户说症状 → terminology-layer 翻译（1-3 条）
                 需要依据 → rag.py 检索（无命中则标注推断）
P2 方向          brand-direction：三旋钮 + 五轴组合（≥3 轴不同于上一条）
                 有品牌 → brand-spec-library 取四件事 + 禁忌
P3 结构          品牌页：四骨架之一
                 工作台：workbench-blueprint 五部件 + 数据地板
P4 系统          token-architecture（令牌）→ typography-system（字体）→ component-library（组件）
P5 表现          motion-decision-table（要不要/哪类/多久）→ motion-spec（参数）
                 visual-interaction-spec（8 态/成功动画/聚焦）
P6 交付          六段设计依据 → review-rubric 评分 → audit_all.py → 七问自检
```

### 4.1 决策树（用户说 X，先开哪份）

```
"不好看/说不上哪不对"     → P0 灰度测试 → diagnosis-protocol
"太挤/太空"               → design-system-spec 的间距档 + intake 的密度映射
"太土/廉价"               → brand-direction（昂贵感七条）+ anti-patterns
"AI 味重"                 → anti-patterns（组合识别，≥3 条换骨架）
"要高级/要质感"           → brand-direction（旋钮 + 材质）+ typography-system
"要动起来/加动效"         → motion-decision-table（先问服务哪类）→ motion-spec
"按钮点了没感觉"           → visual-interaction-spec §3.2（8 态 + 成功动画）
"信息太多放不下"           → SKILL.md §9 冲突裁决（折叠→降权→分屏，最后才删）
"做后台/工作台"           → workbench-blueprint（数据地板）→ dashboard-style
"照这个截图做"             → clone-mode（取样）→ 必须过 brand-direction 五轴改造
"多端要一致"               → platform-matrix（差异）+ token-architecture（转换层）
"要组件库"                 → component-library（四件必改 + variant 纪律）
```

### 4.2 允许跳过的步骤（以及条件）

| 可跳过 | 条件 |
|---|---|
| P1 三问 | 用户已给出完整画像/任务/场景，且文档里有 |
| P2 五轴 | 组件级改造（只改一个按钮/卡片），不涉及整页人格 |
| P3 骨架 | 只做 token 级修复（对比度、间距、字号） |
| P5 动效 | 工具型高频界面，且 `MOTION ≤3` |
| 六段依据 | **永不允许跳过**（可以精简到 6 行，但六段必须都在） |

---

## 5. 组合调用示例

### 5.1 品牌站（要质感、要记忆点）
```
intake 三问 → rag 检索（行业配色/字体依据）→ brand-direction（SOUL 7 / SPECTACLE 6 / DENSITY 4，五轴组合）
→ 四骨架选"落地页"→ token-architecture（暖纸底 + 单强调）→ typography-system（衬线 display + 无衬线正文）
→ motion-decision-table（一个引擎 + 入场编排）→ motion-spec（CSS-only 扫描，3.2s 一次）
→ visual-interaction-spec（对比度 + 8 态）→ 六段依据 → audit_all
```

### 5.2 工作台（要好用、要耐看）
```
intake → workbench-blueprint（身份→钩子→数据地板→模块→收入缝，先拿数据地板）
→ rag 检索（KPI 数量/密度依据）→ dashboard-style（KPI 四段、表格、徽章）
→ token-architecture（语义令牌 + 深浅）→ component-library（表格/弹层用 Radix 行为）
→ motion-decision-table（MOTION 3-4：只有状态反馈与展开）→ 六段依据 → audit_all
```

### 5.3 H5 工具页（单手、强光）
```
intake（场景=强光/单手/戴手套）→ platform-matrix（移动端六条 + 44px）
→ design-system-spec（密度偏紧但字号不缩）→ typography-system（16px 输入、等宽数字）
→ visual-interaction-spec（吸底+安全区、单点呼吸）→ motion-decision-table（100/150ms 两档）
→ 六段依据 → audit_all
```

---

## 6. 统一规范（跨 SKILL 的"宪法"15 条）

任何层、任何文件产出的方案，必须同时满足：

1. **灰度成立**：去色后层级仍在，否则不谈美化
2. **一屏一焦点**：靠尺寸/对比/孤立建立，不靠到处强调
3. **内部 ≤ 外部间距**：违反即分组崩塌
4. **对齐零容忍**：同列误差 ≤1px
5. **正文 ≥4.5:1，UI ≥3:1**，浅深两套都过
6. **触控 ≥44px**（紧凑 ≥40），焦点环可见
7. **字族 ≤2、字重 ≤3、正文 ≥16（移动 mockup ≥14）**
8. **颜色是拐杖**：强调色一屏 ≤5 处，语义色软底深字
9. **动效必属五类**，说不出目的就删；重复交互 ≤500ms
10. **记忆点唯一**：1 个、1 次、可跳过、不阻断
11. **组件只消费语义令牌**，不写死色值
12. **多端差异只在转换层**，不允许各端各写一套色
13. **每个决策可追溯**：一条原理 或 一项用户成本
14. **信息超载先折叠/降权/分屏**，最后才删
15. **六段依据 + 自动审计**，缺一不交付

---

## 7. 趋势立场（2026）

### 7.1 当下共识（可作为默认值）
| 趋势 | 具体表现 | 为什么成立 |
|---|---|---|
| 静奢 / 低饱和 | 暖纸底、单强调、大留白 | 高饱和疲劳，低饱和更耐看、更易过对比度 |
| 编辑式栅格 | 非对称、细线、真数字 | 对抗"四列等宽卡片"的同质化 |
| 质感物理层 | 极轻颗粒、半透明描边、无纯黑纯白 | 屏幕分辨率过剩后，"塑料矢量感"成了廉价信号 |
| 克制动效 | 功能分类、一次性编排、终态设计 | 动效从"炫技"回归"沟通" |
| 语义令牌 | 三层 + oklch + 深浅成对 | 多端与主题化的必然结果 |
| AI 原生界面 | AI 输出作为一等组件（摘要/建议/生成块） | 聊天浮窗已不够用 |
| 表格回归 | 图表少而准，表格承载明细 | 大屏图表疲劳，可核对的数据更可信 |
| 无障碍默认 | 对比度/键盘/降级写进流程 | 法规与用户结构变化 |

### 7.2 已过时 / 高危（默认禁用）
满屏玻璃拟态 · 紫蓝渐变 + 发光暗色 · 每段 pill / 每节 eyebrow · 全屏假大数字 · 装饰 3D 插画充数 · 无限循环装饰动效 · 三族字体混搭 · 组件库默认皮肤直出。

### 7.3 趋势的使用判据（防止追风）
1. 趋势只提供**默认值**，不提供**正确性**
2. 任何趋势违反宪法（对比度/触控/焦点）→ 立刻否决
3. 采用趋势时必须能说出"它解决了什么"，说不出就是跟风
4. 同一趋势在**同一页面最多用一次**（比如颗粒只能一层）
5. 行业惯例优先级高于趋势（金融不用紫粉、医疗不用高饱和）

---

## 8. 单一入口：一条命令过关

```bash
python scripts/audit_all.py tests/*.html
# 依次跑 preflight（7 类硬伤）+ audit_contrast（浅深全部配对）
# 输出单一结论：PASS / FAIL，并列出必须先修的三处
```

**交付判定**：`audit_all` 为 PASS + 六段依据齐全 + 七问自检全"是"。

---

## 9. 演进规则（防止再次长成一团）

新增能力前，先回答三个问题：

1. **它属于哪一层？** 答不出 → 不要新增文件
2. **它和现有 SSOT 是"替代"还是"补充"？** 替代 → 冻结旧文件并在本表登记；补充 → 写进已有文件的新章节
3. **它可被验证吗？** 不能验证的规则（"更有呼吸感"）不入规范，只入风格参考

**文件数量上限**：参考文件 ≤32 份。超过说明在做"收藏"而不是"规范"。
**每季度一次**：跑 `grep -l "冻结" references/*.md` 检查冻结文件是否仍在被引用；清理重复条目。


---

## 10. 子技能路由（v3.1）

主 SKILL 负责编排；子技能只解决单一领域，**不得自行改结构或配色**。

| 触发关键词 | 子技能 | 输入 | 输出 | 边界（不做什么） |
|---|---|---|---|---|
| 小程序 / rpx / 微信 | miniprogram-ui | 页面清单 + 平台约束 | rpx 换算、胶囊避让、包体积方案 | 不做品牌视觉与动效编排 |
| 动画 / 滚动叙事 / 交互 | motion-design | 模块清单 + 目的 | 时长/缓动/编排/降级表 | 不改布局与信息架构 |
| 仪表盘 / 图表 / 数据 | data-viz | 指标清单 + 数据地板 | 图表选型、KPI、表格、空态 | 不做品牌视觉 |
| 游戏 / HUD / 战斗 | game-ui | 屏幕分区 + 输入方式 | 帧预算、HUD 安全区、输入方案 | 不做关卡与玩法视觉 |
| 其余 | Design Token 流程 | 需求卡 | Design Spec | 不替代专项实现 |

**编排规则**
1. 一次任务最多加载 2 个子技能；超过说明需求未拆清
2. 子技能产出必须回到主 SKILL 的 §10 优先级裁决（可访问性 > 结构 > 语义 > 视觉 > 动效）
3. 子技能与主 SKILL 冲突时，**主 SKILL 优先**，并在交付说明里记录冲突点


---

## 11. 维护纪律：单一数据源（v3.3）

事实：`~/.workbuddy/skills/website-ui-designer/` 与工作区仓库 `website-ui-designer/` 各有一份副本，
双向复制已导致**两次修复被旧版本覆盖**。

**规则**
1. **技能目录是唯一源**（Agent 实际加载的就是它）；仓库只做只读镜像
2. 任何修改：先改技能目录 → 验证 → **单向** `cp` 到仓库 → 提交
3. **禁止**从仓库反向复制到技能目录（除明确的版本回滚，且需在 CHANGELOG 记录）
4. 提交前对比一次：`diff -r` 或逐文件 `cmp`，确认两边一致
