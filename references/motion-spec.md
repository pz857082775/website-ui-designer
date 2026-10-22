# 动效规范（库选型 · 参数 · 性能 · 验收）

> 来源核实（2026-10-22）：
> - `curiositech/windags-skills · motion-design-web` ✅ 真实（LobeHub 收录，**Apache-2.0**，非 MIT）
> - `bouclem/animate` ✅ 真实（SkillMD 收录，7 star）
> - `motiondivision/motion` ✅ 34.4k｜`nandorojo/moti` ✅ 4.5k｜`greensock/GSAP` ✅ 29.6k｜`magicuidesign/magicui` ✅ 22.8k｜`pmndrs/react-spring` ✅ 29.2k
> - `aceternity/aceternity-ui`、`aceternity/ui` ❌ GitHub 404；实际通过 shadcn registry 分发（见 5.5）
> - `robb0wen/folex-fx` ❌ 不存在（纯 CSS 呼吸/涟漪用本文 6.1 自写即可）

---

## 一、库选型决策树（先选库，再写参数）

```
需求 →
├─ 简单过渡（hover / fade / slide）？
│   └─ 纯 CSS transition       体积 0，硬件加速，覆盖 80% 场景
├─ 布局动画 / 手势 / 编排序列？
│   ├─ React 项目 → Motion（原 Framer Motion）  layout 自动、AnimatePresence、spring 内置
│   └─ 非 React / 需要极致控制 → GSAP          timeline、ScrollTrigger、SVG 绘制
├─ 只在滚动上做效果？
│   ├─ 现代浏览器（Chrome 115+）→ CSS scroll-driven animations  零 JS，主线程之外
│   └─ 兼容旧浏览器 → GSAP ScrollTrigger
├─ 跨页面共享元素转场？
│   └─ View Transitions API（不支持则降级为普通加载）
├─ React Native / Taro、Remax 小程序？
│   └─ moti（Reanimated 驱动，原生弹簧、下拉回弹、骨架呼吸）
└─ 需要现成高级组件（液体玻璃 / 磁吸 / 流光边框）？
    ├─ Aceternity UI  npx shadcn@latest add https://ui.aceternity.com/registry/<name>.json
    └─ Magic UI       复制组件源码，依赖 motion + tailwind
```

| 库 | 适合 | 不适合 | 体积/备注 |
|---|---|---|---|
| 纯 CSS | 微交互、hover、呼吸 | 复杂时序、手势 | 0 |
| Motion | React 布局动画、手势、共享元素 | 非 React | ~34k（可 tree-shake） |
| GSAP | 时间线编排、SVG、滚动、开场 | 简单 hover（过重） | 核心 ~70k；B 端谨慎 |
| react-spring | 自定义物理曲线、惯性、橡皮筋 | 快速搭页面 | 中 |
| moti | RN / Taro 小程序 | Web 端 | 依赖 Reanimated |
| Aceternity / Magic UI | 营销页、磨砂玻璃、Bento | 数据后台（太重） | 按组件引入 |

---

## 二、时长与缓动（唯一标准）

| 目的 | 时长 | 缓动 |
|---|---|---|
| 即时反馈（按下、hover 确认） | **100-150ms** | ease-out |
| 状态变化（切换、选中、菜单） | **200-250ms** | ease-in-out |
| 内容展开（手风琴、下拉、卡片展开） | **300-400ms** | spring 或 ease-out |
| 主要上下文切换（弹层、页面） | **400-600ms** | 带 anticipation + follow-through |
| 背景活动（加载、进度） | **1.5-2s 循环** | linear 或跟随真实进度 |

**退场 = 入场 × 0.75**（ux 铁律：离开要更快）。

缓动曲线只用这三条（bouclem）：
```css
--ease-out-quart: cubic-bezier(.25, 1, .5, 1);    /* 平滑精致 */
--ease-out-quint: cubic-bezier(.22, 1, .36, 1);   /* 稍利落（默认） */
--ease-out-expo:  cubic-bezier(.16, 1, .3, 1);    /* 果断 */
```
**禁用**：`bounce`（`cubic-bezier(.34,1.56,.64,1)`）、`elastic`（`cubic-bezier(.68,-.6,.32,1.6)`）——显廉价、且会拖长"等它停下"的时间。

---

## 三、弹簧参数库（stiffness / damping / mass）

| 场景 | stiffness | damping | mass | 说明 |
|---|---|---|---|---|
| 灵敏控件（按钮、开关、Tab） | **400** | **28** | 1 | 快速收敛，几乎不回弹 |
| 平滑面板（弹层、卡片） | **200** | **24** | 1 | 有质感但安静 |
| 成功/愉悦反馈（勾选、撒花） | **300** | **15** | 1 | 允许少量回弹 |
| 重物（整页 sheet、大抽屉） | **120** | **20** | **1.5** | 有重量感，不飘 |
| 手势驱动（拖拽、侧滑） | **300** | **20** | 1 | 必须继承松手速度 |

**红线**
- 交互元素 `damping ≥ 20`；低于 15 就会出现"果冻效应"
- 弹簧总收敛时间 **≤600ms**；超过用户会等它停
- 过冲（overshoot）控制在 **0-10%**
- 手势释放时传 `velocity`，否则"松手即停"很假

```js
// Motion
<motion.div transition={{ type:"spring", stiffness:200, damping:24 }} />
// react-spring
const s = useSpring({ from:{x:0}, to:{x:100}, config:{ tension:200, friction:24 } });
// GSAP（没有真弹簧，用弹性缓动近似；B 端建议直接用 power3.out）
gsap.to(el, { y:-6, duration:.45, ease:"elastic.out(1, 0.6)" }); // 营销页才用
```

---

## 四、呼吸动画三档（按端与场景，不按喜好）

| 档位 | 周期 | 振幅 | 手法 | 适用 |
|---|---|---|---|---|
| **B 端低动效** | 6-8s | ≤1.5%（scale）或 opacity ±0.06 | 只让 AI/实时/紧急元素呼吸 | 工厂后台、点检、数据台 |
| **C 端柔和** | **2.8-4s** | ≤3% | 背景渐变位移、光晕明暗、卡片微弱缩放 | 官网、APP 个人页 |
| **小程序轻量** | 4-6s | ≤2% | 纯 CSS（transform/opacity），不引 JS 库 | 商品卡、会员页 |

```css
/* 6.1 纯 CSS 呼吸（零依赖，可任意裁剪） */
@keyframes breathe-glow{
  0%,100%{ transform:scale(1);    opacity:.45 }
  50%    { transform:scale(1.02); opacity:.7  }
}
.breathe{ animation:breathe-glow 6.5s ease-in-out infinite; will-change:transform,opacity }

/* 渐变呼吸：只动 background-position，不动颜色 */
@keyframes drift{
  0%,100%{ background-position:0% 50% }
  50%    { background-position:100% 50% }
}
.aurora{ background-size:200% 200%; animation:drift 8s ease-in-out infinite }

@media (prefers-reduced-motion: reduce){
  .breathe,.aurora{ animation:none; opacity:.6 }
}
```
**纪律**：一屏 ≤2 个呼吸元素；同时动画组 ≤2；呼吸不改变布局、不遮挡文字。

---

## 五、编排（Stagger / 时序 / 共享元素）

### 5.1 交错
- 子元素 **40-80ms** 间隔（比 100ms 更紧凑，避免"排队感"）
- 页面加载的区块级交错：100-150ms
- **主元素先动**，其余跟随；一屏只允许 1-2 组并行动画（第 3 组开始就是"动画汤"）

### 5.2 入场结构
```
0ms    主视觉（标题/hero）fade+translateY(16px)  400-600ms
+80ms  次级内容
+160ms 辅助元素/卡片
```
不要每个区块都 fade-up（这是 AI 默认病）。

### 5.3 FLIP / 共享元素
- Motion：`layoutId="card-1"` 自动做 FLIP；列表重排用 `layout`
- 原生：`View Transitions API` + `view-transition-name`
- 展开类：先量 `getBoundingClientRect()`，再 `transform` 过渡（不适用于超长内容）
- 小程序：不支持 View Transitions，用 `wx.createAnimation` 或 moti，降级为淡入

### 5.4 手势
- 拖拽：`drag` + `dragElastic={0.2}` + `onDragEnd` 取 `velocity` 判断飞走
- 侧滑抽屉：跟手位移 → 松手按速度决定开/合（阈值 30% 或 v>500px/s）
- 下拉刷新：位移阻尼 0.5，超过 64px 触发，回弹用 spring(300/20)
- APP 必须留安全区：`env(safe-area-inset-*)`

---

## 六、性能红线（会卡就不合格）

```
[ ] 中端设备 60fps（DevTools CPU 4x 降速测）
[ ] 只动 transform / opacity / filter / clip-path —— 零 Layout 块
[ ] 不用 width/height/top/left/margin 做动画
[ ] will-change 只在动画期间加，结束移除
[ ] 首屏关键路径动画库 <20KB；简单效果不引库
[ ] 长列表用虚拟滚动，动画元素数 ≤3 同时
[ ] 图片/SVG 动画不触发整层重绘（加 contain: paint）
```

**五大翻车与检测**

| 症状 | 根因 | 修法 |
|---|---|---|
| 掉帧、DevTools 有紫色 Layout 块 | 动画了布局属性 | 改 `transform: scale()` / `translate` |
| 元素弹了 1 秒还没停 | damping<15 或 stiffness>500 | damping ≥20；交互场景改 duration 过渡 |
| 页面加载所有元素一起动 | 没有 staging | 主元素先动 + 40-80ms 交错 + ≤2 组 |
| 无障碍审计不过 | 没写 reduced-motion | 全局 0.01ms 降级 + 保留静态反馈 |
| 首屏变慢 | 为简单效果引了大库 | CSS 优先；库按需懒加载 |

---

## 七、四端差异

| 维度 | PC 网站 | H5 | 小程序 | APP |
|---|---|---|---|---|
| 默认库 | CSS / Motion / GSAP | CSS / Motion | 纯 CSS / moti | moti / react-spring |
| 时长上限 | 600ms（营销页可 800） | 400ms | 300ms | 500ms（跟手手势不限） |
| 呼吸档位 | C 端柔和 | C 端柔和 | 小程序轻量 | C 端柔和 |
| 必做 | hover/focus 过渡 | `@media (hover:hover)` 包裹 hover | rpx 单位、无 View Transitions | 安全区、下拉回弹、侧滑返回 |
| 禁止 | 滚动劫持 | 粘滞 hover、100vh | 重 JS 动画、大图未压缩 | 自造导航转场 |

**小程序特别注意**：动画单位用 rpx；`wx.createAnimation` 只支持有限属性，复杂效果用 CSS；
分包内不要放动画库；`setData` 驱动的动画会掉帧，优先 CSS。

---

## 八、与其他库的集成方式

### 8.1 Motion（React 主力）
```bash
npm i motion
```
```jsx
import { motion } from "motion/react";
<motion.button whileHover={{ scale:1.02 }} whileTap={{ scale:.97 }}
  transition={{ type:"spring", stiffness:400, damping:28 }} />
```

### 8.2 moti（RN / Taro）
```bash
npm i moti
```
```jsx
<MotiView from={{ opacity:0, scale:.96 }} animate={{ opacity:1, scale:1 }}
  transition={{ type:"spring", damping:20 }} />
```

### 8.3 GSAP（精细时序）
```js
gsap.timeline({ defaults:{ ease:"power3.out", duration:.5 } })
  .from(".hero-title", { y:20, autoAlpha:0 })
  .from(".hero-card", { y:16, autoAlpha:0, stagger:.06 }, "-=0.3");
```

### 8.4 Magic UI / Aceternity（现成组件）
```bash
# Magic UI：复制源码，依赖 motion + tailwind
# Aceternity：走 shadcn registry
npx shadcn@latest add https://ui.aceternity.com/registry/focus-cards.json
```
两者都允许直接改源码，**引入后必须按本文时长/弹簧参数校准**（它们的默认值偏"展示型"）。

---

## 九、验收清单（10 条，逐条过）

```
[ ] 1 时长落在四档区间内（100-150 / 200-250 / 300-400 / 400-600）
[ ] 2 退场 = 入场 × 0.75
[ ] 3 缓动只用 quart/quint/expo；无 bounce、无 elastic
[ ] 4 弹簧：交互 damping ≥20，收敛 ≤600ms，过冲 ≤10%
[ ] 5 呼吸：一屏 ≤2 个，周期按端取档，振幅 ≤3%
[ ] 6 编排：子元素 40-80ms 交错，主元素先动，并发 ≤2 组
[ ] 7 性能：只动 transform/opacity/filter/clip-path，60fps 无 Layout 块
[ ] 8 降级：reduced-motion 下动画归零但保留静态反馈
[ ] 9 手势：继承速度、有阈值、尊重安全区
[ ] 10 无"动画汤"：所有动画都能说出它解决什么问题
```

**一句话判据**：如果用户注意到"这个动画很好看"，说明它太抢了；正常状态是"用起来很顺，但说不出哪里动了"。
