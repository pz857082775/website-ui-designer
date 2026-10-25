# GSAP 动效提示词库（按场景分类，可直接填入主提示词第 6 段）

> **状态（v2.3.0）：实现层参考。** 动效「该不该做、做哪类、多久」看 **motion-decision-table**；参数与库选型看 **motion-spec**。本文件只提供代码片段。

来自 `greensock/gsap-skills`（官方）+ 社区 vibe-animation 经验。每条都是"自包含"的：说明感觉 + 元素 + 机制 + 参数意图。

## 铁律（每条提示词都适用）

1. 写 "GSAP 3.x"，点名禁止：TweenMax / TimelineMax / .staggerTo() / 旧 ease 字符串（Power2.easeInOut）
2. `gsap.registerPlugin(ScrollTrigger)` 必须出现在代码里
3. 只动 `x / y / scale / rotation / autoAlpha`（transform + opacity），禁止 left/top/width/height
4. UI 动效时长 0.2-0.6s，入场 0.6-0.9s；超过 1s 的常规交互像坏了
5. 必须给 `prefers-reduced-motion` 降级路径
6. React/Next：`useGSAP(() => {...}, { scope: ref })` 或 `gsap.context()` + revert

## 1. 首屏入场（Hero）

```
"让 Hero 元素按 标题→副文案→按钮→视觉 的顺序依次浮现：
每个元素从下方 40px 处以 autoAlpha 0→1 淡入上移，
duration 0.8s，ease power3.out，stagger 0.1s。
要求：内容必须在动画开始前已在 DOM 中（不允许 JS 注入后才可见）。"
```

## 2. 滚动揭示（Scroll Reveal）

```
"当 .feature-card 进入视口 80% 时，卡片从 y:40、autoAlpha:0 浮现，
duration 0.6s，power3.out，stagger 0.08s（每张错开）。
toggleActions: 'play none none none'（只播一次，不来回抽风）。"
```

## 3. 数字滚动（Count-up）

```
".stat-number 进入视口时从 0 滚动到目标值，duration 1.5s，
snap 到整数，once: true。数字必须真实可验证，禁止虚荣数字。"
```

## 4. 滚动叙事（Pin + Scrub）

```
"故事区块钉在视口顶部（pin），滚动 2 屏高度的距离内，
按 scrub:1 平滑推进三幕：主张→证据→CTA。
禁止 scroll-jacking：滚动始终由用户控制，只映射进度。"
```

## 5. 视差（Parallax）

```
"主视觉图片以 0.3 倍速随滚动上移（yPercent: -15，scrub），
背景色块以 0.1 倍速移动，制造三层景深。移动端关闭视差。"
```

## 6. 文字效果

```
"大标题按行揭示：每行从 y:100% 的容器里推上来，
clip 遮罩不动、duration 0.7s，stagger 0.12s。
（用 SplitText 或手动按行拆分，标注若 SplitText 不可用就用手动 span 拆分）。"
```

## 7. 悬停反馈

```
"主按钮 hover 时 scale 1.03、阴影加深，duration 0.25s power2.out；
按下时 scale 0.97。所有过渡必须同时支持鼠标和键盘 focus。"
```

## 8. 环境氛围（Ambient，谨慎用）

```
"一个 6-8s 的无限循环 float 动画（y: ±8px，sine.inOut）只允许用于
一个装饰元素，禁止满屏漂浮。reduced-motion 时停止。"
```

## 常见翻车点（生成后自查）

| 症状 | 原因 | 修法 |
|---|---|---|
| **整页空白，只有外壳** | CSS 预先 `.anim{opacity:0}` 隐藏内容 + GSAP CDN 加载失败 → 脚本 return，内容永久隐身 | 用下方「正确兜底模式」，禁止 CSS 预隐藏 |
| 刷新后元素闪一下才出现 | 无预隐藏也无 gsap.set | 接受（内容优先）；或在 gsap 确认加载后再 set 初始态 |
| ScrollTrigger 不触发 | trigger 元素高度为 0 或在 overflow 容器里 | 确保 trigger 有高度；嵌套滚动需 scroller 配置 |
| 路由切换后动画重复/泄漏 | 没清理 | useGSAP scope 或 gsap.context().revert() |
| 图片加载后位置错乱 | 布局变化未刷新 | 图片 onload 后 ScrollTrigger.refresh() |
| 动画卡顿 | 动了布局属性 / 同时动画太多 | 只动 transform/opacity；减少并发层数 |

## ⚠️ 正确兜底模式（本技能强制，踩过坑）

**错误写法（会导致 CDN 失败时整页空白）**
```html
<style>.js-anim .anim{opacity:0}</style>          <!-- ① 一开始就隐藏 -->
<script>document.documentElement.classList.add('js-anim')</script>  <!-- ② 同步加类 -->
<script src="gsap-cdn"></script>
<script>
  if(!window.gsap) return;   // ③ CDN 挂了 → 永远不执行 → 内容永久隐藏
</script>
```

**正确写法：默认可见，只让 gsap 自己设初始态**
```html
<!-- 不要写任何 .anim{opacity:0} -->
<script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/ScrollTrigger.min.js"></script>
<script>
(function(){
  var reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!window.gsap || reduced) return;   // 直接返回 → 内容本来就可见，页面完整
  gsap.registerPlugin(ScrollTrigger);
  gsap.from(".anim", { y:14, autoAlpha:0, duration:.4, ease:"power3.out", stagger:.055 });
})();
</script>
```

要点：
1. `gsap.from()` 自己会在动画开始时设置初始态，**不需要 CSS 预隐藏**
2. 判断放在**统一守卫**里，`return` 是安全出口（页面完整，只是没有动画）
3. 若坚持零闪烁，只能在 `if (window.gsap)` 分支内才加隐藏类，绝不无条件加
4. 交付前跑 `scripts/preflight.py`，E1 项就是查这个坑
