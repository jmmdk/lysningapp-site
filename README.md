# lysningapp.dk – deploy til GitHub Pages

Statisk, færdigbygget side. Ingen build-trin.

## Indhold
- `index.html` – hele sitet i én fil (skrifttyper og billeder er indlejret, ingen tredjepartskald)
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
Venteliste og kontakt sender JSON med `fetch` til Formspree (konstanten `FORMSPREE` i `index.html`, søg efter `formspree.io/f/`). Begge formularer bruger samme Formspree-form; feltet `formular` er `Venteliste` eller `Kontakt`. Svar-til sættes automatisk til afsenderens e-mail.

Skift Formspree-form: erstat ID'et efter `https://formspree.io/f/` i `index.html`, commit og push.
