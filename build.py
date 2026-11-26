#!/usr/bin/env python3
"""Build the Lune website pages. Run: python3 build.py   (writes *.html next to this file)

Copy rules: ASD-STE100 at about 80%. Sentences of 20 words or fewer, active voice, present tense.
The build prints each sentence that breaks the length or punctuation rule.
"""
import html, re, sys
from mocks import MOCKS
import motion as M
from pathlib import Path

ROOT = Path(__file__).parent
SALES = "https://sales.lunedata.io"
DOCS_API = "https://docs.lunedata.io/enrichment/enrichment-api"
DOCS_SDK = "https://docs.lunedata.io/pfm-sdk/"
LUNEHUB = "https://lunehub.lunedata.io/auth/login"
LIVE = "https://www.lunedata.io"

NAV = [("enrich.html", "Enrich"), ("analytics.html", "Analytics"), ("expenses.html", "Expenses"),
       ("cashflow.html", "Cashflow"), ("pulse.html", "Pulse"), ("customers.html", "Customers")]

# Sets the hero option before the page draws. The option comes from the address or from the last choice.
BOOT = """<script>(function(){var d=document.documentElement,h='c';try{h=new URLSearchParams(location.search).get('hero')||localStorage.getItem('lune-hero')||'c'}catch(e){}d.dataset.hero=/^[abc]$/.test(h)?h:'c';var b='ink';try{b=new URLSearchParams(location.search).get('btn')||localStorage.getItem('lune-btn')||'ink'}catch(e){}d.dataset.btn=/^(ink|emerald|coral)$/.test(b)?b:'ink';d.classList.add('js')})()</script>"""

CLIENTS = [("adib.avif", "ADIB"), ("cbd.svg", "Commercial Bank of Dubai"), ("ajman-bank.png", "Ajman Bank"),
           ("nbf.avif", "National Bank of Fujairah"), ("uab.jpg", "United Arab Bank"), ("nbb.avif", "National Bank of Bahrain"),
           ("vision-bank.avif", "Vision Bank"), ("d360.avif", "D360 Bank"), ("beyon-money.avif", "Beyon Money"),
           ("alaan.avif", "Alaan"), ("tweeq.png", "Tweeq"), ("karty.png", "Karty"), ("myne.avif", "Myne"),
           ("sifi.avif", "Sifi"), ("afs.avif", "AFS"), ("simplifi.jpg", "Simplifi")]

e = html.escape


# ------------------------------------------------------------------ components
def page(slug, title, desc, body):
    cur = ' aria-current="page"'
    nav = "".join(f'<a href="{h}"{cur if h == slug else ""}>{t}</a>' for h, t in NAV)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="stylesheet" href="ds/tokens/fonts.css">
<link rel="stylesheet" href="ds/tokens/colors.css">
<link rel="stylesheet" href="ds/tokens/typography.css">
<link rel="stylesheet" href="ds/tokens/spacing.css">
<link rel="stylesheet" href="ds/tokens/base.css">
<link rel="stylesheet" href="site.css">
<link rel="stylesheet" href="motion.css">
{BOOT}
</head>
<body>
<header class="site-head">
  <div class="wrap site-head__row">
    <a class="brand" href="index.html"><i></i>Lune</a>
    <nav class="site-nav" id="site-nav" aria-label="Main">{nav}</nav>
    <div class="site-head__end">
      <a class="login" href="{LUNEHUB}">Log in</a>
      <a class="btn btn--dark btn--sm" href="contact.html">Talk to us</a>
      <button class="menu-btn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="site-nav">≡</button>
    </div>
  </div>
</header>
<main>
{body}
</main>
<footer class="site-foot">
  <div class="wrap site-foot__grid">
    <div><a class="brand" href="index.html" style="font-size:20px"><i style="width:24px;height:24px;box-shadow:inset -6px 0 0 #10A37F"></i>Lune</a><span class="muted" style="min-height:36px">© 2026 Lune Technologies</span>
      <a href="{LIVE}/lune-privacy">Privacy policy</a><a href="{LIVE}/terms">Terms</a></div>
    <div><b>Enrichment</b><a href="enrich.html">Enrich</a><a href="analytics.html">Analytics</a><a href="expenses.html">Expenses</a><a href="cashflow.html">Cashflow</a></div>
    <div><b>Pulse</b><a href="pulse.html#how">How Pulse works</a><a href="pulse.html#merchant">For merchants</a><a href="pulse.html#bank">For banks</a><a href="pulse.html#customer">For cardholders</a></div>
    <div><b>Company</b><a href="platform.html">How the products fit</a><a href="customers.html">Customers</a><a href="contact.html">Contact sales</a></div>
    <div><b>Developers</b><a href="{DOCS_API}" target="_blank" rel="noopener">Enrichment API ↗</a><a href="{DOCS_SDK}" target="_blank" rel="noopener">Mobile SDK ↗</a><a href="{LUNEHUB}">Log in to LuneHub</a></div>
  </div>
</footer>
<script src="site.js"></script>
<script src="motion.js"></script>
</body>
</html>
"""


def sec(inner, cls="", id_=""):
    attr = f' id="{id_}"' if id_ else ""
    return f'<section class="sec {cls}"{attr}><div class="wrap stack">' + "\n" + inner + "\n</div></section>"


def head(eyebrow, h2, lead=""):
    p = f'<p class="lead">{lead}</p>' if lead else ""
    return f'<div class="head"><h2>{h2}</h2>{p}</div>'


def hero(eyebrow, h1, lead, btns, side=""):
    grid = "hero__grid" if side else ""
    return f"""<section class="hero"><div class="wrap {grid}">
  <div class="hero__copy"><h1 class="h1--page">{h1}</h1><p class="lead">{lead}</p><div class="btns">{btns}</div></div>
  {side}
</div></section>"""


BTN_TALK = '<a class="btn btn--primary" href="contact.html">Talk to us</a>'
BTN_LIVE = f'<a class="btn btn--ghost" href="{SALES}" target="_blank" rel="noopener">Try enrichment live ↗</a>'


def shot(img, bar, cap, alt):
    if img in MOCKS:   # a drawn exhibit of the screen (mocks.py), not a capture
        return f"""<figure class="shot"><div class="shot__frame"><span class="shot__bar">{e(bar)}</span>
<div class="ui-wrap" role="img" aria-label="{e(alt)}">{MOCKS[img]}</div></div><figcaption>{cap}</figcaption></figure>"""
    if img.endswith("cardholder-preview.jpg"):
        return f"""<figure class="shot"><div class="shot__frame"><span class="shot__bar">{e(bar)}</span>
<img class="shot__phone" src="img/app/cust-03-offer.png" alt="{e(alt)}" loading="lazy"></div><figcaption>{cap.replace(TEST, "Screen from the customer app with sample data.")}</figcaption></figure>"""
    return f"""<figure class="shot"><div class="shot__frame"><span class="shot__bar">{e(bar)}</span>
<img src="img/product/{img}" alt="{e(alt)}" loading="lazy"></div><figcaption>{cap}</figcaption></figure>"""


def phone(img, title, text):
    return f'<figure class="phone"><img src="img/app/{img}" alt="{e(title)} screen" loading="lazy"><figcaption><b>{title}</b><span>{text}</span></figcaption></figure>'


def card(tag, h3, body, ticks=(), who="", link=None):
    t = f'<span class="tag">{tag}</span>' if tag else ""
    ul = '<ul class="ticks">' + "".join(f"<li>{x}</li>" for x in ticks) + "</ul>" if ticks else ""
    w = f'<span class="for">For: <b>{who}</b></span>' if who else ""
    ln = f'<a class="more" href="{link[0]}">{link[1]} →</a>' if link else ""
    return f'<div class="card">{t}<h3>{h3}</h3><p>{body}</p>{ul}{w}{ln}</div>'


def facts(items):
    return '<ul class="facts">' + "".join(f"<li><b>{a}</b> {b}</li>" for a, b in items) + "</ul>"


def feature(eyebrow, h3, body, items, fig, wide=True, link=None):
    ln = f'<a class="more" href="{link[0]}">{link[1]} →</a>' if link else ""
    return f"""<div class="feature {'feature--wide' if wide else ''}"><div class="feature__copy"><h2 style="font-size:clamp(26px,2.6vw,38px)">{h3}</h2>
<p class="lead">{body}</p>{facts(items)}{ln}</div>{fig}</div>"""


def cta(h2, p, second=BTN_LIVE):
    second = second.replace("btn--ghost", "btn--ghost-ink")
    return f"""<section class="sec"><div class="wrap"><div class="cta"><h2>{h2}</h2><div class="cta__end"><p>{p}</p>
<div class="btns"><a class="btn btn--ink" href="contact.html">Talk to us</a>{second}</div></div></div></div></section>"""


def stats():
    return """<div class="stats">
<div><b>1.5 bn+</b><span>Transactions enriched each year</span></div>
<div><b>0.5 ms</b><span>Enrich API response time</span></div>
<div><b>99%</b><span>Categorisation coverage</span></div>
<div><b>121+</b><span>Spend subcategories</span></div></div>
<p class="small">Source: Lune platform data.</p>"""


BADGES = '<div class="badges"><span>Certified and audited for regulated banks</span><span>ISO 27001</span><span>SOC 2 Type II</span><span>Dubai AI Seal</span><span>Hosted in UAE and KSA</span></div>'


def logos():
    hid = ' aria-hidden="true"'
    row = "".join(f'<img src="img/clients/{f}" alt="{e(a) if r == 0 else ""}"{"" if r == 0 else hid}>' for r in (0, 1) for f, a in CLIENTS)
    return f'<div class="wrap logos"><p class="eyebrow muted" style="color:var(--neutral-500)">Trusted by banks and fintechs across the Middle East</p><div class="logos__mask"><div class="logos__row">{row}</div></div></div>'


TEST = "Illustration of the product screen with sample data."

# ------------------------------------------------------------------ HOME
FLOW = """<div class="flow">
<div class="flow__step"><span class="n">01</span><h3>Card description from your bank</h3><span class="v mono">POS PUR 448812 LVL SHS DXB MALL 00AE</span><span class="v">AED 1,032.00</span></div>
<div class="flow__step"><span class="n">02</span><h3>Enriched by Lune</h3><span class="v flow__who"><img src="img/logos/levelshoes.png" alt="" width="40" height="40"><span><b style="color:#fff">Level Shoes</b><br>Shopping › Clothing</span></span></div>
<div class="flow__step"><span class="n">03</span><h3>Matched to an activated offer</h3><span class="v"><b style="color:#fff">10% cashback</b><br>Funded by Level Shoes</span></div>
<div class="flow__step flow__step--end"><span class="n">04</span><h3>Cashback recorded</h3><span class="big">AED 103.20</span><span class="v">The merchant pays the cashback. Your bank uses no rewards budget.</span></div>
</div><p class="small">Example transaction.</p>"""

PRODUCTS = [
    ("Enrich", "Each card description gets a merchant name.",
     "Enrich returns the merchant, logo and category for each transaction. Your team sees the result in LuneHub.",
     [("Merchant and logo", "The name your customer knows"), ("Category", "19 categories with subcategories"), ("Real time", "0.5 ms response time")],
     ("enrich.html", "See how Enrich works"),
     ("shot", "lunehub-transactions.jpg", "LuneHub · Transactions", "The Transactions page in LuneHub.", "LuneHub transactions list with raw description, brand and category")),
    ("Pulse", "Merchants pay for the offers. You see the result.",
     "Your team approves each offer and selects the cards. LuneHub then shows the performance and the cashback of each offer.",
     [("Choose the cards", "Card programmes by BIN"), ("Performance", "Activation rate and redemptions"), ("Cashback", "Earned by customers, paid by merchants")],
     ("pulse.html", "See all Pulse screens"),
     ("shot", "lunehub-campaign-analytics.jpg", "LuneHub · Campaign Analytics", "Campaign Analytics in LuneHub.", "LuneHub Campaign Analytics: activation rate 11.4 percent, 1,572 redemptions, AED 618,100 spend at merchants, AED 76,082 cashback earned")),
    ("Analytics", "Find the merchants where your customers spend most.",
     "Analytics shows spend by brand, category and customer. Your team finds the merchants to bring into Pulse.",
     [("Brand explorer", "Spend and customers for each brand"), ("Category explorer", "All 19 Lune categories"), ("Spend dashboard", "Totals for a period and a market")],
     ("analytics.html", "See all Analytics screens"),
     ("shot", "lunehub-analytics-brands.jpg", "LuneHub · Analytics · Brands", "The Brand explorer in LuneHub.", "LuneHub brand explorer with spend, transactions and customers for each brand")),
    ("Expenses", "Customers see where their money goes.",
     "Expenses adds ready spending screens to your iOS and Android app, with real merchant names and logos.",
     [("This month", "Spending day by day"), ("Trends", "By category and by brand"), ("Budgets", "By category or in total")],
     ("expenses.html", "See all Expenses screens"),
     ("phone", "exp-home.png", "", "The Expenses home screen from the Lune SDK.", "Expenses home screen with spending this month and a category chart")),
    ("Cashflow", "Customers compare money in with money out.",
     "Cashflow adds ready screens to your iOS and Android app. Customers follow the trend month by month.",
     [("Total cashflow", "Money in against money out"), ("Money in", "Sources and transfers in"), ("Trends", "Six months of history")],
     ("cashflow.html", "See all Cashflow screens"),
     ("phone", "cf-home.png", "", "The Cashflow home screen from the Lune SDK.", "Cashflow home screen with money in and money out this month")),
]


def tabs_block():
    tabs = "".join(f'<button type="button" role="tab" class="tab" id="prod-tab-{i}" aria-controls="prod-{i}" aria-selected="{"true" if i == 0 else "false"}">{t[0]}</button>' for i, t in enumerate(PRODUCTS))
    panels = ""
    for i, (_, title, body, kv, link, fig) in enumerate(PRODUCTS):
        rows = "".join(f"<div><b>{k}</b><span>{v}</span></div>" for k, v in kv)
        kind, img, bar, cap, alt = fig
        if kind == "shot":
            figure = shot(img, bar, cap + " " + TEST, alt)
        else:
            figure = f'<figure class="phone phone--solo"><img src="img/app/{img}" alt="{e(alt)}" loading="lazy"><figcaption><span>{cap} Sample data.</span></figcaption></figure>'
        hidden = " hidden" if i else ""
        panels += f"""<div class="panel prod" role="tabpanel" id="prod-{i}" aria-labelledby="prod-tab-{i}"{hidden}>
<div class="feature__copy"><h3 class="h2" style="font-size:clamp(26px,2.6vw,38px)">{title}</h3><p class="lead">{body}</p><div class="kv">{rows}</div><a class="more" href="{link[0]}">{link[1]} →</a></div>
{figure}</div>"""
    return f"""{head("The platform", "Five products. One set of card data.", "Start with one product and add the others later. Each one runs on the same enriched transactions.")}
<div class="switch"><div class="switch__bar"><div class="tabs" role="tablist" aria-label="Product">{tabs}</div></div>{panels}</div>"""


PROOF = '''
<div class="cols cols--2">
<figure class="quote"><blockquote>“We integrated Lune Enrich in a couple of months, with the team being responsive and helping every step of the way.”</blockquote>
<figcaption><img src="img/clients/d360.avif" alt="D360 Bank"><span><b>Masharty</b><i>Associate Director, D360 Bank</i></span></figcaption></figure>
<div style="display:grid;gap:20px">
<a class="case case--dark" href="customers.html#adib"><span class="eyebrow">Case study · ADIB</span><b>ADIB shows customers where their money goes. →</b></a>
<a class="case" href="customers.html#nbf"><span class="eyebrow">Case study · National Bank of Fujairah</span><b>NBF replaced manual data work with structured insight. →</b></a>
</div></div>'''

def chapter(id_, tag, h2, lead, link, fig, cls=""):
    ln = f'<a class="more" href="{link[0]}">{link[1]} →</a>'
    return sec(f'<div class="chap"><div class="chap__copy">{M.chapter_head(tag, h2, lead)}{ln}</div>{fig}</div>', "chapter " + cls, id_)


HERO_BTNS = BTN_TALK + '<a class="btn btn--ghost" href="#solution">See how it works</a>'
POINTS = """<div class="points points--plain">
<div><h3>Customers do not recognise their payments.</h3></div>
<div><h3>Your teams cannot see where customers spend.</h3></div>
<div><h3>Your bank pays for every reward.</h3></div>
</div>"""
APP = f"""<div class="cols cols--2 appduo">
<div class="appduo__c"><h3>Expenses</h3>{M.EXPENSES_STAGE}<a class="more" href="expenses.html">See Expenses →</a></div>
<div class="appduo__c"><h3>Cashflow</h3>{M.CASHFLOW_STAGE}<a class="more" href="cashflow.html">See Cashflow →</a></div>
</div><p class="small">Animations with sample data.</p>"""

HOME = f"""<section class="hero hero--v">{M.heroes(HERO_BTNS)}
{logos()}
</section>
{M.OPTIONS}

{sec(head("", 'Card data can grow your revenue. Today, most of it is <span class="serif">unreadable.</span>') + POINTS, "sec--teal", "problem")}

{sec(head("", 'Lune reads each card payment. <span class="serif">Then the data earns.</span>', "Start with Enrich. Add the other products when you need them.") + M.STACK + '<a class="more" href="platform.html">See how the products fit together →</a>', "", "solution")}

<div class="journey">
{chapter("enrich", "The foundation", 'Each card payment gets <span class="serif">a name your customer knows.</span>',
 "Enrich returns the merchant name, the logo and the category.",
 ("enrich.html", "See how Enrich works"), M.ENRICH_STAGE, "sec--white")}

{chapter("lunehub", "Comes with Enrich", "Your team sees each enriched transaction in LuneHub.",
 "LuneHub is the Lune portal for your bank's teams.",
 ("enrich.html", "See LuneHub on the Enrich page"), '<div data-plx="0.05">' + shot("lunehub-transactions.jpg", "LuneHub · Transactions", "The Transactions page in LuneHub. " + TEST, "LuneHub transactions list with raw description, brand and category") + "</div>")}

{chapter("analytics", "Comes with LuneHub", "Find the merchants where your customers spend most.",
 "Analytics shows spend by brand, category and customer.",
 ("analytics.html", "See all Analytics screens"), M.ANALYTICS_STAGE, "sec--white")}

{sec(M.chapter_head("Separate SDKs for your app", "Your customers see where their money goes.", "Expenses and Cashflow add ready screens to your iOS and Android app.", " chead--split") + APP, "chapter", "app")}

{chapter("pulse", "A separate product", 'Merchants pay to reward <span class="serif">your customers.</span>',
 "Pulse is a rewards programme under your bank's name. Merchants fund each offer.",
 ("pulse.html", "See how Pulse works"), M.PULSE_STAGE, "sec--ink")}
</div>

{sec(stats() + PROOF + BADGES, "", "proof")}

{cta("See what your card transactions can earn.", "Contact sales for a live demo. We show Lune on sample data, then on a sample of your own transactions.")}
"""

# ------------------------------------------------------------------ ENRICH
RAW = [
    ("AMZ*MKTPL UK 2R45T LON GB 826", "amazon.png", "Amazon", "", "Shopping › Online marketplaces", "", "GBP 42.99"),
    ("POS 551204 MAF HYPMKT RYD PARK 682", "carrefour.png", "Carrefour", "كارفور", "Groceries › Supermarkets", "", "SAR 214.50"),
    ("CB INDITEX 3315 PARIS HAUSSM FR", "zara.png", "Zara", "", "Shopping › Clothing", "", "EUR 89.95"),
    ("UBR* PENDING 8005928996 NY 840", "uber.png", "Uber", "", "Transportation › Ride hailing", "", "USD 31.40"),
    ("IKANO PTE TMPNS 0291 SGP 702", "ikea.png", "IKEA", "宜家家居", "Home › Furniture", "", "SGD 189.00"),
    ("SBUX SHIBUYA TKY JP 392", "starbucks.png", "Starbucks", "スターバックス", "Dining › Cafés", "", "JPY 650"),
    ("NF* 8665797172 LOS GATOS 00012", "netflix.png", "Netflix", "نتفليكس", "Entertainment › Streaming", "Recurring", "AED 56.99"),
]
rawrows = "".join(f"""<div class="rawrow"><span class="rawrow__raw" data-ux-ignore="long-number-unchunked">{e(r)}</span><span class="rawrow__arrow">→</span>
<span class="rawrow__out"><img src="img/logos/{lg}" alt=""><span><b>{e(m)}{f' · {loc}' if loc else ''}</b><span><em>{cat}</em>{' · ' + city if city else ''} · {amt}</span></span></span></div>""" for r, lg, m, loc, cat, city, amt in RAW)

ENRICH = f"""{hero("Enrich", 'Every card payment, named: <span class="serif">merchant, logo and category.</span>',
 "Your core banking system sends a raw card description. Enrich returns the merchant, logo and category in under a millisecond.",
 BTN_TALK + BTN_LIVE + f'<a class="btn btn--ghost" href="{DOCS_API}" target="_blank" rel="noopener">Read the API docs ↗</a>', M.page_stage("enrich"))}

{sec(head("Sample transactions", "Enrich reads the card descriptions that customers cannot read.", "Seven card transactions from seven markets. Each result comes from one real-time API call.") + f'''
<div class="rawtable">{rawrows}</div><p class="small">Sample transactions. Local names come from Lune's merchant database.</p>''')}

{sec(stats(), "sec--white")}

{sec(head("What you get back", "One API call returns four fields for each transaction.") + f'''
<div class="cols cols--4">
{card("", "Merchant name", "The name your customer knows, in all languages, from local and global merchant databases.")}
{card("", "Merchant logo", "A logo for each merchant, updated every day. Statements and apps show names that customers know.")}
{card("", "Category and subcategory", "19 consumer categories, each with subcategories. Examples are Groceries, Dining, Travel and Income.")}
{card("", "Recurring transactions", "Lune finds transactions that repeat. Examples are payments such as subscriptions and income such as a salary.")}
</div>''')}

{sec(feature("In LuneHub", "Your team sees each enriched transaction.", "LuneHub is the Lune portal for bank teams. It lists each transaction with its raw description and its enriched result.",
 [("Search", "by raw description or transaction ID."), ("Compare", "the raw description with the brand and category."), ("Flag", "a result that looks wrong.")],
 shot("lunehub-transactions.jpg", "LuneHub · Transactions", "The Transactions page in LuneHub. " + TEST, "LuneHub transactions list with raw description, brand, category, date and amount")), "sec--white")}

{sec(head("Built for banks", "Certified, audited and hosted in the UAE and Saudi Arabia.") + f'''
<div class="cols cols--4">
{card("", "ISO 27001", "Certified information security management.")}
{card("", "SOC 2 Type II", "Independent audit of security controls.")}
{card("", "Audit logs", "Lune logs every enrichment API call.")}
{card("", "Regional hosting", "Deployments in the UAE and Saudi Arabia, with disaster recovery.")}
</div>''')}

{cta("See Enrich on your own transactions.", "Contact sales for a live demo on a sample of your transactions. Or enrich a sample feed in your browser now.")}
"""

# ------------------------------------------------------------------ ANALYTICS
def qa(title, items):
    rows = "".join(f"<div><b>{q}</b><span>{a}</span></div>" for q, a in items)
    return f'<div class="feature__copy"><h3>{title}</h3><div class="kv kv--qa">{rows}</div></div>'


BRAND_MORE = f'''
<div class="cols">
{card("Filter", "Find a brand in seconds", "Search by brand name. Filter by category. Set a range for spend, transactions, customers or spend per customer.")}
{card("Sort", "Rank brands your way", "Sort the list by spend, transactions, customers or spend per customer.")}
{card("Scope", "Select the period and the market", "Select a date range, a currency and a country. The list shows only that scope.")}
</div>
''' + qa("Questions the Brand explorer answers", [
    ("Which brands take most of our card spend?", "Sort by total spend."),
    ("Which brands do most of our customers use?", "Sort by customers."),
    ("Where is spend per customer high?", "Sort by spend per customer."),
    ("Which brands lead one category?", "Filter by category, then sort by spend."),
    ("Which merchants do we bring into Pulse first?", "Start with the brands that have the most customers."),
])

CATEGORY_MORE = f'''
<div class="cols">
{card("Filter", "Set a range for each metric", "Set a range for total spend, transactions or customers. The list shows the categories in that range.")}
{card("Sort", "Rank categories your way", "Sort the list by spend, transactions or customers.")}
{card("Scope", "Select the period and the market", "Select a date range, a currency and a country. The list shows only that scope.")}
</div>
''' + qa("Questions the Category explorer answers", [
    ("Where does our card spend go?", "Sort by total spend."),
    ("Which categories do most customers use?", "Sort by customers."),
    ("Which categories have many small payments?", "Compare transactions with total spend."),
    ("How does a category change by market?", "Change the country and compare."),
    ("Which categories do we target with offers?", "Start with the categories that have the most customers."),
])


ANALYTICS = f"""{hero("Analytics", 'See where your customers spend, <span class="serif">by merchant and category.</span>',
 "Analytics shows spend by merchant, category and customer from your enriched transactions. Your teams get answers without a data request.", BTN_TALK, M.page_stage("analytics"))}

{sec(feature("Spend dashboard", "One view of customers, transactions and spend.", "Select a date range, a currency and a country. The dashboard shows the totals and the split.",
 [("Total customers", "and total transactions."), ("Total spend", "and spend per customer."), ("Spend by category and brand", "in one chart.")],
 shot("lunehub-analytics-dashboard.jpg", "LuneHub · Analytics · Dashboard", "The Analytics dashboard in LuneHub. " + TEST, "LuneHub analytics dashboard with total customers, transactions, spend and spend per customer")), "sec--white")}

{sec(feature("Brand explorer", "Find the merchants where your customers spend most.", "The Brand explorer lists each enriched merchant with six columns. Your team filters and sorts the list to find the brands that matter.",
 [("Brand and category", "for each enriched merchant."), ("Total spend and transactions", "for the period you select."), ("Customers", "who paid that brand with your cards."), ("Spend per customer", "to compare brands of different size.")],
 shot("lunehub-analytics-brands.jpg", "LuneHub · Analytics · Brands", "The Brand explorer in LuneHub. " + TEST, "LuneHub brand explorer with spend, transactions, customers and spend per customer for each brand")) + BRAND_MORE)}

{sec(feature("Category explorer", "See spend for each category.", "The Category explorer lists all 19 Lune categories with their totals. Your team sees where card spend goes and how many customers are behind it.",
 [("Total spend and transactions", "for each category."), ("Customers", "who spend in each category."), ("The number of subcategories", "below each category.")],
 shot("lunehub-analytics-categories.jpg", "LuneHub · Analytics · Categories", "The Category explorer in LuneHub, with the first eight of 19 categories. " + TEST, "LuneHub category explorer with spend, transactions, customers and subcategories")) + CATEGORY_MORE, "sec--white")}

{sec('''<div class="split"><div class="head"><h2>Spend data shows which merchants can <span class="serif">fund your rewards.</span></h2></div>
<div class="feature__copy"><p class="lead">The Brand explorer shows the merchants where your customers spend most. Through Pulse, those merchants fund cashback for your customers.</p>''' + facts([("One portal.", "Analytics and Pulse share one LuneHub sign-in."), ("One data set.", "Pulse audiences come from the same enriched transactions."), ("Your data only.", "Each bank sees its own customers and transactions.")]) + '''<a class="more" href="pulse.html">See Pulse →</a></div></div>''', "sec--teal")}

{sec(head("Also in LuneHub", "Your teams answer spend questions in one place.") + f'''
<div class="cols">
{card("", "Spend over time", "Daily, weekly or monthly trends, with the leaders and the split by category.")}
{card("", "Enriched transactions", "Search and filter each transaction with its merchant, logo and category.")}
{card("", "Usage and access", "Track enrichment usage against your plan. Manage API keys and invite your team.")}
</div>''')}

{cta("See your own spend data in LuneHub.", "We show Analytics with sample data, or with a sample of your own enriched transactions.")}
"""

# ------------------------------------------------------------------ EXPENSES / CASHFLOW
BTN_SDK = f'<a class="btn btn--ghost" href="{DOCS_SDK}" target="_blank" rel="noopener">SDK docs ↗</a>'
IN_APP = f'''<div class="cols">
{card("", "Your look", "Your colours, light and dark mode, and your currency.")}
{card("", "Two platforms", "Native SDKs for iOS and Android.")}
{card("", "Enriched by default", "Each transaction shows the merchant name, logo and category from Lune Enrich.")}
</div>'''

EXPENSES = f"""{hero("Expenses", 'Show customers where <span class="serif">their money goes.</span>',
 "Expenses adds ready spending screens to your iOS and Android app. Customers see spend by category and merchant, with real merchant names.", BTN_TALK + BTN_SDK, M.page_stage("expenses"))}

{sec(head("Expenses screens", "Payments show real merchant names and categories.") + f'''
<div class="phones" style="max-width:980px">
{phone("exp-home.png", "This month", "Spending day by day, against last month.")}
{phone("exp-all.png", "Every transaction", "Search by merchant, category or amount.")}
{phone("exp-tx.png", "Transaction detail", "Merchant, category and card.")}
</div><p class="small">Screens from the Lune SDK with sample data.</p>''', "sec--white")}

{sec(head("Trends", "Customers follow each category and each brand over time.", "Two trend pages show where the money goes. A customer opens a category or a brand to see its history.") + f'''
<div class="phones" style="max-width:980px">
{phone("exp-cats.png", "Category trends", "Top categories with spend and share of spend.")}
{phone("exp-brands.png", "Brand trends", "Spend for each day and the top brands.")}
{phone("exp-brand.png", "One brand", "Six months of spend with that brand.")}
</div><p class="small">Screens from the Lune SDK with sample data.</p>''')}

{sec(head("What customers can do", "Customers see their spend and plan their month.") + f'''
<div class="cols cols--4">
{card("", "Spend by category", "For this month, last month, the last three months or this year.")}
{card("", "Search and filter", "Search by merchant, category or amount. Filter the list by category or tag.")}
{card("", "Budgets", "Budgets by category or in total, with progress for the month.")}
{card("", "Feedback", "A customer can report a wrong merchant or category on a transaction.")}
</div>''', "sec--white")}

{sec(head("In your app", "Native screens for iOS and Android.") + IN_APP)}

{cta("See Expenses in a sample bank app.", "Contact sales for a live demo of Expenses on sample data.", BTN_SDK)}
"""

CASHFLOW = f"""{hero("Cashflow", 'Show customers money in <span class="serif">against money out.</span>',
 "Cashflow adds ready screens to your iOS and Android app. Customers compare money in with money out and follow the trend.", BTN_TALK + BTN_SDK, M.page_stage("cashflow"))}

{sec(head("Cashflow screens", "Customers compare money in with money out.") + f'''
<div class="phones" style="max-width:980px">
{phone("cf-home.png", "Total cashflow", "Money in against money out this month.")}
{phone("cf-in.png", "Money in", "Sources and transfers in.")}
{phone("cf-trends.png", "Trends", "Six months of money in and out.")}
</div><p class="small">Screens from the Lune SDK with sample data.</p>''', "sec--white")}

{sec(head("What customers can do", "Customers see where money comes from and where it goes.") + f'''
<div class="cols">
{card("", "Inflow and outflow", "Money in and money out for a period, with transaction counts.")}
{card("", "Smart insights", "Insights in plain language, such as the cashflow summary.")}
{card("", "Cashflow history", "A timeline of inflow and outflow, month by month.")}
</div>''')}

{sec(head("In your app", "Native screens for iOS and Android.") + IN_APP, "sec--white")}

{cta("See Cashflow in a sample bank app.", "Contact sales for a live demo of Cashflow on sample data.", BTN_SDK)}
"""

# ------------------------------------------------------------------ PULSE
PULSE_H1 = "Rewards under your bank's name. " + '<span class="serif">Merchants pay.</span>'
BTN_HOW = '<a class="btn btn--ghost" href="#how">See how it works</a>'
PULSE = f"""{hero("Pulse", PULSE_H1,
 "Pulse is a rewards programme for your customers: cashback or points, with tiers and missions. Merchants fund the offers. Your bank approves them.", BTN_TALK + BTN_HOW, M.page_stage("pulse"))}

{sec(head("Why card managers use Pulse", "Customers earn with your card. Merchants pay for the rewards.") + f'''
<div class="cols">
{card("Card spend", "Customers earn only with your card", "A customer activates an offer in your app. The customer then earns on purchases with your card.")}
{card("Cost", "Merchants fund each reward", "The merchant sets the budget, the cashback rate and the cap. Your bank needs no rewards budget.")}
{card("Control", "Your bank approves each offer", "Your team sees the terms, the stores and the audience. Your team chooses the cards that can earn.")}
</div>''', "sec--white")}

{sec(head("How Pulse works", "Four parties. One offer.", "Each offer moves from the merchant to Lune, to your bank, then to your customer. Each party has its own tool and its own view.") + '''
<div class="party">
<div><b>Merchant creates</b><span>Sets the budget, cashback rate, cap and stores.</span><a class="more" href="#merchant">Merchant portal →</a></div>
<div><b>Lune targets</b><span>Builds the offer and selects eligible customers from enriched spend.</span><a class="more" href="#targeting">Targeting →</a></div>
<div><b>Bank approves</b><span>Accepts or rejects the offer and chooses the cards.</span><a class="more" href="#bank">LuneHub →</a></div>
<div><b>Customer earns</b><span>Joins, activates the offer in the app and pays by card.</span><a class="more" href="#customer">Customer app →</a></div>
</div>''', id_="how")}

{sec(head("Merchant portal", "Merchants run their campaigns in their own portal.", "Your team does no campaign setup. The merchant creates the campaign, pays the cashback and sees its own results.") +
 feature("Merchant creates", "The merchant sets the goal, the budget and the cashback.", "A merchant sets up a campaign and sends it for review. The merchant pays cashback only on purchases that meet the terms.",
 [("Goal and budget.", "A goal, a total budget, the cashback rate, a cap and a minimum spend."), ("Two budget modes.", "Run until the budget is spent, or run for fixed dates."), ("Each brand and store.", "Several brands, with merchant IDs and terminal IDs.")],
 shot("merchant-create-campaign-step1.jpg", "Pulse merchant portal · Create campaign", "Step 1 of the campaign form in the merchant portal. " + TEST, "Merchant portal create campaign form with goal, budget, cashback percentage, cap and dates")) +
 feature("Merchant analytics", "The merchant sees the return on each campaign.", "The same portal shows the sales and the cost of each campaign. The merchant sees only its own campaigns.",
 [("Sales after refunds.", "Sales that earned cashback for each campaign."), ("Return on cashback.", "Sales for each unit of cashback spent."), ("Net cashback cost.", "Cashback accrued minus cashback reversed by refunds.")],
 shot("merchant-analytics.jpg", "Pulse merchant portal · Analytics", "Merchant analytics in the merchant portal. " + TEST, "Merchant portal analytics with sales, return on cashback and cashback cost")), "sec--white", "merchant")}

{sec(head("02 · Lune targets", 'Each offer reaches the customers who <span class="serif">match the goal.</span>', "The merchant selects a goal for the campaign. Lune builds the audience for that goal from your enriched transactions.") + f'''
<div class="cols cols--4">
{card("Goal: acquire customers", "New to the brand", "Customers who spend in the category but not at this brand. Example: they buy coffee each week, but not at this café.")}
{card("Goal: win back customers", "Stopped buying", "Customers who bought from the brand before and then stopped. Example: no purchase in the last 90 days.")}
{card("Goal: increase frequency", "Buy now and then", "Customers who buy from the brand, but not often. Example: one purchase a month or less.")}
{card("Goal: grow average spend", "Small baskets", "Customers who buy from the brand with a low amount for each purchase. A minimum spend on the offer moves them up.")}
</div>
<div class="cols">
{card("More ways to target", "By category or subcategory", "Customers who spend in one category, such as Dining, or one subcategory, such as Food Delivery.")}
{card("More ways to target", "By spend level", "Customers above or below a spend amount in a period. Example: more than AED 2,000 on Travel in six months.")}
{card("More ways to target", "By card programme", "Your team selects the card programmes that can earn. Example: Platinum credit only.")}
</div>''' + '<div class="split split--top"><div class="feature__copy">' + facts([("Audience size first.", "Your team sees how many customers can earn before the offer goes live."), ("Your data stays yours.", "Each bank's audience comes from its own customers and transactions.")]) + '</div><div class="feature__copy">' + facts([("Terms written for you.", "Lune writes the offer terms from the campaign settings."), ("No work for your data team.", "Lune builds each audience. Your team approves the offer.")]) + '</div></div>', "sec--teal", "targeting")}

{sec(head("LuneHub", "Your team controls and measures each offer in LuneHub.", "LuneHub is the portal for your bank. Your team approves the offers, selects the cards and sees the results.") +
 feature("Bank approves", "No offer goes live without your approval.", "The offer arrives in the Campaign Manager in LuneHub. Your team sees the terms, the stores and the audience.",
 [("One inbox.", "Pending, accepted, completed and rejected offers, with search."), ("Accept or reject.", "One decision for each offer."), ("Clear terms.", "Cashback rate, budget, cap, dates and refund window.")],
 shot("lunehub-campaign-details-review-pending.jpg", "LuneHub · Campaign Manager · Campaign details", "An offer that waits for the bank's decision in LuneHub. " + TEST, "LuneHub campaign details with Reject and Accept buttons")) + f'''
<div class="cols cols--2">
{shot("lunehub-card-management.jpg", "LuneHub · Card Management", "Register card programmes by BIN. Select which programmes can earn on each offer. " + TEST, "LuneHub card management with card programmes, BIN, active users and cardholders")}
{shot("lunehub-campaign-details-review-pending-tab-cardholder-preview.jpg", "Customer app · Offer", "See the offer and its terms as your customers see them. " + TEST, "LuneHub cardholder preview of an offer on a phone")}
</div>''' +
 feature("Bank analytics", "Your team sees the performance and the cashback of each offer.", "Campaign Analytics in LuneHub shows all your offers in one view. The figures are for your bank only.",
 [("Offer performance.", "Activation rate, redemptions and spend at merchants for each offer."), ("Cashback.", "Cashback earned by your customers, net of refunds."), ("All offers in one view.", "Totals for the period, and each offer in one table.")],
 shot("lunehub-campaign-analytics.jpg", "LuneHub · Campaign Analytics", "Campaign Analytics in LuneHub. " + TEST, "LuneHub Campaign Analytics with activation rate, redemptions, spend at merchants and cashback earned for each offer")), "sec--white", "bank")}

{sec(head("04 · Customer journey", "Customers join once, activate offers with one tap and track their rewards.", "Pulse runs in your mobile app through the Lune SDK for iOS and Android. It uses your bank's name and colour.") + f'''
<div class="phones">
{phone("cust-01-join.png", "Join", "The customer reads the terms and joins.")}
{phone("cust-02-home.png", "Offers", "The offers for the customer's card.")}
{phone("cust-03-offer.png", "Read the offer", "Minimum spend, maximum cashback and end date.")}
{phone("cust-04-activated.png", "Activate and pay", "One tap. Then the customer pays by card.")}
{phone("cust-05-rewards.png", "Track rewards", "Cashback this month, payable and pending.")}
{phone("cust-06-tiers.png", "Tiers", "The customer earns more at each tier.")}
</div><p class="small">Screens from the customer app without a bank colour.</p>''', id_="customer")}

{sec(head("Offer types", "Card-linked, affiliate and promo-code offers in one programme.", "Your customers see each offer type in the same place in your app.") + f'''
<div class="cols">
{card("", "Card-linked offers", "Merchant-funded cashback. The customer activates the offer, then pays by card in store or online.")}
{card("", "Affiliate offers", "Cashback from online brands through affiliate networks. The customer shops through the offer link.")}
{card("", "Promo codes", "Discount codes from online brands. The customer copies the code and uses it at checkout.")}
</div>''' + head("Reward types", "Cashback or points, with tiers and missions.", "You choose how your customers earn.") + f'''
<div class="cols cols--4">
{card("", "Cashback", "Customers earn money back on each eligible purchase.")}
{card("", "Points", "Customers earn points and redeem them for cash value. You set the expiry dates.")}
{card("", "Tiers", "Customers move up tiers on the points they earn in 12 months.")}
{card("", "Missions and badges", "Bonus rewards for repeat spend, such as five purchases in a month.")}
</div>''', "sec--white")}

{sec(head("Cashback you can trust", "Lune checks each purchase against the offer terms.") + f'''
<div class="cols cols--4">
{card("", "Budgets stay in limits", "A campaign closes when its budget runs out. No customer earns more than the cap.")}
{card("", "Refunds handled", "A refund in the refund window reduces the cashback.")}
{card("", "Confirmed after the window", "Cashback becomes final when the refund window ends.")}
{card("", "A full record", "Each purchase has a recorded result, with the reason when it does not earn.")}
</div>''', "sec--white")}

{cta("See one offer go from merchant to customer.", "Contact sales for a live demo. It runs one campaign through the merchant portal, LuneHub and the customer app.", '<a class="btn btn--ghost" href="customers.html">See customers</a>')}
"""

# ------------------------------------------------------------------ CUSTOMERS
STUDIES = [
    ("adib", "adib.avif", "ADIB", "Retail bank · UAE", "ADIB shows customers where their money goes.",
     [("Client", "Abu Dhabi Islamic Bank"), ("Lune products", "Enrich, personal finance SDK"), ("Category accuracy", "98%")],
     "ADIB wanted to give customers useful insight into their spending. Raw transaction descriptions were not clear. Too many transactions had no category.",
     "Enrich adds the merchant name, logo, category and subcategory to each transaction. The Lune SDK gives ADIB ready personal finance screens.",
     ["Customers see the real merchant behind each payment.", "Customers track spending, saving and goals in the ADIB app.", "ADIB can build merchant offers on the same data."], ""),
    ("d360", "d360.avif", "D360 Bank", "Digital bank · Saudi Arabia", "D360 shows the real merchant behind each card payment.",
     [("Client", "D360 Bank"), ("Lune products", "Enrich"), ("Category accuracy", "98%"), ("Time to integrate", "About 2 months")],
     "Many card transactions in the region show a holding-company name, not the store. Customers cannot see where their money goes.",
     "D360 integrated the Enrich API. Each transaction now shows the merchant name, a logo and an accurate category.",
     ["Customers recognise where their money goes.", "D360 personalises its app from clean, categorised data."],
     "“We integrated Lune Enrich in a couple of months, with the team being responsive and helping every step of the way.” Masharty, Associate Director, D360 Bank"),
    ("nbf", "nbf.avif", "National Bank of Fujairah", "Retail bank · UAE", "NBF replaced manual data work with structured insight.",
     [("Client", "National Bank of Fujairah"), ("Lune products", "Enrich, Analytics")],
     "NBF staff read unstructured transaction rows by hand to understand customer spend. The work was slow and hard to scale.",
     "Lune enriches NBF's transactions and gives structured spend insight by merchant and category.",
     ["Teams make decisions faster and with more accurate data.", "NBF builds more personalised services for corporate clients.", "Faster data processing reduces operating cost."], ""),
    ("beyon-money", "beyon-money.avif", "Beyon Money", "Digital wallet · Bahrain", "Beyon Money launched in-app insights in under three months.",
     [("Client", "Beyon Money"), ("Lune products", "Enrich, Analytics"), ("Start to go-live", "Under 3 months")],
     "Beyon Money wanted one app where users see their spending by category in real time. Central Bank of Bahrain data-storage rules also applied.",
     "Enrich categorises each transaction in real time. Lune deployed the platform to meet local data-storage rules.",
     ["Users spend more time in the app.", "Users understand their finances better.", "Beyon Money can add merchant offers on the same data."], ""),
    ("alaan", "alaan.avif", "Alaan", "Fintech · UAE", "Alaan gave SME card users clear transaction insight.",
     [("Client", "Alaan"), ("Lune products", "Enrich")],
     "Alaan issues corporate cards for SMEs in the UAE. It wanted to remove manual work and give customers clearer transactions.",
     "Alaan integrated the Enrich API. Each card transaction now shows the merchant name, logo and a detailed category.",
     ["Alaan shipped transaction insights faster.", "Finance teams see who they paid and for what."], ""),
]


def study(s):
    sid, logo, name, kind, title, dl, ch, dv, out, quote = s
    d = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in dl)
    q = f'<p style="font-weight:600;font-size:22px;line-height:1.3;letter-spacing:-0.02em;color:var(--lune-teal)">{quote}</p>' if quote else ""
    return f"""<article class="card study" id="{sid}"><img class="logo" src="img/clients/{logo}" alt="{e(name)}"><span class="tag">{kind}</span><h3 class="h2" style="font-size:clamp(24px,2.4vw,34px)">{title}</h3>
<dl>{d}</dl><div class="cols"><div><h4 style="margin:0 0 6px">The challenge</h4><p>{ch}</p></div><div><h4 style="margin:0 0 6px">What Lune delivered</h4><p>{dv}</p></div>
<div><h4 style="margin:0 0 6px">The outcome</h4>{facts([(o, "") for o in out])}</div></div>{q}</article>"""


CUSTOMERS = f"""{hero("Customers", 'Banks and fintechs that <span class="serif">run on Lune data.</span>',
 "Retail banks, digital banks and fintechs in the UAE, Saudi Arabia and Bahrain use Lune. Their transactions are clear to customers and to their teams.", BTN_TALK)}
<section><div class="wrap">{logos().replace('<div class="wrap logos">', '<div class="logos" style="margin-top:0">')}</div></section>
{sec(head("Case studies", "Five clients. One result: clear transactions.") + '<div class="stack" style="gap:20px">' + "".join(study(s) for s in STUDIES) + "</div>" + stats())}
{cta("Your bank can be the next case study.", "Contact sales for a live demo on sample data, then on a sample of your own transactions.")}
"""

# ------------------------------------------------------------------ CONTACT
PRODUCTS = ["Enrich", "Analytics", "Expenses", "Cashflow", "Pulse", "Not sure yet"]
COUNTRIES = ["United Arab Emirates", "Saudi Arabia", "Bahrain", "Qatar", "Kuwait", "Oman", "Egypt", "Jordan", "Other"]
CONTACT = f"""{hero("Contact sales", 'Talk to our sales team about <span class="serif">a live demo.</span>',
 "Tell us about your bank and what you want to see. We show Lune on sample data, then on a sample of your own transactions.", "")}
{sec(f'''<div class="split split--top">
<form class="form card" id="contact-form" novalidate>
<div class="form__row">
<div class="field" data-field="first"><label for="f-first">First name</label><input id="f-first" name="first" enterkeyhint="next" autocomplete="given-name" required><span class="err">Enter your first name.</span></div>
<div class="field" data-field="last"><label for="f-last">Last name</label><input id="f-last" name="last" enterkeyhint="next" autocomplete="family-name" required><span class="err">Enter your last name.</span></div>
</div>
<div class="form__row">
<div class="field" data-field="email"><label for="f-email">Work email</label><input id="f-email" name="email" enterkeyhint="next" type="email" inputmode="email" autocomplete="email" required><span class="err">Enter a work email, for example name@bank.com.</span></div>
<div class="field" data-field="company"><label for="f-company">Company</label><input id="f-company" name="company" enterkeyhint="next" autocomplete="organization" required><span class="err">Enter your company name.</span></div>
</div>
<div class="form__row">
<div class="field"><label for="f-title">Job title (optional)</label><input id="f-title" name="title" enterkeyhint="next" autocomplete="organization-title"></div>
<div class="field"><label for="f-country">Country</label><select id="f-country" name="country" autocomplete="country-name">{"".join(f"<option>{c}</option>" for c in COUNTRIES)}</select></div>
</div>
<fieldset class="field" data-field="product"><legend>What do you want to see?</legend><div class="checks">{"".join(f'<label><input type="checkbox" name="product" value="{p}">{p}</label>' for p in PRODUCTS)}</div><span class="err">Select at least one product.</span></fieldset>
<div class="field"><label for="f-notes">Other information for our sales team (optional)</label><textarea id="f-notes" name="notes"></textarea></div>
<p class="small">We use your details only to reply to this request. See our <a href="{LIVE}/lune-privacy">privacy policy</a>.</p>
<div><button class="btn btn--primary" type="submit">Send request</button></div>
<p id="form-done" hidden><b>Your email app opens with the request.</b> Send the email to complete the request.</p>
</form>
<div class="stack" style="gap:24px">
<div class="card card--muted"><h2 class="h3">What happens next</h2>{facts([("1.", "Our sales team replies to your request."), ("2.", "We agree a time for a live demo."), ("3.", "We show the products you selected on sample data.")])}</div>
<div class="card card--muted"><h2 class="h3">Your data</h2><p>The first demo uses sample data only. Lune is ISO 27001 certified and has a SOC 2 Type II report.</p></div>
<div class="card card--muted"><h2 class="h3">Contact details</h2><p><a href="mailto:hello@lunedata.io">hello@lunedata.io</a></p><p>156 Gate Avenue, DIFC<br>Dubai, United Arab Emirates</p>
<a class="more" href="{SALES}" target="_blank" rel="noopener">Try enrichment live ↗</a></div>
</div></div>''')}
"""

PLAT_CARDS = '<div class="cols">' + "".join([
    card("Step 1", "Enrich", "The enrichment API. It returns the merchant name, the logo and the category for each card payment.", ["LuneHub, the portal for your team", "The Transactions page", "Analytics"], link=("enrich.html", "See Enrich")),
    card("Comes with LuneHub", "Analytics", "The Brand explorer, the Category explorer and the spend dashboard.", ["Spend by brand", "Spend by category", "Spend per customer"], link=("analytics.html", "See Analytics")),
    card("Step 2", "Expenses", "Spending screens for your banking app.", ["Lune SDK for iOS and Android", "Your bank's name and colour"], link=("expenses.html", "See Expenses")),
    card("Step 2", "Cashflow", "Money in and money out screens for your banking app.", ["Lune SDK for iOS and Android", "Your bank's name and colour"], link=("cashflow.html", "See Cashflow")),
    card("Step 3", "Pulse", "A rewards programme that merchants fund.", ["Pulse SDK for your app", "Offer approval in LuneHub", "A portal for merchants"], link=("pulse.html", "See Pulse")),
]) + "</div>"
PLAT_H1 = 'Start with Enrich. <span class="serif">Add the others when you need them.</span>'
PLATFORM = f"""{hero("", PLAT_H1,
 "Lune has five products. Each one runs on the same enriched transactions, so each new product uses the data you already have.", BTN_TALK)}

{sec(head("", "Three steps. Each step uses the step before it.") + M.path(detail=True), "sec--white")}

{sec(head("", "Each product, and what comes with it.") + PLAT_CARDS)}

{cta("See which products fit your bank.", "Contact sales for a live demo. We show Lune on sample data, then on a sample of your own transactions.")}
"""

PAGES = [
    ("index.html", "Lune | More card revenue from every transaction", "Lune turns the card transactions you already process into new revenue. Know where your customers spend, and let merchants pay to reach them.", HOME),
    ("enrich.html", "Enrich | Real-time transaction enrichment API | Lune", "Enrich returns the merchant, logo and category for each card transaction in under a millisecond.", ENRICH),
    ("analytics.html", "Analytics | Spend by merchant and category | Lune", "Analytics shows spend by merchant, category and customer from your enriched transactions.", ANALYTICS),
    ("expenses.html", "Expenses | Spending screens for your app | Lune", "Expenses adds ready spending screens to your iOS and Android app.", EXPENSES),
    ("cashflow.html", "Cashflow | Money in against money out | Lune", "Cashflow adds ready screens to your iOS and Android app.", CASHFLOW),
    ("pulse.html", "Pulse | Merchant-funded rewards under your bank's name | Lune", "Pulse is a rewards programme for your customers. Merchants fund the offers. Your bank approves them.", PULSE),
    ("customers.html", "Customers | Banks and fintechs on Lune", "Case studies from ADIB, D360 Bank, National Bank of Fujairah, Beyon Money and Alaan.", CUSTOMERS),
    ("contact.html", "Contact sales | Lune", "Talk to the Lune sales team about a live demo.", CONTACT),
    ("platform.html", "How the Lune products fit together | Lune", "Start with Enrich. Add Expenses, Cashflow and Pulse when you need them.", PLATFORM),
]


# ------------------------------------------------------------------ copy check (STE)
def ste_check(slug, body):
    t = re.sub(r"<(script|style)[\s\S]*?</\1>", " ", body)
    t = re.sub(r"</(p|h\d|li|span|div|b|a|dt|dd|figcaption|button|label|legend|option|blockquote)>", ". ", t)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    issues = []
    for s in re.split(r"(?<=[.!?])\s+", t):
        s = s.strip(" .")
        words = [w for w in s.split() if re.search(r"[A-Za-z]", w)]
        if len(words) > 20 and "“" not in s:          # customer quotes stay as spoken
            issues.append(f"{len(words)} words: {s[:110]}")
        if re.search(r"[;—–]", s):
            issues.append(f"punctuation: {s[:110]}")
    for i in issues:
        print(f"  STE {slug}: {i}")
    return len(issues)


if __name__ == "__main__":
    bad = 0
    for slug, title, desc, body in PAGES:
        (ROOT / slug).write_text(page(slug, title, desc, body), encoding="utf-8")
        bad += ste_check(slug, body)
        for src in set(re.findall(r'(?:src|href)="((?:img|ds)/[^"]+|[a-z-]+\.(?:html|css|js))(?:#[^"]*)?"', page(slug, title, desc, body))):
            if not (ROOT / src).exists():
                print(f"  MISSING {slug}: {src}"); bad += 1
    print(f"built {len(PAGES)} pages, {bad} issue(s)")
    sys.exit(1 if bad else 0)
