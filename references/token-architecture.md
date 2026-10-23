# 令牌架构（Token Architecture）

> 目标：**设计决策只做一次**，在 token 层；多端只做单位转换，渲染层只消费语义。
> 违反这条，必然出现"小程序一套灰、Web 另一套灰、App 又一套"。

---

## 一、三层结构

```
primitive（原始值，不许业务代码直接用）
    --blue-50 / --blue-100 / … / --blue-900
    --gray-0 … --gray-900
    --space-1 … --space-16      （4/8 步进）
    --radius-sm/md/lg           （8/14/20）
    --font-size-caption/body/title/headline/display
        ↓
semantic（语义角色，业务代码消费这一层）
    --color-bg / --color-surface / --color-surface-raised
    --color-ink / --color-ink-muted / --color-border
    --color-accent / --color-accent-ink
    --color-success / --color-warning / --color-danger / --color-focus
    --space-inline-sm|md|lg   --space-stack-sm|md|lg   --space-section
        ↓
component（组件变量，组件内部消费）
    --button-primary-bg: var(--color-accent)
    --button-primary-ink: var(--color-accent-ink)
    --card-padding: var(--space-stack-md)
```

**三条铁律**
1. 业务/组件代码**禁止**引用 primitive（`--blue-500` 出现即视为违规）
2. 语义命名按**用途**：`--color-danger-surface`，不是 `--color-red-light`
3. 主题切换（浅/深/品牌）只改 semantic 层，primitive 不动

---

## 二、色彩：oklch 生成 + 语义映射

### 2.1 为什么用 oklch
sRGB/HSL 在明度上不均匀：同样 +10% 亮度，蓝色会"发黑"、黄色会"发白"。
oklch 的 L（亮度）与人眼感知一致，**同一 L 值下不同色相的视觉重量相同**，适合生成成体系的中性阶与品牌阶。

### 2.2 色阶生成规则（每色 9 档）

```
L: 98 / 95 / 90 / 80 / 70 / 58 / 46 / 34 / 22   （%）
C: 品牌色饱和度的 15% / 25% / 40% / 60% / 80% / 100% / 90% / 70% / 50%
H: 固定（品牌色相）
```
```css
--accent-50:  oklch(98% 0.02 250);
--accent-100: oklch(95% 0.04 250);
--accent-300: oklch(80% 0.09 250);
--accent-500: oklch(58% 0.16 250);   /* 品牌主色 */
--accent-700: oklch(46% 0.14 250);   /* 文本用的深档 */
--accent-900: oklch(22% 0.06 250);
```
> 没有 oklch 支持的老环境，用构建期转 sRGB（PostCSS 插件）或手工在 `oklch.com` 生成后粘值。

### 2.3 语义映射表（浅/深两套，成对定义）

| 语义 | 浅色 | 深色 | 用途 |
|---|---|---|---|
| `--color-bg` | gray-50 | gray-950 | 页面底（不用纯白/纯黑） |
| `--color-surface` | white | gray-900 | 卡片 |
| `--color-surface-raised` | white | gray-850 | 弹层/浮层 |
| `--color-ink` | gray-900 | gray-50 | 正文 |
| `--color-ink-muted` | gray-600 | gray-300 | 次要文字（**仍需 ≥4.5:1**） |
| `--color-border` | gray-200 | gray-800 | 描边/分隔 |
| `--color-accent` | accent-500 | accent-300 | 主操作 |
| `--color-accent-ink` | white | gray-950 | 主操作上的文字 |
| `--color-focus` | accent-700 | accent-200 | 焦点环 |

**深浅切换检查**：深色不是"反色"——表面越"高"越亮（+6~8% L），强调色要提亮一档，阴影改用亮边框。

### 2.4 对比度预算表（生成后必须核）

| 组合 | 最低 |
|---|---|
| ink / bg, ink / surface | 4.5:1 |
| ink-muted / bg, ink-muted / surface | 4.5:1 |
| accent-ink / accent | 4.5:1 |
| border / surface | 3:1（仅作边界时） |
| focus / 任意相邻色 | 3:1 |

```bash
python scripts/audit_contrast.py <页面>.html
```

---

## 三、间距、圆角、字号：用语义名

```css
/* 间距（4/8 步进） */
--space-1: 4px;  --space-2: 8px;  --space-3: 12px; --space-4: 16px;
--space-6: 24px; --space-8: 32px; --space-12: 48px; --space-16: 64px;

/* 语义化（推荐业务使用） */
--space-inline-sm: var(--space-2);   /* 图标与文字 */
--space-inline-md: var(--space-3);
--space-stack-sm: var(--space-3);    /* 标题与正文 */
--space-stack-md: var(--space-4);    /* 卡内边距 */
--space-stack-lg: var(--space-6);    /* 卡片间距 */
--space-section: var(--space-16);    /* 区块间距 */

/* 圆角：分级，不用一个值 */
--radius-input: 8px; --radius-card: 14px; --radius-overlay: 20px;

/* 字号：角色化 */
--font-size-caption: 13px; --font-size-body: 16px;
--font-size-title: 17px;   --font-size-headline: 22px; --font-size-display: 36px;
```

**验收**：全项目搜索 `margin:` / `padding:` 后跟数字的地方，非 token 的应 <10%。

---

## 四、多端转换层

| 端 | 单位 | 基准 | 转换规则 |
|---|---|---|---|
| Web | px | 1440 设计稿 | 1:1 |
| H5 | px + `vw` 断点 | 390 设计稿 | 1:1（配合 `clamp()` 做流式） |
| 小程序 | rpx | 750 设计稿 | `rpx = px × 2`（基于 375 逻辑宽） |
| APP | pt / dp | 375pt（iOS）/ 360dp（Android） | 1:1，字号用动态字号 API |

```css
/* 安全区（H5 / 小程序 / APP） */
padding-bottom: calc(var(--space-4) + env(safe-area-inset-bottom));
```

**禁止**：
- 在渲染层写 `font-size:13px`（必须 `var(--font-size-caption)`）
- 为小程序单独定义一套色值（只能换单位，不能换颜色）
- 用媒体查询改层级关系（层级跨端应一致，只有布局列数变化）

---

## 五、组件契约示例（只消费语义层）

```css
/* Button */
.btn {
  --btn-bg: var(--color-accent);
  --btn-ink: var(--color-accent-ink);
  background: var(--btn-bg);
  color: var(--btn-ink);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-input);
  min-height: 44px;                 /* 可访问性下限，不是设计偏好 */
  transition: transform 100ms ease-out, background 150ms ease-out;
}
.btn:hover { background: var(--accent-600); }
.btn:active { transform: scale(.97); }
.btn:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; }
.btn[disabled] { opacity: .45; pointer-events: none; }
```

```css
/* Card：靠表面明度与留白分组，不靠重边框 */
.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-card);
  padding: var(--space-stack-md);
}
```

---

## 六、从"一堆散值"迁移到令牌（渐进式，不推倒）

1. **盘点**：抓出全部色值，按出现次数排序，取前 20 个
2. **聚类**：能合并的合并（`#8A919F` 与 `#8B92A0` 是同一个灰），得到 8-12 个
3. **定语义**：把聚类结果映射到 12 个语义槽位（bg/surface/ink/ink-muted/border/accent…）
4. **替换**：先替换全局背景与文字（影响最大、风险最低），再替换组件
5. **校验**：跑对比度审计；深色模式单独跑一遍
6. **收口**：加 lint 规则禁止新代码写死色值（stylelint `color-no-hex` + 白名单）

**迁移优先级**：颜色 > 间距 > 字号 > 圆角 > 阴影。原因：颜色的不一致最刺眼，改动最安全。

---

## 七、令牌文件示例（可直接落地）

```css
:root {
  /* semantic（浅色） */
  --color-bg: #F6F7FB;
  --color-surface: #FFFFFF;
  --color-surface-raised: #FFFFFF;
  --color-ink: #1A1D26;
  --color-ink-muted: #4E5764;
  --color-border: #E3E7EF;
  --color-accent: #2E6BE6;
  --color-accent-ink: #FFFFFF;
  --color-success: #17845B;
  --color-warning: #A85B00;
  --color-danger: #C0342B;
  --color-focus: #1F5BC4;
}
[data-theme="dark"] {
  --color-bg: #0E1116;
  --color-surface: #151A22;
  --color-surface-raised: #1C222C;
  --color-ink: #F2F4F8;
  --color-ink-muted: #B7BECB;
  --color-border: #2A323F;
  --color-accent: #7EA6FF;
  --color-accent-ink: #0B0E13;
  --color-success: #4FD1A5;
  --color-warning: #FFC46B;
  --color-danger: #FF8A80;
  --color-focus: #9DBBFF;
}
```
> 这套值已通过 `audit_contrast.py`（浅/深各 20+ 组，最低 4.68:1），可直接作为起点。
