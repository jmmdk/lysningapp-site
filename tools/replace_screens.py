"""Erstatter telefon-skærmbillederne i src/lysning.bundle.html med nye PNG'er
fra tools/screenshots.mjs (skaleres til 480 px bredde og gemmes som WebP).

Kør fra repo-roden:  python tools/replace_screens.py <mappe med PNG'er>
Kør derefter:        python tools/unbundle.py
"""
import base64, io, json, re, sys
from pathlib import Path
from PIL import Image

# uuid i bundlen -> skærmbillede fra tools/screenshots.mjs
MAP = {
    'f7422fe6-63cd-4e10-b45a-fc7c266e0ef5': 'ramt_hjem',
    '0a60a4d6-cecd-4fe4-b3fd-6bd5032c37c8': 'ramt_helbred',
    '56ab6833-da8e-4bca-b35b-7cfbbd161c70': 'ramt_arbejdslog',
    '8f1317f7-595d-4a6b-b3b7-9fafbba18d7a': 'ramt_traening',
    'c4b3fe3b-5c5c-4e79-9e69-f0d800ba7082': 'ramt_viden',
    'c7c39ab2-bf85-45ba-a219-d6b26947e2fd': 'ramt_profil',
    'e35ca4b5-acee-41ab-93d9-974e4faa678a': 'ramt_spoergeskema',
    'fffdba54-0425-4e3d-b055-2c63eb64c593': 'paar_hjem',
    '36b4e7f2-9113-4ee4-b4fb-99c2701f216a': 'paar_helbred',
}

src_dir = Path(sys.argv[1])
p = Path(__file__).resolve().parent.parent / 'src' / 'lysning.bundle.html'
s = p.read_text(encoding='utf-8')
m = re.search(r'(<script type="__bundler/manifest">)(.*?)(</script>)', s, re.S)
raw = m.group(2)
manifest = json.loads(raw)
for uuid, name in MAP.items():
    im = Image.open(src_dir / f'{name}.png').convert('RGBA')
    im = im.resize((480, round(480 * im.height / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'WEBP', quality=86, method=6)
    manifest[uuid] = {'mime': 'image/webp', 'compressed': False,
                      'data': base64.b64encode(buf.getvalue()).decode()}
    print(name, len(buf.getvalue()) // 1024, 'KB')
new = json.dumps(manifest, separators=(',', ':'))
s = s[:m.start(2)] + raw.replace(raw.strip(), new) + s[m.end(2):]
p.write_text(s, encoding='utf-8', newline='')
