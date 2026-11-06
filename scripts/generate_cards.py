"""Generate About-me and Tech-stack SVG cards (dark + light) into <repo>/assets."""
import base64, os, sys, urllib.request
from xml.sax.saxutils import escape

OUT = os.path.join(sys.argv[1], "assets")
os.makedirs(OUT, exist_ok=True)
FONT = "'JetBrains Mono','Fira Code',Consolas,'Courier New',monospace"
SANS = "'Segoe UI',-apple-system,Helvetica,Arial,sans-serif"

THEMES = {
    "dark": dict(bg="#0d1117", card="#1e1f22", bar="#2b2d30", border="#30363d", gutter="#4b5059",
                 text="#bcbec4", kw="#cf8e6d", str="#6aab73", ann="#b3ae60", field="#c77dbb",
                 cls="#56a8f5", cmt="#7a7e85", title="#dfe1e5", tile="#f6f8fa", tileb="#d0d7de",
                 label="#e6edf3", sub="#8b949e", accent="#6db33f"),
    "light": dict(bg="#ffffff", card="#ffffff", bar="#f2f3f5", border="#d0d7de", gutter="#aeb3c2",
                  text="#080808", kw="#0033b3", str="#067d17", ann="#9e880d", field="#871094",
                  cls="#00627a", cmt="#8c8c8c", title="#24292f", tile="#ffffff", tileb="#d0d7de",
                  label="#24292f", sub="#57606a", accent="#4e8a2a"),
}

# ---------------------------------------------------------------- About me
# each line: list of (token_type, text)
def S(t): return ("str", f'"{t}"')
LINES = [
    [("cmt", "// Hi there! Thanks for dropping by 👋")],
    [("ann", "@Developer"), ("text", "("), ("field", "since"), ("text", " = "), ("str", "2024"), ("text", ")")],
    [("kw", "public class "), ("cls", "NgoTranQuocTuan"), ("kw", " extends "), ("cls", "MechanicalEngineer"), ("text", " {")],
    [],
    [("kw", "    String   "), ("field", "role"), ("text", "       = "), S("Java Backend Developer"), ("text", ";")],
    [("kw", "    String   "), ("field", "experience"), ("text", " = "), S("2+ years"), ("text", ";")],
    [("kw", "    String   "), ("field", "location"), ("text", "   = "), S("Ha Noi, Viet Nam"), ("text", ";")],
    [("kw", "    String   "), ("field", "currently"), ("text", "  = "), S("Tax payment modules for BIDV Direct @ IGNIFY"), ("text", ";")],
    [("kw", "    String[] "), ("field", "focus"), ("text", "      = { "), S("Secure APIs"), ("text", ", "), S("Payment processing"), ("text", ", "), S("Data integrity"), ("text", " };")],
    [("kw", "    String   "), ("field", "education"), ("text", "  = "), S("B.Eng Mechanical Engineering @ HUST"), ("text", ";")],
    [("kw", "    String   "), ("field", "funFact"), ("text", "    = "), S("Self-taught: from machines to microservices"), ("text", ";")],
    [],
    [("ann", "    @Override")],
    [("kw", "    public "), ("cls", "String"), ("text", " "), ("cls", "toString"), ("text", "() {")],
    [("kw", "        return "), S("Let's build reliable systems together!"), ("text", ";")],
    [("text", "    }")],
    [("text", "}")],
]

def about(theme):
    c = THEMES[theme]
    W, LH, TOP, PADL = 900, 24, 70, 64
    H = TOP + LH * len(LINES) + 24
    rows = []
    for i, toks in enumerate(LINES):
        y = TOP + i * LH
        spans = "".join(f'<tspan fill="{c[t]}">{escape(s)}</tspan>' for t, s in toks)
        rows.append(
            f'<g class="ln" style="animation-delay:{0.25 + i * 0.12:.2f}s">'
            f'<text x="44" y="{y}" fill="{c["gutter"]}" text-anchor="end">{i + 1}</text>'
            f'<text x="{PADL}" y="{y}" xml:space="preserve">{spans}</text></g>')
    last_y = TOP + (len(LINES) - 1) * LH
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
  text {{ font-family: {FONT}; font-size: 14.5px; }}
  .ln {{ animation: in .35s ease-out both; }}
  @keyframes in {{ from {{ opacity: 0; transform: translateX(-6px); }} to {{ opacity: 1; transform: none; }} }}
  .cur {{ animation: blink 1s step-end infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  @media (prefers-reduced-motion: reduce) {{ .ln {{ animation: none; opacity: 1; }} }}
</style>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="{c["card"]}" stroke="{c["border"]}"/>
<path d="M12.5 .5 H{W - 12.5} a12 12 0 0 1 12 12 V38 H.5 V12.5 a12 12 0 0 1 12-12z" fill="{c["bar"]}"/>
<line x1="0" y1="38" x2="{W}" y2="38" stroke="{c["border"]}"/>
<circle cx="22" cy="19" r="6" fill="#ff5f57"/><circle cx="42" cy="19" r="6" fill="#febc2e"/><circle cx="62" cy="19" r="6" fill="#28c840"/>
<rect x="88" y="6" width="150" height="32" rx="6" fill="{c["card"]}"/>
<rect x="88" y="35" width="150" height="3" fill="{c["accent"]}"/>
<text x="104" y="27" fill="{c["title"]}" style="font-family:{SANS};font-size:13px">☕ AboutMe.java</text>
<text x="{W - 18}" y="27" fill="{c["cmt"]}" text-anchor="end" style="font-family:{SANS};font-size:12px">tuanntq99 / profile</text>
{chr(10).join(rows)}
<rect class="cur" x="{PADL + 9}" y="{last_y - 14}" width="9" height="18" fill="{c["accent"]}" style="animation-delay:{0.25 + len(LINES) * 0.12:.2f}s"/>
</svg>'''

# ---------------------------------------------------------------- Tech stack
DEV = "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/{0}/{0}-{1}.svg"
GROUPS = [
    ("Backend", [("Java", "java", "original"), ("Spring", "spring", "original"), ("Kafka", "apachekafka", "original"),
                 ("Redis", "redis", "original"), ("Hibernate", "hibernate", "plain"), ("Quartz", None, "Qz")]),
    ("Databases", [("Oracle", "oracle", "original"), ("MySQL", "mysql", "original"),
                   ("PostgreSQL", "postgresql", "original"), ("MongoDB", "mongodb", "original")]),
    ("DevOps & Cloud", [("Docker", "docker", "original"), ("AWS", "amazonwebservices", "original"),
                        ("Linux", "linux", "original"), ("Ubuntu", "ubuntu", "original")]),
    ("Testing & Tools", [("JUnit", "junit", "original"), ("Mockito", None, "Mk"), ("SonarQube", "sonarqube", "original"),
                         ("IntelliJ", "intellij", "original"), ("Postman", "postman", "original"),
                         ("Git", "git", "original"), ("GitHub", "github", "original"), ("GitLab", "gitlab", "original")]),
]
_cache = {}
def icon(name, variant):
    key = (name, variant)
    if key not in _cache:
        with urllib.request.urlopen(DEV.format(name, variant), timeout=30) as r:
            _cache[key] = base64.b64encode(r.read()).decode()
    return _cache[key]

def stack(theme):
    c = THEMES[theme]
    W, LABW, TW, TH, GAP, RH = 900, 180, 76, 84, 10, 104
    H = 24 + RH * len(GROUPS)
    parts, n = [], 0
    for gi, (label, items) in enumerate(GROUPS):
        y = 24 + gi * RH
        parts.append(f'<text x="20" y="{y + TH / 2 + 5}" fill="{c["label"]}" style="font-family:{SANS};font-size:15px;font-weight:600">{escape(label)}</text>')
        parts.append(f'<rect x="20" y="{y + TH / 2 + 14}" width="28" height="3" rx="1.5" fill="{c["accent"]}"/>')
        for ii, (nm, dev, var) in enumerate(items):
            x = LABW + ii * (TW + GAP)
            if dev:
                body = f'<image x="{x + 18}" y="{y + 10}" width="40" height="40" href="data:image/svg+xml;base64,{icon(dev, var)}"/>'
            else:
                body = (f'<rect x="{x + 18}" y="{y + 10}" width="40" height="40" rx="10" fill="{c["accent"]}"/>'
                        f'<text x="{x + TW / 2}" y="{y + 36}" fill="#fff" text-anchor="middle" style="font-family:{SANS};font-size:16px;font-weight:700">{var}</text>')
            parts.append(
                f'<g class="t" style="animation-delay:{0.1 + n * 0.05:.2f}s">'
                f'<rect x="{x + .5}" y="{y + .5}" width="{TW - 1}" height="{TH - 1}" rx="12" fill="{c["tile"]}" stroke="{c["tileb"]}"/>'
                f'{body}<text x="{x + TW / 2}" y="{y + 70}" fill="#24292f" text-anchor="middle" style="font-family:{SANS};font-size:11.5px">{escape(nm)}</text></g>')
            n += 1
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
  .t {{ animation: pop .4s ease-out both; }}
  @keyframes pop {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
  @media (prefers-reduced-motion: reduce) {{ .t {{ animation: none; opacity: 1; }} }}
</style>
{chr(10).join(parts)}
</svg>'''

STATIC = os.environ.get("STATIC") == "1"
for th in THEMES:
    for name, fn in (("about", about), ("tech-stack", stack)):
        with open(os.path.join(OUT, f"{name}-{th}.svg"), "w", encoding="utf-8", newline="\n") as f:
            svg = fn(th)
            if STATIC: svg = svg.replace("animation:", "x-a:").replace("animation-delay", "x-d")
            f.write(svg)
print("ok", sorted(os.listdir(OUT)))
