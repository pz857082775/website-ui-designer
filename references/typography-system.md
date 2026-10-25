# 字体系统（Typography System）

> 核实：`vercel/geist-font` 3.7k★，SIL OFL-1.1（商用免费）；npm `geist` 1.8.2。
> 核心观点：**字体是最便宜的品牌差异**——换字族比换配色更能改"气质"，但必须选得有理由。

---

## 一、字族策略（先定关系，再选具体字体）

| 页面类型 | 字族关系 | 为什么 |
|---|---|---|
| 品牌/编辑/文化 | **衬线 display + 无衬线正文** | 对比制造"被设计过"的感觉；衬线承载语气 |
| 产品/后台/工具 | **单一无衬线 + 等宽数字** | 高频阅读，减少切换成本；数字等宽才能对齐 |
| 数据/终端/开发工具 | **无衬线 + 等宽**（代码/ID/时间戳） | 等宽表达"这是机器数据" |
| 儿童/亲和 | 圆体或高 x-height 无衬线 | 字形开口大，易读 |
| 极简/高端 | 单一无衬线 + 极限字重差（200/700） | 靠字重与留白，不靠装饰 |

**上限**：字族 ≤2 个，字重 ≤3 个（400/500/700），总字体文件 ≤4 个 woff2。
**禁令**：Inter / Roboto / system-ui 裸用（无字距、无字重策略）＝ AI 指纹。

---

## 二、Geist 家族（Vercel 质感的一半）

| 字体 | 用途 | 气质 |
|---|---|---|
| **Geist Sans** | 界面标题与正文 | 中性、几何、字形紧凑，接近 Vercel 官网 |
| **Geist Mono** | 代码、终端、数字、ID | 等宽，适合日志与时间戳 |
| **Geist Pixel** | 像素风标题（5 种变体） | 极端场景，慎用；一页最多一处 |

```bash
npm i geist
```
```js
// Next.js
import { GeistSans } from "geist/font/sans";
import { GeistMono } from "geist/font/mono";
```
```css
/* 非 Next 项目：用 fontsource 或自托管 woff2 */
@font-face{
  font-family:"Geist"; src:url("/fonts/Geist-Regular.woff2") format("woff2");
  font-weight:400; font-display:swap;
}
:root{ --font-sans:"Geist","PingFang SC","Microsoft YaHei",sans-serif; }
```

**许可证**：OFL-1.1，可商用、可嵌入、可改；**保留版权声明**，不得单独售卖字体文件。

---

## 三、中文搭配（最常见的翻车点）

- 西文 + 中文必须**分别声明**：`font-family: "Geist", "PingFang SC", "Microsoft YaHei", sans-serif`
- 中文没有真正的"细体"：`font-weight:300` 常被渲染成 400，**中文层级靠字号与颜色档，不靠字重**
- 中文行高比西文高：正文 1.6-1.75（西文 1.5 就够）
- 中文标题字距收紧 `-0.01 ~ -0.02em`；大标题可到 `-0.03em`，但**正文不要负字距**
- 中英混排行宽按"中文字符数"算：30-45 字

| 场景 | 中文候选 | 注意 |
|---|---|---|
| 苹方 / 思源黑体（Noto Sans SC） | 通用、免费 | 字重齐全，文件大，需 subset |
| 思源宋体（Noto Serif SC） | 品牌/编辑 | 小字号发虚，只用于 ≥20px |
| 系统字体栈 | 快速原型 | 跨平台差异大，不可当品牌字体 |
| 商业字体（方正/汉仪等） | 品牌 | **必须确认 Web 授权**，否则违法 |

---

## 四、字阶与参数（可直接抄）

```
display   36-48 / 700 / 行高 1.1-1.2 / 字距 -0.03em   （一屏一处）
headline  24-28 / 700 / 1.25 / -0.02em
title     17-20 / 500-600 / 1.35 / -0.01em
body      16（移动 mockup ≥14）/ 400 / 1.6 / 0
caption   12-13 / 400 / 1.45 / 0.01em
数字       等宽（tabular-nums），单位小一号
```
- 相邻层级 ≥1.25 倍；display 与 body ≥2.4 倍
- 全大写标题行高下限 **1.0**（推荐 1.02-1.08），否则中文/大写混排会糊行
- 数字一律 `font-variant-numeric: tabular-nums`（表格、KPI、金额）

---

## 五、性能与加载（字体是首屏最大变量之一）

```
[ ] woff2，≤4 个文件，总 ≤300KB
[ ] font-display: swap（或 optional + 本地回退栈）
[ ] 关键字体 preload；非关键延迟
[ ] 中文 subset（常用 3500 字）或按页拆包
[ ] 回退栈写全（含系统中文），避免 FOUT 时布局跳动
[ ] 用 size-adjust / ascent-override 对齐回退字体的度量
```

```css
@font-face{
  font-family:"BrandSans"; src:url("/f/brand.woff2") format("woff2");
  font-weight:400 700; font-display:swap;
  size-adjust:102%; ascent-override:92%; descent-override:24%;
}
```

---

## 六、验收

```
[ ] 字族 ≤2、字重 ≤3、文件 ≤4 且 ≤300KB
[ ] 正文 ≥16（移动 mockup ≥14）、行高 1.6-1.75
[ ] 中文有独立声明与回退栈，不是靠西文字体渲染
[ ] 数字等宽；金额/指标右对齐
[ ] 大标题字距为负，正文不为负
[ ] 全大写标题行高 ≥1.0
[ ] 商业字体有 Web 授权，或已换成 OFL 字体
[ ] swap + preload + subset 已做，首屏无布局跳动
```
