(() => {
  const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  // ---- Mobile menu ----
  const menuBtn = document.querySelector('.menu-btn');
  const nav = document.querySelector('.site-nav');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', () => {
      const open = nav.classList.toggle('is-open');
      menuBtn.setAttribute('aria-expanded', String(open));
    });
  }

  // ---- Home hero: live enrichment feed ----
  // Raw lines use the short, cut and coded forms that card networks and acquirers send.
  const TX = [
    { raw: 'POS PUR 448812 LVL SHS DXB MALL 00AE', merchant: 'Level Shoes', logo: 'levelshoes.png', category: 'Shopping', cat: '#F26076', sub: 'Clothing', amount: 'AED 1,032.00', offer: '10% cashback' },
    { raw: 'UBR* PENDING 4029357733 NLD', merchant: 'Uber', logo: 'uber.png', category: 'Transport', cat: '#5A9CB5', sub: 'Ride hailing', amount: 'GBP 18.40' },
    { raw: 'ALSHAYA SBX 0921 NEWYORK 100NY', merchant: 'Starbucks', logo: 'starbucks.png', category: 'Dining', cat: '#FF7444', sub: 'Cafés', amount: 'USD 6.75' },
    { raw: 'NF* 8665797172 LOS GATOS 00012', merchant: 'Netflix', logo: 'netflix.png', category: 'Entertainment', cat: '#A594F9', sub: 'Streaming · Recurring', amount: 'USD 15.49' },
    { raw: 'MAF HYPMKT MOE-0042 DXB ARE', merchant: 'Carrefour', logo: 'carrefour.png', category: 'Groceries', cat: '#E76F2E', sub: 'Supermarkets', amount: 'AED 412.30' },
    { raw: 'EXP*72619940183 ECOM WA 840', merchant: 'Expedia', logo: 'expedia.png', category: 'Travel', cat: '#6F8F72', sub: 'Travel booking', amount: 'USD 642.18', offer: '8% cashback' },
    { raw: 'AMZ*MKTPL SA 2K4LP0 RUH 682', merchant: 'Amazon', logo: 'amazon.png', category: 'Shopping', cat: '#F26076', sub: 'Online marketplaces', amount: 'SAR 249.00' },
    { raw: 'FZ 1418829 T2 DXB AE 784', merchant: 'flydubai', logo: 'flydubai.png', category: 'Travel', cat: '#6F8F72', sub: 'Airlines', amount: 'AED 1,890.00' },
    { raw: 'RBK 3307 MIRDIF CC TID88120', merchant: 'Reebok', logo: 'reebok.png', category: 'Shopping', cat: '#F26076', sub: 'Sportswear', amount: 'AED 329.00', offer: '15% cashback' },
    { raw: 'SPTF AB P2A91F STO 752', merchant: 'Spotify', logo: 'spotify.png', category: 'Entertainment', cat: '#A594F9', sub: 'Music · Recurring', amount: 'EUR 10.99' },
    { raw: 'ALSHAYA BBW 0118 DFC MID4471', merchant: 'Bath & Body Works', logo: 'bbw.png', category: 'Shopping', cat: '#F26076', sub: 'Beauty', amount: 'AED 215.00', offer: '15% cashback' },
    { raw: 'ARLO*ESIM 6531 SGP 702', merchant: 'Airalo', logo: 'airalo.png', category: 'Travel', cat: '#6F8F72', sub: 'Mobile services', amount: 'USD 9.00' },
    { raw: 'FTLKR #2291 PARIS 08 FR 250', merchant: 'Foot Locker', logo: 'footlocker.png', category: 'Shopping', cat: '#F26076', sub: 'Sportswear', amount: 'EUR 129.99' }
  ];
  const feedEl = document.getElementById('feed');
  if (feedEl) {
    const countEl = document.getElementById('feed-count');
    const INTERVAL = 2400;
    const rows = new Map();
    let feed = [4, 3, 2, 1, 0].map((i, k) => ({ ...TX[i], key: k, phase: 'done' }));
    let next = 5, count = 1482113;

    const rowHtml = t => t.phase === 'raw'
      ? `<div class="tx__raw"><b>${esc(t.raw)}</b><span>Enriching…</span></div><span class="tx__amt tx__amt--raw">${esc(t.amount)}</span>`
      : `<div class="tx__who"><img src="img/logos/${esc(t.logo)}" alt=""><div><b>${esc(t.merchant)}</b>
           <span class="tx__meta"><span style="color:${esc(t.cat)};font-weight:600">${esc(t.category)}</span><span>› ${esc(t.sub)}</span></span></div></div>
         <div class="tx__end"><span class="tx__amt">${esc(t.amount)}</span>${t.offer ? `<span class="tx__offer">${esc(t.offer)}</span>` : ''}</div>`;

    const render = () => {
      const live = new Set(feed.map(t => t.key));
      rows.forEach((el, key) => { if (!live.has(key)) { el.remove(); rows.delete(key); } });
      feed.forEach((t, idx) => {
        let el = rows.get(t.key);
        if (!el) { el = document.createElement('div'); el.className = 'tx'; rows.set(t.key, el); }
        if (el.dataset.phase !== t.phase) { el.innerHTML = rowHtml(t); el.dataset.phase = t.phase; }
        el.classList.toggle('tx--top', idx === 0);
        el.style.opacity = String(1 - idx * 0.08);
        if (feedEl.children[idx] !== el) feedEl.insertBefore(el, feedEl.children[idx] || null);
      });
      countEl.textContent = count.toLocaleString('en-US');
    };
    const schedule = () => setTimeout(() => {
      const key = Date.now();
      feed = [{ ...TX[next % TX.length], key, phase: 'raw' }, ...feed].slice(0, 5);
      next += 1;
      count += 37 + Math.floor(Math.random() * 60);
      render();
      setTimeout(() => { feed = feed.map(t => (t.key === key ? { ...t, phase: 'done' } : t)); render(); }, 1100);
      schedule();
    }, INTERVAL);
    render();
    schedule();
  }

  // ---- Tabs ----
  document.querySelectorAll('[role="tablist"]').forEach(list => {
    const tabs = [...list.querySelectorAll('[role="tab"]')];
    const select = (i, focus) => {
      tabs.forEach((t, k) => {
        t.setAttribute('aria-selected', String(k === i));
        t.tabIndex = k === i ? 0 : -1;
        document.getElementById(t.getAttribute('aria-controls')).hidden = k !== i;
      });
      if (focus) tabs[i].focus();
    };
    tabs.forEach((t, i) => {
      t.addEventListener('click', () => select(i));
      t.addEventListener('keydown', e => {
        if (e.key === 'ArrowRight') select((i + 1) % tabs.length, true);
        if (e.key === 'ArrowLeft') select((i + tabs.length - 1) % tabs.length, true);
      });
    });
  });

  // ---- Contact form: checks the fields, then opens an email draft ----
  const form = document.getElementById('contact-form');
  if (form) {
    const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
    const bad = (name, isBad) => { form.querySelector(`[data-field="${name}"]`).classList.toggle('is-bad', isBad); return isBad; };
    form.addEventListener('submit', e => {
      e.preventDefault();
      const v = n => form.elements[n].value.trim();
      const products = [...form.querySelectorAll('input[name=product]:checked')].map(c => c.value);
      const errors = [
        bad('first', !v('first')), bad('last', !v('last')), bad('email', !EMAIL.test(v('email'))),
        bad('company', !v('company')), bad('product', products.length === 0)
      ];
      if (errors.some(Boolean)) { form.querySelector('.is-bad input, .is-bad select').focus(); return; }
      const body = [
        `Name: ${v('first')} ${v('last')}`, `Work email: ${v('email')}`, `Company: ${v('company')}`,
        `Job title: ${v('title')}`, `Country: ${v('country')}`, `Products: ${products.join(', ')}`, '', v('notes')
      ].join('\n');
      window.location.href = 'mailto:hello@lunedata.io?subject=' + encodeURIComponent('Demo request: ' + v('company')) + '&body=' + encodeURIComponent(body);
      document.getElementById('form-done').hidden = false;
    });
  }
})();
