# Live audit of the clinic websites. Read-only: fetches pages and prints findings.
import re, ssl, socket, json, datetime, urllib.request, urllib.error
from urllib.parse import urljoin, urlparse
from html.parser import HTMLParser
UA = {'User-Agent': 'Mozilla/5.0 (Linux; Android 13) SobtiSiteAudit/1.0'}
SITES = ['https://www.sobtidentalcare.com/', 'https://drparulssobti.com/', 'https://dentalimplantsdelhi.com/']
BAD = ['83682', '80762', '98101', '98182', '9818290908']
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
nr = urllib.request.build_opener(NoRedirect)
def head(url):
    try:
        r = nr.open(urllib.request.Request(url, headers=UA), timeout=20); return r.status, r.headers.get('Location')
    except urllib.error.HTTPError as e: return e.code, e.headers.get('Location')
    except Exception as e: return 'ERR', str(e)[:80]
def get(url):
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25)
        return r.status, r.geturl(), r.read().decode('utf-8', 'ignore')
    except urllib.error.HTTPError as e: return e.code, url, ''
    except Exception as e: return 'ERR ' + str(e)[:60], url, ''
class L(HTMLParser):
    def __init__(s): super().__init__(); s.l = []
    def handle_starttag(s, t, a):
        a = dict(a)
        for k in ('href', 'src'):
            if a.get(k) and t in ('a', 'img', 'link', 'script', 'source', 'iframe'): s.l.append(a[k])
print('### redirects')
for u in ['http://sobtidentalcare.com/', 'http://www.sobtidentalcare.com/', 'https://sobtidentalcare.com/',
          'http://drparulssobti.com/', 'https://www.drparulssobti.com/', 'http://dentalimplantsdelhi.com/',
          'https://www.dentalimplantsdelhi.com/', 'http://drpushkarsobti.com/', 'https://drpushkarsobti.com/',
          'http://www.drpushkarsobti.com/', 'https://www.sobtidentalcare.com/about-us', 'https://dentalimplantsdelhi.com/blog',
          'https://dentalimplantsdelhi.com/index.html', 'https://www.sobtidentalcare.com/nonexistent-page-xyz']:
    print(u, '->', *head(u))
print('### certificates')
for h in ['www.sobtidentalcare.com', 'sobtidentalcare.com', 'drparulssobti.com', 'www.drparulssobti.com', 'dentalimplantsdelhi.com', 'www.dentalimplantsdelhi.com', 'drpushkarsobti.com', 'www.drpushkarsobti.com']:
    try:
        c = ssl.create_default_context().wrap_socket(socket.create_connection((h, 443), timeout=10), server_hostname=h).getpeercert()
        print(h, 'OK until', c['notAfter'])
    except Exception as e: print(h, 'CERT FAIL', str(e)[:100])
ext = {}
for site in SITES:
    host = urlparse(site).netloc
    print('### site', site)
    for f in ['robots.txt', 'llms.txt', 'sitemap.xml']:
        st, _, body = get(site + f); print(f, st, len(body))
    st, _, sm = get(site + 'sitemap.xml')
    urls = re.findall(r'<loc>(.*?)</loc>', sm)
    seen = set(); checked = {}
    for u in urls:
        st, final, html = get(u)
        flags = []
        if st != 200: flags.append(f'STATUS {st}')
        if final != u: flags.append(f'redirected to {final}')
        flat = re.sub(r'\s', '', html)
        flags += [f'BADNUM {b}' for b in BAD if b in flat]
        if 'AW-18553206533' not in html and 'sobtidentalcare' not in host: flags.append('no ads tag')
        if 'name="viewport"' not in html: flags.append('no viewport')
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
            try: json.loads(m.group(1))
            except Exception as e: flags.append('bad JSON-LD')
        p = L(); p.feed(html)
        for l in p.l:
            a = urljoin(u, l); pu = urlparse(a)
            if pu.scheme not in ('http', 'https'): continue
            if pu.netloc == host:
                a = a.split('#')[0]
                if a not in checked: checked[a] = head(a)[0]
                if checked[a] not in (200,): flags.append(f'link {a} -> {checked[a]}')
            else: ext.setdefault(a.split('#')[0], set()).add(u)
        print(u, st, '; '.join(sorted(set(flags))) or 'ok')
print('### external links')
for a in sorted(ext):
    if any(x in a for x in ['fonts.g', 'googletagmanager', 'gstatic', 'schema.org']): continue
    print(head(a)[0], a, '(on', len(ext[a]), 'pages)')
