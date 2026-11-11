#!/usr/bin/env python3
"""Builds www.sobtidentalcare.com into _site/.

Plain Python, no dependencies. Run `python3 build.py` and open _site/index.html.
Clinic details (NAP) live in the CLINIC block below and must match the
Google Business Profile exactly.
"""
import html
import json
import shutil
from pathlib import Path

from videos_data import V as VIDEOS, obj as video_obj, card as video_card, JS as VIDEO_JS

ROOT = Path(__file__).parent
OUT = ROOT / "_site"
SITE = "https://www.sobtidentalcare.com"

# ---- Clinic details: keep identical to the Google Business Profile ----
CLINIC = {
    "name": "Dr Sobti's Dental Care",
    "street": "J 12/26, First Floor, Rajouri Garden",
    "landmark": "Above Rajmandir, Rajouri Garden",
    "locality": "New Delhi",
    "region": "Delhi",
    "postcode": "110027",
    "phone_display": "+91 87449 85976",
    "phone_tel": "+918744985976",
    "wa_display": "+91 80767 77307",
    "wa_tel": "+918076777307",
    "wa_link": "https://wa.me/918076777307",
    "email": "sobticlinic@gmail.com",
    "lat": 28.6407497,
    "lng": 77.120662,
    "maps": "https://maps.google.com/maps?cid=6577991291147149801",
    "review_link": "https://search.google.com/local/writereview?placeid=ChIJf7C_p8MDDTkR6WFwRDq4SVs",
    "rating": "5.0",
    "review_count": 118,
}
ADDRESS_LINE = f'{CLINIC["street"]}, {CLINIC["locality"]}, {CLINIC["region"]} {CLINIC["postcode"]}'
MAP_EMBED = "https://maps.google.com/maps?q=Dr+Sobti%27s+Dental+Care,+J+12/26+Rajouri+Garden,+New+Delhi+110027&z=16&output=embed"
IMPLANTS = "https://dentalimplantsdelhi.com"
UPDATED = "2026-11-09"  # change when facts on the site change; shown to AI search as dateModified
LINKEDIN_PUSHKAR = "https://www.linkedin.com/in/pushkar-sobti-159699200/"
LINKEDIN_CLINIC = "https://www.linkedin.com/company/sobti-dental-clinic/"
SMILE = "https://drparulssobti.com"
SOCIAL = {
    "Google": "https://maps.google.com/maps?cid=6577991291147149801",
    "Instagram": "https://www.instagram.com/sobtidentalcare/",
    "Facebook": "https://www.facebook.com/sobtidentalcare",
    "YouTube": "https://www.youtube.com/@DrSobtiDental",
}
# ---- Brand and branches ----
# One brand, several clinics. Rajouri Garden (CLINIC above) is the main clinic: it owns the home page
# and all marketing. Other branches get their own page at /<slug>.html, built from BRANCHES.
# A branch is only published once its signboard name, own phone and hours are confirmed by Dr,
# and its NAP must match that branch's own Google Business Profile exactly.
BRAND = {
    "name": "Dr Sobti's Dental Care",
    "founding_year": "1982",
    "founding_place": "Vishnu Garden, New Delhi",
    "founder": "Dr Rajesh Sobti",
    "founder_quals": "MBBS, DCH",
    "story": "A family clinic since 1982, when Dr Rajesh Sobti (MBBS, DCH), Dr Pushkar Sobti's father, opened it in Vishnu Garden. Dr Pushkar joined him in 2009 and opened the Rajouri Garden dental clinic in 2024.",
}
CLINIC_AREA = "Rajouri Garden"
CLINIC_OPENED = "2024-10-01"  # opening date on the Rajouri Garden Google profile
CLINIC_DOCTORS = ["dr-pushkar", "dr-parul"]
BRANCHES = [
    {
        "slug": "vishnu-garden",
        "publish": True,
        "area": "Vishnu Garden",
        "name": "Sobti Medical & Dental Clinic",  # signboard name (Dr, 4 Nov 2026)
        "types": ["MedicalClinic", "Dentist"],
        "specialty": ["Pediatric", "Dentistry"],
        "street": "WZ 168, Mangal Bazaar Road, Vishnu Garden",  # as on the branch's Google profile
        "landmark": "",
        "locality": "New Delhi", "region": "Delhi", "postcode": "110018",
        "phone_display": "+91 11 4214 3719", "phone_tel": "+911142143719",  # Vishnu Garden landline (Dr, 4 Nov 2026)
        "hours": [("Monday to Saturday, morning", "Mo-Sa", "09:30", "12:00"),
                  ("Monday to Saturday, evening", "Mo-Sa", "17:30", "19:30")],
        "closed": "Sunday",
        # (doctor, when, based here?). Dr Pushkar and Dr Parul are based at Rajouri Garden and see
        # Vishnu Garden patients by appointment only (Dr, 4 Nov 2026), so they stay out of this branch's schema.
        "doctors": [("dr-rajesh", "Monday to Saturday, 9:30 am to 12 noon and 5:30 pm to 7:30 pm", True),
                    ("dr-pushkar", "By appointment only; based at the Rajouri Garden clinic", False),
                    ("dr-parul", "By appointment only; based at the Rajouri Garden clinic", False)],
        "lat": 28.6451866, "lng": 77.1008765,
        "maps": "https://maps.google.com/maps?cid=4235763968755079234",
        "opened": "1982",
        "about": "The family's first clinic, opened in 1982 by Dr Rajesh Sobti (MBBS, DCH). Dr Pushkar Sobti began practice here in 2009.",
    },
]
LIVE_BRANCHES = [b for b in BRANCHES if b["publish"]]
DAY_NAMES = {"Mo": "Monday", "Tu": "Tuesday", "We": "Wednesday", "Th": "Thursday", "Fr": "Friday", "Sa": "Saturday", "Su": "Sunday"}
DAY_ORDER = list(DAY_NAMES)


def clock(t):
    """'17:30' -> '5:30 pm', '12:00' -> '12 noon'."""
    h, m = map(int, t.split(":"))
    if (h, m) == (12, 0):
        return "12 noon"
    return f"{h % 12 or 12}{':%02d' % m if m else ''} {'am' if h < 12 else 'pm'}"


def day_list(spec):
    """'Mo-Sa' or 'Mo,We,Fr' -> schema.org day names."""
    if "-" in spec:
        a, b = spec.split("-")
        return [DAY_NAMES[d] for d in DAY_ORDER[DAY_ORDER.index(a):DAY_ORDER.index(b) + 1]]
    return [DAY_NAMES[d] for d in spec.split(",")]


FONTS = "https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;1,9..144,500&family=Manrope:wght@400;500;600;700&display=swap"

NAV = [
    ("index.html", "Home"),
    ("about.html", "About us"),
    ("treatments.html", "Treatments"),
    ("reviews.html", "Reviews"),
    ("contact.html", "Contact"),
]

e = html.escape


def wa(text):
    from urllib.parse import quote
    return f'{CLINIC["wa_link"]}?text={quote(text)}'


WA_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7a2.8 2.8 0 0 0 1.8-1.3 2.3 2.3 0 0 0 .2-1.3c-.1-.1-.2-.2-.5-.3Z"/></svg>'

# ---------------- Schema ----------------

ORG_ID = f"{SITE}/#organization"


def org_schema():
    org = {
        "@type": "MedicalOrganization",
        "@id": ORG_ID,
        "name": BRAND["name"],
        "url": f"{SITE}/",
        "logo": f"{SITE}/assets/img/logo.png",
        "description": BRAND["story"],
        "foundingDate": BRAND["founding_year"],
        "foundingLocation": {"@type": "Place", "name": BRAND["founding_place"]},
        "email": CLINIC["email"],
        "medicalSpecialty": ["Dentistry"],
        "sameAs": [SOCIAL["Instagram"], SOCIAL["Facebook"], SOCIAL["YouTube"], LINKEDIN_CLINIC],
        "subOrganization": [{"@id": f"{SITE}/#clinic", "name": f"{CLINIC['name']}, {CLINIC_AREA}", "url": f"{SITE}/"}]
        + [{"@id": f"{SITE}/{b['slug']}.html#clinic", "name": f"{b['name']}, {b['area']}", "url": f"{SITE}/{b['slug']}.html"}
           for b in LIVE_BRANCHES],
        "employee": [{"@id": f"{SITE}/#dr-pushkar"}, {"@id": f"{SITE}/#dr-parul"}],
    }
    if BRAND["founder"]:
        org["founder"] = {"@type": "Person", "@id": f"{SITE}/#dr-rajesh", "name": BRAND["founder"], "honorificSuffix": BRAND["founder_quals"],
                          "jobTitle": "Physician"}
    return org


def branch_schema(b):
    node = {
        "@type": b.get("types", "Dentist"),
        "@id": f"{SITE}/{b['slug']}.html#clinic",
        "name": b["name"],
        "url": f"{SITE}/{b['slug']}.html",
        "parentOrganization": {"@id": ORG_ID},
        "telephone": b["phone_tel"],
        "address": {"@type": "PostalAddress", "streetAddress": b["street"], "addressLocality": b["locality"],
                    "addressRegion": b["region"], "postalCode": b["postcode"], "addressCountry": "IN"},
        "hasMap": b["maps"],
        "foundingDate": b["opened"],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": day_list(spec),
                                       "opens": o, "closes": c} for _, spec, o, c in b["hours"]],
        "employee": [{"@id": f"{SITE}/#{d}"} for d, _, here in b["doctors"] if here],
        "medicalSpecialty": b.get("specialty", ["Dentistry"]),
        "sameAs": [b["maps"]],
    }
    if b["lat"]:
        node["geo"] = {"@type": "GeoCoordinates", "latitude": b["lat"], "longitude": b["lng"]}
    return node


def clinic_schema():
    return {
        "@type": "Dentist",
        "@id": f"{SITE}/#clinic",
        "parentOrganization": {"@id": ORG_ID},
        "foundingDate": CLINIC_OPENED,
        "name": CLINIC["name"],
        "url": f"{SITE}/",
        "logo": f"{SITE}/assets/img/logo.png",
        "image": [f"{SITE}/assets/img/clinic-reception-waiting.jpg", f"{SITE}/assets/img/clinic-treatment-room.jpg", f"{SITE}/assets/img/clinic-treatment-room-3.jpg"],
        "description": "Dental clinic in Rajouri Garden, West Delhi, led by implantologist Dr Pushkar Sobti and aesthetic dentist Dr Parul Sharma Sobti. Implants, cosmetic dentistry and family dental care with in-house CBCT and lab.",
        "telephone": "+91-87449-85976",
        "email": CLINIC["email"],
        "priceRange": "₹₹",
        "currenciesAccepted": "INR",
        "paymentAccepted": "Cash, Credit Card, Bank Transfer",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": CLINIC["street"],
            "addressLocality": CLINIC["locality"],
            "addressRegion": CLINIC["region"],
            "postalCode": CLINIC["postcode"],
            "addressCountry": "IN",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": CLINIC["lat"], "longitude": CLINIC["lng"]},
        "hasMap": CLINIC["maps"],
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "10:00", "closes": "19:00",
        }],
        "contactPoint": [
            {"@type": "ContactPoint", "telephone": "+91-87449-85976", "contactType": "customer service", "areaServed": "IN", "availableLanguage": ["English", "Hindi"]},
            {"@type": "ContactPoint", "telephone": "+91-80767-77307", "contactType": "reservations", "description": "WhatsApp", "availableLanguage": ["English", "Hindi"]},
        ],
        "areaServed": ["Rajouri Garden", "Punjabi Bagh", "Tagore Garden", "Subhash Nagar", "Ramesh Nagar", "Tilak Nagar", "Janakpuri", "Vikaspuri", "Paschim Vihar", "Naraina", "Kirti Nagar", "Moti Nagar", "Patel Nagar", "Rajinder Nagar", "Pitampura", "Netaji Subhash Place", "West Delhi"],
        "medicalSpecialty": ["Dentistry"],
        "isAcceptingNewPatients": True,
        "knowsLanguage": ["English", "Hindi"],
        "knowsAbout": ["Dental implants", "All-on-4 and All-on-X full mouth implants", "CBCT 3D dental scanning",
                       "Veneers", "Teeth whitening", "Smile design", "Root canal treatment", "Zirconia and E-max crowns",
                       "Children's dentistry", "Emergency dental care"],
        "makesOffer": [offer(n, price, unit) for n, price, unit in PRICES],
        "employee": [{"@id": f"{SITE}/#{d}"} for d in CLINIC_DOCTORS],
        "sameAs": [CLINIC["maps"], SOCIAL["Instagram"], SOCIAL["Facebook"], SOCIAL["YouTube"], LINKEDIN_CLINIC],
        "availableService": [{"@type": "MedicalProcedure", "name": n} for n in [
            "Dental implants", "Full mouth dental implants (All-on-4 / All-on-X)", "Veneers", "Teeth whitening",
            "Smile makeover", "Root canal treatment", "Dental crowns and bridges", "Braces", "Clear aligners",
            "Teeth cleaning (air polishing)", "Wisdom tooth removal", "Dentures", "Children's dentistry", "Emergency dental care"]],
    }


PRICES = [
    # (service, starting price in INR, unit). Only prices already published on the clinic's sites.
    ("In-clinic dental consultation with examination", 700, None),
    ("Single dental implant with crown", 35000, None),
    ("All-on-4 full arch dental implants", 200000, "per jaw"),
    ("All-on-6 full arch dental implants", 300000, "per jaw"),
    ("Veneers", 10000, "per tooth"),
    ("Teeth whitening", 8000, None),
    ("Zirconia crown", 8000, "per tooth"),
    ("E-max crown", 10000, "per tooth"),
]


def inr(n):
    """Indian digit grouping: 300000 -> 3,00,000."""
    t = str(n)
    if len(t) <= 3:
        return t
    head, tail = t[:-3], t[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:]); head = head[:-2]
    return ",".join([head, *parts, tail]) if head else ",".join([*parts, tail])


def offer(name, price, unit):
    return {"@type": "Offer", "itemOffered": {"@type": "MedicalProcedure", "name": name},
            "priceSpecification": {"@type": "PriceSpecification", "minPrice": price, "priceCurrency": "INR",
                                   **({"description": f"From ₹{inr(price)} {unit}"} if unit else {})}}


def work_locations(doc):
    """The clinic(s) a doctor works at: Rajouri Garden plus any published branch that lists them."""
    locs = [{"@id": f"{SITE}/#clinic"}] if doc in CLINIC_DOCTORS else []
    return locs + [{"@id": f"{SITE}/{b['slug']}.html#clinic"} for b in LIVE_BRANCHES if any(d == doc and here for d, _, here in b["doctors"])]


def doctor_schema():
    return [
        {"@type": "Person", "@id": f"{SITE}/#dr-pushkar", "name": "Dr Pushkar Sobti",
         "jobTitle": "Implantologist", "honorificSuffix": "BDS, MDS",
         "image": f"{SITE}/assets/img/dr-pushkar-sobti-portrait.jpg",
         "worksFor": {"@id": ORG_ID}, "workLocation": work_locations("dr-pushkar"), "url": f"{IMPLANTS}/",
         "sameAs": [f"{IMPLANTS}/", LINKEDIN_PUSHKAR],
         "alumniOf": {"@type": "CollegeOrUniversity", "name": "UCAM Universidad Católica San Antonio de Murcia"},
         "description": "Implantologist at Dr Sobti's Dental Care, Rajouri Garden. In practice since 2009, more than 5,000 implants placed, focused on All-on-X full-arch implants planned on CBCT with guided surgery.",
         "knowsAbout": ["Dental implants", "All-on-X full-arch implants", "Guided implant surgery", "Bone grafting"],
         "knowsLanguage": ["English", "Hindi"]},
        {"@type": "Person", "@id": f"{SITE}/#dr-parul", "name": "Dr Parul Sharma Sobti",
         "jobTitle": "Aesthetic dentist", "honorificSuffix": "BDS",
         "image": f"{SITE}/assets/img/dr-parul-sharma-sobti.jpg",
         "worksFor": {"@id": ORG_ID}, "workLocation": work_locations("dr-parul"), "url": f"{SMILE}/", "sameAs": [f"{SMILE}/"],
         "description": "Aesthetic dentist at Dr Sobti's Dental Care, Rajouri Garden: veneers, whitening, smile makeovers and everyday dentistry.",
         "knowsAbout": ["Smile design", "Veneers", "Teeth whitening", "Cosmetic dentistry"],
         "knowsLanguage": ["English", "Hindi"]},
    ]


def website_schema():
    return {"@type": "WebSite", "@id": f"{SITE}/#website", "url": f"{SITE}/", "name": CLINIC["name"],
            "publisher": {"@id": ORG_ID}, "inLanguage": "en-IN"}


def crumbs_schema(path, name):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": f"{SITE}/{path}"}]}


def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


# ---------------- Layout ----------------

def layout(path, title, desc, body, current, extra_ld=(), og_image="assets/img/share.jpg"):
    canonical = f"{SITE}/" if path == "index.html" else f"{SITE}/{path}"
    webpage = {"@type": "WebPage", "@id": f"{canonical}#webpage", "url": canonical, "name": title, "description": desc,
               "isPartOf": {"@id": f"{SITE}/#website"},
               "about": {"@id": next((n["@id"] for n in extra_ld if n.get("@type") == "Dentist"), f"{SITE}/#clinic")},
               "inLanguage": "en-IN", "dateModified": UPDATED}
    graph = [org_schema(), clinic_schema(), *doctor_schema(), website_schema(), webpage, *extra_ld]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    nav = "".join(
        f'<a href="{"/" if href == "index.html" else "/" + href}"{" aria-current=\"page\"" if href == current else ""}>{label}</a>' for href, label in NAV)
    return f"""<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#1e4ea2">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(CLINIC['name'])}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/{og_image}">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="/assets/img/favicon.png">
<link rel="apple-touch-icon" href="/assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="/assets/style.css">
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap">
  <span class="addr">{e(CLINIC['street'])}, New Delhi 110027 · Open all 7 days, 10 am to 7 pm</span>
  <span>Call <a href="tel:{CLINIC['phone_tel']}" data-track="call">{CLINIC['phone_display']}</a> · WhatsApp <a href="{CLINIC['wa_link']}" data-track="whatsapp">{CLINIC['wa_display']}</a></span>
</div></div>
<header class="site"><div class="wrap">
  <a class="brand" href="/" aria-label="{e(CLINIC['name'])}, home"><img src="/assets/img/logo.png" alt="{e(CLINIC['name'])}" width="560" height="167"></a>
  <button class="menu-btn" aria-expanded="false" aria-controls="nav">Menu</button>
  <nav class="main" id="nav" aria-label="Main">{nav}</nav>
  <a class="btn" href="/booking.html">Book a visit</a>
</div></header>
<main id="main">
{body}
</main>
<footer class="site"><div class="wrap">
  <div class="cols">
    <div>
      <span class="flogo"><img src="/assets/img/logo.png" alt="{e(CLINIC['name'])}" width="560" height="167" loading="lazy"></span>
      <p><strong style="color:#fff">{e(CLINIC['name'])}</strong><br>{e(CLINIC['street'])}<br>{e(CLINIC['locality'])}, {e(CLINIC['region'])} {CLINIC['postcode']}<br><span class="muted" style="color:#9fb0cf">{e(CLINIC['landmark'])}</span></p>
      <p>Phone <a href="tel:{CLINIC['phone_tel']}" data-track="call">{CLINIC['phone_display']}</a><br>WhatsApp <a href="{CLINIC['wa_link']}" data-track="whatsapp">{CLINIC['wa_display']}</a><br><a href="mailto:{CLINIC['email']}">{CLINIC['email']}</a></p>
    </div>
    <div><h3>Clinic</h3><ul>
      <li><a href="/about.html">About the clinic</a></li>
      <li><a href="/about.html#doctors">Our dentists</a></li>
      <li><a href="/reviews.html">Patient reviews</a></li>
      <li><a href="/contact.html">Timings and directions</a></li>
      <li><a href="/faq.html">Clinic facts and FAQ</a></li>
      <li><a href="/dentist-west-delhi.html">Dentist in West Delhi</a></li>
      {'<li><a href="/clinics.html">Our clinics</a></li>' if LIVE_BRANCHES else ''}
      <li><a href="/booking.html">Book an appointment</a></li>
    </ul></div>
    <div><h3>Treatments</h3><ul>
      <li><a href="{IMPLANTS}/">Dental implants in Delhi</a></li>
      <li><a href="{IMPLANTS}/dental-implant-cost-delhi/">Implant cost in Delhi</a></li>
      <li><a href="{SMILE}/veneers.html">Veneers</a></li>
      <li><a href="{SMILE}/teeth-whitening-cost-delhi.html">Teeth whitening</a></li>
      <li><a href="{SMILE}/root-canal-cost-delhi.html">Root canal</a></li>
      <li><a href="/treatments.html">All treatments</a></li>
    </ul></div>
    <div><h3>Our websites</h3><ul>
      <li><a href="{IMPLANTS}/">dentalimplantsdelhi.com</a><br><small>Dr Pushkar Sobti, implants</small></li>
      <li><a href="{SMILE}/">drparulssobti.com</a><br><small>Dr Parul Sharma Sobti, smile design</small></li>
      <li><a href="{SOCIAL['Google']}" rel="noopener">Google</a> · <a href="{SOCIAL['Instagram']}" rel="noopener">Instagram</a> · <a href="{SOCIAL['Facebook']}" rel="noopener">Facebook</a> · <a href="{SOCIAL['YouTube']}" rel="noopener">YouTube</a> · <a href="/videos.html">Videos</a></li>
    </ul></div>
  </div>
  <div class="legal"><span>© 2026 {e(CLINIC['name'])}, Rajouri Garden, New Delhi.</span><span>Information on this site is general and is not a diagnosis. Treatment is planned after an examination.</span></div>
</div></footer>
<a class="wa-float" href="{wa('Hello, I would like to book an appointment at Dr Sobti' + chr(39) + 's Dental Care.')}" data-track="whatsapp" aria-label="Chat on WhatsApp">{WA_ICON}<span>WhatsApp us</span></a>
<script>
(function(){{var b=document.querySelector('.menu-btn'),n=document.getElementById('nav');if(b&&n)b.addEventListener('click',function(){{var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)}});
document.addEventListener('click',function(ev){{var a=ev.target.closest&&ev.target.closest('[data-track]');if(a&&window.gtag)gtag('event',a.getAttribute('data-track')+'_click',{{link_url:a.href}})}});}})();
</script>
</body>
</html>
"""


def pagehead(title, crumb, lead=""):
    lead_html = f'<p class="lead">{lead}</p>' if lead else ""
    return f"""<section class="pagehead"><div class="wrap">
  <div class="crumbs"><a href="/">Home</a> › {e(crumb)}</div>
  <h1>{title}</h1>{lead_html}
</div></section>"""


def stars(n=5):
    return '<span aria-label="5 out of 5 stars">' + "★" * n + "</span>"


# ---------------- Content ----------------

TREATMENT_GROUPS = [
    {
        "cls": "", "title": "Dental implants", "who": "Dr Pushkar Sobti",
        "intro": "Fixed teeth for one gap or a whole jaw, planned in 3D on our own CBCT scanner.",
        "items": [
            ("Dental implants in Delhi", f"{IMPLANTS}/", "Dr Pushkar Sobti"),
            ("Single tooth implant in Delhi", f"{IMPLANTS}/dental-implant-cost-delhi/", ""),
            ("Dental implant cost in Delhi", f"{IMPLANTS}/dental-implant-cost-delhi/", "prices"),
            ("Full mouth implants (All-on-4, All-on-X)", f"{IMPLANTS}/full-mouth-dental-implants-delhi/", ""),
            ("Basal implants", f"{IMPLANTS}/basal-implants-delhi/", ""),
            ("Bone grafting and sinus lift", f"{IMPLANTS}/bone-grafting-for-dental-implants-delhi/", ""),
            ("Implant consultation: what happens", f"{IMPLANTS}/blog/dental-implant-consultation/", "guide"),
        ],
        "more": (f"{IMPLANTS}/", "dentalimplantsdelhi.com"),
    },
    {
        "cls": "gold", "title": "Smile design and cosmetic", "who": "Dr Parul Sharma Sobti",
        "intro": "Changes to colour, shape and line of the smile, planned around your face before anything is done.",
        "items": [
            ("Veneers in Delhi", f"{SMILE}/veneers.html", "from ₹10,000 per tooth"),
            ("Teeth whitening cost in Delhi", f"{SMILE}/teeth-whitening-cost-delhi.html", "from ₹8,000"),
            ("Smile makeover", f"{SMILE}/treatments.html", "case by case"),
            ("Clear aligners (invisible braces)", f"{SMILE}/clear-aligners-cost-delhi.html", "cost"),
            ("Braces cost in Delhi", f"{SMILE}/braces-cost-delhi.html", ""),
            ("Composite bonding", f"{SMILE}/treatments.html", ""),
        ],
        "more": (f"{SMILE}/", "drparulssobti.com"),
    },
    {
        "cls": "teal", "title": "Everyday dental care", "who": "Both doctors and the team",
        "intro": "Check-ups, pain relief and repairs for the whole family, including children.",
        "items": [
            ("Root canal (RCT) cost in Delhi", f"{SMILE}/root-canal-cost-delhi.html", ""),
            ("Tooth cap and zirconia crown price", f"{SMILE}/dental-crown-cost-delhi.html", ""),
            ("Teeth cleaning cost (air polishing)", f"{SMILE}/teeth-cleaning-cost-delhi.html", ""),
            ("Wisdom tooth removal", "/booking.html", ""),
            ("Fillings, extractions and dentures", "/booking.html", ""),
            ("Children's dentistry", "/booking.html", ""),
        ],
        "more": ("/booking.html", "Book a check-up"),
    },
]


def treatment_groups_html(full=False):
    out = []
    for g in TREATMENT_GROUPS:
        lis = []
        for name, href, note in g["items"]:
            small = f" <small>{e(note)}</small>" if note else ""
            ext = "" if href.startswith("/") else ' rel="noopener"'
            lis.append(f'<li><a href="{href}"{ext}><span>{e(name)}{small}</span></a></li>')
        more_href, more_label = g["more"]
        foot = (f'Led by {e(g["who"])}. Full details on <a href="{more_href}">{e(more_label)}</a>.'
                if not more_href.startswith("/") else f'Led by {e(g["who"])}. <a href="{more_href}">{e(more_label)}</a>.')
        out.append(f"""<article class="tgroup {g['cls']}">
  <header><h3>{e(g['title'])}</h3><p>{e(g['intro'])}</p></header>
  <ul>{''.join(lis)}</ul>
  <footer>{foot}</footer>
</article>""")
    return f'<div class="grid g3">{"".join(out)}</div>'


REVIEWS = [
    # (name, treatment, words, source). Quoted word for word from Google and Practo, shortened only where marked "…".
    ("Ravi G.", "Root canal and crown", "My Root Canal Treatment (RCT) was completed in a single sitting, and the crown was also prepared in-house and fitted on the same day. I am extremely happy and fully satisfied with the treatment.", "rg"),
    ("Nidhi G.", "Implant consultation", "I walked into the clinic feeling nervous, but I walked out smiling… Another thing I loved was that all the advanced dental imaging, including CBCT, is available within the clinic itself.", "rg"),
    ("Puran Chand K.", "Implants", "Though I am myself a Doctor and close to five decades in Medicine… Everything is so precise… as in house CBCT scan as well as inhouse implant lab. I can recommend to all my patients as well as fellow Doctors.", "rg"),
    ("Geet K.", "Wisdom tooth removal", "He was very professional, patient, and explained the entire procedure clearly, which made me feel comfortable and confident throughout the treatment. The surgery was handled smoothly, and the post-surgery guidance and care were excellent.", "rg"),
    ("Kiran N.", "Long-time patient", "I've been visiting Dr. Pushkar Sobti for almost two decades, and he has always been my go-to dentist. He is warm, patient and genuinely caring, and makes every visit feel comfortable and easy.", "rg"),
    ("Raghunandan K.", "Treatment for his son", "The clinic is neat, clean, and well-maintained. The entire procedure was handled very softly and gently. The doctor and staff were patient, caring, and made sure my son felt at ease throughout the treatment.", "rg"),
    ("Shaurya D.", "Root canal", "She and her team explained the procedure to me exceptionally well and gave me clarity, I would recommend this place to anyone looking for dental care.", "rg"),
    ("Sunita M.", "Implants", "I have been getting all my dental treatments done from them for 8 years now and recently got implants done from Dr Sobti's Dental Care, painless procedure throughout, very kind and patient doctors.", "rg"),
    ("Rohit K.", "CBCT consultation", "The doctor examined my condition, explained the findings of my CBCT scan, and discussed the possible treatment options in detail. The front desk receptionist was also professional, polite, and helpful.", "rg"),
    ("Jaspreet S.", "Air polishing cleaning", "The air polishing cleaning procedure was entirely pain free handled gently. The doctor and staff explained things in detail.", "rg"),
    ("Mona T.", "Dental implant", "Went in with lot of apprehension for tooth implant… but had an amazing experience with super supportive staff and thoroughly professional doctor.", "rg"),
    ("Ekta A.", "General care", "You don't get the usual feeling of being at a dentist's clinic—it has a very calm and relaxing atmosphere. The doctors are highly skilled, professional and make you feel completely at ease.", "rg"),
    ("Shobhit K.", "Fillings and root canal", "I have had the privilege to get treated by Both, Dr. Parul & Dr. Pushkar. I had minor fillings and a Root Canal Treatment, both of which were taken care with utmost care. All appointments were on time…", "vg"),
    ("Ishmeet K.", "Treatment for her daughter", "I had a great experience with Dr Sobti. Actually I should say he is amazing doctor because the way he handle my daughter during treatment . He is friendly and make patient so comfortable while treating.", "vg"),
    ("Soumyajit C.", "Treatment while travelling", "It is very neat and clean with professional staff. The treatment quality is extremely high… I had limited time because of travel and they did my work in time.", "vg"),
    ("Seema S.", "Long-time patient", "I have been receiving treatment at Sobti Dental Care, Rajouri garden from Dr. Pushkar Sobti and Dr Parul Sobti since many years . Both doctors are very professional dentist and along with experienced staff… Highly meticulous and great quality of work.", "practo"),
    ("Dhirendra S.", "Tooth pain", "I had severe pain in my tooth. The doctor not only explained me the treatment thoroughly but also answered all my queries patiently. My treatment was painless n smooth. The clinic is hygienic and the staff is friendly too.", "practo"),
    ("Anju G.", "Scaling and filling", "I'm thoroughly impressed with Dr. Sobti's Dental Care all the staff here is friendly professional and made me feel at ease throughout my entire visit to Dr. Parul Sharma . I have got my scaling and filling done here smoothly and comfortably.", "practo"),
]


PRACTO = "https://www.practo.com/delhi/clinic/sobti-dental-clinic-vishnu-garden/reviews"
REVIEW_SOURCES = {
    "rg": "Google review, Rajouri Garden",
    "vg": "Google review, Vishnu Garden clinic",
    "practo": "Practo patient story",
}


def review_cards(items):
    return "".join(f"""<article class="review"><div class="stars">{stars()}</div>
<blockquote>“{e(text)}”</blockquote><cite>{e(name)}<small>{e(what)} · {REVIEW_SOURCES[src]}</small></cite></article>""" for name, what, text, src in items)


PHOTOS = [
    ("clinic-reception-waiting.jpg", "Reception and waiting area"),
    ("clinic-treatment-room.jpg", "Treatment room, Rajouri Garden"),
    ("clinic-treatment-room-blue.jpg", "Treatment room with dental microscope"),
    ("clinic-treatment-room-3.jpg", "Treatment room, wide view"),
    ("clinic-treatment-room-2.jpg", "Second treatment room"),
    ("clinic-lounge-certificates.jpg", "Patient lounge"),
    ("clinic-lounge-sofa.jpg", "Waiting lounge"),
]

LAB_WORK = [
    ("lab-full-arch-implant-bridge.jpg", "Full-arch implant bridge on a titanium framework"),
    ("lab-implant-bridge.jpg", "Implant bridge on its implant analogues"),
    ("lab-zirconia-bridge.jpg", "Zirconia bridge, milled in-house"),
    ("lab-veneers-on-model.jpg", "Veneers on the patient's model"),
    ("lab-smile-design-mock-up.jpg", "Smile design mock-up on a printed model"),
    ("lab-full-arch-teeth.jpg", "Full-arch teeth, finished in our lab"),
    ("lab-full-arch-bridge-try-in.jpg", "Full-arch bridge beside its clear try-in"),
    ("lab-clear-aligner.jpg", "Clear aligner"),
    ("lab-zirconia-molar-bridge.jpg", "Zirconia molar bridge"),
    ("lab-front-implant-bridge.jpg", "Front implant bridge with pink gum"),
    ("lab-implant-overdenture.jpg", "Implant-supported denture on bar attachments"),
    ("lab-front-teeth-bridge.jpg", "Front teeth bridge, hand-finished"),
    ("lab-crowns-on-printed-model.jpg", "Crowns on a 3D-printed model"),
    ("lab-full-arch-try-in.jpg", "Full-arch try-in before the final teeth"),
]


def photo_grid(items):
    return '<div class="photos">' + "".join(
        f'<figure><img src="/assets/img/{f}" alt="{e(c)}" width="1200" height="900" loading="lazy"><figcaption>{e(c)}</figcaption></figure>'
        for f, c in items) + "</div>"


def doctors_html():
    return f"""<div class="grid g2">
  <article class="card doc" id="dr-pushkar">
    <img class="pic" src="/assets/img/dr-pushkar-sobti-portrait.jpg" alt="Dr Pushkar Sobti, implantologist" width="800" height="1000" loading="lazy">
    <div>
      <h3>Dr Pushkar Sobti</h3>
      <div class="role">Implantologist · Full mouth rehabilitation</div>
      <p>Dr Pushkar heads implant work at the clinic, from a single missing tooth to fixed teeth for a whole jaw on four to six implants. He has placed more than 5,000 implants since he began practice in 2009, and plans each case on the clinic's own CBCT scan with guided surgery.</p>
      <p class="quals">BDS, MDS, PG in Oral Implantology (UCAM)</p>
      <p><a href="{IMPLANTS}/">His implant website →</a></p>
    </div>
  </article>
  <article class="card doc" id="dr-parul">
    <img class="pic" src="/assets/img/dr-parul-sharma-sobti.jpg" alt="Dr Parul Sharma Sobti, aesthetic dentist" width="800" height="1000" loading="lazy">
    <div>
      <h3>Dr Parul Sharma Sobti</h3>
      <div class="role">Aesthetic dentist · Smile design</div>
      <p>Dr Parul looks after cosmetic and everyday dentistry: veneers, whitening, bonding and smile makeovers, along with root canals, crowns and gentle cleanings. Patients often mention how clearly she explains a treatment before starting it.</p>
      <p class="quals">BDS · Digital Smile Design</p>
      <p><a href="{SMILE}/">Her smile design website →</a></p>
    </div>
  </article>
</div>"""


def visit_html():
    return f"""<div class="visit">
  <div>
    <dl class="info">
      <div><dt>Address</dt><dd><strong>{e(CLINIC['name'])}</strong><br>{e(CLINIC['street'])}<br>{e(CLINIC['locality'])}, {e(CLINIC['region'])} {CLINIC['postcode']}<br><span class="muted">{e(CLINIC['landmark'])}</span></dd></div>
      <div><dt>Phone</dt><dd><a href="tel:{CLINIC['phone_tel']}" data-track="call">{CLINIC['phone_display']}</a></dd></div>
      <div><dt>WhatsApp</dt><dd><a href="{CLINIC['wa_link']}" data-track="whatsapp">{CLINIC['wa_display']}</a></dd></div>
      <div><dt>Timings</dt><dd><table class="hours"><tbody>
        <tr><td>Monday to Saturday</td><td>10:00 am – 7:00 pm</td></tr>
        <tr><td>Sunday</td><td>10:00 am – 7:00 pm</td></tr>
      </tbody></table><p class="muted" style="margin:8px 0 0;font-size:.92rem">Dr Pushkar Sobti and Dr Parul Sharma Sobti see patients by prior appointment only. Please call or WhatsApp to book a time.</p></dd></div>
    </dl>
    <p style="margin-top:22px" class="actions"><a class="btn" href="{CLINIC['maps']}" rel="noopener">Get directions</a> <a class="btn ghost" href="/booking.html">Book a visit</a></p>
  </div>
  <iframe class="map" src="{MAP_EMBED}" title="Map to Dr Sobti's Dental Care, Rajouri Garden" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
</div>"""


def social_buttons():
    labels = {"Google": "Google reviews", "Instagram": "Instagram", "Facebook": "Facebook", "YouTube": "YouTube"}
    return "".join(f'<a class="btn ghost" href="{SOCIAL[k]}" rel="noopener">{v}</a>' for k, v in labels.items())


def cta_band():
    return f"""<section><div class="wrap"><div class="cta">
  <div><h2>Not sure what you need?</h2><p>Send a photo or your X-ray on WhatsApp for a free first opinion, or book an in-clinic consultation (₹700) with an examination and a written plan.</p></div>
  <div class="actions"><a class="btn gold" href="{wa('Hello, I would like a free first opinion on my teeth.')}" data-track="whatsapp">WhatsApp {CLINIC['wa_display']}</a><a class="btn light" href="tel:{CLINIC['phone_tel']}" data-track="call">Call {CLINIC['phone_display']}</a></div>
</div></div></section>"""


HOME_FAQ = [
    ("Where is Dr Sobti's Dental Care?", "On the first floor of J 12/26, Rajouri Garden, New Delhi 110027, above Rajmandir. It is a short walk from Rajouri Garden metro station and easy to reach from Punjabi Bagh, Tagore Garden, Subhash Nagar and Janakpuri."),
    ("What are the clinic timings?", "The clinic is open all seven days, Monday to Sunday, from 10 am to 7 pm. Dr Pushkar Sobti and Dr Parul Sharma Sobti see patients by prior appointment only, so please call or WhatsApp to book a time."),
    ("How much is a consultation?", "A first opinion on WhatsApp is free: send a photo or an X-ray and the doctors will reply. An in-clinic consultation with an examination is ₹700."),
    ("Do you place dental implants at the clinic?", "Yes. Dr Pushkar Sobti places implants at the clinic, from single teeth to full mouth implants, planned on the clinic's own CBCT 3D scanner."),
    ("Is the clinic open on Sunday?", "Yes. Dr Sobti's Dental Care in Rajouri Garden is open on Sundays too, 10 am to 7 pm, which helps patients from across West Delhi who cannot come on weekdays."),
    ("Which areas do your patients come from?", "Mostly West Delhi: Rajouri Garden, Punjabi Bagh, Tagore Garden, Subhash Nagar, Ramesh Nagar, Tilak Nagar, Janakpuri, Vikaspuri and Paschim Vihar. Implant patients also travel from elsewhere in Delhi NCR and from abroad."),
    ("Do you treat children?", "Yes. The clinic sees patients of all ages, including children, for check-ups, fillings and other routine care."),
    ("Who places dental implants at Dr Sobti's Dental Care?", "Dr Pushkar Sobti (BDS, MDS, PG in Oral Implantology, UCAM), who has placed more than 5,000 implants since 2009. A single implant with crown starts from ₹35,000 and All-on-4 from ₹2,00,000 per jaw (All-on-6 from ₹3,00,000 per jaw); the exact price follows a CBCT scan."),
    ("How do patients rate the clinic?", "Dr Sobti's Dental Care in Rajouri Garden is rated 5.0 out of 5 from 118 Google reviews. Patients most often mention the in-house CBCT scan and lab, clear explanations before treatment and painless procedures."),
]


def page_home():
    facts = """<div class="facts">
  <div><b>5,000+</b><span>implants placed</span></div>
  <div><b>Since 2009</b><span>in practice</span></div>
  <div><b>CBCT + lab</b><span>under one roof</span></div>
  <div><b>7 days</b><span>10 am to 7 pm</span></div>
</div>"""
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in HOME_FAQ)
    return f"""<section class="hero"><div class="wrap">
  <div>
    <div class="eyebrow">Dr Sobti's Dental Care · family practice since 1982</div>
    <h1>Your dentist in Rajouri Garden, <em>West Delhi</em></h1>
    <p class="lead">Dental care that is explained before it begins. Dr Sobti's Dental Care is a family-run dental clinic in Rajouri Garden led by implantologist Dr Pushkar Sobti and aesthetic dentist Dr Parul Sharma Sobti. Implants, smile design and everyday dentistry, with 3D scanning and our own dental lab in the same building.</p>
    <div class="actions"><a class="btn" href="/booking.html">Book a visit</a><a class="btn ghost" href="tel:{CLINIC['phone_tel']}" data-track="call">Call {CLINIC['phone_display']}</a></div>
    {facts}
  </div>
  <div class="photo">
    <img src="/assets/img/clinic-reception-waiting.jpg" alt="Reception and waiting area at Dr Sobti's Dental Care, Rajouri Garden" width="1280" height="720" fetchpriority="high">
    <a class="badge" href="/reviews.html" style="text-decoration:none"><b>{CLINIC['rating']}</b><div><div class="stars">★★★★★</div><small>{CLINIC['review_count']} Google reviews</small></div></a>
  </div>
</div></section>

<section id="treatments"><div class="wrap">
  <div class="section-head"><div class="eyebrow">Treatments</div><h2>Three kinds of care, one clinic</h2>
  <p class="lead">Each doctor writes in depth about their own work on a separate website. Pick a treatment below to read about it, with prices where we publish them.</p></div>
  {treatment_groups_html()}
  <p style="margin-top:24px"><a href="/treatments.html">See the full treatment list →</a></p>
</div></section>

<section class="tint" id="doctors"><div class="wrap">
  <div class="section-head"><div class="eyebrow">Your dentists</div><h2>Two doctors, one plan for your mouth</h2>
  <p class="lead">Implant and cosmetic cases are often planned by both doctors together, so the teeth that go on an implant also look right in your smile.</p></div>
  {doctors_html()}
</div></section>

<section><div class="wrap">
  <div class="section-head"><div class="eyebrow">Inside the clinic</div><h2>Diagnosis, planning and lab work in one place</h2>
  <p class="lead">Scans, crowns and treatment all happen on the same floor in Rajouri Garden. That saves you trips to outside imaging centres and labs, and lets some treatments finish in fewer visits.</p></div>
  {photo_grid(PHOTOS[:4])}
  <p style="margin-top:22px"><a href="/about.html#clinic">See more of the clinic →</a></p>
</div></section>

<section class="tint"><div class="wrap">
  <div class="section-head"><div class="eyebrow">Reviews</div><h2>Rated {CLINIC['rating']} by {CLINIC['review_count']} patients on Google</h2></div>
  <div class="grid g3">{review_cards(REVIEWS[:3])}</div>
  <p style="margin-top:24px" class="actions"><a class="btn ghost" href="/reviews.html">Read more reviews</a></p>
</div></section>

<section><div class="wrap" style="max-width:960px">
  <div class="section-head"><div class="eyebrow">Videos</div><h2>Watch our dentists explain treatments</h2>
  <p class="lead">Short videos from Dr Pushkar Sobti and Dr Parul Sharma Sobti on implants, smile design and what to expect at the clinic. The latest videos from our YouTube channel play below.</p></div>
  <div style="position:relative;padding-top:56.25%;border-radius:16px;overflow:hidden;background:#0b1b3a">
    <iframe src="https://www.youtube-nocookie.com/embed/videoseries?list=UUsgOAckYkgZCJXmDpgCAgVg" title="Latest videos from Dr Sobti's Dental Care on YouTube" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position:absolute;inset:0;width:100%;height:100%;border:0"></iframe>
  </div>
  <p class="actions" style="margin-top:20px"><a class="btn" href="/videos.html">Watch our videos by topic</a><a class="btn ghost" href="{SOCIAL['YouTube']}" rel="noopener">See all videos on YouTube</a></p>
</div></section>

<section class="tint"><div class="wrap">
  <div class="grid g2" style="align-items:start">
    <div><div class="eyebrow">Areas we serve</div><h2>A dentist close to home in West Delhi</h2>
    <p class="muted">Patients reach us easily from Rajouri Garden, Punjabi Bagh, Tagore Garden, Subhash Nagar, Ramesh Nagar, Tilak Nagar, Janakpuri, Vikaspuri and Paschim Vihar. Rajouri Garden metro station (Blue and Pink lines) is the nearest stop.</p></div>
    <div><div class="eyebrow">Follow the clinic</div><h2>Find us online</h2>
    <p class="actions">{social_buttons()}</p>
    <p class="muted">Before-and-after cases, short videos and answers to common questions, posted by the doctors.</p></div>
  </div>
</div></section>

<section id="visit"><div class="wrap">
  <div class="section-head"><div class="eyebrow">Visit us</div><h2>Rajouri Garden, above Rajmandir</h2></div>
  {visit_html()}
</div></section>

<section class="tint"><div class="wrap" style="max-width:860px">
  <div class="section-head"><div class="eyebrow">Questions</div><h2>Before your first visit</h2></div>
  {faq}
</div></section>
{cta_band()}"""


def page_about():
    steps = """<ol class="steps">
  <li><h3>Talk</h3><p>Tell us what is bothering you. Send photos on WhatsApp first if you like.</p></li>
  <li><h3>Examine and scan</h3><p>An examination, and X-rays or a CBCT scan only if your case needs them.</p></li>
  <li><h3>Written plan</h3><p>Options, visits and costs in writing, so you can decide at home.</p></li>
  <li><h3>Treatment</h3><p>Done in our rooms, with crowns and teeth made in our own lab.</p></li>
</ol>"""
    return pagehead("About Dr Sobti's Dental Care", "About us",
                    "A dental clinic in Rajouri Garden run by two dentists, Dr Pushkar Sobti and Dr Parul Sharma Sobti. A family clinic since 1982, when Dr Rajesh Sobti (MBBS, DCH) opened it in Vishnu Garden; Dr Pushkar joined in 2009 and opened this Rajouri Garden dental clinic, on the first floor of J 12/26, in 2024.") + f"""
<section id="doctors"><div class="wrap">
  <div class="section-head"><div class="eyebrow">Your dentists</div><h2>Meet the doctors</h2></div>
  {doctors_html()}
  <div class="duo">
    <figure><img src="/assets/img/dr-pushkar-and-dr-parul-sobti.jpg" alt="Dr Pushkar Sobti and Dr Parul Sharma Sobti at Dr Sobti's Dental Care" width="1440" height="1200" loading="lazy"><figcaption>Dr Pushkar Sobti and Dr Parul Sharma Sobti</figcaption></figure>
    <figure><img src="/assets/img/dr-pushkar-sobti-reception.jpg" alt="Dr Pushkar Sobti at the reception of Dr Sobti's Dental Care, Rajouri Garden" width="1600" height="901" loading="lazy"><figcaption>Dr Pushkar at the Rajouri Garden reception</figcaption></figure>
  </div>
</div></section>

<section class="tint"><div class="wrap">
  <div class="section-head"><div class="eyebrow">How a visit works</div><h2>No treatment before you understand it</h2>
  <p class="lead">Patients tell us the thing they value most is knowing what will happen and what it will cost. So every course of treatment starts the same way.</p></div>
  {steps}
</div></section>

<section id="clinic"><div class="wrap">
  <div class="section-head"><div class="eyebrow">The clinic</div><h2>What is on the first floor</h2>
  <p class="lead">A CBCT 3D scanner, a dental microscope, an implant surgery room and <a href="/lab.html">our in-house lab, Titanium Arts Dental Studio</a>, which mills crowns on site. Instruments are sterilised in a Class B autoclave, and single-use items are used once.</p></div>
  {photo_grid(PHOTOS)}
</div></section>

<section class="tint"><div class="wrap">
  <div class="grid g3">
    <div class="card"><h3>Implant brands</h3><p>Implant plans name the brand in writing. The clinic regularly uses Osstem, Hiossen and Nobel Biocare, among others.</p></div>
    <div class="card"><h3>Gentle cleaning</h3><p>Air polishing removes stains and deposits with a fine powder and water spray, which most people with sensitive teeth find more comfortable.</p></div>
    <div class="card"><h3>Patients from far away</h3><p>Patients come from across West Delhi, the wider NCR and abroad. Ask on WhatsApp and we will plan your visits around your travel.</p></div>
  </div>
</div></section>
{cta_band()}"""


def page_treatments():
    rows = [
        ("Dental implants", "Single tooth, several teeth or full mouth (All-on-4, All-on-X). Planned on CBCT, guided surgery.", f"{IMPLANTS}/dental-implant-cost-delhi/", "Implant costs"),
        ("Full mouth implants", "Fixed teeth for a whole jaw on four to six implants, for people with loose dentures or many failing teeth.", f"{IMPLANTS}/", "dentalimplantsdelhi.com"),
        ("Basal implants", "An option for some patients with thin or low bone.", f"{IMPLANTS}/basal-implants-delhi/", "Basal implants"),
        ("Veneers", "Thin porcelain or composite facings that change the colour and shape of front teeth. From ₹10,000 per tooth.", f"{SMILE}/veneers.html", "Veneers"),
        ("Teeth whitening", "In-clinic whitening, from ₹8,000 depending on the case.", f"{SMILE}/teeth-whitening-cost-delhi.html", "Whitening cost"),
        ("Smile makeover", "A combined plan (whitening, veneers, bonding, aligners) designed digitally first. Priced case by case.", f"{SMILE}/treatments.html", "Smile design"),
        ("Clear aligners", "Removable clear trays that straighten teeth gradually.", f"{SMILE}/clear-aligners-cost-delhi.html", "Aligner cost"),
        ("Braces", "Fixed braces for teenagers and adults.", f"{SMILE}/braces-cost-delhi.html", "Braces cost"),
        ("Root canal treatment", "Saves an infected or badly decayed tooth; often finished in one sitting.", f"{SMILE}/root-canal-cost-delhi.html", "Root canal cost"),
        ("Crowns and bridges", "Caps made in the clinic's own lab, sometimes fitted the same day.", f"{SMILE}/dental-crown-cost-delhi.html", "Crown cost"),
        ("Our in-house lab", "Titanium Arts Dental Studio makes our crowns, veneers and implant teeth on the same floor.", "/lab.html", "See the lab"),
        ("Teeth cleaning", "Scaling and air polishing to remove tartar and stains.", f"{SMILE}/teeth-cleaning-cost-delhi.html", "Cleaning cost"),
        ("Wisdom tooth removal", "Surgical removal of impacted wisdom teeth, planned on a scan when needed.", "/booking.html", "Book"),
        ("Fillings and extractions", "Tooth-coloured fillings, and gentle extractions when a tooth cannot be saved.", "/booking.html", "Book"),
        ("Dentures", "Full and partial dentures.", "/booking.html", "Book"),
        ("Children's dentistry", "Check-ups, fillings and preventive care for children.", "/booking.html", "Book"),
        ("Emergency dental care", "Toothache, swelling, a broken tooth or a lost crown. Call or WhatsApp and we will fit you in the same day where we can.", f"tel:{CLINIC['phone_tel']}", "Call now"),
    ]
    cards = "".join(f'<article class="card"><h3>{e(n)}</h3><p class="muted">{e(d)}</p><p><a href="{h}">{e(l)} →</a></p></article>' for n, d, h, l in rows)
    return pagehead("Dental treatments in Rajouri Garden", "Treatments",
                    "Everything the clinic offers, grouped by the doctor who leads it. Detailed pages and prices are on each doctor's website.") + f"""
<section><div class="wrap">{treatment_groups_html()}</div></section>
<section class="tint"><div class="wrap">
  <div class="section-head"><h2>All treatments A to Z</h2></div>
  <div class="grid g3">{cards}</div>
</div></section>
<section><div class="wrap" style="max-width:860px">
  <div class="pricebox"><h3>Published prices</h3><ul>
    <li>Free first opinion on WhatsApp (send a photo or X-ray)</li>
    <li>In-clinic consultation with examination: ₹700</li>
    <li>Veneers: from ₹10,000 per tooth</li>
    <li>Teeth whitening: from ₹8,000, depending on the case</li>
    <li>Implants: see <a href="{IMPLANTS}/dental-implant-cost-delhi/">implant costs in Delhi</a></li>
  </ul><p class="muted" style="margin:12px 0 0">Every plan comes with a written estimate after your examination.</p></div>
</div></section>
{cta_band()}"""


def page_lab():
    made = [
        ("Zirconia crowns and bridges", "Milled in-house on a Roland dry mill. Zirconia crowns from ₹8,000 per tooth, with a warranty.", f"{SMILE}/dental-crown-cost-delhi.html", "Crown cost"),
        ("E-max crowns and glass-ceramic veneers", "Milled on an Upcera wet mill. E-max crowns from ₹10,000 per tooth; veneers from ₹10,000 per tooth.", f"{SMILE}/veneers.html", "Veneers"),
        ("Teeth on implants", "Titanium parts for implant teeth milled on a Kelkar wet mill, so the crown, bridge or full-arch teeth fit the implant exactly.", f"{IMPLANTS}/dental-implant-cost-delhi/", "Implant cost"),
        ("Surgical guides", "3D-printed guides that carry the implant plan from the CBCT scan to the mouth.", f"{IMPLANTS}/", "Guided implants"),
        ("Temporaries and trial smiles", "PMMA temporary teeth, mock-ups and study models, printed or milled in-house.", f"{SMILE}/treatments.html", "Smile design"),
    ]
    cards = "".join(f'<article class="card"><h3>{e(n)}</h3><p class="muted">{e(d)}</p><p><a href="{h}" rel="noopener">{e(l)} →</a></p></article>' for n, d, h, l in made)
    return pagehead("Our in-house dental lab: Titanium Arts Dental Studio", "Our lab",
                    "Crowns, veneers and implant teeth for our patients are designed and made on the same floor as the clinic, at Titanium Arts Dental Studio (TADS), our in-house digital lab.") + f"""
<section><div class="wrap grid g2">
  <div class="prose">
    <h2>Why an in-house lab matters to you</h2>
    <ul>
      <li><strong>Fewer visits.</strong> A crown can often be scanned, milled and fitted on the same day, instead of waiting a week for an outside lab.</li>
      <li><strong>A better fit.</strong> Your doctor checks the crown's design on screen against your scan before it is milled.</li>
      <li><strong>Changes on the spot.</strong> If a shade or shape needs adjusting, it is done in the clinic, not sent away again.</li>
    </ul>
    <h2>How a crown is made here</h2>
    <ol>
      <li>Your tooth is scanned with an intraoral 3D scanner (Medit i900, Medit i500 or Upcera). No impression trays.</li>
      <li>The crown is designed in exocad and checked against your bite.</li>
      <li>It is milled from zirconia or E-max and finished to match your teeth.</li>
      <li>It is fitted and checked, often on the same day for a single crown.</li>
    </ol>
  </div>
  <figure style="margin:0"><img src="/assets/img/clinic-dental-lab.jpg" alt="3D printers and milling machines at Titanium Arts Dental Studio" width="1200" height="900" loading="lazy" style="width:100%;height:auto;border-radius:16px"><figcaption class="muted">3D printers and milling machines at Titanium Arts Dental Studio</figcaption></figure>
</div></section>

<section class="tint"><div class="wrap">
  <div class="section-head"><div class="eyebrow">Made at TADS</div><h2>What our lab makes</h2></div>
  <div class="grid g3">{cards}</div>
</div></section>

<section><div class="wrap">
  <div class="section-head"><div class="eyebrow">Recent work</div><h2>From our lab bench</h2>
  <p class="lead">Teeth, bridges and veneers made at Titanium Arts Dental Studio for patients of the clinic.</p></div>
  {photo_grid(LAB_WORK)}
</div></section>

<section class="tint"><div class="wrap">
  <div class="section-head"><div class="eyebrow">On video</div><h2>Watch the lab at work</h2></div>
  {video_grid(LAB_VIDEOS)}
</div></section>
{VIDEO_JS}
{cta_band()}"""


CLINIC_VIDEOS = [
    ("The clinic", "Our story and a look inside the Rajouri Garden clinic.",
     ["thmGh27-57I", "lDd7hbX0E9k", "VL64ySkZs60", "u_y8lzaJhoQ"]),
    ("Patients in their own words", "Patients from Delhi, Greater Noida and abroad on their treatment here.",
     ["YsTfqx1xLLM", "Q4XgYfekrpw", "_LgsARouKa0", "8W8GF76DnyA", "mOf8SY1nW9Y"]),
    ("Made in our lab", "Crowns, bridges and implant parts designed and milled at Titanium Arts Dental Studio, on the same floor.",
     ["kRn6ixupOLc", "nkUCoO-IgKk", "3rPYx82hlhk", "fvKcdFYR3R8"]),
]
LAB_VIDEOS = ["kRn6ixupOLc", "nkUCoO-IgKk", "3rPYx82hlhk", "fvKcdFYR3R8"]


def video_grid(ids):
    return '<div class="yt-grid">' + "".join(video_card(VIDEOS[i], e) for i in ids) + "</div>"


def video_ld(ids, page):
    return [dict(video_obj(VIDEOS[i], f"{SITE}/{page}"), publisher={"@id": f"{SITE}/#clinic"}) for i in ids]


def page_videos():
    secs = "".join(f"""<section{' class="tint"' if n % 2 else ''}><div class="wrap">
  <div class="section-head"><div class="eyebrow">Videos</div><h2>{e(h)}</h2><p class="lead">{e(intro)}</p></div>
  {video_grid(ids)}
</div></section>""" for n, (h, intro, ids) in enumerate(CLINIC_VIDEOS))
    return pagehead("Videos from Dr Sobti's Dental Care", "Videos",
                    "Short videos from our clinic in Rajouri Garden, New Delhi: a tour of the clinic, patients in their own words, and work from our in-house lab. Tap a video to play it here.") + secs + f"""
<section><div class="wrap grid g2">
  <article class="card"><h3>Dental implant videos</h3><p class="muted">Dr Pushkar Sobti on CBCT scans, guided surgery, All-on-X, bone grafting, and implants for diabetics, patients on blood thinners and older patients.</p><p><a href="{IMPLANTS}/videos/" rel="noopener">Watch the implant videos →</a></p></article>
  <article class="card"><h3>Smile makeover videos</h3><p class="muted">Smile designing, composite veneers, same-day crowns, gentle root canals for children, and laughing gas for nervous patients.</p><p><a href="{SMILE}/videos.html" rel="noopener">Watch the smile videos →</a></p></article>
</div></section>
{VIDEO_JS}
{cta_band()}"""


def page_reviews():
    return pagehead(f"Patient reviews: {CLINIC['rating']} stars on Google", "Reviews",
                    f"{CLINIC['review_count']} patients have reviewed Dr Sobti's Dental Care, Rajouri Garden on Google, with an average of {CLINIC['rating']} out of 5. Our family's Vishnu Garden clinic is rated 4.9 from 107 Google reviews, and the Rajouri Garden clinic has 59 patient stories on Practo (5.0). A few of them are below, in the patients' own words (shortened where marked …).") + f"""
<section><div class="wrap">
  <div class="columns">{review_cards(REVIEWS)}</div>
  <p class="actions" style="margin-top:12px"><a class="btn" href="{CLINIC['maps']}" rel="noopener">Read all reviews on Google</a><a class="btn ghost" href="{PRACTO}" rel="noopener">Read stories on Practo</a><a class="btn ghost" href="{CLINIC['review_link']}" rel="noopener">Leave us a review</a></p>
</div></section>
{cta_band()}"""


CONTACT_FAQ = [
    ("Which metro station is closest?", "Rajouri Garden metro station (Blue and Pink lines). The clinic is on the first floor of J 12/26, above Rajmandir."),
    ("Do I need an appointment?", "Yes. Dr Pushkar Sobti and Dr Parul Sharma Sobti see patients by prior appointment only. Call or WhatsApp to book; for pain or swelling, call and we will try to fit you in the same day."),
]


def page_contact():
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in CONTACT_FAQ)
    return pagehead("Contact and timings", "Contact",
                    "Open all seven days, 10 am to 7 pm. Call, WhatsApp or walk in at J 12/26, Rajouri Garden.") + f"""
<section><div class="wrap">{visit_html()}</div></section>
<section class="tint"><div class="wrap">
  <p class="actions" style="margin-bottom:24px">{social_buttons()}</p>
  <div class="grid g3">
    <div class="card"><h3>Call</h3><p>For appointments and emergencies.</p><p><a class="btn" href="tel:{CLINIC['phone_tel']}" data-track="call">{CLINIC['phone_display']}</a></p></div>
    <div class="card"><h3>WhatsApp</h3><p>Send photos or X-rays for a free first opinion.</p><p><a class="btn gold" href="{CLINIC['wa_link']}" data-track="whatsapp">{CLINIC['wa_display']}</a></p></div>
    <div class="card"><h3>Email</h3><p>For reports, records and anything that is not urgent.</p><p><a class="btn ghost" href="mailto:{CLINIC['email']}">{CLINIC['email']}</a></p></div>
  </div>
</div></section>
<section><div class="wrap" style="max-width:860px">
  <div class="section-head"><h2>Getting here</h2><p class="lead">We see patients from Rajouri Garden, Punjabi Bagh, Tagore Garden, Subhash Nagar, <a href="/dentist-tilak-nagar.html">Tilak Nagar</a>, <a href="/dentist-janakpuri.html">Janakpuri</a>, <a href="/dentist-vikaspuri.html">Vikaspuri</a>, <a href="/dentist-paschim-vihar.html">Paschim Vihar</a> and <a href="/dentist-west-delhi.html">across West Delhi</a>.</p></div>
  {faq}
</div></section>"""


def page_booking():
    opts = "".join(f"<option>{e(o)}</option>" for o in [
        "Check-up or consultation", "Tooth pain or emergency", "Dental implants", "Full mouth implants",
        "Veneers or smile makeover", "Teeth whitening", "Braces or aligners", "Root canal", "Cleaning", "Something else"])
    return pagehead("Book an appointment", "Book",
                    "Fill this in and it opens WhatsApp with your message ready to send. The clinic will confirm a time with you.") + f"""
<section><div class="wrap">
  <div class="grid g2" style="align-items:start">
    <form class="book card" id="book" novalidate>
      <label>Your name<input name="name" required autocomplete="name"></label>
      <label>Phone number<input name="phone" type="tel" required autocomplete="tel" inputmode="tel"></label>
      <label>What is it about?<select name="reason">{opts}</select></label>
      <label>Preferred day and time<input name="when" placeholder="e.g. Saturday morning"></label>
      <label>Anything else (optional)<textarea name="note" rows="3"></textarea></label>
      <button class="btn" type="submit">{WA_ICON.replace('<svg', '<svg width="20" height="20"')} Send on WhatsApp</button>
      <p class="muted" style="margin:0;font-size:.88rem">Nothing is stored on this website. Your details go only into the WhatsApp message you send.</p>
    </form>
    <div>
      <div class="card" style="margin-bottom:22px"><h3>Prefer to call?</h3><p><a href="tel:{CLINIC['phone_tel']}" data-track="call">{CLINIC['phone_display']}</a>, every day 10 am to 7 pm.</p></div>
      <div class="pricebox"><h3>Good to know</h3><ul>
        <li>First opinion on WhatsApp is free.</li>
        <li>In-clinic consultation: ₹700.</li>
        <li>Bring old X-rays, scans or reports if you have them.</li>
        <li>{e(CLINIC['street'])}, above Rajmandir. <a href="{CLINIC['maps']}" rel="noopener">Map</a></li>
      </ul></div>
    </div>
  </div>
</div></section>
<script>
document.getElementById('book').addEventListener('submit',function(ev){{ev.preventDefault();var f=ev.target;
if(!f.name.value.trim()||!f.phone.value.trim()){{alert('Please add your name and phone number.');return}}
var t='Hello, I would like to book an appointment at Dr Sobti\\'s Dental Care.\\nName: '+f.name.value+'\\nPhone: '+f.phone.value+'\\nAbout: '+f.reason.value+(f.when.value?'\\nPreferred time: '+f.when.value:'')+(f.note.value?'\\nNote: '+f.note.value:'');
if(window.gtag)gtag('event','booking_whatsapp',{{reason:f.reason.value}});
window.location.href='{CLINIC['wa_link']}?text='+encodeURIComponent(t)}});
</script>"""


FAQ_GROUPS = [
    ("Visiting the clinic", [
        ("Where is Dr Sobti's Dental Care?", "Dr Sobti's Dental Care is on the first floor of J 12/26, Rajouri Garden, New Delhi 110027, above Rajmandir. The nearest metro station is Rajouri Garden (Blue and Pink lines)."),
        ("What are the clinic timings?", "The clinic is open every day, Monday to Sunday, from 10 am to 7 pm, including Sundays."),
        ("How do I book an appointment?", "Call +91 87449 85976, WhatsApp +91 80767 77307, or use the booking page on this website, which opens WhatsApp with your message ready. Walk-ins are seen when a doctor is free."),
        ("Can I be seen the same day for tooth pain?", "Usually yes. Call the clinic for pain, swelling or a broken tooth and the team will try to see you the same day."),
        ("How long has Dr Sobti's Dental Care been running?", "It has been a family clinic since 1982, when Dr Rajesh Sobti (MBBS, DCH) opened it in Vishnu Garden. Dr Pushkar Sobti joined in 2009 and opened the Rajouri Garden dental clinic in 2024."),
        ("Which languages do the dentists speak?", "English and Hindi."),
        ("Which areas do patients come from?", "Mostly West Delhi: Rajouri Garden, Punjabi Bagh, Tagore Garden, Subhash Nagar, Ramesh Nagar, Tilak Nagar, Janakpuri, Vikaspuri and Paschim Vihar. Implant patients also come from across Delhi NCR and from abroad."),
    ]),
    ("Costs and payment", [
        ("How much is a dental consultation?", "A first opinion on WhatsApp is free: send a photo or X-ray. An in-clinic consultation with an examination and a written plan is ₹700."),
        ("How much does a dental implant cost at Dr Sobti's Dental Care?", "A single implant with crown starts from ₹35,000, and All-on-4 full arch implants start from ₹2,00,000 per jaw and All-on-6 from ₹3,00,000 per jaw. The final price depends on the implant brand, bone and the type of teeth, and is given in writing after a CBCT scan."),
        ("How much do veneers and whitening cost?", "Veneers start from ₹10,000 per tooth and in-clinic teeth whitening from ₹8,000, depending on the case. A smile makeover is priced case by case after a digital design."),
        ("How much does a crown cost?", "Zirconia crowns start from ₹8,000 per tooth and E-max crowns from ₹10,000 per tooth. Both are made in the clinic's own lab."),
        ("How can I pay?", "Cash, credit or debit card, and bank transfer. Dr Sobti's Dental Care is not on the CGHS panel."),
    ]),
    ("Doctors and expertise", [
        ("Who are the dentists at Dr Sobti's Dental Care?", "Dr Pushkar Sobti, an implantologist (BDS, MDS, PG in Oral Implantology, UCAM), and Dr Parul Sharma Sobti, an aesthetic dentist (BDS) who leads smile design, veneers and everyday dentistry."),
        ("How experienced is the implant dentist?", "Dr Pushkar Sobti has been in practice since 2009 and has placed more than 5,000 dental implants, from single teeth to fixed teeth for a whole jaw on four to six implants (All-on-4, All-on-6, All-on-X)."),
        ("Which implant brands does the clinic use?", "The brand is named in writing on every implant plan. The clinic regularly uses Osstem, Hiossen and Nobel Biocare, among others."),
        ("Does the clinic have a CBCT scanner and its own lab?", "Yes. A CBCT 3D scanner, a dental microscope, an implant surgery room and an in-house lab, Titanium Arts Dental Studio, are all on the same floor in Rajouri Garden. Many crowns are made and fitted the same day."),
        ("How are instruments sterilised?", "In a Class B autoclave, and single-use items are used once."),
    ]),
    ("Choosing a dentist in West Delhi", [
        ("How do patients rate Dr Sobti's Dental Care?", "Dr Sobti's Dental Care in Rajouri Garden is rated 5.0 out of 5 from 118 Google reviews (November 2026). Reviews often mention painless treatment, clear explanations and having the CBCT scan and lab in the clinic."),
        ("What should I look for in an implant clinic?", "Ask who places the implant and how many they have placed, whether a CBCT scan is used to plan it, which implant brand you will get, what warranty applies and whether the price is given in writing. Dr Sobti's Dental Care answers all of these in a written plan before treatment."),
        ("Do you treat patients from abroad?", "Yes. Send an X-ray or CBCT on WhatsApp for a free online assessment from Dr Pushkar Sobti, usually within 24 hours. The clinic can provide a medical visa invitation letter and plan your visits around your travel."),
        ("Do you treat children?", "Yes. The clinic sees patients of all ages, including children, for check-ups, fillings and preventive care."),
    ]),
]
FAQ_ALL = [qa for _, qs in FAQ_GROUPS for qa in qs]


def page_faq():
    facts = [
        ("Name", CLINIC["name"]),
        ("Type", "Dental clinic (dentist), family-run"),
        ("Address", f"{ADDRESS_LINE}, India"),
        ("Landmark", "Above Rajmandir. Nearest metro: Rajouri Garden (Blue and Pink lines)"),
        ("Timings", "Monday to Sunday, 10 am to 7 pm"),
        ("Phone", CLINIC["phone_display"]),
        ("WhatsApp", CLINIC["wa_display"]),
        ("Email", CLINIC["email"]),
        ("Dentists", "Dr Pushkar Sobti (implantologist) and Dr Parul Sharma Sobti (aesthetic dentist)"),
        ("History", "A family clinic since 1982, opened by Dr Rajesh Sobti (MBBS, DCH) in Vishnu Garden; Dr Pushkar Sobti joined in 2009 and opened the Rajouri Garden dental clinic in 2024"),
        ("Experience", "5,000+ implants placed by Dr Pushkar Sobti"),
        ("Equipment", "CBCT 3D scanner, dental microscope, implant surgery room, Class B autoclave"),
        ("In-house lab", "Titanium Arts Dental Studio (zirconia and E-max crowns, veneers, implant teeth)"),
        ("Implant brands", "Osstem, Hiossen and Nobel Biocare, among others"),
        ("Starting prices", "Consultation ₹700 · single implant with crown ₹35,000 · All-on-4 ₹2,00,000 per jaw · veneers ₹10,000 per tooth · whitening ₹8,000 · zirconia crown ₹8,000"),
        ("Languages", "English, Hindi"),
        ("Payment", "Cash, card, bank transfer"),
        ("Google rating", f"{CLINIC['rating']} from {CLINIC['review_count']} reviews"),
        ("Websites", "sobtidentalcare.com (clinic) · dentalimplantsdelhi.com (implants) · drparulssobti.com (smile design and other treatments)"),
    ]
    rows = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts)
    groups = "".join(
        f'<h2 style="margin-top:36px">{e(title)}</h2>' + "".join(
            f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in qs)
        for title, qs in FAQ_GROUPS)
    return pagehead("Clinic facts and frequently asked questions", "FAQ",
                    "Dr Sobti's Dental Care is a family-run dental clinic at J 12/26, Rajouri Garden, New Delhi, open 7 days from 10 am to 7 pm, led by implantologist Dr Pushkar Sobti and aesthetic dentist Dr Parul Sharma Sobti. The key facts and the questions patients ask most are below.") + f"""
<section><div class="wrap" style="max-width:860px">
  <div class="section-head"><div class="eyebrow">At a glance</div><h2>Clinic facts</h2></div>
  <dl class="info">{rows}</dl>
  <p class="muted" style="margin-top:14px">Last updated {UPDATED}.</p>
</div></section>
<section class="tint"><div class="wrap" style="max-width:860px">
  <div class="section-head"><div class="eyebrow">Questions</div><h2>Frequently asked questions</h2></div>
  {groups}
</div></section>
{cta_band()}"""


DOCTOR_NAMES = {"dr-pushkar": "Dr Pushkar Sobti", "dr-parul": "Dr Parul Sharma Sobti",
                "dr-rajesh": "Dr Rajesh Sobti (MBBS, DCH)"}


def branch_card(name, area, street, postcode, phone_display, phone_tel, hours_line, href, note, main=False):
    tag = '<div class="eyebrow">Main clinic</div>' if main else '<div class="eyebrow">Branch</div>'
    return f"""<article class="card">{tag}<h3>{e(name)}, {e(area)}</h3>
  <p>{e(street)}<br>New Delhi {postcode}</p>
  <p>{e(hours_line)}<br>Phone <a href="tel:{phone_tel}" data-track="call">{phone_display}</a></p>
  <p class="muted">{e(note)}</p>
  <p><a class="btn ghost" href="{href}">{'Visit this clinic' if main else 'Branch details'}</a></p>
</article>"""


def page_clinics():
    cards = [branch_card(CLINIC["name"], CLINIC_AREA, CLINIC["street"], CLINIC["postcode"], CLINIC["phone_display"],
                         CLINIC["phone_tel"], "Open all 7 days, 10 am to 7 pm", "/", 
                         "Opened in 2024. CBCT scanner, implant surgery room and our in-house lab are here.", main=True)]
    cards += [branch_card(b["name"], b["area"], b["street"], b["postcode"], b["phone_display"], b["phone_tel"],
                          "Mon to Sat, " + " and ".join(f"{clock(o)} to {clock(c)}" for _, _, o, c in b["hours"]) + (f"; {b['closed']} closed" if b.get("closed") else ""), f"/{b['slug']}.html", b["about"])
              for b in LIVE_BRANCHES]
    return pagehead("Our clinics", "Our clinics", BRAND["story"]) + f"""
<section><div class="wrap">
  <div class="grid g2">{''.join(cards)}</div>
  <p style="margin-top:22px">For implants, smile design and anything that needs a CBCT scan, most patients are seen at the Rajouri Garden clinic. <a href="/booking.html">Book a visit</a> or <a href="{CLINIC['wa_link']}" data-track="whatsapp">WhatsApp {CLINIC['wa_display']}</a> and we will suggest the right clinic.</p>
</div></section>
{cta_band()}"""


def page_branch(b):
    hours = "".join(f"<tr><td>{e(label)}</td><td>{clock(o)} – {clock(c)}</td></tr>" for label, _, o, c in b["hours"])
    if b.get("closed"):
        hours += f"<tr><td>{e(b['closed'])}</td><td>Closed</td></tr>"
    docs = "".join(f"<li><strong>{DOCTOR_NAMES[d]}</strong>: {e(when)}</li>" for d, when, _ in b["doctors"])
    return pagehead(f"{b['name']}, {b['area']}", b["area"], b["about"]) + f"""
<section><div class="wrap"><div class="visit">
  <div>
    <dl class="info">
      <div><dt>Address</dt><dd><strong>{e(b['name'])}</strong><br>{e(b['street'])}<br>{e(b['locality'])}, {e(b['region'])} {b['postcode']}{'<br><span class="muted">' + e(b['landmark']) + '</span>' if b['landmark'] else ''}</dd></div>
      <div><dt>Phone</dt><dd><a href="tel:{b['phone_tel']}" data-track="call">{b['phone_display']}</a></dd></div>
      <div><dt>Timings</dt><dd><table class="hours"><tbody>{hours}</tbody></table></dd></div>
      <div><dt>Doctors here</dt><dd><ul>{docs}</ul></dd></div>
    </dl>
    <p style="margin-top:22px" class="actions"><a class="btn" href="{b['maps']}" rel="noopener">Get directions</a> <a class="btn ghost" href="/clinics.html">All our clinics</a></p>
  </div>
</div>
<p style="margin-top:22px">Implant surgery, CBCT scans and lab work are done at our main clinic, <a href="/">{e(CLINIC['name'])} in Rajouri Garden</a>, open all 7 days, 10 am to 7 pm. Call <a href="tel:{CLINIC['phone_tel']}" data-track="call">{CLINIC['phone_display']}</a> or WhatsApp <a href="{CLINIC['wa_link']}" data-track="whatsapp">{CLINIC['wa_display']}</a>.</p>
</div></section>"""


# ---------------- West Delhi area pages ----------------
# Honest "patients from" pages: the clinic is in Rajouri Garden only. Each page gives the real route,
# what patients from that area usually come for, and answers local questions. No fake addresses.
AREAS = [
    {
        "slug": "dentist-tilak-nagar",
        "area": "Tilak Nagar",
        "keyword": "Dentist near Tilak Nagar",
        "distance": "about 2.5 km",
        "route": [
            ("By metro", "Take the Blue Line from Tilak Nagar towards Noida or Vaishali. Rajouri Garden is three stops away (Subhash Nagar, Tagore Garden, Rajouri Garden). From the station it is a short walk to J 12/26, above Rajmandir."),
            ("By car or auto", "Come along Najafgarh Road towards Rajouri Garden. The clinic is on the first floor with a lift, and there is parking close by."),
        ],
        "intro": "Tilak Nagar is three metro stops from our clinic in Rajouri Garden, so many families from Tilak Nagar and Chaukhandi come to us for check-ups, root canals, crowns and dental implants.",
        "faq": [
            ("Is there a dental clinic of Dr Sobti's in Tilak Nagar?", "No. Our clinic is in Rajouri Garden, at J 12/26, First Floor, above Rajmandir. It is three stops from Tilak Nagar on the Blue Line, which is quicker for most patients than a drive through the market."),
            ("Can I get an appointment on Sunday?", "Yes. The clinic is open all seven days from 10 am to 7 pm, including Sunday. The doctors see patients by appointment, so call or WhatsApp first."),
            ("Can I send my X-ray before coming from Tilak Nagar?", "Yes. Send a photo of your teeth or your X-ray on WhatsApp for a free first opinion, so you know what to expect before you travel."),
        ],
    },
    {
        "slug": "dentist-janakpuri",
        "area": "Janakpuri",
        "keyword": "Dentist near Janakpuri",
        "distance": "about 4 km",
        "route": [
            ("By metro", "From Janakpuri East take the Blue Line towards Noida or Vaishali; Rajouri Garden is four stops away. From Janakpuri West (Blue and Magenta lines) it is five stops. The clinic is a short walk from Rajouri Garden station."),
            ("By car", "Drive along Najafgarh Road past Tilak Nagar to Rajouri Garden. The clinic has a lift, and parking is close by."),
        ],
        "intro": "Patients from Janakpuri, including A, B, C and D blocks, Asalatpur and Possangipur, come to our Rajouri Garden clinic mainly for dental implants, full mouth implants and smile design, because the clinic has its own CBCT 3D scanner and dental lab on the same floor.",
        "faq": [
            ("Is Dr Sobti's Dental Care in Janakpuri?", "No. The clinic is in Rajouri Garden, four metro stops from Janakpuri East on the Blue Line. Many Janakpuri patients choose to travel for implant and smile work because the scan, the surgery and the lab are all in one place."),
            ("Why travel from Janakpuri for dental implants?", "Dr Pushkar Sobti has placed more than 5,000 implants since 2009. Each case is planned on the clinic's own CBCT scan with guided surgery, and the implant teeth are made in the in-house lab, so you do not visit three different places."),
            ("Is the clinic open on Sundays?", "Yes, 10 am to 7 pm every day of the week, by appointment."),
        ],
    },
    {
        "slug": "dentist-vikaspuri",
        "area": "Vikaspuri",
        "keyword": "Dentist near Vikaspuri",
        "distance": "about 5 km",
        "route": [
            ("By car or cab", "Most patients from Vikaspuri come by car or cab towards Rajouri Garden. The clinic is on the first floor of J 12/26, above Rajmandir, with a lift and parking close by."),
            ("By metro", "Take the metro to Janakpuri West or Janakpuri East and change to the Blue Line towards Noida or Vaishali. Get off at Rajouri Garden; the clinic is a short walk away."),
        ],
        "intro": "Vikaspuri is one of West Delhi's biggest residential areas, and many of our implant and full mouth patients come from its blocks and from nearby Hastsal and Krishna Park. They travel to Rajouri Garden for a team that plans, places and makes the implant teeth under one roof.",
        "faq": [
            ("Do you have a clinic in Vikaspuri?", "No. Our clinic is in Rajouri Garden. We would rather tell you that plainly: patients from Vikaspuri come to us for implants, full mouth implants and smile work, and we try to keep the number of visits low."),
            ("How many visits does an implant need?", "Usually a consultation with a CBCT scan, the surgery visit, and a visit for the final tooth after the implant has healed, plus short check-ups. Your plan, written after the scan, tells you exactly how many."),
            ("Can elderly patients manage the visit?", "Yes. The clinic is on the first floor and has a lift, and there is parking close by."),
        ],
    },
    {
        "slug": "dentist-paschim-vihar",
        "area": "Paschim Vihar",
        "keyword": "Dentist near Paschim Vihar",
        "distance": "about 4 km",
        "route": [
            ("By car or cab", "Come towards Punjabi Bagh and then Rajouri Garden. The clinic is on the first floor of J 12/26, above Rajmandir, with a lift and parking close by."),
            ("By metro", "Take the Green Line to Punjabi Bagh, walk across to Punjabi Bagh West on the Pink Line, and ride two stops to Rajouri Garden. The clinic is a short walk from the station."),
        ],
        "intro": "Patients from Paschim Vihar, Meera Bagh and Punjabi Bagh come to our Rajouri Garden clinic for dental implants, veneers and everyday dentistry. The clinic is open seven days, so Sunday appointments are easy to fit in.",
        "faq": [
            ("Is there a Dr Sobti's clinic in Paschim Vihar?", "No. The clinic is in Rajouri Garden, a short drive from Paschim Vihar through Punjabi Bagh, or a short metro ride with one change to the Pink Line."),
            ("What do patients from Paschim Vihar usually come for?", "Mostly dental implants and full mouth implants with Dr Pushkar Sobti, and veneers, whitening and smile design with Dr Parul Sharma Sobti, plus root canals and crowns."),
            ("Can I get a first opinion without travelling?", "Yes. Send a photo or your X-ray on WhatsApp for a free first opinion. An in-clinic consultation with an examination is ₹700."),
        ],
    },
    {
        "slug": "dentist-punjabi-bagh",
        "area": "Punjabi Bagh",
        "keyword": "Dentist near Punjabi Bagh",
        "distance": "about 3 km",
        "route": [
            ("By metro", "From Punjabi Bagh West take the Pink Line; Rajouri Garden is two stops away (ESI Basaidarapur, then Rajouri Garden). The clinic is a short walk from the station, above Rajmandir."),
            ("By car", "Drive down Ring Road or Club Road towards Rajouri Garden. The clinic is on the first floor of J 12/26 with a lift, and there is parking close by."),
        ],
        "intro": "Families from East and West Punjabi Bagh, Madipur and Shivaji Park come to our Rajouri Garden clinic for dental implants, full mouth implants, veneers and smile design. The CBCT 3D scanner and our own dental lab are on the same floor, so planning, surgery and the final teeth happen in one place.",
        "faq": [
            ("Is there a Dr Sobti's clinic in Punjabi Bagh?", "No. Our clinic is in Rajouri Garden, two stops from Punjabi Bagh West on the Pink Line, or a short drive."),
            ("What do Punjabi Bagh patients usually come for?", "Mostly single and full mouth dental implants with Dr Pushkar Sobti, and veneers and smile design with Dr Parul Sharma Sobti. Root canals, crowns and cleanings are done here too."),
            ("Is the implant quote all-inclusive?", "Yes. The written plan you get after the CBCT scan lists the full cost of your treatment, with nothing extra to pay later."),
        ],
    },
    {
        "slug": "dentist-naraina",
        "area": "Naraina",
        "keyword": "Dentist near Naraina",
        "distance": "about 2 km",
        "route": [
            ("By metro", "From Naraina Vihar take the Pink Line towards Majlis Park. Rajouri Garden is two stops away (Mayapuri, then Rajouri Garden). The clinic is a short walk from the station."),
            ("By car or auto", "Come up Ring Road past Mayapuri to Rajouri Garden. The clinic is on the first floor of J 12/26, above Rajmandir, with a lift and parking close by."),
        ],
        "intro": "Naraina Vihar, Naraina Village and Inderpuri are only a few minutes from our Rajouri Garden clinic. Patients from these colonies come to us for dental implants, veneers, root canals and regular check-ups, any day of the week.",
        "faq": [
            ("Is Dr Sobti's Dental Care in Naraina?", "No. The clinic is in Rajouri Garden, two stops from Naraina Vihar on the Pink Line."),
            ("Can I come on a Sunday?", "Yes. The clinic is open all seven days, 10 am to 7 pm, by appointment. Please call or WhatsApp first."),
            ("Do you make crowns and implant teeth in-house?", "Yes. Crowns, veneers and implant teeth are made in our own lab on the same floor, which saves visits and waiting time."),
        ],
    },
    {
        "slug": "dentist-kirti-nagar",
        "area": "Kirti Nagar and Moti Nagar",
        "keyword": "Dentist near Kirti Nagar and Moti Nagar",
        "distance": "about 2 to 3 km",
        "route": [
            ("By metro", "From Kirti Nagar take the Blue Line towards Dwarka. Rajouri Garden is three stops away (Moti Nagar, Ramesh Nagar, Rajouri Garden); from Moti Nagar it is two stops. The clinic is a short walk from the station."),
            ("By car or auto", "Drive along Najafgarh Road towards Rajouri Garden. The clinic is on the first floor of J 12/26 with a lift, and parking is close by."),
        ],
        "intro": "Patients from Kirti Nagar, Moti Nagar and Ramesh Nagar come to our Rajouri Garden clinic for dental implants, smile design with veneers, root canals and crowns. It is a short metro ride on the Blue Line.",
        "faq": [
            ("Do you have a clinic in Kirti Nagar or Moti Nagar?", "No. The clinic is in Rajouri Garden, two or three stops away on the Blue Line."),
            ("Who does veneers and smile design?", "Dr Parul Sharma Sobti. She plans veneers, whitening and bonding digitally first, so you see the result before treatment starts."),
            ("Can I send a photo first?", "Yes. Send a photo of your teeth or your X-ray on WhatsApp for a free first opinion. An in-clinic consultation is ₹700."),
        ],
    },
    {
        "slug": "dentist-patel-nagar-rajinder-nagar",
        "area": "Patel Nagar and Rajinder Nagar",
        "keyword": "Dentist near Patel Nagar and Rajinder Nagar",
        "distance": "about 5 to 6 km",
        "route": [
            ("By metro", "From Patel Nagar take the Blue Line towards Dwarka. Rajouri Garden is five stops away (Shadipur, Kirti Nagar, Moti Nagar, Ramesh Nagar, Rajouri Garden). From Rajendra Place it is six stops. The clinic is a short walk from the station."),
            ("By car", "Drive along Patel Road and Najafgarh Road towards Rajouri Garden. The clinic is on the first floor of J 12/26, above Rajmandir, with a lift and parking close by."),
        ],
        "intro": "Patients from East and West Patel Nagar, Old and New Rajinder Nagar and Karol Bagh travel to our Rajouri Garden clinic for dental implants, full mouth implants and smile design. Each implant case is planned on our own CBCT scan with guided surgery, and the teeth are made in our in-house lab.",
        "faq": [
            ("Is there a Dr Sobti's clinic in Patel Nagar or Rajinder Nagar?", "No. The clinic is in Rajouri Garden, on the same Blue Line as Patel Nagar and Rajendra Place."),
            ("Why travel to Rajouri Garden for implants?", "Dr Pushkar Sobti has placed more than 5,000 implants since 2009. The CBCT scan, the guided surgery and the lab that makes your implant teeth are all in one clinic, which keeps the number of visits low."),
            ("How many visits will I need?", "Usually a consultation with a CBCT scan, the surgery visit, and a visit for the final teeth after healing, plus short check-ups. Your written plan tells you exactly how many."),
        ],
    },
    {
        "slug": "dentist-pitampura",
        "area": "Pitampura and Netaji Subhash Place",
        "keyword": "Dentist near Pitampura and Netaji Subhash Place",
        "distance": "about 8 to 9 km by road",
        "route": [
            ("By metro", "From Netaji Subhash Place take the Pink Line; Rajouri Garden is four stops away (Shakurpur, Punjabi Bagh West, ESI Basaidarapur, Rajouri Garden). From Pitampura station, take the Red Line two stops to Netaji Subhash Place and change to the Pink Line."),
            ("By car", "Come down Ring Road past Punjabi Bagh to Rajouri Garden. The clinic is on the first floor of J 12/26, above Rajmandir, with a lift and parking close by."),
        ],
        "intro": "Patients from Pitampura, Netaji Subhash Place, Shalimar Bagh, Ashok Vihar and Wazirpur travel to our Rajouri Garden clinic for dental implants, full mouth implants and veneers. The clinic is four stops away on the Pink Line, and it is open every day.",
        "faq": [
            ("Is Dr Sobti's Dental Care in Pitampura?", "No. The clinic is in Rajouri Garden, four stops from Netaji Subhash Place on the Pink Line, or about 8 to 9 km by road."),
            ("What is included in the implant price?", "A single implant starts at ₹35,000. That includes the CBCT scan, guided surgery, a custom abutment and a zirconia crown, with nothing extra to pay later. Your written plan after the scan gives the exact cost."),
            ("Can I get a first opinion before travelling from Pitampura?", "Yes. Send a photo or your X-ray on WhatsApp for a free first opinion, so you know what to expect before you make the trip."),
        ],
    },
]

WEST_DELHI_NEARBY = [
    ("Tagore Garden", "One stop west on the Blue Line, or a few minutes by auto."),
    ("Ramesh Nagar and Moti Nagar", "One and two stops east on the Blue Line."),
    ("Subhash Nagar", "Two stops west on the Blue Line."),
    ("Punjabi Bagh", "Two stops north on the Pink Line (Punjabi Bagh West), or a short drive."),
    ("Kirti Nagar", "Three stops east on the Blue Line."),
    ("Mayapuri and Naraina", "One and two stops south on the Pink Line."),
    ("Hari Nagar", "A short drive by car or auto."),
]

WEST_DELHI_FAQ = [
    ("Where is Dr Sobti's Dental Care in West Delhi?", "At J 12/26, First Floor, Rajouri Garden, New Delhi 110027, above Rajmandir. It is a short walk from Rajouri Garden metro station, where the Blue and Pink lines meet, so it is easy to reach from most of West Delhi."),
    ("Is the clinic open on Sunday?", "Yes. It is open all seven days, 10 am to 7 pm. Dr Pushkar Sobti and Dr Parul Sharma Sobti see patients by prior appointment, so please call or WhatsApp first."),
    ("Which treatments do patients from across West Delhi come for?", "Mostly dental implants and full mouth implants with Dr Pushkar Sobti, and veneers, whitening and smile design with Dr Parul Sharma Sobti, along with root canals, crowns, cleanings and children's dentistry."),
    ("How are the reviews?", "The Rajouri Garden clinic is rated 5.0 out of 5 from 118 Google reviews. Patients most often mention clear explanations before treatment, painless procedures and the in-house scan and lab."),
    ("How much does a consultation cost?", "A first opinion on WhatsApp is free. An in-clinic consultation with an examination and a written plan is ₹700."),
]


def area_links_html(skip=""):
    items = "".join(f'<li><a href="/{a["slug"]}.html">Patients from {e(a["area"])}</a></li>' for a in AREAS if a["slug"] != skip)
    return f'<ul>{items}<li><a href="/dentist-west-delhi.html">All of West Delhi</a></li></ul>'


def why_cards():
    return f"""<div class="grid g3">
  <article class="card"><h3>Implants planned in 3D</h3><p>Dr Pushkar Sobti has placed more than 5,000 implants since 2009. Every case is planned on the clinic's own CBCT scan, with guided surgery. <a href="{IMPLANTS}/">Dental implants in Delhi →</a></p></article>
  <article class="card"><h3>Smile design</h3><p>Dr Parul Sharma Sobti plans veneers, whitening and bonding digitally first, so you see the result before treatment. <a href="{SMILE}/">Smile design →</a></p></article>
  <article class="card"><h3>Our own lab</h3><p>Crowns, veneers and implant teeth are made in <a href="/lab.html">our in-house lab</a> on the same floor, which saves visits and waiting time.</p></article>
</div>"""


def page_area(a):
    route = "".join(f"<div class=\"card\"><h3>{e(t)}</h3><p>{e(d)}</p></div>" for t, d in a["route"])
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(ans)}</p></details>" for q, ans in a["faq"])
    return pagehead(f"{e(a['keyword'])}: Dr Sobti's Dental Care, Rajouri Garden", f"Patients from {a['area']}",
                    e(a["intro"])) + f"""
<section><div class="wrap">
  <div class="section-head"><h2>Getting here from {e(a['area'])}</h2><p class="lead">The clinic is {a['distance']} from {e(a['area'])}, in Rajouri Garden. It is open every day, 10 am to 7 pm, by appointment.</p></div>
  <div class="grid g2">{route}</div>
</div></section>
<section class="tint"><div class="wrap">
  <div class="section-head"><h2>Why patients from {e(a['area'])} choose us</h2></div>
  {why_cards()}
  <p style="margin-top:22px"><span class="stars">★★★★★</span> Rated {CLINIC['rating']} from {CLINIC['review_count']} Google reviews. <a href="/reviews.html">Read the reviews →</a></p>
</div></section>
<section><div class="wrap">{visit_html()}</div></section>
<section class="tint"><div class="wrap" style="max-width:860px">
  <div class="section-head"><h2>Questions from {e(a['area'])} patients</h2></div>
  {faq}
  <h3 style="margin-top:28px">Patients from other areas</h3>
  {area_links_html(a['slug'])}
</div></section>
{cta_band()}"""


def page_west_delhi():
    areas = "".join(
        f'<div class="card"><h3><a href="/{a["slug"]}.html">{e(a["area"])}</a></h3><p>{e(a["route"][0][1] if a["route"][0][0] == "By metro" else a["route"][1][1])}</p></div>'
        for a in AREAS)
    near = "".join(f"<li><strong>{e(n)}</strong>: {e(d)}</li>" for n, d in WEST_DELHI_NEARBY)
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(ans)}</p></details>" for q, ans in WEST_DELHI_FAQ)
    return pagehead("Dentist in West Delhi: Dr Sobti's Dental Care, Rajouri Garden", "West Delhi",
                    "One clinic for implants, smile design and family dentistry, in the middle of West Delhi at Rajouri Garden metro. Open all seven days, 10 am to 7 pm.") + f"""
<section><div class="wrap">
  <div class="section-head"><h2>Why West Delhi patients choose Dr Sobti's</h2><p class="lead">Rated {CLINIC['rating']} from {CLINIC['review_count']} Google reviews. A family practice since 1982, with the Rajouri Garden clinic opened in 2024.</p></div>
  {why_cards()}
</div></section>
<section class="tint"><div class="wrap">
  <div class="section-head"><h2>Coming from further away</h2></div>
  <div class="grid g2">{areas}</div>
</div></section>
<section><div class="wrap" style="max-width:860px">
  <div class="section-head"><h2>Close by</h2><p class="lead">Rajouri Garden station is where the Blue and Pink lines meet, so these colonies are only a stop or two away.</p></div>
  <ul>{near}</ul>
</div></section>
<section class="tint"><div class="wrap">{visit_html()}</div></section>
<section><div class="wrap" style="max-width:860px">
  <div class="section-head"><h2>Questions</h2></div>
  {faq}
</div></section>
{cta_band()}"""


def page_404():
    return f"""<section class="pagehead"><div class="wrap"><h1>Page not found</h1>
<p class="lead">The page you were looking for is not here. Try the <a href="/">home page</a>, our <a href="/treatments.html">treatments</a> or <a href="/contact.html">contact details</a>.</p></div></section>"""


PAGES = [
    ("index.html", "Dentist in Rajouri Garden, West Delhi | Dr Sobti's Dental Care",
     "Dr Sobti's Dental Care, J 12/26 Rajouri Garden, New Delhi. Dental implants, veneers, whitening, root canal and family dentistry. Open 7 days, 10 am to 7 pm. Call +91 87449 85976.",
     page_home, "index.html", [faq_schema(HOME_FAQ)], 1.0),
    ("about.html", "About Us and Our Dentists | Dr Sobti's Dental Care, Rajouri Garden",
     "Meet Dr Pushkar Sobti (implantologist) and Dr Parul Sharma Sobti (aesthetic dentist), and see inside the clinic in Rajouri Garden: CBCT, dental microscope and in-house lab.",
     page_about, "about.html", [crumbs_schema("about.html", "About us")], 0.8),
    ("treatments.html", "Dental Treatments in Rajouri Garden | Dr Sobti's Dental Care",
     "Implants, full mouth implants, veneers, teeth whitening, aligners, braces, root canal, crowns, cleaning and children's dentistry at Dr Sobti's Dental Care, Rajouri Garden.",
     page_treatments, "treatments.html", [crumbs_schema("treatments.html", "Treatments")], 0.9),
    ("lab.html", "In-House Dental Lab in Rajouri Garden: Titanium Arts Dental Studio | Dr Sobti's",
     "Crowns, veneers and implant teeth made on site at Titanium Arts Dental Studio, the in-house digital lab of Dr Sobti's Dental Care, Rajouri Garden. Same-day crowns for many patients.",
     page_lab, "about.html", [crumbs_schema("lab.html", "Our lab")] + video_ld(LAB_VIDEOS, "lab.html"), 0.6),
    ("reviews.html", "Patient Reviews | Dr Sobti's Dental Care, Rajouri Garden",
     "Rated 5.0 by 118 patients on Google. Read what patients say about implants, root canals, cleanings and smile work at Dr Sobti's Dental Care, Rajouri Garden.",
     page_reviews, "reviews.html", [crumbs_schema("reviews.html", "Reviews")], 0.6),
    ("videos.html", "Videos: Clinic Tour, Patient Stories and Our Lab | Dr Sobti's Dental Care",
     "Watch a tour of Dr Sobti's Dental Care, Rajouri Garden, patient testimonials, and crowns and bridges made in our in-house lab, plus implant and smile makeover videos.",
     page_videos, "about.html", [crumbs_schema("videos.html", "Videos")] + video_ld([i for _, _, l in CLINIC_VIDEOS for i in l], "videos.html"), 0.6),
    ("contact.html", "Dental Clinic in Rajouri Garden: Timings and Directions | Dr Sobti's",
     "J 12/26, First Floor, Rajouri Garden, New Delhi 110027, above Rajmandir. Open 7 days, 10 am to 7 pm. Call +91 87449 85976 or WhatsApp +91 80767 77307.",
     page_contact, "contact.html", [crumbs_schema("contact.html", "Contact"), faq_schema(CONTACT_FAQ)], 0.8),
    ("booking.html", "Book an Appointment | Dr Sobti's Dental Care, Rajouri Garden",
     "Book a dental appointment at Dr Sobti's Dental Care, Rajouri Garden, on WhatsApp or by phone. Free first opinion on WhatsApp; in-clinic consultation ₹700.",
     page_booking, "booking.html", [crumbs_schema("booking.html", "Book")], 0.7),
    ("faq.html", "Dentist in Rajouri Garden: Clinic Facts, Prices and FAQ | Dr Sobti's",
     "Timings, address, doctors, implant and treatment prices, and answers to common questions about Dr Sobti's Dental Care, J 12/26 Rajouri Garden, New Delhi. Open 7 days.",
     page_faq, "contact.html", [crumbs_schema("faq.html", "FAQ"), faq_schema(FAQ_ALL)], 0.8),
]


PAGES.append(("dentist-west-delhi.html", "Dentist in West Delhi, Open 7 Days | Dr Sobti's Dental Care, Rajouri Garden",
              "Dental implants, smile design and family dentistry for West Delhi at Rajouri Garden metro. Rated 5.0 from 118 Google reviews. Open 7 days, 10 am to 7 pm.",
              page_west_delhi, "contact.html", [crumbs_schema("dentist-west-delhi.html", "West Delhi"), faq_schema(WEST_DELHI_FAQ)], 0.8))
for _a in AREAS:
    PAGES.append((f"{_a['slug']}.html", f"{_a['keyword']} | Dr Sobti's Dental Care, Rajouri Garden",
                  f"Dentist for {_a['area']} patients: Dr Sobti's Dental Care, J 12/26 Rajouri Garden, {_a['distance']} away. Implants, smile design, root canals. Open 7 days, 10 am to 7 pm.",
                  (lambda a=_a: page_area(a)), "contact.html",
                  [crumbs_schema(f"{_a['slug']}.html", f"Patients from {_a['area']}"), faq_schema(_a["faq"])], 0.6))


if LIVE_BRANCHES:
    PAGES.append(("clinics.html", "Our Clinics in Rajouri Garden and West Delhi | Dr Sobti's Dental Care",
                  f"{BRAND['story']} Addresses, phone numbers and timings for every Dr Sobti's clinic.",
                  page_clinics, "about.html", [crumbs_schema("clinics.html", "Our clinics")], 0.6))
    for _b in LIVE_BRANCHES:
        PAGES.append((f"{_b['slug']}.html", f"{_b['name']}, {_b['area']}, New Delhi: Timings and Directions",
                      f"{_b['name']}, {_b['street']}, New Delhi {_b['postcode']}. Call {_b['phone_display']}. A branch of {BRAND['name']}.",
                      (lambda b=_b: page_branch(b)), "about.html",
                      [branch_schema(_b), crumbs_schema(f"{_b['slug']}.html", _b["area"])], 0.5))


REDIRECTS = {
    "home": "/", "index": "/",
    "about-us": "/about.html", "our-team": "/about.html#doctors", "team": "/about.html#doctors", "doctors": "/about.html#doctors",
    "services": "/treatments.html", "our-services": "/treatments.html", "treatment": "/treatments.html",
    "testimonials": "/reviews.html", "gallery": "/about.html#clinic",
    "contact-us": "/contact.html", "appointment": "/booking.html", "book-appointment": "/booking.html", "book": "/booking.html",
    # Old-site pages Google still lists (site: search, 5 Nov 2026); they 404 without these.
    "our-doctors.html": "/about.html#doctors", "Pushkar-Sobti.html": "/about.html#doctors",
    "services.html": "/treatments.html", "impaction.html": "/treatments.html",
    "cosmetic-dental-fillings.html": "/treatments.html", "gallery.html": "/about.html#clinic",
    "Careers.html": "/contact.html",
    # Old-site blog page Google crawled in Jul 2026 (Search Console, 9 Nov 2026).
    "blog.html": "/treatments.html", "blog": "/treatments.html",
}


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / "assets", OUT / "assets")
    for path, title, desc, fn, current, ld, _ in PAGES:
        (OUT / path).write_text(layout(path, title, desc, fn(), current, ld), encoding="utf-8")
    (OUT / "404.html").write_text(
        layout("404.html", "Page not found | Dr Sobti's Dental Care", "Page not found.", page_404(), "")
        .replace('<meta name="viewport"', '<meta name="robots" content="noindex">\n<meta name="viewport"'), encoding="utf-8")
    urls = "".join(
        f"<url><loc>{SITE}/{'' if p == 'index.html' else p}</loc><lastmod>{UPDATED}</lastmod><priority>{pr}</priority></url>" for p, *_, pr in PAGES)
    (OUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
    ai_bots = ["OAI-SearchBot", "ChatGPT-User", "GPTBot", "PerplexityBot", "Perplexity-User", "ClaudeBot",
               "Claude-SearchBot", "Claude-User", "Google-Extended", "Applebot-Extended", "Bingbot"]
    (OUT / "robots.txt").write_text(
        "User-agent: *\nAllow: /\n\n# AI search and answer engines: welcome to read and cite this site\n"
        + "".join(f"User-agent: {b}\n" for b in ai_bots) + f"Allow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    (OUT / "CNAME").write_text("www.sobtidentalcare.com\n", encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    prices = "; ".join(f"{n} from INR {inr(pr)}{' ' + u if u else ''}" for n, pr, u in PRICES)
    faq_md = "\n".join(f"- {q} {a}" for q, a in FAQ_ALL)
    branches_md = ("## Our clinics\n" + f"- Main clinic: {CLINIC['name']}, {ADDRESS_LINE} (opened 2024): {SITE}/\n" + "".join(
        f"- Branch: {b['name']}, {b['street']}, {b['locality']} {b['postcode']}; phone {b['phone_display']}: {SITE}/{b['slug']}.html\n"
        for b in LIVE_BRANCHES) + f"- All clinics: {SITE}/clinics.html\n\n") if LIVE_BRANCHES else ""
    (OUT / "llms.txt").write_text(f"""# {CLINIC['name']}

> {CLINIC['name']} is a dental clinic at {ADDRESS_LINE}, India (above Rajmandir), open 7 days a week from 10 am to 7 pm. It has been a family clinic since 1982, when Dr Rajesh Sobti (MBBS, DCH) opened it in Vishnu Garden; Dr Pushkar Sobti joined in 2009 and opened this Rajouri Garden dental clinic in 2024. It is led by implantologist Dr Pushkar Sobti (BDS, MDS, PG in Oral Implantology, UCAM; in practice since 2009; 5,000+ implants placed) and aesthetic dentist Dr Parul Sharma Sobti (BDS). The clinic has its own CBCT 3D scanner and in-house dental lab (Titanium Arts Dental Studio) on the same floor. Google rating {CLINIC['rating']} from {CLINIC['review_count']} reviews.

## Key facts
- Address: {ADDRESS_LINE}, India. Landmark: {CLINIC['landmark']}. Nearest metro: Rajouri Garden (Blue and Pink lines).
- Map: {CLINIC['maps']} (lat {CLINIC['lat']}, lng {CLINIC['lng']})
- Timings: Monday to Sunday, 10:00 to 19:00 (open on Sundays)
- Phone: {CLINIC['phone_display']}. WhatsApp: {CLINIC['wa_display']}. Email: {CLINIC['email']}
- Book: {SITE}/booking.html (opens WhatsApp). Free first opinion on WhatsApp; in-clinic consultation INR 700.
- Doctors: Dr Pushkar Sobti, implantologist (single implants, All-on-4, All-on-6, All-on-X full-arch implants, guided surgery, bone grafting); Dr Parul Sharma Sobti, aesthetic dentist (veneers, whitening, smile makeovers, root canals, crowns, cleanings).
- Equipment: CBCT 3D scanner, dental microscope, implant surgery room, Class B autoclave, in-house CAD/CAM lab.
- Implant brands: Osstem, Hiossen and Nobel Biocare, among others; brand named in writing on every plan.
- Starting prices: {prices}. Exact prices are given in writing after an examination.
- Areas served: Rajouri Garden, Punjabi Bagh, Tagore Garden, Subhash Nagar, Ramesh Nagar, Tilak Nagar, Janakpuri, Vikaspuri, Paschim Vihar and the rest of West Delhi; implant patients from across Delhi NCR and abroad.
- Languages: English, Hindi. Payment: cash, card, bank transfer. Not on the CGHS panel.
- Profiles: Google {SOCIAL['Google']} · Instagram {SOCIAL['Instagram']} · Facebook {SOCIAL['Facebook']} · YouTube {SOCIAL['YouTube']}
- Last updated: {UPDATED}

## Pages
- [Home]({SITE}/): the clinic, doctors, treatments, reviews, visit
- [Clinic facts and FAQ]({SITE}/faq.html): timings, prices, doctors and common questions
- [About and doctors]({SITE}/about.html)
- [Treatments]({SITE}/treatments.html): every treatment, with links to the detailed pages
- [In-house lab, Titanium Arts Dental Studio]({SITE}/lab.html)
- [Videos: clinic tour, patient stories, lab work]({SITE}/videos.html) · implant videos: {IMPLANTS}/videos/ · smile makeover videos: {SMILE}/videos.html
- [Patient reviews]({SITE}/reviews.html)
- [Contact and timings]({SITE}/contact.html)
- [Dentist in West Delhi: routes from Tilak Nagar, Janakpuri, Vikaspuri, Paschim Vihar and nearby colonies]({SITE}/dentist-west-delhi.html)
- [Book an appointment]({SITE}/booking.html)

{branches_md}## Related sites (same clinic)
- [Dental implants in Delhi, Dr Pushkar Sobti]({IMPLANTS}/): implants, All-on-4, full mouth implants, costs
- [Dental implant cost in Delhi]({IMPLANTS}/dental-implant-cost-delhi/)
- [Smile design and other treatments, Dr Parul Sharma Sobti]({SMILE}/): veneers, whitening, aligners, braces, root canal, crowns, cleaning

## Frequently asked questions
{faq_md}
""", encoding="utf-8")
    # Common addresses from the old site and typical links, sent to the matching new page.
    # GitHub Pages cannot send a 301, so each stub is an instant meta refresh plus canonical, which
    # Google treats as a permanent redirect. No noindex here: it would stop Google passing the old
    # page's signals to the new one (Search Console audit, 11 Nov 2026).
    for old, new in REDIRECTS.items():
        if old.endswith(".html"):
            f = OUT / old
        else:
            (OUT / old).mkdir(parents=True, exist_ok=True)
            f = OUT / old / "index.html"
        f.write_text(
            f'<!doctype html><meta charset="utf-8"><title>Redirecting</title><link rel="canonical" href="{SITE}{new}">'
            f'<meta http-equiv="refresh" content="0; url={new}"><a href="{new}">Continue</a>\n',
            encoding="utf-8")
    print(f"Built {len(PAGES) + 1} pages and {len(REDIRECTS)} redirects into {OUT}")


if __name__ == "__main__":
    main()
