# 主提示词模板 — 喂给 AI 大模型生成 UI 的完整提示词

七段式结构。使用时：删掉 `{说明}`，按需求填写，整段投喂给生成模型（WorkBuddy / Claude / Gemini 等）。
第 2 段（风格）与第 3 段（令牌）按工作流第 3、4 步的结论填入。

---

```
## 1. 角色
你是一位同时精通艺术指导与前端开发的资深设计师。你的作品以
Awwwards 水准为标准：克制、有层级、每个像素都有理由。
你已通读反 slop 规则，不会产出"AI 平均脸"页面。

## 2. 风格（完整粘贴 style-library.md 中选定方向的提示词）
{粘贴选定的风格提示词，含精确色值}

## 3. 设计令牌（粘贴 DESIGN.md 的 YAML 部分）
{精确的颜色/字体/圆角/间距/组件令牌}

## 4. 页面结构（按"主张+证据"排序，一行一区块，无主张区块已删）
- 导航：{logo、链接、CTA}
- Hero：{一句话价值主张 + 主按钮 + 主视觉（真实图/产品图/可运行界面）}
- {主张 2 区块}：{证据/内容}
- {主张 3 区块}：{证据/内容}
- CTA 区：{行动号召 + 按钮}
- 页脚：{链接分组 + 版权}

## 5. 排版硬规则
- 标题字号跨度 ≥ 3 倍（如 88px / 40px / 16px），标题敢大
- 区块留白 ≥ 96px，内容最大宽 1200px，8pt 网格对齐，等宽边距
- 一种强调色，只用于主按钮；正文字色对比度 ≥ 4.5:1
- 最多 2 种字体家族；图标用 SVG 线性图标，不用 emoji
- 主视觉必须是真实图片/产品渲染/可运行界面，禁止灰块占位

## 6. 动效脚本（GSAP 3，CDN: https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js）
- 首屏入场：Hero 元素按"标题→副文案→按钮→视觉"顺序 stagger 入场
  （y: 40 → 0, autoAlpha: 0 → 1, duration: 0.8, ease: "power3.out", stagger: 0.1）
- 滚动揭示：区块内容进入视口时向上浮现（ScrollTrigger, toggleActions: "play none none none"）
- 数据区：数字 count-up（ScrollTrigger once: true）
- 硬规则：只动 transform/opacity；禁止 scroll-jacking；必须包含
  prefers-reduced-motion 降级；GSAP 加载失败时页面靠 CSS 动画/静态呈现依然完整可读

## 7. 输出要求
- 单文件 index.html：内联 CSS 与 JS，GSAP 走 CDN，双击即可打开
- 响应式：375px / 768px / 1440px 三档可用
- 附 3 行以内实现说明（风格、动效、关键决策）
- 不确定的 API 必须标出来，禁止编造
```

---

## 提示词质量自检（GSAP 部分尤其重要，来自 greensock/gsap-skills 与社区经验）

| 检查项 | 为什么 |
|---|---|
| 明确写 "GSAP 3.x"，点名禁止 TweenMax/TimelineMax/.staggerTo() | AI 高频回退到 2019 年的 GSAP 2 语法 |
| 要求 `gsap.registerPlugin(ScrollTrigger)` | 漏注册是 AI 生成代码最常见静默失败 |
| React 场景要求 useGSAP/gsap.context() 清理 | 不清理会在路由切换后泄漏动画 |
| 每条动效写清：目的、时长（0.2-0.6s UI 动效）、缓动意图 | "加个动画" 只会得到一个敷衍的 fade |
| 强调 prefers-reduced-motion | 无障碍硬要求，AI 默认不给 |
| 只动 transform/opacity（x/y/scale/rotation/autoAlpha） | 动 left/top/width 会引发布局抖动 |

## 常用 GSAP 快速配方
```
# 卡片 stagger 入场
gsap.from(".card", { y: 40, autoAlpha: 0, duration: 0.6, ease: "power3.out", stagger: 0.1 });

# 数字滚动
gsap.from(".stat-number", { textContent: 0, duration: 1.5, snap: { textContent: 1 },
  scrollTrigger: { trigger: ".stats", start: "top 80%", once: true } });

# 滚动钉住叙事
ScrollTrigger.create({ trigger: ".story", start: "top top", end: "+=200%",
  pin: true, scrub: 1 });

# 降级守卫
const rm = matchMedia("(prefers-reduced-motion: reduce)").matches;
if (rm) gsap.globalTimeline.timeScale(1000); // 或直接跳过动画注册
```

## 三方向选型模板（工作流第 3 步用）

对同一需求，同时产出 3 个方向，每个按此格式：

```
【方向 A · {风格名}】气质：{三个关键词}
构图：{版式描述}  字体：{字体+字号跨度}  色彩：{主色/背景/强调色}
承载的独有素材：{第 1 步清单里的哪一条}
一句话理由：{为什么这个方向适合这个客户}
```

选型标准：不是选最熟悉的，是选**最能承载客户独有素材**的那个。
