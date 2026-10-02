"""Pakker Claude Design-bundlen (src/lysning.bundle.html) ud til index.html + assets/.

Bundlen pakker alle filer ud i browseren bag en "L"-indlæsningsskærm. Udpakket
viser browseren siden med det samme, og filerne kan caches hver for sig.

Kør fra repo-roden:  python tools/unbundle.py
"""
import base64, gzip, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'src' / 'lysning.bundle.html'
ASSETS = ROOT / 'assets'
EXT = {'image/svg+xml': 'svg', 'image/png': 'png', 'image/webp': 'webp',
       'text/javascript': 'js', 'font/woff2': 'woff2'}

s = SRC.read_text(encoding='utf-8')
block = lambda name: json.loads(re.search(
    r'<script type="__bundler/%s">(.*?)</script>' % name, s, re.S).group(1))
manifest, template = block('manifest'), block('template')

ASSETS.mkdir(exist_ok=True)  # Dropbox kan låse mappen, så den slettes ikke
paths = {}
for uuid, entry in manifest.items():
    data = base64.b64decode(entry['data'])
    if entry.get('compressed'):
        data = gzip.decompress(data)
    name = f'{uuid}.{EXT[entry["mime"]]}'
    (ASSETS / name).write_bytes(data)
    paths[uuid] = f'/assets/{name}'
    template = template.replace(uuid, paths[uuid])
for f in ASSETS.iterdir():  # fjern assets, der ikke længere er i bundlen
    if f'/assets/{f.name}' not in paths.values():
        f.unlink()

# React hentes lokalt i stedet for fra unpkg (ingen tredjepartskald).
resources = {e['id']: paths[e['uuid']] for e in block('ext_resources')}
fonts = ''.join(f'<link rel="preload" href="{p}" as="font" type="font/woff2" crossorigin>\n'
                for p in paths.values() if p.endswith('.woff2'))
head = (f'\n<script>window.__resources = {json.dumps(resources)};</script>\n'
        + fonts
        + '<style>body{margin:0;background:#F6F4EF}</style>')
i = template.index('<head>') + len('<head>')
template = template[:i] + head + template[i:]

(ROOT / 'index.html').write_text(template, encoding='utf-8', newline='\n')
print(f'index.html: {len(template)} tegn, {len(paths)} assets')
