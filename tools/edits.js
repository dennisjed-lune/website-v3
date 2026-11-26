// Sample data for the real product snapshots. Runs in the page before capture.
(() => {
  const L = 'file:///Users/dennisjedburgh/code/product/lune-home/img/logos/';
  const leaves = el => { const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); const o = []; let n; while ((n = w.nextNode())) if (n.nodeValue.replace(/\u00a0/g, ' ').trim()) o.push(n); return o; };
  const setText = (n, v) => { if (v == null) return; n.nodeValue = v; const p = n.parentElement; if (p && p.hasAttribute('title')) p.setAttribute('title', v); };
  const fillRows = rows => { const trs = (rows.sel ? [...document.querySelectorAll('[data-slot="logo-fetcher"]')].filter(e => !e.closest('h1,header') && !e.parentElement.querySelector('h1')).map(e => { let r = e; while (r.parentElement && leaves(r).length < rows.sel) r = r.parentElement; return r; }) : [...document.querySelectorAll('tbody tr')].filter(tr => leaves(tr).length > 2)); const log = [];
    rows.forEach((r, i) => { const tr = trs[i]; if (!tr) return; const t = leaves(tr); log.push(t.length);
      r.t.forEach((v, k) => t[k] && setText(t[k], v)); if (r.logo) { const im = tr.querySelector('img'); if (im) { im.src = r.logo.startsWith('http') ? r.logo : L + r.logo; im.style.objectFit = 'contain'; im.style.background = '#fff'; } } });
    if (!rows.sel) trs.slice(rows.length).forEach(tr => tr.remove()); return log; };
  const swap = map => { const used = {}; leaves(document.body).forEach(n => { const k = n.nodeValue.replace(/\u00a0/g, ' ').trim(); if (!(k in map)) return; const v = map[k]; const i = used[k] = (used[k] || 0) + 1; setText(n, Array.isArray(v) ? (v[i - 1] ?? v[v.length - 1]) : v); }); return used; };
  // Offer merchants come only from the Affiliate Programmes sheet (Admitad, TakeAds). The story brand is Level Shoes.
  const subAll = pairs => { leaves(document.body).forEach(n => { let v = n.nodeValue; pairs.forEach(([a, b]) => { v = v.split(a).join(b); }); if (v !== n.nodeValue) n.nodeValue = v; });
    document.querySelectorAll('[title],[alt]').forEach(el => ['title', 'alt'].forEach(k => { let v = el.getAttribute(k); if (!v) return; pairs.forEach(([a, b]) => { v = v.split(a).join(b); }); el.setAttribute(k, v); })); };
  const brand = (from) => {
    document.querySelectorAll('img').forEach(im => { const s = im.getAttribute('src') || '';
      if (/active_storage/.test(s)) { const d = document.createElement('div'); d.style.cssText = 'width:100%;height:100%;min-height:96px;background:#EDE7DF url(' + L + 'levelshoes.png) center/34% no-repeat'; im.replaceWith(d); }
      else if (s.indexOf(from.logo) > -1 || (im.alt || '') === from.name) { im.src = L + 'levelshoes.png'; im.style.objectFit = 'contain'; im.style.background = '#fff'; } });
    subAll(from.pairs.concat([['trial.28sep', 'Nova Bank'], ['trial 28sep', 'Retail Offers team']]));
  };
  const BOSE = { name: 'Bose', logo: 'Bose.png', pairs: [['Bose · Bose Summer Special', 'Level Shoes · Designer shoes'], ['Bose Summer Special', 'Designer shoes'],
    ['Get 10% off with your next purchase at Bose - either online or in store', 'Get 10% cashback on your next purchase at Level Shoes, in store or online'], ['Bose', 'Level Shoes']] };
  const f = location.pathname.split('/').pop();
  const fmt = n => n.toLocaleString('en-US');
  if (f.startsWith('lh-11')) {
    const B = 'https://brandlogos.azureedge.net/media/brand_logos/';
    const R = [
      ['POS PUR 448812 LVL SHS DXB MALL 00AE', 'Level Shoes', 'Shopping', '24 Nov 2026', '-1,032.00', 'AED', 'levelshoes.png'],
      ['MAF HYPMKT MOE-0042 DXB ARE', 'Carrefour', 'Groceries', '24 Nov 2026', '-412.30', 'AED', 'carrefour.png'],
      ['UBR* PENDING 4029357733 NLD', 'Uber', 'Transportation', '24 Nov 2026', '-38.50', 'AED', B + 'Uber.png'],
      ['NF* 8665797172 LOS GATOS 00012', 'Netflix', 'Entertainment', '23 Nov 2026', '-56.99', 'AED', B + 'Netflix.png'],
      ['ALSHAYA SBX 0921 DIFC GT AE', 'Starbucks', 'Dining', '23 Nov 2026', '-24.00', 'AED', B + 'Starbucks.png'],
      ['AMZ*MKTPL AE 2K4LP0 DXB 784', 'Amazon', 'Shopping', '23 Nov 2026', '-249.00', 'AED', B + 'Amazon.png'],
      ['FZ 1418829 T2 DXB AE 784', 'flydubai', 'Travel', '22 Nov 2026', '-1,890.00', 'AED', 'flydubai.png'],
      ['FTLKR #2291 DXB MALL 784', 'Foot Locker', 'Shopping', '22 Nov 2026', '-479.00', 'AED', 'footlocker.png'],
      ['SPTF AB P2A91F STO 752', 'Spotify', 'Entertainment', '21 Nov 2026', '-21.99', 'AED', B + 'Spotify.png'],
      ['RBK 3307 MIRDIF CC TID88120', 'Reebok', 'Shopping', '21 Nov 2026', '-329.00', 'AED', 'reebok.png'],
      ['AL FUTTAIM HML 0291 DFC DXB', 'IKEA', 'Household', '21 Nov 2026', '-645.00', 'AED', B + 'IKEA.png'],
      ['ALSHAYA BBW 0118 DFC MID4471', 'Bath & Body Works', 'Shopping', '20 Nov 2026', '-215.00', 'AED', 'bbw.png'],
      ['EXP*72619940183 ECOM WA 840', 'Expedia', 'Travel', '20 Nov 2026', '-2,358.40', 'AED', 'expedia.png'],
      ['TLBT*ORD 5512093 DXB 784', 'Talabat', 'Dining', '20 Nov 2026', '-64.25', 'AED', 'talabat.png'],
      ['SPNYS 0044 MARINA DXB 784', 'Spinneys', 'Groceries', '19 Nov 2026', '-188.60', 'AED', 'spinneys.png'],
      ['ARLO*ESIM 6531 SGP 702', 'Airalo', 'Travel', '19 Nov 2026', '-33.00', 'AED', 'airalo.png'],
    ];
    const st = document.createElement('style'); st.textContent = 'table{table-layout:auto!important}td div[title]{max-width:none!important;overflow:visible!important;text-overflow:clip!important;white-space:nowrap!important}td:has(div[title]),td:has(div[title]) > div{min-width:300px!important;max-width:none!important;width:auto!important}'; document.head.appendChild(st);
    return JSON.stringify(fillRows(R.map((r, i) => ({ t: [String(3752393 - i * 17), r[0], r[1], r[2], r[3], r[4], r[5]], logo: r[6] }))));
  }
  if (f.startsWith('lh-21')) {
    const R = [['Carrefour', 'Groceries', 96214300, 1421880, 188410, 'carrefour.png'], ['Amazon', 'Shopping', 88402150, 1063240, 161220], ['Starbucks', 'Dining', 41730900, 1804300, 152036, 'starbucks.png'],
      ['Netflix', 'Entertainment', 27915440, 498600, 83100], ['IKEA', 'Shopping', 21660280, 46410, 38036], ['Uber', 'Transportation', 18304760, 912400, 74912], ['Nike', 'Shopping', 9842110, 31950, 22480]];
    const rows = R.map(r => ({ t: [r[0], r[1], 'AED ' + fmt(r[2]), fmt(r[3]), fmt(r[4]), 'AED ' + (r[2] / r[4]).toFixed(2)], logo: r[5] })); rows.sel = 6; return JSON.stringify(fillRows(rows));
  }
  if (f.startsWith('lh-22')) {
    // All 19 consumer categories from docs.lunedata.io/enrichment/transaction-categories. Icon file = category ID.
    const C = [[11, 'Shopping', 698115900, 4118300, 288410, 9], [6, 'Groceries', 695406200, 9204100, 301220, 6], [10, 'Dining', 511204480, 8960700, 296905, 7],
      [15, 'Travel', 447318250, 612400, 142380, 4], [9, 'Household', 398720100, 2105600, 231470, 7], [14, 'Transportation', 252304480, 3811200, 198340, 11],
      [7, 'Wellness', 214660750, 1402900, 176215, 7], [4, 'Entertainment', 146220750, 2960700, 214905, 15], [3, 'Education', 121480300, 96200, 41870, 6],
      [17, 'Insurance', 96305900, 188400, 73120, 4], [1, 'Financial Services', 84912640, 402700, 118930, 3], [18, 'Services', 71204150, 934800, 152610, 3],
      [5, 'Government Services', 58730400, 316500, 124480, 3], [16, 'Loans', 52118900, 141300, 38205, 3], [8, 'Savings & Investments', 44906220, 58900, 21640, 6],
      [2, 'Charity & Gifts', 18402700, 204100, 64370, 3], [13, 'Transfer', 12840500, 86300, 29115, 6], [19, 'Miscellaneous', 9105880, 311200, 87450, 2], [12, 'Income', 6214300, 22400, 9840, 6]];
    const first = [...document.querySelectorAll('[data-slot="logo-fetcher"]')].map(e => { let r = e; while (r.parentElement && leaves(r).length < 5) r = r.parentElement; return r; });
    const tpl = first[0], host = tpl.parentElement; first.slice(1).forEach(r => r.remove());
    C.forEach((c, i) => { const r = i ? tpl.cloneNode(true) : tpl; if (i) host.appendChild(r); const t = leaves(r);
      [c[1], 'AED ' + fmt(c[2]), fmt(c[3]), fmt(c[4]), String(c[5])].forEach((v, k) => setText(t[k], v));
      const ic = r.querySelector('[role="img"]'); if (ic) { const u = 'url("https://brandlogos.azureedge.net/media/category_icons/' + c[0] + '.webp")'; ic.style.maskImage = u; ic.style.webkitMaskImage = u; ic.setAttribute('aria-label', c[1]); } });
    swap({ 'Categories4/4': 'Categories19/19', '4/4': '19/19' });
    return 'rows ' + host.children.length + ' h ' + document.documentElement.scrollHeight;
  }
  if (f.startsWith('lh-05')) {
    const R = [['Gold credit', null, '64%', '31,905', '7', '4'], ['Platinum credit', null, '71%', '18,420', '7', '4'], ['Classic debit', null, '48%', '96,110', '6', '3'], ['Wealth programme', null, '77%', '4,260', '7', '4']];
    return JSON.stringify(fillRows(R.map(r => ({ t: r }))));
  }
  if (f.startsWith('lh-20')) return JSON.stringify(swap({ '20': '412,880', '52': '18.6M', 'AED 12.87K': 'AED 3.94B', 'AED 643.56': 'AED 9,543', '12.87K': '3.94B', 'Categories (4)': 'Categories (19)', 'Brands (7)': 'Brands (1,284)' }));
  if (f.startsWith('lh-03')) { brand(BOSE); return 'brand ok'; }
  if (f.startsWith('mp-04')) { brand({ name: 'Al Beiruti Restaurant', logo: '\u0000none', pairs: [['Al Beiruti Restaurant', 'Level Shoes']] }); document.querySelectorAll('main img').forEach(im => { im.src = L + 'levelshoes.png'; im.style.background = '#fff'; im.style.objectFit = 'contain'; }); return 'brand ok'; }
  if (f.startsWith('lh-04')) {
    document.querySelectorAll('main img, [data-slot="logo-fetcher"] img').forEach(im => { if (!/LuneLogo/.test(im.src)) im.src = 'https://brandlogos.azureedge.net/media/brand_logos/Bose.png'; });
    swap({ 'Aalam Al Shalalat Shawerma · trial campaign': 'Bose · Bose Summer Special', 'Received 28 Sep, 11:57 GST · N-137': 'Received 29 Sep, 18:36 GST · N-142',
      'Live · Day 50 of 59 · ends 27 November, 2026': 'Live · Day 9 of 15 · ends 15 October, 2026', 'Accepted 28 Sep 2026 · 11:59 GST by trial 28sep': 'Accepted 30 Sep 2026 · 09:12 GST by Retail Offers team',
      '11': '50,325', '2': ['6,492', '18,420', '31,905'], '40%': '12.9%', '1': ['20,130', '4,260'], 'trial campaign description': 'Get 10% off with your next purchase at Bose - either online or in store',
      'AED 4,000': 'AED 10,000', 'AED 20': 'AED 100', '28 Sep 2026': '1 Oct 2026', '27 Nov 2026': '15 Oct 2026', '14 days': '30 days' }); brand(BOSE); return 'brand ok';
  }
  return 'no edits';
})()
