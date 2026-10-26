/**
 * contrast_runtime.js — 浏览器端"真实计算样式"对比度检查
 *
 * 为什么需要它：token 级审计（audit_contrast.py）只能查令牌配对，
 * 查不出「同一元素被两个选择器分别设了背景与文字色」这类特异性覆盖
 * （真实案例：.nav a 的字色覆盖了 .btn-primary 的白字，按钮变成隐形）。
 *
 * 用法：把整段贴进浏览器控制台（页面已加载），按回车。
 * 输出：违规列表 + 每条的 元素/文字/背景/对比度/字号。
 * 合格：打印 "PASS 0 violations"。
 */
(function contrastRuntime() {
  function toRGBA(str) {
    const m = str.match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const p = m[1].split(',').map(Number);
    return { r: p[0], g: p[1], b: p[2], a: p[3] === undefined ? 1 : p[3] };
  }
  function lum({ r, g, b }) {
    const f = (v) => { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  }
  function ratio(a, b) {
    const l1 = lum(a), l2 = lum(b);
    const hi = Math.max(l1, l2), lo = Math.min(l1, l2);
    return (hi + 0.05) / (lo + 0.05);
  }
  function blend(fg, bg) {
    const a = fg.a;
    return {
      r: Math.round(fg.r * a + bg.r * (1 - a)),
      g: Math.round(fg.g * a + bg.g * (1 - a)),
      b: Math.round(fg.b * a + bg.b * (1 - a)),
      a: 1,
    };
  }
  function effectiveBg(el) {
    let node = el;
    while (node && node !== document.documentElement) {
      const cs = getComputedStyle(node);
      const c = toRGBA(cs.backgroundColor);
      if (c && c.a > 0.01) {
        let base = c;
        if (c.a < 1) {
          let p = node.parentElement, under = null;
          while (p) {
            const pc = toRGBA(getComputedStyle(p).backgroundColor);
            if (pc && pc.a > 0.01) { under = pc.a < 1 ? blend(pc, { r: 255, g: 255, b: 255, a: 1 }) : pc; break; }
            p = p.parentElement;
          }
          base = blend(c, under || { r: 255, g: 255, b: 255, a: 1 });
        }
        if (getComputedStyle(node).backgroundImage !== 'none' && node === el) {
          /* 有背景图/渐变时无法精确计算，跳过并记账 */
          return null;
        }
        return base;
      }
      node = node.parentElement;
    }
    return { r: 255, g: 255, b: 255, a: 1 };
  }

  const bad = [], skipped = [];
  document.querySelectorAll('body *').forEach((el) => {
    if (el.closest('script,style,svg')) return;
    const rect = el.getBoundingClientRect();
    if (rect.width < 4 || rect.height < 4) return;

    /* 只看直接含文本的元素 */
    const hasText = Array.from(el.childNodes).some(
      (n) => n.nodeType === 3 && n.textContent.trim().length > 0
    );
    if (!hasText) return;

    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none' || parseFloat(cs.opacity) < 0.1) return;

    const fg = toRGBA(cs.color);
    const bg = effectiveBg(el);
    if (!fg || !bg) { skipped.push(el); return; }

    const fgSolid = fg.a < 1 ? blend(fg, bg) : fg;
    const r = ratio(fgSolid, bg);
    const size = parseFloat(cs.fontSize);
    const bold = parseInt(cs.fontWeight, 10) >= 700;
    const large = size >= 24 || (size >= 18.66 && bold);
    const min = large ? 3 : 4.5;

    if (r < min) {
      bad.push({
        el: el.className ? `${el.tagName.toLowerCase()}.${String(el.className).split(' ')[0]}` : el.tagName.toLowerCase(),
        text: (el.textContent || '').trim().slice(0, 24),
        color: cs.color,
        bg: `rgb(${bg.r},${bg.g},${bg.b})`,
        ratio: +r.toFixed(2),
        need: min,
        size,
      });
    }
  });

  if (bad.length === 0) {
    console.log(`%cPASS 0 violations（已检查 ${document.querySelectorAll('body *').length} 个元素）`, 'color:#17845B;font-weight:600');
  } else {
    console.log(`%cFAIL ${bad.length} 处文字不可读`, 'color:#C0342B;font-weight:700');
    console.table(bad);
    console.log('提示：常见原因是「一个选择器设背景、另一个选择器设文字色」的覆盖（特异性陷阱）。');
  }
  if (skipped.length) console.log(`跳过 ${skipped.length} 个背景为图片/渐变的元素（需人工目测）`);
})();
