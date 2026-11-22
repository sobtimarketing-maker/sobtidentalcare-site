"""From the clinic: the hub blog for general treatments (Dr, 22 Nov 2026).

Implant posts live on dentalimplantsdelhi.com and smile-design posts on drparulssobti.com.
This blog covers everything else: cleaning and air polishing, crowns, children, braces,
root canal, wisdom teeth, extractions, sterilisation and the lab.

Each post is a Markdown file in content/blog/ named NN-slug.md:

    TITLE: Post title
    DATE: 2026-11-24
    DESC: Meta description, under 160 characters.
    AUTHOR: Dr Pushkar Sobti | Dr Parul Sharma Sobti | Dr Sobti's Dental Care
    ---
    Body in simple Markdown: ## headings, paragraphs, "- " lists, [text](url) links.
    A "## Questions" section with **Question?** lines, each followed by its answer, becomes FAQ schema.

A post only appears once its DATE has arrived (India time), so a build never shows a post early.
No prices in posts (Dr, 22 Nov 2026): readers are asked to WhatsApp or call.
"""
import datetime as dt
import html
import json
import re
from pathlib import Path

DIR = Path(__file__).resolve().parent / "content" / "blog"
e = html.escape


def today_ist():
    return (dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)).date()


def inline(s):
    s = e(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)


def parse(path):
    head, body = path.read_text(encoding="utf-8").split("\n---\n", 1)
    meta = dict(line.split(": ", 1) for line in head.strip().splitlines())
    slug = path.stem.split("-", 1)[1]
    main, _, qs = body.partition("\n## Questions\n")
    faq = re.findall(r"\*\*(.+?)\*\*\n(.+)", qs)
    return {"slug": slug, "path": f"blog/{slug}.html", "title": meta["TITLE"], "desc": meta["DESC"],
            "date": dt.date.fromisoformat(meta["DATE"]), "author": meta.get("AUTHOR", "Dr Sobti's Dental Care"),
            "body": main.strip(), "faq": faq}


def render(md):
    out, lst = [], []
    for block in re.split(r"\n\s*\n", md):
        block = block.strip()
        if not block:
            continue
        if block.startswith("## "):
            out.append(f"<h2>{inline(block[3:])}</h2>")
        elif all(line.startswith("- ") for line in block.splitlines()):
            out.append("<ul>" + "".join(f"<li>{inline(l[2:])}</li>" for l in block.splitlines()) + "</ul>")
        else:
            out.append(f"<p>{inline(' '.join(block.splitlines()))}</p>")
    return "\n".join(out)


def posts():
    if not DIR.exists():
        return []
    items = [parse(p) for p in sorted(DIR.glob("*.md"))]
    return sorted([p for p in items if p["date"] <= today_ist()], key=lambda p: p["date"], reverse=True)


def fmt(d):
    return f"{d.day} {d.strftime('%B %Y')}"


def pages(SITE, layout_helpers):
    """Return PAGES entries: (path, title, desc, fn, current, ld, priority)."""
    pagehead, wa, crumbs_schema, faq_schema = layout_helpers
    live = posts()
    if not live:
        return []

    def cta(topic):
        return f"""<section><div class="wrap"><div class="cta">
  <div><h2>Have a question about your teeth?</h2><p>Send us a message on WhatsApp or call the clinic. Our front desk will check with the doctor and get back to you with the next step.</p></div>
  <div class="actions"><a class="btn gold" href="{wa('I read your post "' + topic + '" and would like to ask about it.')}" data-track="whatsapp">WhatsApp us</a><a class="btn light" href="/booking.html">Book a visit</a></div>
</div></div></section>"""

    def index_page():
        cards = "".join(
            f'<article class="card"><p class="muted" style="margin-bottom:.4em">{fmt(p["date"])} · {e(p["author"])}</p>'
            f'<h3><a href="/{p["path"]}">{e(p["title"])}</a></h3><p class="muted">{e(p["desc"])}</p></article>' for p in live)
        return pagehead("From the clinic", "Blog",
                        "Notes from the clinic in Rajouri Garden on everyday dental care: cleaning, crowns, children's teeth, braces, root canals and wisdom teeth. "
                        "For implants, read <a href=\"https://dentalimplantsdelhi.com/\">Dr Pushkar Sobti's implant blog</a>; for smile design, "
                        "<a href=\"https://drparulssobti.com/blog.html\">Dr Parul Sharma Sobti's Smile Journal</a>.") + \
            f'<section><div class="wrap"><div class="grid g2">{cards}</div></div></section>'

    def post_page(p, i):
        newer = live[i - 1] if i > 0 else None
        older = live[i + 1] if i + 1 < len(live) else None
        nav = "".join(
            f'<p class="muted"><strong>{lab}:</strong> <a href="/{q["path"]}">{e(q["title"])}</a></p>'
            for lab, q in (("Newer", newer), ("Older", older)) if q)
        faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in p["faq"])
        faq_html = f'<div class="section-head" style="margin-top:2em"><h2>Questions</h2></div>{faq}' if faq else ""
        return pagehead(e(p["title"]), "Blog", f'{fmt(p["date"])} · {e(p["author"])}') + f"""
<section><div class="wrap blogpost" style="max-width:780px">
{render(p['body'])}
{faq_html}
<hr style="border:0;border-top:1px solid var(--line);margin:2em 0">
{nav}
<p class="muted"><a href="/blog/">All posts from the clinic</a></p>
</div></section>
{cta(p['title'])}"""

    def post_ld(p):
        url = f"{SITE}/{p['path']}"
        art = {"@type": "BlogPosting", "headline": p["title"], "description": p["desc"], "url": url,
               "datePublished": p["date"].isoformat(), "dateModified": p["date"].isoformat(),
               "inLanguage": "en-IN", "mainEntityOfPage": url,
               "author": ({"@type": "Organization", "name": p["author"], "@id": f"{SITE}/#clinic"}
                          if p["author"].startswith("Dr Sobti") else {"@type": "Person", "name": p["author"]}),
               "publisher": {"@id": f"{SITE}/#clinic"}}
        ld = [art, crumbs_schema(p["path"], p["title"])]
        if p["faq"]:
            ld.append(faq_schema(p["faq"]))
        return ld

    out = [("blog/index.html", "From the Clinic: Dental Care Blog | Dr Sobti's Dental Care, Rajouri Garden",
            "Everyday dental care explained by the dentists at Dr Sobti's Dental Care, Rajouri Garden: cleaning and air polishing, crowns, children's teeth, braces, root canals and wisdom teeth.",
            index_page, "", [crumbs_schema("blog/", "Blog")], 0.6)]
    for i, p in enumerate(live):
        out.append((p["path"], f"{p['title']} | Dr Sobti's Dental Care", p["desc"],
                    (lambda p=p, i=i: post_page(p, i)), "", post_ld(p), 0.6))
    return out


def llms_lines(SITE):
    return "".join(f"- [{p['title']}]({SITE}/{p['path']})\n" for p in posts())
