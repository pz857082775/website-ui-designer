# website-ui-designer

> 让 AI 生成"不像 AI 生成"的网站 UI。一个 Skill，融合 5 个开源项目的精华。

[English](#english) · 中文

## 它解决什么问题

让大模型直接写页面，产出的是"所有页面的平均值"：居中大标题 + 小标签 + 图标卡片 + 柔和渐变。没有错，也没有任何**决定**。
本技能把 UI 生成拆成一条有纪律的流水线，每一步都在逼出"决定"。

## 工作流（七步）

1. **读需求** — 提取产品/受众/唯一目标/既有品牌，并盘点 8-12 条"只属于这个客户"的素材（名字的含义、街道、数字、约束、材料、仪式）。创意从这里长出来，不从"科技感"这类类别概念来。
2. **先写论证** — 页面 = 主张 + 证据，一行一区块。没有主张的区块删掉。这一步消灭"hero→logo墙→三特性→评价→定价→CTA"库存序列。
3. **三个方向选一个** — 同时给 3 个版式/字体/配色完全不同的方向，各自说明承载哪条独有素材。不指定方向，AI 必选类别默认值。
4. **设计系统先行** — 产出 DESIGN.md：YAML 精确令牌 + Markdown 设计理由，WCAG AA 对比度自检。
5. **七段式主提示词** — 角色 / 风格锚定 / 设计令牌 / 页面结构 / 排版硬规则 / GSAP 动效脚本 / 输出要求。
6. **生成** — 单文件 HTML，内联 CSS/JS，GSAP CDN + CSS 降级兜底，375/768/1440 三档响应式。
7. **自检修复循环** — 过质量清单 → 修最严重的 3 个问题 → 再查一轮（最多 3 轮）。核心警告：只删装饰不补实质 = 单薄页面；删卡片的同时必须补更大的字号、整片色彩、真实图片、完整内容。

## 目录

```
website-ui-designer/
├── SKILL.md                        # 技能主文件（七步工作流 + 质量清单）
└── references/
    ├── style-library.md            # 6 种风格的专业提示词模板（填空即用）
    ├── design-md-template.md       # DESIGN.md 设计系统模板（Google 规范）
    ├── prompt-master.md            # 七段式主提示词 + 三方向选型模板
    ├── gsap-prompts.md             # GSAP 动效提示词库（8 类场景 + 翻车点自查表）
    └── anti-slop.md                # 反 AI 脸清单（默认病黑名单）
```

## 风格库

| 风格 | 气质 | 适用 |
|---|---|---|
| 极简留白 Modern Minimalism | 干净有重点 | SaaS、作品集 |
| 莫兰迪柔和 Soft Muted | 越看越舒服 | 生活方式、教育 |
| 玻璃美学 Glassmorphism | 通透有呼吸 | 科技/AI 产品 |
| 极简 3D 空间 Minimal 3D | 产品像展品 | 硬件、金融 |
| 暗色杂志 Dark Editorial | 克制的黑，放大的字 | 创意机构、开发者品牌 |
| 柔和新粗野 Soft Neo-Brutalism | 有个性的清爽 | 创意工具、活动页 |

## 方法论来源（均为真实开源项目）

| 项目 | 贡献 |
|---|---|
| [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) | 反 slop 体系：247 站点研究、独有素材盘点、主张先行、真实浏览器自检 |
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 设计智能：设计系统先行、色板/字体组合、可访问性与反模式校验 |
| [google-labs-code/design.md](https://github.com/google-labs-code/design.md) | DESIGN.md 设计令牌规范（YAML tokens + Markdown） |
| [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) | 提示词增强方法论 |
| [greensock/gsap-skills](https://github.com/greensock/gsap-skills) | GSAP 3 官方规范：registerPlugin、transform-only、清理、reduced-motion |

## 测试样例

`tests/` 下三个单文件成品页（本流水线的真实产出）：

- `test1-lumen-minimal.html` — 极简留白 · Markdown 编辑器官网
- `test2-nebula-glass.html` — 玻璃美学 · AI 知识库产品
- `test3-banmu-morandi.html` — 莫兰迪柔和 · 咖啡品牌页（含"每月一烘"独有约束驱动的创意）

## 安装

```bash
npx skills add <你的仓库地址> --skill website-ui-designer
```

或直接拷贝本目录到你的 agent skills 目录（`~/.workbuddy/skills/`、`~/.claude/skills/` 等）。

## License

MIT

---

<a id="english"></a>
**English:** A skill that makes AI-generated websites look *designed*, not generated. Seven-step pipeline: brief & unique-asset inventory → claims-first structure → three distinct art directions → DESIGN.md token system → seven-part master prompt → single-file HTML with GSAP → self-review fix loop. Synthesized from taste-skill, ui-ux-pro-max, Google design.md, and greensock/gsap-skills.
