# lysningapp.dk – deploy til GitHub Pages

Statisk side. Kilden er Claude Design-bundlen i `src/`; `index.html` og `assets/` genereres med `python tools/unbundle.py`.

## Indhold
- `src/lysning.bundle.html` – kildefilen: Claude Design-eksporten (alt i én fil). Ret her.
- `tools/unbundle.py` – pakker bundlen ud til `index.html` + `assets/`, så siden vises med det samme uden indlæsningsskærm
- `index.html`, `assets/` – genererede filer (skrifttyper, billeder og React ligger lokalt, ingen tredjepartskald)
- `CNAME` – custom domæne: lysningapp.dk
- `.nojekyll` – slår Jekyll fra på GitHub Pages
- `404.html` – sender ukendte stier til forsiden
- `robots.txt`, `sitemap.xml`

Undersider bruger hash-routing (`/#/ramte`, `/#/paaroerende`, `/#/sundhedspersoner`, `/#/kommuner-og-regioner`, `/#/arbejdsgivere`, `/#/om-lysning`, `/#/privatlivspolitik`), så der kræves ingen server-opsætning.

## Prompt til Claude Code

> Jeg har en mappe `lysningapp-site/` med et færdigt statisk website. Læg det op på GitHub Pages med custom domænet lysningapp.dk:
> 1. Opret et nyt offentligt GitHub-repo `lysningapp-site` (brug `gh repo create`), og læg indholdet af mappen i roden af repoet. Behold `CNAME` og `.nojekyll`.
> 2. Commit og push til `main`.
> 3. Slå GitHub Pages til fra branch `main`, mappe `/` (`gh api -X POST repos/{owner}/lysningapp-site/pages -f "source[branch]=main" -f "source[path]=/"`), og sæt custom domain til lysningapp.dk.
> 4. Fortæl mig præcis hvilke DNS-records jeg skal oprette hos min domæneudbyder, og slå "Enforce HTTPS" til, når certifikatet er udstedt.
> Ændr ikke i `index.html`.

## DNS hos domæneudbyderen
| Type | Navn | Værdi |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| AAAA | @ | 2606:50c0:8000::153 |
| AAAA | @ | 2606:50c0:8001::153 |
| AAAA | @ | 2606:50c0:8002::153 |
| AAAA | @ | 2606:50c0:8003::153 |
| CNAME | www | <github-brugernavn>.github.io |

Det kan tage op til 24 timer, før DNS og HTTPS-certifikat er på plads. Verificér gerne domænet under GitHub → Settings → Pages → "Verified domains" for at undgå domæne-kapring.

## Formularer (Formspree)
Venteliste og kontakt sender JSON med `fetch` til Formspree (konstanten `FORMSPREE` i `src/lysning.bundle.html`, søg efter `formspree.io/f/`). Begge formularer bruger samme Formspree-form; feltet `formular` er `Venteliste` eller `Kontakt`. Svar-til sættes automatisk til afsenderens e-mail.

Skift Formspree-form: erstat ID'et efter `https://formspree.io/f/` i `src/lysning.bundle.html`, kør `python tools/unbundle.py`, commit og push.

## Ny eksport fra Claude Design
Gem den nye eksport som `src/lysning.bundle.html`, genindsæt Formspree-koden i `sendWl`/`sendCt` (se git-historikken), og kør `python tools/unbundle.py`.

## Opdatér app-skærmbilleder fra prototypen
1. Server den nyeste Claude Design-prototype (`Lysning App.html`) lokalt, fx `python -m http.server 8766` i dens mappe.
2. `npm i puppeteer-core` (kræver installeret Chrome), og kør `node tools/screenshots.mjs screens`.
3. `python tools/replace_screens.py screens` (kræver `pip install pillow`) og `python tools/unbundle.py`.

Hvis prototypens knaptekster ændrer sig, skal navigationen i `tools/screenshots.mjs` rettes.
