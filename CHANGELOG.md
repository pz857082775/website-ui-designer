# 版本记录

语义化版本：`MAJOR.MINOR.PATCH`
- **MAJOR**：结构或方法论重写（如新增主规范、入口模式变更）
- **MINOR**：新增能力、新增参考文件、新增实测页
- **PATCH**：修复 bug、文档优化、参数微调

---

## v5.2.0 — 2026-10-22

**文档与版本体系**

- README 重构：版本徽章、三分钟上手、四种用法、小白话术对照表、常见问题
- 建立版本号体系（此前只有 git 提交，无可读版本）
- 新增本 CHANGELOG
- SKILL.md 增加 `version` 与 `updated` 字段，便于判断当前装的哪一版

## v5.1.0 — 2026-10-22

**灵感资源库与学习方法**

- 新增 `references/inspiration-sources.md`：10 类资源（视觉方向 / 落地页 / 真实产品界面 / 组件 / 排版 / 色彩 / 动效 / 设计系统 / 中文 / 深读），含 2026 状态变更（Godly → recent.design，Design Vault → screensdesign.dev）
- 新增 `references/learning-loop.md`：六步闭环（收集 → 拆解 → 参数化 → 生成 → 校验 → 沉淀）、三库建设、A/B 四步法、30 天计划
- 新增配套技能 `ui-taste-engine` 的交叉引用

## v5.0.0 — 2026-10-22

**整合 9 个开源技能的规范**

- 新增 `references/open-source-integration.md`：9 个项目映射 + 12 条新规则 + 四端差异 + 冲突裁决
- 新增 `references/review-rubric.md`：10 项验收条 + 三轴评分卡（Nielsen × 6 法则 × 业务影响标签）+ 最坏数据清单
- `anti-slop.md` 增补：5 类 AI 视觉集群、8 条排版禁忌、结构即信息、动效默认病
- `platform-matrix.md` 增补：移动端原生化七项（粘滞 hover / 点击高亮 / 100vh / 输入缩放 / 点击延迟 / 安全区 / 滚动链）
- `style-library.md` 增补：11 个具名动效配方（number ticker / bento grid / border beam 等）
- SKILL.md 重构为 A0 旋钮 → A8 验收

## v4.1.0 — 2026-10-22

**修复致命 bug + 自动化校验**

- 修复：CSS 预隐藏 `.anim{opacity:0}` 在 GSAP CDN 不可达时导致**整页空白**。改为"内容默认可见 + gsap.from 设初始态"
- 新增 `scripts/preflight.py`：7 类硬伤扫描（预隐藏 / reduced-motion / viewport / 图表库 / emoji / 等宽数字 / 布局属性动画 / 滚动劫持）
- 全部 10 个页面（8 个 tests + 3 个旧样例）通过检测：0 error 0 warning
- 规范同步：`gsap-prompts.md` 增「正确兜底模式」代码对照

## v4.0.0 — 2026-10-22

**主规范与服务型工作台**

- 新增 `references/design-system-spec.md`：八要素分析框架 + 九段式提示词框架 + "视觉意图 → 技术参数"对照表 + 四个设计旋钮
- 新增服务型工作台路线（医疗/教育/客服）：Hero 问候横幅、时间轴列表、主从双栏
- 新增 `tests/test8-medical-workbench-home.html`
- 页面类型路由扩展为四类

## v3.2.0 — 2026-10-22

**创作工作台模式**

- `dashboard-style.md` 增第八至十节：问候页头、今日待办卡（首页 C 位）、迷你 KPI + sparkline、快捷入口渐变卡、对标列表、AI 报告文档页、素材库、发布日历、AI 复盘三段式
- 新增 `tests/test7-workbuddy-creator-home.html`
- 明确趋势色约定：金融红涨 / 通用绿涨，全站只能一种

## v3.1.0 — 2026-10-22

**数据工作台模式**

- 新增 `references/dashboard-style.md`：布局骨架、KPI 卡解剖、色彩系统、组件规范、完整提示词模板、自检清单
- 新增 `tests/test6-yunshang-dashboard.html`
- SKILL.md 增加「页面类型路由」：营销页 vs 工作台

## v3.0.0 — 2026-10-21

**三入口模式**

- 重构为三模式：A 需求 → UI、B 参考图/目标站 → 复刻、C 已开发界面 → 美化
- 新增 `references/prompt-anatomy.md`：从 4 张获奖参考图提炼的 5 行式提示词解剖（含原图 prompt 存档）
- 新增 `references/clone-mode.md`、`references/redesign-mode.md`、`references/platform-matrix.md`
- 新增 `tests/test4-banmu-h5.html`、`tests/test5-clone-prompt-glass.md`

## v2.0.0 — 2026-10-21

**首个可用版本**

- 七步流水线：独有素材盘点 → 主张先行 → 三方向选型 → DESIGN.md → 七段式提示词 → 生成 → 自检修复
- 6 种风格提示词库（极简留白 / 莫兰迪柔和 / 玻璃美学 / 极简 3D / 暗色杂志 / 柔和新粗野）
- DESIGN.md 设计令牌模板（Google 规范）
- GSAP 动效提示词库 + 反 slop 清单
- 首批 3 个实测页（test1–test3）
