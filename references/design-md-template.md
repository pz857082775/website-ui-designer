# DESIGN.md 模板（基于 Google google-labs-code/design.md 规范）

一份 DESIGN.md = YAML 设计令牌（精确值）+ Markdown 设计理由（怎么用、为什么）。
生成后建议校验：`npx @google/design.md lint DESIGN.md`（检查断链引用与 WCAG 对比度）。

章节顺序（可省略，不可乱序）：Overview → Colors → Typography → Layout → Elevation & Depth → Shapes → Components → Do's and Don'ts

---

```markdown
---
version: alpha
name: {项目名}
description: {一句话气质描述}
colors:
  primary: "#1A1C1E"        # 标题与核心文字
  secondary: "#6C7278"      # 次级文字、说明、边框
  accent: "#B8422E"         # 唯一交互强调色
  neutral: "#F7F5F2"        # 背景
  surface: "#FFFFFF"        # 卡片面
typography:
  h1:
    fontFamily: {字体}
    fontSize: 4rem
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "-0.02em"
  body-md:
    fontFamily: {字体}
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.6
  label-caps:
    fontFamily: {字体}
    fontSize: 0.75rem
    letterSpacing: "0.08em"
rounded:
  sm: 8px
  md: 16px
  lg: 24px
spacing:
  xs: 8px
  sm: 16px
  md: 24px
  lg: 48px
  xl: 120px
components:
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "#FFFFFF"
    rounded: "{rounded.sm}"
    padding: 12px 24px
  button-primary-hover:
    backgroundColor: "{colors.primary}"
  card:
    backgroundColor: "{colors.surface}"
    rounded: "{rounded.md}"
    padding: 24px
---

## Overview
{两句话：这是什么气质的设计，像什么。例：Architectural Minimalism meets
Journalistic Gravitas —— 高端哑光质感，像一本当代画廊画册。}

## Colors
- **Primary (#1A1C1E):** 深墨色，用于标题与核心正文。
- **Accent (#B8422E):** 全页唯一的交互驱动色，只出现在主按钮与关键链接。

## Typography
{字体分工与字号尺度说明。例：标题用负字距制造密度感，正文行高 1.6 保证长文可读。}

## Layout
{栅格、区块间距、最大宽度。例：内容最大宽 1200px，区块间留白 120px，8pt 网格。}

## Components
{哪个组件是页面唯一的高强调元素，其余组件如何退后。}

## Do's and Don'ts
- ✅ 强调色只用于一个 CTA
- ❌ 不要给正文使用低于 4.5:1 对比度的灰色
- ❌ 不要引入第二种字体家族
```

---

## 生成规则
1. 每个色值必须是精确 hex，禁止 "深蓝"、"浅灰" 这类模糊词
2. colors 引用组件属性时用 `{token.reference}` 语法
3. hover/active 等变体是独立条目（`button-primary-hover`），不嵌套
4. 主按钮全页只能有一个高强调样式
5. 产出后自检正文/背景对比度 ≥ 4.5:1（WCAG AA）
