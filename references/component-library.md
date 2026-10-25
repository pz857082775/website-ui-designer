# 组件库与设计系统来源（Component Library）

> 核实（2026-10-25）：`shadcn-ui/ui` 126.5k★ MIT｜`material-components/material-web` 11.4k★ Apache-2.0（npm `@material/web` 2.5.0）｜`vercel/geist-font` 3.7k★ OFL-1.1｜Vercel 模板页 HTTP 200｜`getdesign` npm 0.6.26
> 原则：**组件库解决"零件"和"无障碍交互"，不解决信息架构、数据地板、文案与品牌**。

---

## 一、选型矩阵

| 方案 | 本质 | 适合 | 不适合 | 代价 |
|---|---|---|---|---|
| **shadcn/ui** | CLI 把组件源码**复制进你的仓库**（Radix + Tailwind） | React/Next 产品、需要深度定制、要长期维护自己的系统 | 非 React、要求"不动源码只升级包" | 代码归你 = 你负责升级与审计 |
| **Radix / Ark（headless）** | 只有行为与无障碍，没有样式 | 已有设计语言，只缺交互原语 | 想快速出界面 | 样式全自己写 |
| **Material Web（MWC）** | Web Components 实现 M3 | 多框架混用、无构建、品牌就是 Material | 想要非 Material 的视觉 | Google 主力已转内部框架，**维护模式**，长期风险要评估 |
| **Vercel Turborepo DS 模板** | monorepo + Storybook + 共享 UI 包 | 多产品线、要沉淀自己的一套系统 | 单页/小项目 | 前期脚手架成本高 |
| **纯自研** | 完全自建 | 品牌差异是核心竞争力 | 时间紧 | 最贵 |

**决策顺序**：先问"有没有品牌规范" → 有：headless + 自研皮肤；没有且要快：shadcn 改皮；跨框架/无构建：MWC。

---

## 二、shadcn/ui 接入规范（推荐路径）

### 2.1 初始化
```bash
npx shadcn@latest init        # 生成 components.json + CSS 变量主题
npx shadcn@latest add button dialog input table
```
- 组件源码落在 `components/ui/`，**从此属于你的仓库**，可以改
- 升级策略：**锁定 CLI 版本 + 每次 add 前 diff**，不要"删了重装"（会覆盖你的改动）

### 2.2 主题：必须重做的四件事（否则就是"默认 shadcn 脸"）
| 项 | 默认值的问题 | 改成 |
|---|---|---|
| 圆角 | 全站 `--radius: .5rem`，所有组件同一圆角 | 分级：输入 8 / 卡片 14 / 弹层 20 |
| 边框 | 全站 1px `--border` 硬线 | 浅色用 `rgba(0,0,0,.06-.08)`，深色用 `rgba(255,255,255,.07-.14)` |
| 阴影 | 几乎无，靠边框分组 | 两级阴影（近距 2px / 远距 24px），按层级用 |
| 字阶 | 继承项目默认，常见 14px 通铺 | 5 档角色 + 1.25 比例，正文 ≥16（移动 mockup ≥14） |

**判定**：如果换掉 logo 后，你的界面和任何一个 shadcn 项目长得一样 → 皮肤没做完。

### 2.3 令牌映射（把 shadcn 变量接进我们体系）
见 `templates/shadcn-theme.css`：`--background ← --color-bg`、`--foreground ← --color-ink`、
`--muted-foreground ← --color-ink-muted`、`--primary ← --color-accent`、`--ring ← --color-focus`。
**只在这一层做映射**，组件内部不要再出现原始色值。

### 2.4 无障碍契约（不要重新发明）
- Radix 已处理：焦点捕获、Esc 关闭、方向键、`aria-*`、滚动锁
- **禁止**：自己用 `div` 重写 Dialog/Dropdown 的键盘逻辑；改样式时不要删 `data-state` 属性
- 必须补：焦点环（`--ring`）、触控 ≥44px、`prefers-reduced-motion`

---

## 三、Material Web（MWC）注意事项

```bash
npm i @material/web
```
```js
import '@material/web/button/filled-button.js';
```
```html
<md-filled-button>保存</md-filled-button>
```
- 基于 **M3 design tokens**（`--md-sys-color-primary` 等），改主题走 token，不要覆写内部 shadow DOM
- **维护模式**：2024 年起 Google 主力转移，库未废弃但更新慢。选它就要接受"三年后可能自己维护"
- 适合：品牌就是 Material、多框架共存、不想引入构建
- 不适合：需要高度定制视觉（shadow DOM 会让你很难改）

---

## 四、Vercel Turborepo 设计系统模板

```bash
npx create-turbo@latest -e design-system
```
- 产出：`apps/web` + `packages/ui` + Storybook + 共享 tsconfig/eslint
- 适合：**两个以上产品共用一套组件**，需要版本化发布（`packages/ui` 独立 version）
- 关键纪律：`packages/ui` 只消费语义令牌；业务 app 不直接引用 `packages/ui` 内部文件，只走入口导出
- 不适合单页项目——脚手架成本 > 收益

---

## 五、组件消费的三层纪律

```
token（语义） → component contract（variant / size / state） → pattern（页面组合）
```
- 业务代码**只允许**用 `variant` / `size` / `state` 控制组件，**禁止**用 `!important` 改内部
- 需要新样式 → 新增 variant，而不是在页面里覆盖
- 组件内部**禁止**写死颜色（必须 `var(--color-*)`）
- 组件必须有：default / hover / active / focus-visible / disabled / loading（表单再加 error / success）

---

## 六、组件库解决不了的事（别指望）

| 问题 | 组件库能给吗 | 该谁解决 |
|---|---|---|
| 这页该先看什么 | 不能 | 3.1 层级与焦点 |
| 分组对不对（内部 ≤ 外部间距） | 不能 | 3.2 格式塔 |
| 钩子那句话有没有数据支撑 | 不能 | 3.14 数据地板 |
| 文案说不说人话 | 不能 | 说法层 + 文案规范 |
| 品牌差异 | 不能（默认皮肤反而抹平差异） | 2.4 记忆点 + 五轴组合 |
| 无障碍交互原语 | **能**（Radix/Ark/MWC） | 组件库 |
| 状态机与键盘行为 | **能** | 组件库 |

**一句话**：组件库让你"不缺零件"，但**页面是否专业取决于你怎么组装**。
