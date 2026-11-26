"""Read the saved pages of the old lunedata.io site and write content.json.

Run: python3 tools/old-site/extract.py
Input: tools/old-site/raw/*.html (blog posts, case studies and legal pages, saved from www.lunedata.io).
Output: tools/old-site/content.json, used by build.py for blog/ and case-studies/.
The text stays as published on the old site, so the pages keep their search value.
"""
import html, json, re
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).parent
KEEP = {"h2", "h3", "h4", "p", "ul", "ol", "li", "strong", "b", "em", "i", "a", "blockquote", "img", "figure", "figcaption", "br", "table", "thead", "tbody", "tr", "th", "td"}
BLOCK = {"h2", "h3", "h4", "p", "ul", "ol", "blockquote", "figure", "table"}
VOID = {"img", "br"}


class Clean(HTMLParser):
    """Keep only article tags, with href, src and alt. Drop the rest."""

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.out, self.skip, self.seen = [], 0, set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style", "noscript", "svg", "iframe", "form"):
            self.skip += 1
            return
        if self.skip or tag not in KEEP:
            return
        if tag == "img":
            src = a.get("src") or ""
            key = re.sub(r"^.*/[0-9a-f]{24}_", "", src)  # the same picture can appear twice for two layouts
            if not src or key in self.seen or "/plugins/Basic/assets/placeholder" in src:  # empty CMS image
                return
            self.seen.add(key)
            self.out.append(f'<img src="{html.escape(src, quote=True)}" alt="{html.escape(a.get("alt") or "", quote=True)}" loading="lazy">')
            return
        if tag == "a":
            href = a.get("href") or ""
            href = re.sub(r"^https?://(www\.)?lunedata\.io", "", href)
            ext = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
            self.out.append(f'<a href="{html.escape(href, quote=True)}"{ext}>')
            return
        self.out.append(f"<{'strong' if tag == 'b' else 'em' if tag == 'i' else tag}>")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "svg", "iframe", "form"):
            self.skip = max(0, self.skip - 1)
            return
        if self.skip or tag not in KEEP or tag in VOID:
            return
        self.out.append(f"</{'strong' if tag == 'b' else 'em' if tag == 'i' else tag}>")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)

    def handle_entityref(self, name):
        if not self.skip:
            self.out.append(f"&{name};")

    def handle_charref(self, name):
        if not self.skip:
            self.out.append(f"&#{name};")


def clean(fragment):
    c = Clean()
    c.feed(fragment)
    s = "".join(c.out)
    s = s.replace("‍", "")                                   # Webflow fills empty lines with a zero-width joiner
    s = re.sub(r"<(p|li|h2|h3|h4|strong|em)>\s*</\1>", "", s)
    s = re.sub(r"<(p|li|h2|h3|h4|strong|em)>\s*</\1>", "", s)
    s = re.sub(r"<(h2|h3|h4)><strong>([\s\S]*?)</strong></\1>", r"<\1>\2</\1>", s)  # headings carry their own weight
    s = re.sub(r"</ul>\s*<ul>", "", s)                            # one list, not one list for each item
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s*(</?(?:h2|h3|h4|p|ul|ol|li|blockquote|figure|table|tr)>)\s*", r"\1", s)
    s = re.sub(r"(</(?:h2|h3|h4|p|ul|ol|blockquote|figure|table)>|<img [^>]+>)", r"\1\n", s)
    return s.strip()


def text(fragment):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def meta(s, attr, name):
    m = re.search(rf'<meta[^>]*content="([^"]*)"[^>]*{attr}="{re.escape(name)}"', s) or re.search(rf'<meta[^>]*{attr}="{re.escape(name)}"[^>]*content="([^"]*)"', s)
    return html.unescape(m.group(1)).strip() if m else ""


def div_inner(s, start):
    """Inner HTML of the div that opens at index start (counts nested divs)."""
    i = s.index(">", start) + 1
    depth = 1
    for m in re.finditer(r"<(/?)div\b", s[i:]):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return s[i:i + m.start()]
    return s[i:]


def blog(slug, s):
    title = text(re.search(r"<h1\b[^>]*>([\s\S]*?)</h1>", s).group(1))
    summ = re.search(r'class="[^"]*blog-main-summ[^"]*">([\s\S]*?)</div>', s)
    date = re.search(r"<div>Published on</div>\s*<div>([^<]+)</div>", s)
    thumb = re.search(r'blog-thumbnail-image[^>]*|background-image:url\(&quot;([^&]+)&quot;\)[^>]*class="blog-thumbnail-image"', s)
    img = (thumb.group(1) if thumb and thumb.group(1) else "") or meta(s, "property", "og:image")
    body = div_inner(s, s.index('class="blog-body-rich'))
    return {"kind": "blog", "slug": slug, "title": title, "summary": text(summ.group(1)) if summ else "",
            "date": date.group(1).strip() if date else "", "image": img,
            "seo_title": text(re.search(r"<title>([\s\S]*?)</title>", s).group(1)),
            "seo_desc": meta(s, "name", "description"), "body": clean(body)}


def case(slug, s):
    a = s.index("case-study-templete")
    b = s.find('class="section case-studies"', a)
    region = s[a:b if b > 0 else len(s)]
    name = text(re.search(r'<h2[^>]*class="h1-100"[^>]*>([\s\S]*?)</h2>', region).group(1))
    summ_i = region.find('class="short-summary')
    summary = clean(div_inner(region, summ_i)) if summ_i > 0 else ""
    lines = [text(x) for x in re.findall(r"<p>([\s\S]*?)</p>", summary)]
    hero = re.search(r'class="section-greyscale-image"[\s\S]*?<img[^>]*src="([^"]+)"', region)
    rest = region[region.find("section-greyscale-image"):]
    rest = rest[rest.find("</section>"):]
    rest = re.sub(r'<div class="[^"]*w-dyn-bind-empty[^"]*">\s*</div>', "", rest)
    return {"kind": "case", "slug": slug, "name": name, "kicker": lines[0] if lines else "",
            "title": lines[1] if len(lines) > 1 else name, "image": hero.group(1) if hero else "",
            "seo_title": text(re.search(r"<title>([\s\S]*?)</title>", s).group(1)),
            "seo_desc": meta(s, "name", "description"), "body": clean(rest)}


LEGAL = ["terms", "lune-privacy", "cookie", "msa", "msa-secan"]


def legal(slug, s):
    i = s.index("<h1")
    title = text(re.search(r"<h1\b[^>]*>([\s\S]*?)</h1>", s[i:]).group(1))
    j = s.index("w-richtext", i)
    j = s.rindex("<div", 0, j)
    intro = [t for t in (text(x) for x in re.findall(r"<(?:div|p)\b[^>]*>([^<]+)</(?:div|p)>", s[i:j])) if t]
    return {"kind": "legal", "slug": slug, "title": title, "intro": intro,
            "seo_title": text(re.search(r"<title>([\s\S]*?)</title>", s).group(1)),
            "seo_desc": meta(s, "name", "description"), "body": clean(div_inner(s, j))}


def main():
    out = {"blog": [], "case": []}
    order = [p.stem for p in (HERE / "raw").glob("*.html")]
    index = (HERE / "raw" / "blog.html").read_text(encoding="utf-8")
    listed = re.findall(r'href="/blog/([^"#?]+)"', index)
    for slug in dict.fromkeys(listed):
        s = (HERE / "raw" / f"blog__{slug}.html").read_text(encoding="utf-8")
        out["blog"].append(blog(slug, s))
    cindex = (HERE / "raw" / "case-studies.html").read_text(encoding="utf-8")
    for slug in dict.fromkeys(re.findall(r'href="/case-studies/([^"#?]+)"', cindex)):
        s = (HERE / "raw" / f"case-studies__{slug}.html").read_text(encoding="utf-8")
        out["case"].append(case(slug, s))
    out["legal"] = [legal(slug, (HERE / "raw" / f"legal__{slug}.html").read_text(encoding="utf-8")) for slug in LEGAL]
    (HERE / "content.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(out['blog'])} posts, {len(out['case'])} case studies, {len(out['legal'])} legal pages, {len(order)} files read")


if __name__ == "__main__":
    main()
