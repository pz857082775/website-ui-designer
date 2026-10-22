# 视觉与交互规范（可读性 · 美观 · 反馈动效）

> 本文件是**交付硬标准**：不满足即返工。每条规则都配了验收方法与可复制的实现参数。
> 适用：营销页、工作台、H5、小程序、APP；浅色与深色模式都必须过。

---

# 第一部分 · 配色可读性（Contrast）

## 1.1 硬指标（不可协商）

| 对象 | 最低对比度 | 说明 |
|---|---|---|
| 正文（<24px 常规或 <18.66px 粗体） | **4.5:1** | 任何一段可读文字 |
| 大字（≥24px 或 ≥18.66px 粗体） | **3:1** | 标题、数字 |
| 次要文字 / 元信息 / 占位符 | **4.5:1** | 占位符也是文字，不享受豁免 |
| 图标、边框、分割线、输入框描边 | **3:1** | 属于 UI 组件 |
| 焦点环（focus-visible） | **3:1** 且对比相邻色 | 键盘可达性 |
| 禁用态 | ≥2.5:1（推荐） | 法规豁免，但别做成看不见 |

计算公式（WCAG 2.1）：
```
L = 0.2126R + 0.7152G + 0.0722B        （R/G/B 先做 sRGB → 线性化）
对比度 = (L亮 + 0.05) / (L暗 + 0.05)
```

## 1.2 三条禁令

1. **禁止同色系低差**：文字与其直接背景不得落在同一色相且亮度差 < 15%（如 `#F5F7FA` 上的 `#E8EBF0`）
2. **禁止渐变/图片上的裸文字**：文字压在渐变或照片上时，必须在最亮处仍 ≥4.5:1，否则加 scrim（黑色 40-60% 或白色 60-80%）
3. **禁止"软底徽章"文字用浅色**：徽章底是强调色 12% 时，文字必须用该强调色的 800 档（深），不是 400 档

## 1.3 双模式令牌（必须成对定义）

```css
:root{
  /* 浅色 */
  --bg:#F6F7FB;  --surface:#FFFFFF;  --surface-2:#F1F3F8;
  --ink:#1A1D26;  --ink-2:#5A6172;  --ink-3:#5F6A7D;   /* ink-3 也必须 ≥4.5 */
  --border:#E3E7EF;  --accent:#2E6BE6;  --accent-ink:#FFFFFF;
  --success:#17845B;  --warning:#A85B00;  --danger:#C0342B;
  --focus:#1F5BC4;
}
[data-theme="dark"]{
  --bg:#0E1116;  --surface:#151A22;  --surface-2:#1C222C;
  --ink:#F2F4F8;  --ink-2:#B7BECB;  --ink-3:#98A1B0;
  --border:#2A323F;  --accent:#7EA6FF;  --accent-ink:#0B0E13;
  --success:#4FD1A5;  --warning:#FFC46B;  --danger:#FF8A80;
  --focus:#9DBBFF;
}
```

**深色模式纪律**：
- 不用纯黑 `#000` 配纯白 `#FFF`（眩光 + 光晕）；用 `#0E1116` + `#F2F4F8`
- 表面越"高"越亮：`surface-2` 比 `surface` 亮 6-8%
- 深色下强调色要提亮（浅色 `#2E6BE6` → 深色 `#7EA6FF`），否则文字对比不足
- 阴影在深色下几乎不可见，改用 1px 亮边框表达层级

## 1.4 自动审计（交付必跑）

```bash
python scripts/audit_contrast.py tests/*.html          # 检查浅色 + 深色两套令牌
python scripts/audit_contrast.py page.html --verbose    # 输出全部组合的比值
```

输出：每对「背景 × 文字」的实测比值 + 通过/失败；**0 违规才可交付**。

## 1.5 可读性验收清单

```
[ ] audit_contrast.py 0 违规（浅色 + 深色各跑一遍）
[ ] 正文 4.5:1、大字 3:1、UI 元素 3:1、焦点环 3:1
[ ] 无"同色系低差"组合（目测 + 脚本双检）
[ ] 渐变/图片上的文字有 scrim，且最亮处仍达标
[ ] 徽章/标签文字用 800 档深色，不用 400 档
[ ] 禁用态仍可辨认（≥2.5:1）
```

---

# 第二部分 · 视觉美观（Aesthetics）

## 2.1 配色结构：60-30-10

| 比例 | 角色 | 用法 |
|---|---|---|
| 60% | 中性主调 | 页面背景、大面积留白 |
| 30% | 次调 | 卡片、分区色带、次级面 |
| 10% | 强调 | 主按钮、关键数字、激活态（**每屏 3-5 处，不超 5**） |

**鲜明但不脏的配方**：
- 1 个主色家族（5 档：50/100/400/600/800）+ 1 个互补强调色 + 4 个语义色
- 主色饱和度 ≥70%（灰扑扑的根源是饱和度 <50% 又不敢提亮）
- 中性阶带轻微色相（如偏蓝灰 `#F6F7FB`），纯灰 `#F5F5F5` 显廉价
- 分区色带：每 2-3 个区块换一次底色（base → surface → tint），避免"一整墙白"

## 2.2 视觉焦点：一屏一个

主视觉必须能被"眯眼测试"识别：
```
眯眼/模糊截图后，仍能看出一个最亮的焦点 → 合格
看过去一片均匀 → 没有焦点，返工
```
实现手段（选 1-2 个，不要全用）：
- 尺寸对比（主标题比次标题大 ≥1.5 倍）
- 色彩对比（焦点区用唯一高饱和/唯一深色块）
- 空间对比（焦点四周留白是其他区域的 1.5-2 倍）
- 质感对比（唯一有阴影/唯一有图片的区域）

## 2.3 字体层级（三档字重 + 1.25 比例）

```css
--fs-1:13px; --fs-2:15px; --fs-3:17px; --fs-4:21px; --fs-5:26px; --fs-6:33px; --fs-7:41px;
```
- 只用 3 种字重：400 / 500-600 / 700-750
- 相邻层级字号差 ≥1.25 倍；Display 与 Body 差 ≥2.4 倍
- 中文标题 `letter-spacing:-0.01em`；英文大标题 `-0.02em`
- 正文行高 1.6-1.75，行宽 45-75 字符

## 2.4 留白与节奏

| 位置 | 数值 |
|---|---|
| 区块垂直间距 | 96 / 120 / 160（按密度旋钮） |
| 卡片内边距 | 20 / 24 / 32 |
| 卡片间距 | 16 / 20 / 24 |
| 页面左右边距 | 24（移动）/ 48-64（桌面） |
| 标题与正文间距 | 12-16 |

**节奏规则**：大-小-大交替；同一屏不出现三种以上间距值；卡片内边距 ≥ 文字行高。

## 2.5 深度与质感

- 两级阴影：`--shadow-1: 0 1px 2px rgba(16,24,40,.04), 0 2px 8px rgba(16,24,40,.06)`
  / `--shadow-2: 0 8px 24px rgba(16,24,40,.10)`
- 圆角分级：输入 8 / 卡片 14 / 弹层 20 / 大容器 24
- 描边 1px `--border`，与阴影二选一为主，不要"描边+重阴影"叠加
- 禁止：彩虹渐变、发光滥用、纯装饰噪点、假玻璃满屏

## 2.6 美观验收清单

```
[ ] 眯眼测试：一屏一个清晰焦点
[ ] 配色 60-30-10 成立；强调色每屏 3-5 处
[ ] 字号比例 1.25，跨度 ≥2.4 倍；字重 ≤3 种
[ ] 区块间距 ≥96px（营销页）；卡片间距统一
[ ] 每 2-3 个区块有一次底色变化
[ ] 圆角分级、阴影两级，无"描边+重阴影"叠加
[ ] 无纯灰中性阶、无低饱和脏色
```

---

# 第三部分 · 交互反馈与动效（Motion & Feedback）

## 3.1 状态矩阵（每个可交互元素必须齐全）

| 状态 | 视觉变化（至少 2 项） | 时长 |
|---|---|---|
| default | — | — |
| hover | 亮度 +4% / 抬升 1-2px / 边框变深 | 160ms |
| active（按下） | `scale(.97)` + 阴影收 | 90-120ms |
| focus-visible | 2px 焦点环 + 2px offset | 即时 |
| disabled | 透明度 .45 + 禁用手势 | — |
| loading | 文案淡出 + 旋转/进度 + 宽度锁定 | 120ms 进入 |
| success | 背景转语义色 + 勾线绘制 + 文案替换 | 见 3.2 |
| error | 边框转红 + 轻微 shake（±3px，2 次） | 300ms |

## 3.2 点击成功动画（必做，主操作全覆盖）

**时间轴（总 1.4-1.8s，可被打断）**

```
0ms      按下：scale .97
90ms     释放：回到 1，锁定最小宽度（防布局跳动）
120ms    文案淡出（opacity 1→0, 100ms）
200ms    按钮底色过渡到 success（240ms）
200ms    勾线绘制：stroke-dashoffset 1→0，220ms，ease-out
600ms    停留（可显示"已保存"2 字）
900ms    勾线淡出，文案还原（300ms）
```

**硬要求**
- 宽度/高度在动画期间**不变**（`min-width` + 固定 padding），避免布局抖动
- 提交类操作必须**防重复点击**（loading 期间 `pointer-events:none` + `aria-busy="true"`）
- 成功态用 `aria-live="polite"` 宣告；纯视觉反馈不合格
- `prefers-reduced-motion`：跳过缩放与勾线，直接显示"✓ 已保存 + 语义色边框"，2s 后还原

```js
// 极简实现（无依赖）
btn.addEventListener("click", () => {
  if (btn.dataset.state === "loading") return;
  btn.dataset.state = "loading";
  btn.classList.add("is-loading");
  setTimeout(() => {
    btn.dataset.state = "success";
    btn.classList.add("is-success");     // CSS 负责勾线绘制
    setTimeout(() => {
      btn.dataset.state = "";
      btn.classList.remove("is-loading", "is-success");
    }, 1600);
  }, 450);
});
```

## 3.3 模块聚焦（查看即展开放大，离开恢复）

用户交互或悬停某个模块时：**该模块放大突出 + 展开内容，其余模块缩小退后**。

**参数**
```
聚焦模块：scale(1.03) + 阴影升到 shadow-2 + 边框转强调色 1px + z-index +1
其余模块：scale(0.98) + opacity .6 + filter saturate(.92)
容器背景：加 4% 暗角（可选，仅桌面）
进入：380ms cubic-bezier(.22,1,.36,1)
离开：285ms（= 进入的 75%，稍快）
展开内容：grid-template-rows 0fr → 1fr（250ms），或 max-height 0 → 实测高度
```

**实现要点**
- 只动 `transform / opacity / filter`，网格不重排（放大不推动邻居）
- 用 `:focus-within` 让键盘也能触发同样的聚焦
- 支持 `Esc` 恢复；点击遮罩/空白恢复
- 移动端（`hover:none`）不做悬停放大，改为**点击切换**，且只允许一个模块处于聚焦
- 一屏只允许一个模块聚焦；不允许同时多个放大
- 展开区域内容必须真实（不是占位），且不引起横向滚动

```css
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.card{transition:transform .38s cubic-bezier(.22,1,.36,1), box-shadow .38s, opacity .28s, border-color .28s}
.grid[data-focus="on"] .card{transform:scale(.98);opacity:.6}
.grid[data-focus="on"] .card.is-focus{transform:scale(1.03);opacity:1;box-shadow:var(--shadow-2);border-color:var(--accent);z-index:2}
.card .detail{display:grid;grid-template-rows:0fr;transition:grid-template-rows .25s ease}
.card.is-focus .detail{grid-template-rows:1fr}
.card .detail>div{overflow:hidden}
```

## 3.4 动态呼吸感（克制）

| 对象 | 参数 |
|---|---|
| AI/实时元素 | `scale 1→1.02` 或外发光 opacity .35→.6，7s ease-in-out 循环 |
| 紧急徽章 | 圆点 `scale 1→1.6` + opacity 1→0，2s 循环 |
| 数字/图表 | 入场 count-up 1.2s、柱状 0.7s 生长（只播一次） |

**纪律**：一屏 ≤2 个呼吸元素；只给"活的"元素（AI、实时、紧急）；禁止装饰性漂浮。

## 3.5 动效总量与性能

- 入场：**一个编排好的序列**（stagger 0.05-0.08），不做逐区块 fade-up
- 时长档位：微交互 120-180ms / 标准 240-320ms / 入场 400-600ms / 出场 = 入场 ×0.75
- 缓动：入场 `cubic-bezier(.22,1,.36,1)` 或 `power3.out`；出场 `ease-in`
- 同时动画元素 ≤3；`will-change` 只在动画期间加，结束移除
- 只动 `transform/opacity/filter`；禁止动 `width/height/top/left`（第 6 条 preflight 会拦）
- 无 `scroll-jacking`；滚动只做映射与揭示

## 3.6 交互验收清单

```
[ ] 每个可点元素具备 8 态（default/hover/active/focus/disabled/loading/success/error）
[ ] 主操作点击有成功动画：勾线 + 语义色 + 文案变化 + aria-live
[ ] 动画期间按钮尺寸不变（无布局跳动，CLS < 0.1）
[ ] 模块聚焦：放大 + 展开 + 其余退后；Esc 可恢复
[ ] 键盘可触发同样的聚焦（:focus-within）
[ ] 移动端无粘滞 hover，改为点击切换
[ ] 一屏呼吸元素 ≤2；同时动画 ≤3
[ ] prefers-reduced-motion 下全部降级且仍有静态反馈
[ ] 60fps（DevTools Performance 无长任务 >50ms）
```

---

# 第四部分 · 三条命令式总则

1. **看不见 = 不存在**：任何文字与背景对比 <4.5:1，这个设计就是坏的，不管多好看
2. **一屏一个焦点**：想让人看五处，结果一处都记不住
3. **每个操作都要有回应**：点击必须有可见变化；没有反馈的按钮，用户会再点一次
