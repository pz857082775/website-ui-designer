# 四端平台提示词矩阵（PC / H5 / 小程序 / APP）

同一套设计令牌，四种落地的**提示词差异段**。生成前先问/先判断平台，把对应段落加进主提示词。

---

## PC 网站（桌面 Web）

```
平台：桌面 Web，1440px 设计基准，兼容 1024-1920。
- 多列网格（12 列），内容最大宽 1200px 居中
- 必须有 hover 态：按钮上移、卡片浮起、链接下划线动画
- 导航：顶部固定或 sticky，毛玻璃或实色，含下拉菜单的 hover 展开
- 动效可用 ScrollTrigger 叙事（pin/scrub/parallax），克制使用
- 键盘可达：所有交互有 focus-visible 样式
```

## H5（移动端 Web）

```
平台：移动端 H5，375×812 设计基准，兼容 320-430。
- 单列布局，禁止横向滚动；字号正文 ≥ 15px（移动端可读下限）
- 拇指热区：所有可点元素 ≥ 44×44px，间距 ≥ 8px
- 主操作吸底（sticky bottom bar）或固定在首屏；导航收成汉堡菜单或底部 Tab（≤5 个）
- 图片懒加载，首屏资源 ≤ 200KB（提示词里要求标注资源体积）
- 关闭重动效：无 pin/scrub，入场动画时长 ≤ 0.4s
- 适配 iPhone 安全区：env(safe-area-inset-bottom)
```

## 微信小程序

```
平台：微信小程序，WXSS + rpx，375pt 设计基准（2 倍图 @2x/@3x）。
- 尺寸用 rpx（750rpx = 100% 宽），间距字号全部 rpx 换算
- 自定义导航栏：预留状态栏高度（statusBarHeight）+ capsule 按钮位置
- 页面结构建议：index（首页）/ list / detail / profile + 自定义 tabBar（≤5 项，图标 81px）
- 组件用原生组件优先（scroll-view / swiper / picker），避免过重复合组件
- 交互遵循微信习惯：下拉刷新、加载更多、toast/modal 用原生 API
- 性能意识：setData 最小化、图片懒加载、分包（主包 ≤ 1.5MB 写进提示词约束）
- 视觉基线可参考微信设计规范，但品牌色和排版按 DESIGN.md 令牌
```

## APP（iOS / Android 混合或原生皮肤）

```
平台：移动 APP 界面，iOS + Android 双平台一致体验。
- 遵守平台导航模式：iOS 大标题+左滑返回，Android 底部导航+右上动作
- 安全区：顶部刘海/底部 home 指示条全部预留；可点元素 ≥ 44pt
- 手势：左滑返回、下拉刷新、上拉加载；不与横向滚动冲突
- 暗色模式：同一套令牌出 light/dark 两份（颜色令牌 ×2，间距形状不变）
- 列表/表单/弹层/Toast 按平台规范（iOS ActionSheet / Android BottomSheet）
- 状态全覆盖：加载骨架屏、空状态、错误态、断网态——提示词里逐状态列出
```

---

## 平台差异速查

| 维度 | PC | H5 | 小程序 | APP |
|---|---|---|---|---|
| 布局 | 多列网格 | 单列 | 单列 rpx | 单列 + 平台导航 |
| 点击热区 | 32px+ | 44px+ | 44px+ | 44pt+ |
| 主操作位置 | 首屏右侧/CTA 区 | 吸底栏 | 首屏 + tabBar | 首屏 + 底部导航 |
| 动效强度 | 强（可 scrub） | 轻（≤0.4s） | 轻（原生为主） | 中（跟手手势） |
| 适配单位 | px + 断点 | vw/rem + 断点 | rpx | pt + 安全区 |
| 暗色模式 | 建议 | 建议 | 建议 | 必须 |
| 空/错状态 | 必须有 | 必须有 | 必须有 | 必须有 |
| 旋钮默认 | CRAFT 8 / MOTION 6 / DENSITY 5 / VARIANCE 7 | 7 / 3 / 4 / 4 | 7 / 3 / 5 / 3 | 8 / 6 / 4 / 3 |

---

## 移动端原生化七项（H5 / 小程序 / APP 必查）

来自 `emilkowalski/skills` 的 mobile-native。缺任何一条都会"像网页不像应用"：

```
1. 粘滞 hover —— 触屏上 hover 会残留：所有 hover 规则包进 @media (hover:hover)
2. 点击高亮 —— -webkit-tap-highlight-color: transparent（配 :active 反馈）
3. 100vh 陷阱 —— 地址栏吃掉高度：用 100dvh / svh，不用 100vh
4. 输入缩放 —— iOS 焦点放大页面：输入框字号 ≥16px
5. 点击延迟 —— 用 pointerdown 做即时反馈，不等 click
6. 安全区 —— env(safe-area-inset-top/bottom) 全量预留（吸底栏必须）
7. 滚动链 —— 弹层/横向滑动加 overscroll-behavior: contain，防穿透
```

对应提示词写法（直接贴进第 7 段平台段）：
```
移动端原生化：hover 规则全部包在 @media (hover:hover) 内；
-webkit-tap-highlight-color: transparent；高度用 100dvh；
输入框字号 ≥16px；点击反馈用 pointerdown；吸底栏预留 safe-area-inset-bottom；
弹层 overscroll-behavior: contain。禁止 <16px 输入字号、禁止裸 100vh。
```



---

## 游戏端（第五端）

游戏 UI 与网页 UI 的差别不在视觉，而在**帧预算与输入**。

| 维度 | 规则 |
|---|---|
| 帧预算 | 60fps = **16.6ms/帧**；UI 动画与游戏逻辑共享预算，UI 常驻动效 ≤2 处 |
| 分辨率 | 以 1920×1080 为基准，按 `scale = height/1080` 缩放；HUD 字号在 1080p 下 **≥14px**，且**不随场景缩放** |
| 安全区 | HUD 距屏幕边缘 **≥5%**（主机/TV 需 ≥8%）；刘海与圆角屏用 `env(safe-area-inset-*)` |
| 输入 | 至少支持触屏/键鼠/手柄中的**两种**；所有可交互元素必须有焦点态（手柄导航）与焦点顺序 |
| 命中区 | 触屏 ≥ 屏高 6%（约 44px@720p）；手柄焦点框 ≥2px 且与背景对比 ≥3:1 |
| 动效 | 单次 ≤400ms；循环 ≤2 处；**禁止**布局动画（会触发布局重算）；只动 transform/opacity |
| 暂停 | 失焦/暂停必须冻结动画与计时（`visibilitychange` + 游戏状态机） |
| 可读性 | 红绿不可作为唯一区分（过色弱模拟）；深色场景下文字需 1px 描边或 scrim |
| 字体 | 游戏内嵌字体需确认授权；中文优先位图字体或 SDF，避免小字号糊 |

**禁止**：hover 交互（无鼠标）、依赖 `backdrop-filter`（主机/移动 GPU 开销大）、每帧改 DOM 样式（用 canvas 或批量 transform）。
