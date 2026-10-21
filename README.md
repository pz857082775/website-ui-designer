# website-ui-designer

> 专业 UI 提示词工程师：让 AI 生成"不像 AI 生成"的界面。三种入口模式 × 四端平台（PC/H5/小程序/APP）。

[English](#english) · 中文

## 它解决什么问题

让大模型直接写页面，产出的是"所有页面的平均值"：居中大标题 + 小标签 + 图标卡片 + 柔和渐变。没有错，也没有任何**决定**。
本技能的产品是**提示词**——把 UI 需求翻译成大模型能执行的指令。三种入口，一套底层纪律。

## 三种入口模式

| 模式 | 输入 | 产出 |
|---|---|---|
| **A · 需求 → UI** | 开发需求文档/一句话想法 | 七步流水线：独有素材盘点 → 主张先行 → 三方向选型 → DESIGN.md → 七段式提示词 → 单文件 HTML → 自检修复 |
| **B · 参考图/目标站 → 复刻** | 截图、参考网站、竞品页面 | 5 行式风格解剖 + token 取样表 + 复刻提示词；有浏览器时走 getComputedStyle + 像素 Diff 迭代 |
| **C · 已开发界面 → 美化** | 线上/本地页面截图 | 五类病诊断（配色/间距/层级/动效/组件）+ 定向修复句式库，最小改动 |

## 七步流水线（模式 A）

1. **读需求** — 盘点 8-12 条"只属于这个客户"的素材（名字含义、街道、数字、约束、材料、仪式）。创意从这里长出来
2. **先写论证** — 页面 = 主张 + 证据，无主张的区块删掉
3. **三个方向选一个** — 3 个版式/字体/配色完全不同的方向各配一句理由
4. **设计系统先行** — DESIGN.md：YAML 精确令牌 + 设计理由，WCAG AA 自检
5. **组装提示词** — 5 行式风格段 + 令牌 + 结构 + 排版硬规则 + 平台段 + GSAP 动效
6. **生成** — 单文件 HTML，GSAP CDN + CSS 兜底，375/768/1440 三档
7. **自检修复** — 质量清单 → 修 top 3 → 再查一轮（≤3 轮）。警告：只删装饰不补实质 = 单薄页面

## 目录

```
website-ui-designer/
├── SKILL.md                        # 技能主文件（三模式 + 通用纪律）
├── README.md
├── LICENSE                         # MIT
├── references/
│   ├── prompt-anatomy.md           # 参考图 5 行式提示词解剖（含 4 张原图 prompt 存档）
│   ├── style-library.md            # 6+ 风格提示词模板（填空即用）
│   ├── design-md-template.md       # DESIGN.md 设计系统模板（Google 规范）
│   ├── prompt-master.md            # 七段式主提示词 + 三方向选型模板
│   ├── gsap-prompts.md             # GSAP 动效提示词库（8 场景 + 翻车点自查表）
│   ├── anti-slop.md                # 反 AI 脸清单（默认病黑名单）
│   ├── clone-mode.md               # 模式 B：复刻完整流程（浏览器/截图/设计系统三路径）
│   ├── redesign-mode.md            # 模式 C：审计 + 定向修复句式库
│   └── platform-matrix.md          # PC/H5/小程序/APP 四端提示词差异
└── tests/
    ├── test1-lumen-minimal.html    # 模式A · 极简留白 · 编辑器官网
    ├── test2-nebula-glass.html     # 模式A · 玻璃美学 · AI 知识库
    ├── test3-banmu-morandi.html    # 模式A · 莫兰迪柔和 · 咖啡品牌页
    ├── test4-banmu-h5.html         # 模式A · H5 移动端 · 吸底操作栏 + 安全区
    └── test5-clone-prompt-glass.md # 模式B · 复刻提示词真实样例
```

## 风格库

极简留白 / 莫兰迪柔和 / 玻璃美学 / 极简 3D 空间 / 暗色杂志 / 柔和新粗野（+ 组合建议）

## 平台矩阵

| 维度 | PC | H5 | 小程序 | APP |
|---|---|---|---|---|
| 布局 | 12 列网格 | 单列 | 单列 rpx | 单列 + 平台导航 |
| 热区 | 32px+ | 44px+ | 44px+ | 44pt+ |
| 动效 | 可 scrub 叙事 | ≤0.4s 轻 | 原生为主 | 跟手手势 |
| 暗色 | 建议 | 建议 | 建议 | 必须 |

## 方法论来源（均为真实开源项目）

| 项目 | 贡献 |
|---|---|
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | 反 slop 体系：247 站点研究、独有素材盘点、主张先行 |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 设计系统先行、色板/字体组合、可访问性校验 |
| [JCodesMore/ai-website-cloner-template](https://github.com/JCodesMore/ai-website-cloner-template) | 复刻四步：Map → Observe → Build → Compare；getComputedStyle + 像素 Diff |
| [google-labs-code/design.md](https://github.com/google-labs-code/design.md) | DESIGN.md 设计令牌规范 |
| [greensock/gsap-skills](https://github.com/greensock/gsap-skills) | GSAP 3 官方规范 |

## 安装

```bash
npx skills add https://github.com/pz857082775/website-ui-designer --skill website-ui-designer
```

或拷贝目录到 agent 的 skills 目录（`~/.workbuddy/skills/`、`~/.claude/skills/` 等）。

## License

MIT

---

<a id="english"></a>
**English:** A skill whose product is *prompts* — it turns UI requirements into instructions LLMs can execute. Three entry modes: (A) requirements doc → designed UI via a 7-step anti-slop pipeline; (B) reference screenshot/site → pixel-faithful clone prompts (getComputedStyle tokens + pixel-diff loop when a browser is available); (C) existing built UI → audit + minimal targeted fixes. Outputs DESIGN.md token systems, 5-line style prompts distilled from award-winning reference images, GSAP motion specs, and platform-specific guidance for PC web, H5, WeChat mini-programs, and apps.
