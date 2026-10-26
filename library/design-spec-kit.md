# 设计规范落地工具箱（Design Spec Kit）

> 目的：**从"描述"走到"代码"**。一份可交付的规范必须能回答：用什么令牌、有哪些组件、每个组件什么状态、各端怎么变、验收怎么判。
> 用法：选模板（`ui-templates.md`）→ 查术语（`ui-glossary.md`）→ 填本文件五件套 → 写码。

---

## 一、五件套（缺一件就不算"能落地"）

| # | 产物 | 内容 | 不合格的样子 |
|---|---|---|---|
| 1 | **Design Spec** | 8 组令牌（情绪/色/字/间距/圆角/阴影/网格/动效） | "配色高级、留白充足" |
| 2 | **组件清单** | 每个组件的变体 × 尺寸 × 状态 | 只写"按钮" |
| 3 | **状态矩阵** | 每组件 × 8 态（含空/错/加载） | 只有 default |
| 4 | **响应式表** | 4 断点下的列数/字号/间距/隐藏项 | "响应式适配" |
| 5 | **代码骨架** | 令牌 + 区块结构 + 关键动效注释 | 只给文字方案 |

---

## 二、令牌骨架（可直接复制）

```css
:root{
  /* 色：底不用纯白，主色 L* 28–38% */
  --bg:#F7F6F3; --surface:#FFFFFF; --surface-2:#F0EDE7;
  --ink:#1C1B19; --ink-2:#46443F; --muted:#6B6A66;
  --line:rgba(28,27,25,.10); --line-strong:rgba(28,27,25,.20);
  --primary:#1F4E46; --primary-ink:#FFFFFF;
  --accent:#B4552F;  --success:#2F6B57; --warn:#7A4A16; --danger:#A9502F;

  /* 间距 4/8 */
  --s1:4px; --s2:8px; --s3:12px; --s4:16px; --s6:24px;
  --s8:32px; --s12:48px; --s16:64px; --s24:96px;

  /* 圆角 ≤3 档 */
  --r1:8px; --r2:12px; --r3:20px;

  /* 阴影 ≤3 档，带色 */
  --sh1:0 1px 2px rgba(28,27,25,.05), 0 1px 3px rgba(28,27,25,.06);
  --sh2:0 4px 10px -2px rgba(28,27,25,.06), 0 12px 24px -8px rgba(28,27,25,.10);
  --sh3:0 12px 32px -8px rgba(28,27,25,.14), 0 32px 64px -24px rgba(28,27,25,.18);

  /* 字阶 1.25 */
  --t1:13px; --t2:16px; --t3:20px; --t4:25px; --t5:31px; --t6:39px; --t7:49px;

  /* 动效 */
  --d1:120ms; --d2:180ms; --d3:240ms; --d4:320ms; --d5:420ms;
  --ease:cubic-bezier(.22,1,.36,1);
}
```

---

## 三、六个基础区块（拼页面用这些，不重写）

### 1 导航（桌面）
```html
<header class="nav"><div class="wrap">
  <b class="brand">产品名</b>
  <nav><a>功能</a><a>定价</a><a>文档</a></nav>
  <a class="btn btn-primary">开始使用</a>
</div></header>
```
```css
.nav{position:sticky;top:0;z-index:30;background:color-mix(in srgb,var(--bg) 92%,transparent);
  backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.nav .wrap{display:flex;align-items:center;gap:32px;height:64px}
.nav nav{margin-left:auto;display:flex;gap:24px}
.nav a{color:var(--ink-2);text-decoration:none;font-size:14px}
.nav a:hover{color:var(--ink)}
.btn{min-height:44px;padding:0 20px;border-radius:var(--r1);font-weight:600;
  display:inline-flex;align-items:center;text-decoration:none}
.btn-primary{background:var(--primary);color:var(--primary-ink)} /* 背景与文字同规则 */
.btn-primary:active{transform:scale(.97)}
.btn:focus-visible{outline:2px solid var(--primary);outline-offset:2px}
```

### 2 Hero（7:5 非对称）
```html
<section class="hero wrap">
  <div><h1>一句主张，最多 15 字</h1><p class="lede">一句解释，≤38 字。</p>
    <div class="row"><a class="btn btn-primary">主操作</a><a class="btn">次操作</a></div></div>
  <aside class="proof">证据（截图/数据/卡）</aside>
</section>
```
```css
.hero{display:grid;grid-template-columns:7fr 5fr;gap:64px;padding:96px 0 64px}
.hero h1{font-size:clamp(36px,4.4vw,49px);line-height:1.1;letter-spacing:-.03em}
.lede{margin-top:24px;font-size:18px;color:var(--ink-2);max-width:38ch;line-height:1.7}
.row{display:flex;gap:12px;margin-top:32px}
@media (max-width:1024px){.hero{grid-template-columns:1fr;gap:40px;padding:64px 0 40px}}
```

### 3 列表（带状态）
```html
<ul class="list">
  <li class="item"><span class="name">条目</span><span class="meta">说明</span>
    <span class="tag">状态</span></li>
</ul>
```
```css
.item{display:flex;align-items:center;gap:12px;min-height:56px;padding:0 16px;
  border-bottom:1px solid var(--line);min-width:0}
.item .name{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.item:hover{background:var(--surface-2)}
.tag{font-size:12px;padding:2px 8px;border-radius:6px;
  background:rgba(31,78,70,.10);color:#17423A}
```

### 4 表单（8 态）
```html
<label class="field"><span>邮箱</span>
  <input type="email" placeholder="you@example.com" aria-describedby="e1">
  <em id="e1" class="err" hidden>请输入有效邮箱</em></label>
```
```css
.field{display:block;margin-bottom:20px}
.field>span{display:block;font-size:13px;color:var(--ink-2);margin-bottom:6px}
input{width:100%;min-height:44px;padding:0 12px;font-size:16px;color:var(--ink);
  background:var(--surface);border:1px solid var(--line-strong);border-radius:var(--r1)}
input:focus-visible{outline:2px solid var(--primary);outline-offset:1px;border-color:var(--primary)}
input[aria-invalid="true"]{border-color:var(--danger)}
.err{display:block;font-size:12px;color:var(--danger);margin-top:4px}
```

### 5 空状态（必须给恢复路径）
```html
<div class="empty"><b>还没有保存的视图</b><p>筛选后可以存成视图，下次一键打开。</p>
  <button class="btn btn-primary">新建视图</button></div>
```
```css
.empty{padding:48px 24px;text-align:center}
.empty b{display:block;font-size:16px;margin-bottom:6px}
.empty p{font-size:13px;color:var(--muted);max-width:28ch;margin:0 auto 16px}
```

### 6 吸底操作（安全区）
```css
.bar{position:fixed;left:0;right:0;bottom:0;z-index:40;display:flex;gap:10px;
  padding:10px 16px calc(10px + env(safe-area-inset-bottom));
  background:color-mix(in srgb,var(--surface) 94%,transparent);border-top:1px solid var(--line)}
body{padding-bottom:calc(88px + env(safe-area-inset-bottom))} /* 必须预留 */
```

---

## 四、状态矩阵模板

```markdown
| 组件 | default | hover | active | focus-visible | disabled | loading | empty | error |
|---|---|---|---|---|---|---|---|---|
| 主按钮 | 实底 | 亮度+6% | scale.97 | 2px ring | opacity.45 | 转圈+锁定宽 | — | — |
| 列表 | 行 56 | 底 surface-2 | — | 行内焦点 | — | 骨架 3 行 | 空态文案 | 重试条 |
| 输入 | 描边 | 描边加深 | — | ring | 灰底 | — | — | 红框+文案 |
```

## 五、响应式表模板

```markdown
| 断点 | 列数 | 正文字号 | 区块间距 | 隐藏/折叠 |
|---|---|---|---|---|
| ≤640 | 4 | 16 | 48 | 导航收进菜单，侧栏隐藏 |
| 641–1024 | 8 | 16 | 64 | 侧栏折叠为图标 |
| 1025–1440 | 12 | 16 | 96 | — |
| >1440 | 12 | 17 | 96 | 内容居中，最大 1440 |
```

---

## 六、从规范到代码的三步

```
1 token 层   把 §二 的令牌落进 :root + 深色覆盖；跑 audit_contrast（0 违规）
2 组件层     用 §三 的六个区块搭页面，只调变体与状态，不改内部
3 页面层     按模板骨架拼装；补状态（空/错/加载）；加 1 个记忆点
```

**验收**
```bash
python scripts/audit_all.py page.html          # 结构与对比度
python scripts/term_lookup.py "太挤"            # 回到术语确认改法
# 浏览器控制台：粘贴 scripts/contrast_runtime.js → 0 违规
```

---

## 七、"只描述不落地"的五个信号

| 信号 | 说明 | 怎么改 |
|---|---|---|
| 出现"高级感/呼吸感/科技感" | 无法验收 | 换成具体参数（色值/px/ms） |
| 只写组件名，没有变体与状态 | 实现时全靠猜 | 补 §四 状态矩阵 |
| 没有空态/错误态 | 上线必崩 | 每个异步区补两态文案 |
| 没有断点行为 | 移动端挤压/溢出 | 补 §五 响应式表 |
| 没有动效参数 | 开发者自由发挥 | 补时长/缓动/触发/降级四要素 |
