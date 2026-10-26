# 版本记录

语义化版本：`主版本.次版本.修订号`（1.0.0 起）

| 位 | 何时递增 | 本项目的判定 |
|---|---|---|
| 主版本号 | 不兼容变更 | 入口模式重写、规范文件结构重组、输出契约改变 |
| 次版本号 | 新增能力 | 新增页面类型/平台支持/参考文件/脚本/知识检索 |
| 修订号 | 修复与优化 | bug 修复、文档改写、参数微调 |

> 说明：本技能在正式发布前经历过多轮内部迭代（无版本编号）。为保证对外版本号可读，统一收敛为 **1.0.0 作为首个正式版**，此前工作不单独编号。

---

## v2.4.0 — 2026-10-26

**组件能力库：五个来源抽象为"语义原语 + 检索映射 + 落地规则"**

### 抓取核实（2026-10-26，四个站点均成功）
| 来源 | 实测 | 关键事实 |
|---|---|---|
| Beautiful UI | 21 个 AI 原语（01-21） | Loading/Thinking（四态 trace）/Streaming/Approval/Tool Chips/Task Rows/Chat/Prompt Bar/Recommendation/Context/Diff/Records/Filter/Search/Flowchart/Insight/Code/Fine-tune/Selection/Agent Screen |
| beUI | 71 个组件（含 RN） | Motion + Tailwind，**shadcn registry 分发**（`bunx shadcn add @beui/timeline`） |
| Rare UI | 27 个单文件组件 | shadcn CLI + MCP（`npx shadcn@latest add swamimalode07/rare-ui/fluid-orb`） |
| Transitions | 43+ 过渡 | 分 Essential/AI Agents/Effects/Texts/Pro；含 card resize、number pop-in、text swap、origin-aware menu |

### 新增
- `references/component-capability-library.md`
  - A 能力矩阵（来源/能力域/触发场景/提取内容）+ **检索顺序**：shadcn 基座 → beUI/Rare 定风格 → Transitions 加质感 → Beautiful UI 补 AI 原语
  - B 五个来源的三段式（能力域 + 触发场景 + 落地规则），强调"抽象语义、用自己令牌重绘、保留状态机与时序"
  - C **33 条语义 → 组件映射表**，每条含降级路径
  - D 七步检索流程 + 输出模板（原语/来源/抽象了什么/如何重绘/保留的交互/降级）+ 五道质量闸门 + 与现有架构的接法
  - 抓取失败时的降级：Rare UI → 至少一个维度非常规；Transitions → shared axis/120-200ms/骨架屏无缝/reduced-motion

### 主文件与治理
- 新增 3.19 组件能力库（含顺序、来源表、语义示例、铁律与降级）
- `skill-architecture.md`：L5 表现层加入本文件；职责表新增"SSOT·语义原语"；新增第 0 组冲突裁决（语义选型 vs 工程接入）

## v2.3.0 — 2026-10-25

**治理版：把 29 份参考文件收成一套可执行的架构**

### 新增
- `references/skill-architecture.md`：七层结构（宪法/输入/方向/结构/系统/表现/交付）、29 份文件的唯一职责表、
  SSOT 与冻结清单、**12 组重叠的裁决**、P0-P6 调用顺序与决策树、三种场景的组合示例、
  跨 SKILL 的 15 条统一规范、2026 趋势立场（共识 8 项 / 高危 8 项 / 5 条使用判据）、演进规则（≤32 份）
- `scripts/audit_all.py`：统一闸门，一条命令跑 preflight + contrast，输出单一 PASS/FAIL 与前三条必修

### 冲突清理（打状态标记，不删历史）
- 冻结：`anti-slop`（并入 anti-patterns）、`style-library`（选模板→五轴组合）、`redesign-mode`（并入 diagnosis-protocol）、
  `prompt-anatomy`（被五轴 + 六段契约取代）
- 降级为实现层参考：`gsap-prompts`（只给片段）、`design-system-spec`（只给数值）、`dashboard-style`（只给行业细节）
- 明确边界：`prompt-master` 仅作输出格式；`clone-mode` 仅作输入路径且必须过五轴改造；`open-source-integration` 存为溯源

### 主文件
- 顶部加入"冲突先看架构图"的指针；§12 索引把 skill-architecture 置顶
- S5 验证改为"一条命令过闸"（audit_all）+ 闸门 0

## v2.2.0 — 2026-10-25

**组件库、字体、品牌规范三块能力补齐**

### 来源核实（2026-10-25）
| 来源 | 状态 | 采用 |
|---|---|---|
| `shadcn-ui/ui` | 126.5k★ MIT | 源码复制式接入、Radix 无障碍契约、主题映射、升级 diff 策略 |
| `material-components/material-web` | 11.4k★ Apache-2.0（npm 2.5.0） | Web Components 选型与"维护模式"风险提示 |
| `vercel/turborepo` DS 模板 | 页面 HTTP 200 | monorepo + Storybook 适用场景与包边界纪律 |
| `vercel/geist-font` | 3.7k★ OFL-1.1（npm `geist` 1.8.2） | Geist Sans/Mono/Pixel 用法、许可、自托管与回退栈 |
| `nextlevelbuilder/ui-ux-pro-max-skill` | 140k★ MIT | 行业→配色/字体推理（v2 为 192 套配色），作为"起点"而非结论 |
| `nexu-io/open-design` | 104k★ Apache-2.0 | 151 个设计系统包、`DESIGN.md` 作为品牌契约的用法 |
| `getdesign` npm | 0.6.26 | `npx getdesign add <brand>` 装 DESIGN.md 的流程 |

### 新增
- `references/component-library.md`：选型矩阵、shadcn 接入四件必改之事、令牌映射、无障碍契约、MWC 注意事项、Turborepo DS 适用边界、组件消费三层、组件库解决不了的五件事
- `references/typography-system.md`：字族关系表、Geist 家族、中文搭配五种坑、字阶参数、性能预算与 `size-adjust` 回退、八条验收
- `references/brand-spec-library.md`：三个品牌规范来源的用法、只提取四件事、12 令牌映射表、八行业规则速查、五条合规红线、半天落地流程
- `templates/shadcn-theme.css`：本技能令牌 → shadcn CSS 变量（oklch），含圆角/间距/字阶、组件分级与 Tailwind v3 转换说明

### 主文件
- 新增 3.16 组件库（含"shadcn 必须重做四件事"）、3.17 字体、3.18 品牌规范来源
- 反模式 18 → 20 条（组件库默认皮肤直接上线、三族混用/正文 300 字重）
- 索引补四行

## v2.1.1 — 2026-10-24

**工具修正 + 能力验证**

- `audit_contrast.py` 修正两处误判：`--*‑ink`（按钮上的文字）此前被当成正文色与页面底配对，导致"白字压白底"的假违规；现改为"任何 `X-ink` 只与 `X` 配对"
- 新增 `--pairs` 参数，支持自定义命名令牌的显式校验：
  `python scripts/audit_contrast.py page.html --pairs="--ink:--paper,--dark-ink:--dark"`
- 新增两个验证页与一份验证说明：
  - `tests/test11-v2-industrial-site.html` — PC 品牌站（SOUL 7 / SPECTACLE 6 / DENSITY 4，CSS-only 扫描引擎，颗粒质感）
  - `tests/test12-v2-inspection-h5.html` — H5 点检页（渐变头 + 白面板 + 5×2 宫格 + 吸底安全区 + 深色模式）
  - `examples/v2-validation.md` — 两个案例的输入、旋钮、五轴、六段依据、动效映射、审计结果，以及"能做到/做不到"的边界
- 审计：11 个测试页 `preflight` 0/0、`contrast` 0 违规

## v2.1.0 — 2026-10-24

**整合 finesse 系列四技能，补上"品牌方向 / 工作台架构 / 说法层 / 帧级动效"**

### 来源核实（2026-10-24）
| 仓库 | 状态 | 采用 |
|---|---|---|
| `mouse-lin/finesse-skill`（skills/finesse-ui，848★，MIT） | 真实 | 三旋钮、五轴组合、昂贵感物理层、Hero 引擎、四骨架、廉价黑名单、移动端六条 |
| `mouse-lin/finesse-brief`（101★，MIT） | 真实 | 五部件顺序、数据地板五问、幸运饼干测试、四类写入者、时刻、交接即停止 |
| `mouse-lin/frame-smith`（95★，MIT） | 真实 | 秒→帧、clamp、拍点表、终态帧、尺寸系统、反廉价动效 |
| `mouse-lin/finesse-term`（55★，MIT） | 真实 | 说法层、三条门禁、成对坑、trigger/say/trap 词条结构、说法对齐表 |

### 新增参考文件
- `references/brand-direction.md`：三旋钮 + 行业推断 + 五正交轴（反同质化，≥3 轴不同）+ 昂贵感七条（颗粒/暗角/字体张力/分层 z-index/半透明描边/无纯白纯黑/色彩锁定）+ Hero 引擎五种 + 四种页面骨架 + 廉价黑名单 11 条 + 移动端六条
- `references/workbench-blueprint.md`：五部件（身份→钩子→数据地板→模块→收入缝）+ 数据地板五问 + 幸运饼干测试 + 四类写入者（user/system/integration/derived）+ 时刻与节奏 + 工作台十项自检
- `references/terminology-layer.md`：说法层定位 + 三条硬门禁 + 五组成对坑 + 检索方法 + 三种输出模板 + 说法对齐表

### 主文件变更
- 新增 3.13 品牌方向（旋钮 + 五轴 + 宣称即交付）
- 新增 3.14 工作台五部件与数据地板（含幸运饼干测试）
- 新增 3.15 说法层（三条门禁）
- 反模式红线 12 → 18 条（新增：长破折号、渐变文字、每节 eyebrow、相同卡片栅格、假精确数字、该有图处无图）
- 多端章节补移动端六条硬规则
- S5 验证增加「闸门 0：页面是否真的渲染」（文件解析 + 样式加载）
- 动效规范补「帧级纪律」：秒→帧、clamp、拍点表、终态帧、尺寸系统、反廉价动效

## v2.0.0 — 2026-10-23

**不兼容变更：重写为「设计总监版」**

输出契约变了（新增六段设计依据 + 诊断报告），流程从"生成提示词"改为"诊断 → 决策 → 落地 → 验证"。
旧版三入口（A/B/C）保留为参考文件，主流程以新版为准。

### 新增（主文件内建）
- **12 条 UI 认知底座**：层级与焦点、格式塔五项、间距系统、角色化排版、三层色彩、对齐零容忍、
  密度双模式、可访问性、多端 token、动效五类、记忆点、用户成本模型
- **五步诊断流程**：采集 → 七项扫描（灰度/分组/层级/对齐/对比度/触控/动效）→ 优先级排序 →
  三级干预（token→组件→结构，能小改不重做）→ 验证
- **优先级算式**：`影响人数 × 成本等级 ÷ 修复成本`，替代"平均用力"
- **六段强制输出契约**：层级依据 / 降成本机制 / 不拥挤控制 / 特效取舍 / 模块动效映射 / 记忆点
- **12 条反模式红线** + 例外流程；命中 ≥3 条判定为"需换骨架"
- **七条冲突裁决**：信息丰富 vs 拥挤、美观 vs 可用、一致 vs 记忆点、品牌色 vs 可读、
  紧凑 vs 可访问、动效 vs 性能、品牌统一 vs 多端差异
- **交付前七问**

### 新增（参考文件）
- `references/diagnosis-protocol.md`：灰度测试操作法（去色 + 25% + 3 秒）、七项扫描表、10 条处方库、
  优先级打分示例、诊断报告模板
- `references/token-architecture.md`：三层令牌、oklch 色阶生成、语义映射表、深浅成对定义、
  多端单位换算（px/rpx/pt-dp）、组件契约示例、从散值迁移的六步、可直接落地的令牌文件
- `references/motion-decision-table.md`：五类动效参数、不该有动效的六种情况、编排规则、
  降级表、模块映射模板、性能红线、记忆点动效的五个条件
- `references/anti-patterns.md`：12 条红线逐条（判定/损害/替代/例外）、AI 味 12 项组合识别、
  "想表达 → 别用 → 用"对照表
- `examples/design-rationale-demo.md`：工厂点检 App 首页完整示范（诊断 7 项 → 优先级 → 决策 →
  六段依据 → 七问自检 → 沉淀）

### 变更
- README 重写：定位从"提示词工程师"改为"会诊断、能解释、懂取舍"的设计总监
- 保留并接入既有工具链：`audit_contrast.py`（对比度）、`preflight.py`（硬伤）、`rag.py`（知识检索）
- 保留 v1.x 参数库（design-system-spec / dashboard-style / motion-spec 等）作为"数值层"支撑

## v1.3.0 — 2026-10-23

**新增：需求澄清与迭代闭环**

- `references/design-intake.md`：五步流程（Intake → Spec → Preview → Iterate → Capture）
  - 三问画像（画像/核心任务/场景）+ 七类行业默认推断表
  - 五段式方案卡（配色/布局/排版/动效/交互）+ 6 条方案自检
  - 3 屏预览交付（首屏/主流程/状态屏）与四项验证
  - 反馈四分类 → 参数动作映射（结构/视觉/密度/反馈），单轮只改一类，≤3 轮
  - 迭代记录模板与知识沉淀规则
- SKILL.md 新增 A-1 需求澄清、A9 预览确认与迭代；交付物增加需求卡/方案卡/迭代记录
- 触发词补充：需求澄清、UI 方案、效果预览、迭代优化

**知识库（配套技能 ui-taste-engine）**

- 新增批次分析 `analysis/2026-10-23-batch-26.md`：26 张截图（医疗/租车/后台/移动/文旅/大屏）
- 新增 8 张知识卡：P-002 渐变头尺寸、P-003 KPI 数量分级、M-002 图标宫格、M-003 文旅骨架、
  M-004 列表+地图分屏、M-005 sticky 结算卡、J-002 端+行业骨架选型、A-002 浅灰文字陷阱

## v1.2.0 — 2026-10-22

**新增：动效体系（库选型 + 参数 + 性能 + 验收）**

### 来源核实
- `curiositech/windags-skills · motion-design-web` ✅ 真实（**Apache-2.0**，非 MIT）；采纳其库选型决策树、四档时长、五档弹簧、五类翻车与 10 项质量门槛
- `bouclem/animate` ✅ 真实（SkillMD，7 star）；采纳其"禁 bounce/elastic"、三条缓动曲线、GPU 属性纪律、reduced-motion 片段
- `motiondivision/motion` ✅ 34.4k、`nandorojo/moti` ✅ 4.5k、`greensock/GSAP` ✅ 29.6k、`magicuidesign/magicui` ✅ 22.8k、`pmndrs/react-spring` ✅ 29.2k
- `aceternity/aceternity-ui`、`aceternity/ui` ❌ GitHub 404；实际分发方式为 shadcn registry（`ui.aceternity.com/registry/<组件>.json`，依赖 motion）
- `robb0wen/folex-fx` ❌ 不存在；纯 CSS 呼吸/涟漪改用本文内置配方

### 新增
- `references/motion-spec.md`：库选型决策树、时长与缓动、弹簧参数库、呼吸三档、编排（stagger/FLIP/手势）、性能红线与五大翻车、四端差异、集成示例、10 条验收
- `tests/test10-motion-lab.html`：纯 CSS 动效实验室（弹簧按压 + 涟漪、三档呼吸、交错入场、展开），含深色令牌，离线可运行
- SKILL.md 通用纪律扩充为 8 条动效硬规则；质量清单增加动效验收项

### 校准
- 明确"B 端低动效 / C 端柔和 / 小程序轻量"三档呼吸，替代此前笼统的 6-8s
- 明确退场 = 入场 ×0.75、子元素 40-80ms 交错（此前未量化）

## v1.1.0 — 2026-10-22

**新增：三层视觉与交互标准（可自动验收）**

### 可读性
- 新增 `scripts/audit_contrast.py`：解析浅色/深色两套令牌，计算全部「背景 × 文字」组合的 WCAG 对比度，含字面 CSS 规则扫描
- 新增令牌模板：浅色 `#F6F7FB / #FFFFFF / #F1F3F8` + `ink / ink-2 / ink-3`，深色 `#0E1116 / #151A22 / #1C222C`
- 硬规则：正文 4.5:1、大字与 UI 元素 3:1、禁同色系低差、渐变上文字需 scrim、徽章文字用 800 档

### 美观
- 明确 60-30-10 配色结构、强调色 3-5 处预算、1.25 字号比例、字重 ≤3 种
- 新增「一屏一个焦点」的眯眼测试判定法；区块间距与底色轮换规则

### 交互
- 新增按钮 8 态矩阵与点击成功动画时间轴（按下 → 加载 → 勾线 220ms → 还原，宽度锁定）
- 新增模块聚焦模式：聚焦 `scale(1.03)` + 展开，其余 `scale(.98)` + 透明度 .6，Esc 恢复，键盘可触发
- 呼吸感规则：一屏 ≤2 个、6-8s、只给 AI/实时/紧急元素；reduced-motion 全量降级

### 修复（审计发现的存量问题）
- test6/7/8 次要文字对比度仅 1.8-3.0:1 → 调深至 5.1:1 以上
- test3/4 品牌文字与价格色 3.6-4.1:1 → 调深至 5.0:1
- test7 头像首字在浅蓝底上 3.88:1 → 加深字色
- 现全部 8 个测试页 `audit_contrast.py` 0 违规，最低 4.68:1

### 新增文件
- `references/visual-interaction-spec.md`（三层规范 + 代码配方 + 验收清单）
- `scripts/audit_contrast.py`
- `tests/test9-interaction-lab.html`（浅深切换 / 模块聚焦 / 成功与失败反馈）

## v1.0.1 — 2026-10-22

**文档修订**

- 平台徽章用词：`手机网页` → `H5页面`，`应用` → `APP`
- 新增版权徽章「米乐」，页脚与 LICENSE 同步版权人
- 版本号按约定递增（文档修订 → 修订号 +1）

## v1.0.0 — 2026-10-22

**首个正式发布版本**

### 三种入口模式

- 模式 A · 需求 → UI：八步流水线（旋钮 → 独有素材盘点 → 主张先行 → 三方向 → DESIGN.md → 两遍法 → 生成 → 验收）
- 模式 B · 参考图/目标站 → 复刻：浏览器路径（getComputedStyle + 像素比对）与截图路径（5 行式解剖 + 目测取样）
- 模式 C · 已开发界面 → 美化：五类病诊断 + 定向修复句式库，最小改动

### 四类页面 × 四端平台

- 页面类型路由：营销页 / 数据工作台 / 创作工作台 / 服务型工作台
- 平台矩阵：电脑端、手机网页（H5）、微信小程序、应用（APP）
- 移动端原生化七项：粘滞 hover、点击高亮、100vh 陷阱、输入缩放、点击延迟、安全区、滚动链

### 规范体系（15 份参考文件）

- 主规范：八要素分析框架 + 九段式提示词框架 + "视觉意图 → 技术参数"对照表 + 四个设计旋钮
- 反 AI 脸：5 类 AI 视觉套路、8 条排版禁忌、结构即信息、动效默认病
- 风格库：6 种风格模板 + 11 个具名动效配方
- 交付闸门：10 项验收条 + 三轴评分卡 + 最坏数据测试
- 灵感资源库：10 类资源（含 2026 状态变更）
- 持续迭代方法：六步闭环 + 三库建设 + 30 天计划

### 工程能力

- `scripts/preflight.py`：7 类硬伤扫描，0 ERROR 才可交付
- `scripts/rag.py`：UI 知识库检索（RAG），让生成有据可依
- `tests/`：8 个实测页，覆盖营销页、工作台、H5、服务型四类

### 文档

- 中文界面：全部文案与徽章中文化
- 新手路径：三分钟上手、六句示例话术、小白话术对照表、常见问题
- 版本体系：本文件 + README 版本徽章 + SKILL.md 的 `version` 字段三处一致
