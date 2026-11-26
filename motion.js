(() => {
  const root = document.documentElement;
  const calm = matchMedia('(prefers-reduced-motion: reduce)').matches || /[?&]calm\b/.test(location.search);
  if (calm) root.classList.add('calm');
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* the choice lasts for this page only */ } }
  };

  // ---- Headline: each word arrives in turn ----
  const split = h1 => {
    if (h1.dataset.split) return;
    h1.dataset.split = '1';
    let i = 0;
    const walk = node => [...node.childNodes].forEach(n => {
      if (n.nodeType === 3) {
        const frag = document.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(part => {
          if (!part.trim()) { frag.append(part); return; }
          const w = document.createElement('span');
          w.className = 'w'; w.style.setProperty('--i', i++); w.textContent = part;
          frag.append(w);
        });
        n.replaceWith(frag);
      } else if (n.nodeType === 1 && n.tagName !== 'BR') walk(n);
    });
    walk(h1);
  };
  if (!calm) document.querySelectorAll('.hv h1').forEach(split);

  // ---- Hero options ----
  const opts = document.querySelector('.opts:not(.bopts)');
  if (opts) {
    const show = h => {
      root.dataset.hero = h;
      opts.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.hero === h)));
    };
    show(root.dataset.hero || 'a');
    opts.addEventListener('click', e => {
      const b = e.target.closest('button[data-hero]');
      if (!b) return;
      show(b.dataset.hero); store.set('lune-hero', b.dataset.hero);
      window.scrollTo({ top: 0, behavior: calm ? 'auto' : 'smooth' });
    });
  }

  // ---- Button colour options (review control) ----
  const bopts = document.querySelector('.bopts');
  if (bopts) {
    const showB = v => { root.dataset.btn = v; bopts.querySelectorAll('button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.btn === v))); };
    showB(root.dataset.btn || 'ink');
    bopts.addEventListener('click', e => { const b = e.target.closest('button[data-btn]'); if (b) { showB(b.dataset.btn); store.set('lune-btn', b.dataset.btn); } });
  }

  // ---- Spotlight on the stack map ----
  document.querySelectorAll('.sm').forEach(c => c.addEventListener('pointermove', e => {
    const r = c.getBoundingClientRect();
    c.style.setProperty('--mx', `${e.clientX - r.left}px`); c.style.setProperty('--my', `${e.clientY - r.top}px`);
  }));

  // ---- Numbers ----
  const fmt = (n, dec) => n.toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec });
  const count = (el, ms = 900) => {
    const to = parseFloat(el.dataset.count), from = parseFloat(el.dataset.from || '0');
    const dec = (el.dataset.count.split('.')[1] || '').length;
    if (calm) { el.textContent = fmt(to, dec); return; }
    const t0 = performance.now();
    const tick = t => {
      const k = Math.min(1, (t - t0) / ms), eased = 1 - Math.pow(1 - k, 3);
      el.textContent = fmt(from + (to - from) * eased, dec);
      if (k < 1 && el.classList.contains('on')) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  };
  const GLYPHS = 'ABCDEFGHJKLMNPQRSTUVWXYZ0123456789*#';
  const scramble = el => {
    const text = el.dataset.text || (el.dataset.text = el.textContent);
    if (calm) { el.textContent = text; return; }
    const t0 = performance.now(), ms = 520;
    const tick = t => {
      const k = Math.min(1, (t - t0) / ms), keep = Math.floor(text.length * k);
      el.textContent = text.slice(0, keep) + [...text.slice(keep)].map(ch => (ch === ' ' ? ' ' : GLYPHS[Math.floor(Math.random() * GLYPHS.length)])).join('');
      if (k < 1) requestAnimationFrame(tick); else el.textContent = text;
    };
    requestAnimationFrame(tick);
  };

  // ---- Product animations: one step at a time ----
  const player = anim => {
    const steps = anim.dataset.steps.split(',').map(Number);
    const parts = [...anim.querySelectorAll('[data-at]')];
    let i = -1, timer = null;
    const apply = n => parts.forEach(el => {
      const at = +el.dataset.at, until = el.dataset.until;
      const on = n >= at && (until === undefined || n < +until);
      if (on === el.classList.contains('on')) return;
      el.classList.toggle('on', on);
      if (el.dataset.count) { if (on) count(el); else el.textContent = fmt(parseFloat(el.dataset.from || '0'), (el.dataset.count.split('.')[1] || '').length); }
      if (on) el.querySelectorAll('[data-scramble]').forEach(scramble);
    });
    const next = () => { i = (i + 1) % steps.length; apply(i); timer = setTimeout(next, steps[i]); };
    return {
      start() { if (calm) { apply(+(anim.dataset.rest || steps.length - 1)); return; } if (!timer) next(); },
      stop() { clearTimeout(timer); timer = null; }
    };
  };
  document.querySelectorAll('.stage').forEach(stage => {
    const key = 'lune-anim-' + stage.dataset.animKey;
    const players = {};
    stage.querySelectorAll('.anim').forEach(a => { players[a.dataset.v] = player(a); });
    let shown = store.get(key) || stage.dataset.default || '1', visible = false;
    if (shown !== '2' || !players['2']) shown = '1';
    const show = v => {
      Object.values(players).forEach(p => p.stop());
      shown = v; stage.dataset.show = v;
      stage.querySelectorAll('.seg__b').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.v === v)));
      if (visible) players[v].start();
    };
    stage.querySelectorAll('.seg__b').forEach(b => b.addEventListener('click', () => { show(b.dataset.v); store.set(key, b.dataset.v); }));
    show(shown);
    new IntersectionObserver(es => {
      visible = es[0].isIntersecting;
      if (visible) players[shown].start(); else players[shown].stop();
    }, { threshold: 0.25 }).observe(stage);
  });

  // ---- Proof numbers count one time ----
  document.querySelectorAll('.stats b').forEach(b => {
    const m = b.textContent.match(/^([\d.]+)(.*)$/);
    if (!m || calm) return;
    const to = parseFloat(m[1]), dec = (m[1].split('.')[1] || '').length, tail = m[2];
    new IntersectionObserver((es, io) => {
      if (!es[0].isIntersecting) return;
      io.disconnect();
      const t0 = performance.now();
      const tick = t => { const k = Math.min(1, (t - t0) / 1100); b.textContent = (to * (1 - Math.pow(1 - k, 3))).toFixed(dec) + tail; if (k < 1) requestAnimationFrame(tick); else b.textContent = m[0]; };
      requestAnimationFrame(tick);
    }, { threshold: 0.6 }).observe(b);
  });

  // ---- Scroll: parallax, and the current step in the main menu ----
  const plx = calm ? [] : [...document.querySelectorAll('[data-plx]')];
  const journey = document.querySelector('.journey');
  const STEP = { enrich: ['enrich.html'], lunehub: ['enrich.html'], analytics: ['analytics.html'], app: ['expenses.html', 'cashflow.html'], pulse: ['pulse.html'] };
  const chapters = journey ? [...journey.querySelectorAll('.chapter')] : [];
  const links = [...document.querySelectorAll('.site-nav a')];
  const head = document.querySelector('.site-head');
  let queued = false;
  const frame = () => {
    queued = false;
    const vh = innerHeight;
    if (innerWidth > 760) plx.forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.bottom < -200 || r.top > vh + 200) return;
      const off = (r.top + r.height / 2 - vh / 2) * -parseFloat(el.dataset.plx);
      el.style.translate = `0 ${off.toFixed(1)}px`;
    });
    else plx.forEach(el => { el.style.translate = ''; });
    if (journey) {
      const r = journey.getBoundingClientRect();
      const inside = r.top < vh * 0.45 && r.bottom > vh * 0.45;
      let now = null;
      if (inside) chapters.forEach(c => { if (c.getBoundingClientRect().top < vh * 0.45) now = c.id; });
      const here = now ? STEP[now] : [];
      links.forEach(a => a.classList.toggle('is-here', here.includes(a.getAttribute('href'))));
      head.style.setProperty('--p', inside ? Math.max(0, Math.min(1, (vh * 0.45 - r.top) / r.height)).toFixed(3) : (r.bottom <= vh * 0.45 ? 1 : 0));
    }
  };
  const onScroll = () => { if (!queued) { queued = true; requestAnimationFrame(frame); } };
  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', onScroll);
  frame();
})();
