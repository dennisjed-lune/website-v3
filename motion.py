"""Heroes, product animations and flow signifiers for the motion version of the Lune site.

Each animation is plain HTML. motion.js moves one step at a time and adds the class "on"
to each element whose data-at value is reached. motion.css draws the result.
"""
import html

e = html.escape
LOGO = "img/logos/"
CHECK = '<svg class="ck" viewBox="0 0 16 16" aria-hidden="true"><path d="M3.5 8.5l3 3 6-7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
MOON = '<i class="moon" aria-hidden="true"></i>'


def anim(name, v, steps, inner, rest=None):
    r = f' data-rest="{rest}"' if rest is not None else ""
    return f'<div class="anim anim--{name}" data-v="{v}" data-steps="{steps}"{r} aria-hidden="true">{inner}</div>'


def stage(key, label, names, a1, a2, alt):
    """One stage with two animation options and a switch."""
    return f'''<figure class="stage" data-anim-key="{key}">
<div class="stage__top"><span class="shot__bar">{e(label)}</span>
<div class="seg" role="group" aria-label="Animation option"><button type="button" class="seg__b" data-v="1" aria-pressed="true">{names[0]}</button><button type="button" class="seg__b" data-v="2" aria-pressed="false">{names[1]}</button></div></div>
<div class="stage__body" role="img" aria-label="{e(alt)}">{a1}{a2}</div>
<figcaption>Animation with sample data.</figcaption></figure>'''


def solo_stage(key, label, a, alt):
    """One stage with one animation and no switch."""
    return f'''<figure class="stage stage--solo" data-anim-key="{key}">
<div class="stage__top"><span class="shot__bar">{e(label)}</span></div>
<div class="stage__body" role="img" aria-label="{e(alt)}">{a.replace('data-v="2"', 'data-v="1"')}</div>
<figcaption>Animation with sample data.</figcaption></figure>'''


def trio(imgs):
    """Three real app screens in one row."""
    return '<div class="trio">' + "".join(f'<figure><img src="img/app/{f}" alt="{e(t)} screen" loading="lazy"><figcaption>{t}</figcaption></figure>' for f, t in imgs) + "</div>"


EXP_SCREENS = [("exp-home.png", "This month"), ("exp-cats.png", "By category"), ("exp-brand.png", "By brand")]
CF_SCREENS = [("cf-home.png", "Cashflow"), ("cf-in.png", "Money in"), ("cf-trends.png", "Trends")]

# ------------------------------------------------------------------ ENRICH
DEC = [("POS PUR 448812 LVL SHS DXB MALL 00AE", "levelshoes.png", "Level Shoes", "Shopping › Clothing", "AED 1,032.00"),
       ("MAF HYPMKT MOE-0042 DXB ARE", "carrefour.png", "Carrefour", "Groceries › Supermarket", "AED 412.30"),
       ("NF* 8665797172 LOS GATOS 00012", "netflix.png", "Netflix", "Entertainment › Movie Streaming", "AED 56.99")]


def dec_row(i, r, small=False):
    raw, lg, m, cat, amt = r
    return (f'<div class="dr" data-at="{i + 1}"><code class="dr__raw">{e(raw)}</code>'
            f'<span class="dr__out"><img src="{LOGO}{lg}" alt=""><span><b data-scramble>{e(m)}</b><i>{cat}</i></span></span>'
            f'<em class="dr__amt">{amt}</em></div>')


ENRICH_1 = anim("decode", 1, "1300,1200,1200,1200,2800", (
    '<div class="an-card"><div class="an-head"><b>Card payments</b><span class="an-chip" data-at="1">Enriched by Lune</span></div>'
    + "".join(dec_row(i, r) for i, r in enumerate(DEC)) +
    '</div>'), rest=4)

ENRICH_2 = anim("call", 2, "1200,900,900,700,700,700,700,2800", (
    '<div class="call">'
    '<div class="call__node"><span>Your core banking system sends</span><code>POS PUR 448812 LVL SHS DXB MALL 00AE</code></div>'
    '<div class="call__wire" data-at="1"><i></i></div>'
    '<div class="call__node call__node--api" data-at="2"><span>Enrich API</span><b>0.5 ms</b></div>'
    '<div class="call__wire" data-at="3"><i></i></div>'
    '<div class="call__node call__node--out" data-at="3"><span>Your systems receive</span><dl>'
    f'<div data-at="4"><dt>Merchant name</dt><dd>Level Shoes</dd></div>'
    f'<div data-at="5"><dt>Logo</dt><dd><img src="{LOGO}levelshoes.png" alt=""></dd></div>'
    f'<div data-at="6"><dt>Category</dt><dd>Shopping › Clothing</dd></div>'
    f'<div data-at="7"><dt>Recurring</dt><dd>No</dd></div>'
    '</dl></div></div>'), rest=7)

ENRICH_STAGE = stage("enrich", "Enrich", ("Decode", "One API call"), ENRICH_1, ENRICH_2,
                     "Animation: card descriptions change into merchant names, logos and categories")

# ------------------------------------------------------------------ ANALYTICS
SETS = [
    ("All categories", [("carrefour.png", "Carrefour", "AED 96.2M", 100), ("amazon.png", "Amazon", "AED 88.4M", 92), ("starbucks.png", "Starbucks", "AED 41.7M", 43), ("netflix.png", "Netflix", "AED 27.9M", 29)],
     "Carrefour takes the most card spend."),
    ("Shopping", [("amazon.png", "Amazon", "AED 88.4M", 100), ("ikea.png", "IKEA", "AED 21.7M", 25), ("levelshoes.png", "Level Shoes", "AED 14.2M", 16), ("zara.png", "Zara", "AED 12.6M", 14)],
     "In Shopping, Amazon is far ahead of the next brand."),
    ("Travel", [("flydubai.png", "flydubai", "AED 38.5M", 100), ("booking.png", "Booking.com", "AED 22.1M", 57), ("expedia.png", "Expedia", "AED 17.4M", 45), ("airalo.png", "Airalo", "AED 3.9M", 10)],
     "In Travel, one airline leads the spend."),
]


def bars_set(i, s):
    name, rows, note = s
    at, until = i * 2, i * 2 + 2
    body = "".join(f'<div class="br"><img src="{LOGO}{lg}" alt=""><b>{e(n)}</b><span class="br__bar"><i style="--w:{w}%"></i></span><em>{v}</em></div>' for lg, n, v, w in rows)
    return f'<div class="set" data-at="{at}" data-until="{until}">{body}<p class="an-note">{note}</p></div>'


ANALYTICS_1 = anim("brands", 1, "700,2300,700,2300,700,2300", (
    '<div class="an-card"><div class="an-head"><b>Brand explorer</b><span class="an-sub">Total spend · last 6 months</span></div><div class="chips">'
    + "".join(f'<span class="chip" data-at="{i * 2}" data-until="{i * 2 + 2}">{n}</span>' for i, (n, _, _) in enumerate(SETS))
    + '</div><div class="sets">' + "".join(bars_set(i, s) for i, s in enumerate(SETS)) + "</div></div>"), rest=1)

CATS = [
    ("Travel", "137,600", "AED 3,250", "4.1", [("flydubai.png", "flydubai", "AED 38.5M", 100), ("booking.png", "Booking.com", "AED 22.1M", 57), ("expedia.png", "Expedia", "AED 17.4M", 45)]),
    ("Dining", "298,400", "AED 1,710", "21.6", [("starbucks.png", "Starbucks", "AED 41.7M", 100), ("talabat.png", "Talabat", "AED 33.9M", 81), ("costa.png", "Costa Coffee", "AED 12.8M", 31)]),
]


def cat_set(i, c):
    name, cust, per, tx, rows = c
    at, until = i * 2, i * 2 + 2
    tiles = "".join(f'<div class="ct{" ct--key" if k == 1 else ""}"><span>{l}</span><b>{v}</b></div>' for k, (l, v) in enumerate([("Customers", cust), ("Spend per customer", per), ("Payments per customer", tx)]))
    body = "".join(f'<div class="br"><img src="{LOGO}{lg}" alt=""><b>{e(n)}</b><span class="br__bar"><i style="--w:{w}%"></i></span><em>{v}</em></div>' for lg, n, v, w in rows)
    return f'<div class="set" data-at="{at}" data-until="{until}"><div class="cts">{tiles}</div><span class="an-sub">Where these customers spend</span>{body}</div>'


ANALYTICS_2 = anim("customers", 2, "700,2900,700,2900", (
    '<div class="an-card"><div class="an-head"><b>Customers by category</b><span class="an-sub">Last 6 months</span></div><div class="chips">'
    + "".join(f'<span class="chip" data-at="{i * 2}" data-until="{i * 2 + 2}">{c[0]}</span>' for i, c in enumerate(CATS))
    + '</div><div class="sets">' + "".join(cat_set(i, c) for i, c in enumerate(CATS)) + "</div></div>"), rest=1)

ANALYTICS_STAGE = stage("analytics", "LuneHub · Analytics", ("Brands", "Customers"), ANALYTICS_1, ANALYTICS_2,
                        "Animation: spend by brand for each category, and the customers and their spend in one category")


# ------------------------------------------------------------------ EXPENSES and CASHFLOW
def screens(name, v, imgs):
    n = len(imgs)
    pics = "".join(f'<img src="img/app/{f}" alt="" data-at="{i}" data-until="{i + 1}">' for i, (f, _) in enumerate(imgs))
    tabs = "".join(f'<span class="chip" data-at="{i}" data-until="{i + 1}">{t}</span>' for i, (_, t) in enumerate(imgs))
    return anim(name, v, ",".join(["2600"] * n), f'<div class="chips chips--center">{tabs}</div><div class="shots">{pics}</div>', rest=0)


EXPENSES_1 = screens("screens", 1, [("exp-home.png", "This month"), ("exp-cats.png", "By category"), ("exp-brand.png", "By brand")])
EXPENSES_2 = anim("phone", 2, "1200,1000,1000,1000,1400,2800", (
    '<div class="ph"><div class="ph__top"><b>Expenses</b><span>This month</span></div>'
    '<div class="ph__total"><span>Total spent</span><b>AED <span data-count="1501.29" data-at="1">0.00</span></b></div>'
    + "".join(dec_row(i, r) for i, r in enumerate(DEC)) +
    '<div class="ph__cats" data-at="4"><i style="--w:69%;--c:var(--cat-shopping)"></i><i style="--w:27%;--c:var(--cat-grocery)"></i><i style="--w:4%;--c:#A594F9"></i></div>'
    '<div class="ph__legend" data-at="4"><span style="--c:var(--cat-shopping)">Shopping</span><span style="--c:var(--cat-grocery)">Groceries</span><span style="--c:#A594F9">Entertainment</span></div></div>'), rest=5)
EXPENSES_STAGE = solo_stage("expenses", "Expenses · SDK for your app", EXPENSES_2,
                            "Animation: card descriptions become a spending view with merchant names and categories")

CASHFLOW_1 = screens("screens", 1, [("cf-home.png", "Cashflow"), ("cf-in.png", "Money in"), ("cf-trends.png", "Trends")])
MONTHS = [("Jun", 62, 48), ("Jul", 70, 66), ("Aug", 58, 61), ("Sep", 74, 52), ("Oct", 68, 57), ("Nov", 80, 56)]
CASHFLOW_2 = anim("phone", 2, "1100,1100,1100,1300,3000", (
    '<div class="ph"><div class="ph__top"><b>Cashflow</b><span>November</span></div>'
    '<div class="cf"><div class="cf__row" data-at="1"><span>Money in</span><span class="cf__bar cf__bar--in"><i style="--w:100%"></i></span><b>AED 18,400</b></div>'
    '<div class="cf__row" data-at="2"><span>Money out</span><span class="cf__bar"><i style="--w:70%"></i></span><b>AED 12,950</b></div></div>'
    '<div class="ph__total ph__total--net" data-at="3"><span>Left this month</span><b>AED <span data-count="5450" data-at="3">0</span></b></div>'
    '<div class="cf__months" data-at="4">' + "".join(f'<div><span><i style="--h:{a}%"></i><i style="--h:{b}%"></i></span><em>{m}</em></div>' for m, a, b in MONTHS) + "</div></div>"), rest=4)
CASHFLOW_STAGE = solo_stage("cashflow", "Cashflow · SDK for your app", CASHFLOW_2,
                            "Animation: money in against money out for one month, then six months")

# ------------------------------------------------------------------ PULSE
PULSE_1 = anim("cashback", 1, "1500,900,1300,1300,1600,3000", (
    '<div class="pz">'
    f'<div class="pz__offer"><img src="{LOGO}levelshoes.png" alt=""><div><b>Level Shoes</b><span>10% cashback · minimum spend AED 300</span></div>'
    f'<span class="pz__btn" data-at="1" data-until="2">Activate</span><span class="pz__btn pz__btn--idle" data-at="0" data-until="1">Activate</span><span class="pz__btn pz__btn--done" data-at="2">{CHECK}Activated</span></div>'
    '<div class="pz__pay" data-at="3"><span>Card payment</span><b>Level Shoes</b><em>AED 1,032.00</em></div>'
    '<div class="pz__win" data-at="4"><span>Cashback earned</span><b>+ AED <span data-count="103.20" data-at="4">0.00</span></b><i>Paid by Level Shoes</i></div>'
    '<p class="an-note" data-at="5">The customer earns. The merchant pays.</p></div>'), rest=5)

PULSE_2 = anim("tiers", 2, "1300,1000,1000,1000,1500,3000", (
    '<div class="tz"><div class="tz__top"><span>Your tier</span><b><span data-at="0" data-until="4">Silver</span><span data-at="4">Gold</span></b></div>'
    '<div class="tz__track"><i data-at="1" data-until="2" style="--w:55%"></i><i data-at="2" data-until="3" style="--w:75%"></i><i data-at="3" style="--w:100%"></i>'
    '<span class="tz__stop" style="--x:0%">Silver</span><span class="tz__stop" data-at="3" style="--x:100%">Gold</span></div>'
    '<div class="tz__pts"><b><span data-count="2500" data-from="1375" data-at="1">1,375</span></b> of 2,500 points</div>'
    '<div class="tz__mission"><span>Mission: five purchases this month</span><div>'
    + "".join(f'<i data-at="{a}">{CHECK}</i>' for a in (0, 0, 1, 2, 3)) +
    '</div></div>'
    '<div class="tz__badge" data-at="4"><b>Gold tier reached</b><span>The customer now earns more on each offer.</span></div></div>'), rest=5)

PULSE_STAGE = stage("pulse", "Pulse · in your banking app", ("Cashback", "Tiers and missions"), PULSE_1, PULSE_2,
                    "Animation: a customer activates an offer, pays by card and earns cashback, then reaches a higher tier")

# ------------------------------------------------------------------ AI ASSISTANT
def ai_tx(logo, name, cat, amt, at=""):
    return f'<div class="ai__tx"{at}><img src="{LOGO}{logo}" alt=""><span><b>{name}</b><em>{cat}</em></span><b>{amt}</b></div>'


def ai_offer(btn, at=""):
    return f'<div class="ai__offer"{at}><span>Offer for you</span><b>10% cashback</b><em>At Level Shoes, with your card</em>{btn}</div>'


AI_CHAT = anim("chat", 1, "900,1300,1300,1500,1300,3200", (
    '<div class="ph ph--chat"><div class="ph__top"><b>Assistant</b><span>Expenses</span></div>'
    '<p class="ai__q" data-at="0">How much did I spend on shopping this month?</p>'
    '<p class="ai__a" data-at="1">You spent AED 1,477 on shopping this month.</p>'
    + ai_tx("levelshoes.png", "Level Shoes", "Shopping › Clothing", "AED 1,032.00", ' data-at="2"')
    + ai_tx("zara.png", "Zara", "Shopping › Clothing", "AED 445.00", ' data-at="2"')
    + ai_offer('<span class="ai__btns"><span class="ai__btn" data-at="3" data-until="4">Activate offer</span><span class="ai__btn ai__btn--done" data-at="4">Offer activated ✓</span></span>', ' data-at="3"')
    + '<p class="ai__a" data-at="5">Done. Pay with your card at Level Shoes to earn the cashback.</p></div>'), rest=5)
AI_STAGE = solo_stage("ai", "Assistant in the Lune SDK", AI_CHAT,
                      "Animation: a customer asks about shopping spend. The assistant answers with merchants and shows a cashback offer")

STAGES = {"enrich": ENRICH_STAGE, "analytics": ANALYTICS_STAGE, "expenses": EXPENSES_STAGE, "cashflow": CASHFLOW_STAGE, "pulse": PULSE_STAGE}

# ------------------------------------------------------------------ HEROES
H1 = 'More card revenue.<br><span class="serif">From every transaction.</span>'
LEAD = "Lune turns the card transactions you already process into new revenue. Know where your customers spend, and let merchants pay to reach them."


def copy(btns, cls=""):
    return f'<div class="hero__copy {cls}"><h1>{H1}</h1><p class="lead">{LEAD}</p><div class="btns">{btns}</div></div>'


def hero_a(btns):
    """Light stage. A bank card in 3D with the enriched result around it."""
    return f'''<div class="hv hv--a"><div class="wrap hv-a">
{copy(btns)}
<div class="scene" data-tilt aria-hidden="true">
  <div class="scene__rings" data-depth="0.2"><i></i><i></i><i></i></div>
  <div class="scene__card" data-depth="0.6"><div class="bcard"><span class="bcard__chip"></span>{MOON}<span class="bcard__no">5311 22•• •••• 4471</span><span class="bcard__name">Your bank card</span></div></div>
  <div class="scene__w scene__w--raw" data-depth="1.3"><span>Card description</span><code>POS PUR 448812 LVL SHS DXB MALL 00AE</code></div>
  <div class="scene__w scene__w--name" data-depth="1.7"><img src="{LOGO}levelshoes.png" alt=""><div><b>Level Shoes</b><span>Shopping › Clothing</span></div><em>AED 1,032.00</em></div>
  <div class="scene__w scene__w--cash" data-depth="2.2"><span>Cashback</span><b>+ AED 103.20</b><i>Paid by the merchant</i></div>
</div>
</div></div>'''


def hero_b(btns):
    """Grid stage. The headline arrives behind a stripe. A band shows one payment change."""
    return f'''<div class="hv hv--b"><div class="wrap hv-b">
<div class="hv-b__grid" aria-hidden="true" data-plx="0.06"></div>
{copy(btns, "hv-b__copy")}
<div class="band-x" aria-hidden="true"><div class="band-x__in">
  <div class="bx bx--raw"><span>Your bank receives</span><code>POS PUR 448812 LVL SHS DXB MALL 00AE</code></div>
  <div class="bx bx--name"><span>Your customer sees</span><b><img src="{LOGO}levelshoes.png" alt="">Level Shoes</b></div>
  <div class="bx bx--cash"><span>The merchant pays</span><b>+ AED 103.20 cashback</b></div>
  <i class="band-x__wipe"></i>
</div></div>
</div></div>'''


def hero_c(btns):
    """Dark stage. The live enrichment feed."""
    return f'''<div class="hv hv--c"><div class="wrap hero__grid hv-c">
{copy(btns)}
<div class="feed-wrap" data-tilt><div class="feed" data-depth="0.5">
  <div class="feed__top"><span class="feed__live">Live enrichment</span><span class="feed__count"><span id="feed-count">1,482,113</span> enriched today</span></div>
  <div class="feed__rows" id="feed" aria-hidden="true"></div>
  <p class="feed__note">Example feed. Lune turns each card description into a merchant, a logo and a category in under a millisecond.</p>
</div></div>
</div></div>'''


def heroes(btns):
    return hero_a(btns) + hero_b(btns) + hero_c(btns)


OPTIONS = '''<div class="opts bopts" role="group" aria-label="Button colour"><span>Button</span><button type="button" data-btn="ink"><i style="background:#070312"></i>Ink</button><button type="button" data-btn="emerald"><i style="background:#10A37F"></i>Emerald</button><button type="button" data-btn="coral"><i style="background:#FF7A59"></i>Coral</button></div>
<div class="opts" role="group" aria-label="Design options"><span>Hero</span>
<button type="button" data-hero="a" aria-pressed="true">Card in 3D</button><button type="button" data-hero="b" aria-pressed="false">Reveal</button><button type="button" data-hero="c" aria-pressed="false">Live feed</button></div>'''

# ------------------------------------------------------------------ FLOW SIGNIFIERS
STEPS = [("enrich", "Enrich"), ("lunehub", "LuneHub"), ("analytics", "Analytics"), ("app", "Expenses and Cashflow"), ("pulse", "Pulse")]
RAIL = ('<nav class="rail" aria-label="The Lune flow"><div class="wrap rail__row"><span class="rail__now" aria-hidden="true"></span><ol>'
        + "".join(f'<li><a href="#{i}"><i>{n + 1}</i><span>{t}</span></a></li>' for n, (i, t) in enumerate(STEPS)) + "</ol></div></nav>")


def chapter_head(tag, h2, lead, cls=""):
    return f'<div class="chead{cls}"><h2>{h2}</h2><p class="lead">{lead}</p></div>'


STACK = f'''<div class="fan">
<a class="sm fan__base" href="#enrich"><span class="sm__k">The foundation</span><b>Enrich</b><span>Each card payment gets a merchant name, a logo and a category.</span>
<span class="fan__eg" aria-hidden="true"><code>POS PUR 448812 LVL SHS</code><i>↓</i><span><img src="{LOGO}levelshoes.png" alt=""><b>Level Shoes</b><em>Shopping › Clothing</em></span></span></a>
<svg class="fan__lines" viewBox="0 0 100 300" preserveAspectRatio="none" aria-hidden="true"><path d="M0 150 C55 150 45 50 100 50"/><path d="M0 150 L100 150"/><path d="M0 150 C55 150 45 250 100 250"/></svg>
<div class="fan__out">
<a class="sm" href="#lunehub"><span class="sm__k">For your team</span><b>LuneHub</b><span>Transactions and Analytics.</span></a>
<a class="sm" href="#app"><span class="sm__k">For your customers</span><b>Expenses and Cashflow</b><span>Screens for your banking app.</span></a>
<a class="sm sm--pulse" href="#pulse"><span class="sm__k">New revenue</span><b>Pulse</b><span>Merchants pay to reward your customers.</span></a>
</div>
</div>'''

def path(detail=False):
    """Three steps: start with Enrich, add the app screens, add Pulse."""
    def col(n, when, name, what, incl, more):
        chips = "".join(f"<li>{x}</li>" for x in incl)
        extra = f'<p class="path__more">{more}</p>' if detail else ""
        return (f'<div class="path__c"><div class="path__when"><i>{n}</i><span>{when}</span></div><h3>{name}</h3><p>{what}</p>'
                f'<span class="path__inc">Comes with it</span><ul>{chips}</ul>{extra}</div>')
    return ('<div class="path">'
            + col(1, "Start here", "Enrich", "Each card payment gets a merchant name, a logo and a category.", ["LuneHub", "Transactions page", "Analytics"],
                  "Your systems call the Enrich API. Your team works in LuneHub, the portal for your bank.")
            + col(2, "Add for your customers", "Expenses and Cashflow", "Ready screens for your banking app, with the enriched transactions.", ["Lune SDK for iOS and Android"],
                  "Each one is a separate product. Add one or the two together.")
            + col(3, "Add for revenue", "Pulse", "A rewards programme that merchants fund, under your bank's name.", ["Pulse SDK for your app"],
                  "A separate product. Your team approves each offer in LuneHub.")
            + "</div>")


def page_stage(key):
    """The stage on a product page starts with the second animation. The home page starts with the first."""
    return STAGES[key].replace(f'data-anim-key="{key}"', f'data-anim-key="{key}-page" data-default="2"')
