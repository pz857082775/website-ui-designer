# website-ui-designer

**让 AI 生成的界面，不再长得像 AI 生成的。**

![版本](https://img.shields.io/badge/%E7%89%88%E6%9C%AC-1.0.0-2E7CF6?style=flat-square)
![许可](https://img.shields.io/badge/%E8%AE%B8%E5%8F%AF-%E5%BC%80%E6%BA%90-34A853?style=flat-square)
![平台](https://img.shields.io/badge/%E5%B9%B3%E5%8F%B0-%E7%94%B5%E8%84%91%E7%AB%AF%20%C2%B7%20%E6%89%8B%E6%9C%BA%E7%BD%91%E9%A1%B5%20%C2%B7%20%E5%B0%8F%E7%A8%8B%E5%BA%8F%20%C2%B7%20%E5%BA%94%E7%94%A8-8A90A2?style=flat-square)
![语言](https://img.shields.io/badge/%E8%AF%AD%E8%A8%80-%E4%B8%AD%E6%96%87-FF9A3D?style=flat-square)

> 一个"UI 提示词工程师"技能。它不直接画图，而是把你的需求翻译成 AI 能严格执行的设计指令——包含版式、配色、字号、间距、动效，全部是精确数值。
>
> **你不需要懂设计，也能让它做出好看的界面。**

[快速上手](#三分钟上手) · [四种用法](#四种用法) · [版本历史](#版本历史)

---

## 它解决什么问题

让大模型直接写页面，产出的是"所有页面的平均值"：居中大标题 + 上方小标签 + 一行图标卡片 + 柔和渐变。
一处都不算错，但没有一处是**决定**过的。

本技能做三件事：

| 能力 | 说明 |
|---|---|
| **写提示词** | 把"高级一点""干净一点"翻译成精确参数：字号 28/16/13.5、留白 96px、强调色出现 4 次 |
| **给方向** | 一次给 3 个完全不同的设计方向，你挑一个，而不是被动接受第一个结果 |
| **做验收** | 交付前自动检查 10 项硬指标（对比度、字号跨度、状态齐全、无 emoji 图标……） |

---

## 三分钟上手

### 第 1 步 · 安装（30 秒）

```bash
# 方式一：用 skills CLI
npx skills add https://github.com/pz857082775/website-ui-designer --skill website-ui-designer

# 方式二：直接拷贝目录到你的 Agent 技能目录
#   WorkBuddy: ~/.workbuddy/skills/
#   Claude Code: ~/.claude/skills/
```

### 第 2 步 · 说一句话（重点：不用懂术语）

装好之后，直接对它说人话就行。它会被这些说法自动触发：

| 你想做的事 | 你可以直接这么说 |
|---|---|
| 从零做一个页面 | "帮我做一个卖手冲咖啡的品牌官网，要干净一点" |
| 参考别人的页面 | "照这张截图的感觉做一个定价页"（附图） |
| 觉得自己页面丑 | "我这个后台看着很土，帮我看看哪里有问题" |
| 只要提示词 | "给我一段能生成 dashboard 的提示词，我要喂给别的 AI" |
| 出多套方案 | "给我 3 个不同风格的方向，我先看看再定" |
| 改一个细节 | "这个页面太挤了，帮我松一点，其他别动" |

> **不知道要什么风格？** 就说"你定，我不懂设计"。它会先给你 3 个方向 + 每个方向的一句话理由，由你挑。

### 第 3 步 · 拿结果（并知道怎么继续）

一次完整任务，你会拿到三样东西：

```
DESIGN.md      设计系统：颜色 / 字号 / 圆角 / 间距的精确值
主提示词.md     可复用的提示词（想换模型生成时直接粘）
index.html     成品页面（双击就能看，含动效）
```

不满意时，不用重新描述一遍。按这四种说法提要求最有效：

```
"整体太挤了"        → 它调密度旋钮 + 内边距 + 行高
"颜色有点土"        → 它降低饱和度、收敛色相家族
"看不出重点"        → 它拉开字号跨度、减少强调色数量
"太像 AI 做的"      → 它逐条排查 5 类 AI 视觉套路并替换
```

---

## 四种用法（按你的处境选）

| 你的处境 | 输入 | 它会做什么 | 详细规则 |
|---|---|---|---|
| **A · 从需求做** | 需求文档 / 一句话想法 | 盘点独有素材 → 定主张 → 3 方向 → 设计系统 → 提示词 → 生成 → 验收 | `SKILL.md` 模式 A |
| **B · 照着做** | 截图 / 参考网站 | 5 行式风格解剖 + 取样色值字体 → 复刻提示词；有浏览器时用 getComputedStyle 取真值 + 像素比对 | `references/clone-mode.md` |
| **C · 改现有的** | 已开发页面的截图 | 五类病诊断（配色/间距/层级/动效/组件）+ 逐类定向修复，最小改动 | `references/redesign-mode.md` |
| **D · 只要提示词** | 一句话描述 | 直接产出可复制的提示词，不生成代码 | `references/prompt-master.md` |

**页面类型也要先分清**，因为两种页面的"好看"标准相反：

| 类型 | 卖什么 | 提示词语言 |
|---|---|---|
| 营销页（官网 / 落地页） | 卖感受 | 5 行式风格提示词 + 大标题 + 留白 |
| 数据工作台（后台 / 仪表盘） | 卖效率 | KPI 卡 / 表格 / 图表规范 + 高密度 |
| 创作工作台（内容平台） | 卖流程 | 待办卡放首位 + 素材库 + 发布日历 |
| 服务型工作台（医疗 / 教育） | 卖信任 | 问候横幅 + 时间轴 + 主从双栏 |

---

## 小白话术对照表

你说的话，它实际做了什么（这就是"专业提示词"的价值）：

| 你说 | 它翻译成 |
|---|---|
| "高级感" | 低饱和配色 + 大留白 120px + 衬线标题 + 字距 -0.02em + 强调色只留 1 个 |
| "干净一点" | 密度降到 3、圆角收敛到 3 种、去掉渐变、分隔线最多 2 条 |
| "太挤了" | 卡内边距 20→28、列表行高 +8px、区块间距 +30% |
| "字看不清" | 正文 ≥15px（移动 ≥16px）、对比度提到 4.5:1、次要文字提亮一档 |
| "太像 AI 做的" | 排查 5 类 AI 套路：暖奶油+陶土、近黑+荧光、报纸风、SaaS 卡片套装、模板外壳 |
| "要有科技感" | 深色底 + 冷色主色 + 1px 发丝线 + 仅 1 处发光（不是满屏玻璃） |

---

## 知识检索：让提示词有据可依

模型写提示词最容易犯的错是"凭印象给参数"。本技能自带一个本地检索引擎，生成前先查库：

| 项目 | 说明 |
|---|---|
| **输入** | 一句自然语言（用户原话即可）+ 可选过滤：平台、条款类型、返回条数 |
| **检索范围** | 15 份规范文件（217 个片段）+ 配套知识库的四类知识卡；不含测试页与说明文档 |
| **输出** | 三段式注入块：**必须遵守**（知识卡）/ **明确禁止**（反例）/ **参考依据**（规范片段）+ 边界声明 |

```bash
python scripts/rag.py index                              # 首次或内容变更后建索引
python scripts/rag.py query "后台首页 KPI 卡怎么排" --top 5
python scripts/rag.py query "页面太挤了" --platform h5
python scripts/rag.py query "入场动画" --type A --format prompt   # 直接注入提示词
```

**防随意发挥三道闸**：
1. 最高分低于阈值 → 注入块自动改成"以下为推断，不得当作规范"
2. 完全无命中 → 明确告知"无依据"，不编造条款
3. 每条结论都带 ID 与来源文件，可回溯

详细规则见 [`references/rag-retrieval.md`](./references/rag-retrieval.md)。

---

## 核心规则速览

**四个旋钮**（写在提示词最前面，决定"做到什么程度算完成"）

```
CRAFT_LEVEL      = 7    精修深度    3 快出 · 9 像素级
MOTION_INTENSITY = 5    动效强度    1 只 hover · 10 滚动叙事
VISUAL_DENSITY   = 5    信息密度    1 编辑式留白 · 10 仪表盘密集
DESIGN_VARIANCE  = 7    版式胆量    1 对称安全 · 10 实验构图
```

**10 项验收条**（任一不过 = 不算完成）

```
1 层级  3 秒能看出主信息        6 字体  1 正文族（可选 1 展示族）
2 令牌  全部来自令牌，无 magic  7 动效  出场 ≈75% 入场时长
3 配色  90% 中性 + 1 强调色     8 状态  hover/focus/active/disabled/empty/error
4 圆角  分级 6/10/14/20         9 无障碍 对比 4.5:1 + 键盘可达 + reduced-motion
5 阴影  环境光 + 直射光双层    10 独特  有一个签名细节
```

---

## 目录结构

```
website-ui-designer/
├── SKILL.md                        # 技能主文件：三模式 + 页面路由 + 通用纪律
├── README.md                       # 本文件
├── CHANGELOG.md                    # 版本记录
├── LICENSE                         # MIT
├── references/                     # 15 份规范，按需查
│   ├── design-system-spec.md       # 主规范：八要素 + 九段提示词 + 意图→参数 + 旋钮
│   ├── review-rubric.md            # 交付闸门：10 项验收条 + 评分卡 + 最坏数据
│   ├── anti-slop.md                # 反 AI 脸：5 类套路 + 8 条排版禁忌
│   ├── prompt-anatomy.md           # 5 行式风格提示词解剖（含原图 prompt 存档）
│   ├── style-library.md            # 6 种风格模板 + 11 个具名动效配方
│   ├── prompt-master.md            # 九段式主提示词 + 两遍法
│   ├── dashboard-style.md          # 数据/创作/服务型工作台规范
│   ├── clone-mode.md               # 复刻：浏览器 / 截图 / 设计系统三路径
│   ├── redesign-mode.md            # 审计 + 五类病修复句式库
│   ├── platform-matrix.md          # 四端差异 + 移动端原生化七项
│   ├── inspiration-sources.md      # 灵感资源库（10 类，含 2026 状态）
│   ├── learning-loop.md            # 持续提升方法：六步闭环 + 三库
│   ├── rag-retrieval.md            # 知识检索：输入 / 检索范围 / 输出 / 防编造
│   ├── design-md-template.md       # DESIGN.md 令牌模板
│   └── open-source-integration.md  # 开源方法论映射 + 12 条新规则
├── scripts/
│   ├── preflight.py                # 交付前自检（7 类硬伤，0 ERROR 才交付）
│   └── rag.py                      # 知识检索：生成前查依据，避免随意发挥
└── tests/                          # 8 个实测页
    ├── test1-lumen-minimal.html         极简留白 · 编辑器官网
    ├── test2-nebula-glass.html          玻璃美学 · AI 工具
    ├── test3-banmu-morandi.html         莫兰迪柔和 · 咖啡品牌
    ├── test4-banmu-h5.html              H5 · 吸底栏 + 安全区
    ├── test5-clone-prompt-glass.md      复刻提示词样例
    ├── test6-yunshang-dashboard.html    数据工作台 · 经营总览
    ├── test7-workbuddy-creator-home.html 创作工作台 · 自媒体首页
    └── test8-medical-workbench-home.html 服务型工作台 · 医疗首页
```

---

## 版本历史

当前版本 **v1.0.0**（2026-10-22），首个正式发布版本。完整记录见 [CHANGELOG.md](./CHANGELOG.md)。

| 版本 | 日期 | 说明 |
|---|---|---|
| **v1.0.0** | 2026-10-22 | 首个正式版：三入口模式、四类页面、四端平台、知识检索、自检与验收体系 |

**版本约定**：修订号（1.0.x）修 bug 与文档；次版本号（1.x.0）加能力；主版本号（2.0.0）仅在不兼容变更时使用。


## 常见问题

**我不懂设计，能用吗？**
能。你只需要说清"给谁做、做什么、想要什么感觉"，风格、配色、字体、间距由技能决定；它会给 3 个方向让你挑。

**生成的效果不满意怎么办？**
不要重新描述全部需求。用四种精准抱怨法："太挤了 / 颜色土 / 看不出重点 / 太像 AI 做的"，每一种都对应明确的修复动作。

**需要什么技术栈？**
不需要。默认产出单文件 HTML（双击可看）。要 React / Vue / 小程序代码时，直接说"给我 React 版本"或"给我小程序 rpx 版本"。

**支持手机端吗？**
支持 PC、H5、微信小程序、APP 四端。四端的差异（热区、安全区、rpx、导航模式）已写进 `platform-matrix.md`。

**它会不会只是套模板？**
不会。每次任务都要求先盘点"只属于这个客户的素材"（名字含义、街道、数字、约束），创意从这些素材里长出来，而不是从"科技感"这类通用概念。

**它会不会凭印象编设计参数？**
不会。生成前会先跑知识检索（`rag.py`），把库里的依据以"必须遵守 / 明确禁止"的形式注入提示词；查不到依据时会明确标注为推断。

**preflight.py 是干什么的？**
交付前的自动体检，扫 7 类硬伤：内容被预隐藏（会导致空白页）、缺 reduced-motion、引用第三方图表库、emoji 图标、缺等宽数字、动画动布局属性、滚动劫持。0 ERROR 才算可交付。

---

## 方法论来源

均为真实开源项目（2026-10 核实）：

| 项目 | 贡献 |
|---|---|
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | 反 slop：独有素材盘点、主张先行、3 方向、截图修复循环 |
| [anthropics/skills · frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) | 5 类 AI 视觉套路、8 条排版禁忌、结构即信息、两遍法 |
| [emilkowalski/skills](https://github.com/emilkowalski/skills) | 缓动选择、出场快于入场、移动端原生化七项、最坏数据测试 |
| [educlopez/ui-craft](https://github.com/educlopez/ui-craft) | 四个旋钮、Top-12 工艺规则、10 项验收条、评分卡 |
| [Owl-Listener/designer-skills](https://github.com/Owl-Listener/designer-skills) | 优先级修复清单、token 分层、认知法则 |
| [magicuidesign/magicui](https://github.com/magicuidesign/magicui) | 具名动效组件词汇 |
| [greensock/gsap-skills](https://github.com/greensock/gsap-skills) | GSAP 3 官方规范 |
| [google-labs-code/design.md](https://github.com/google-labs-code/design.md) | DESIGN.md 令牌规范 |
| [JCodesMore/ai-website-cloner-template](https://github.com/JCodesMore/ai-website-cloner-template) | 复刻四步：Map → Observe → Build → Compare |

配套技能：[ui-taste-engine](https://github.com/pz857082775/ui-taste-engine) —— 负责积累经验、让规则按证据自我晋升。

---

## License

MIT

---
