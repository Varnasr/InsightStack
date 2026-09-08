# InsightStack

MEL tools, calculators, research documentation, and loaders for real survey
microdata. Part of the [OpenStacks](https://openstacks.dev) family. Status:
Stable, per the family [maintenance policy](https://github.com/Varnasr/OpenStacks-for-Change/blob/main/MAINTENANCE.md).

## Layout

Polyglot by design: Stata, Python, R, SPSS. See the README table for the full
list. Two parts matter most when working here.

- `stata_snippets/`, `spss_scripts/`, `label_variables/`, `data_validation/` —
  technique taught against stand-in data. `import_cleaning.do` reads a
  `health_survey.csv` that does not exist. That is deliberate and fine.
- `data_starters/` — the opposite: code that knows a specific named dataset and
  opens the files as they actually arrive. One folder per dataset, each with the
  same loader in Stata, R and Python, a README naming the raw files to fetch, and
  tests against seeded synthetic fixtures.

## data_starters conventions

- **No data ships and none can.** DHS and MoSPI both prohibit redistribution.
  Every folder has a `make_fixture.py` that builds synthetic files carrying the
  structure and nobody's data. `fixtures/` is gitignored.
- **Scale factors and byte positions are read at runtime**, from `variables.csv`
  for DHS and from the round's own layout for PLFS, never hardcoded. Documented
  behaviour and applied behaviour cannot then drift apart.
- **A folder earns its place** when its loader opens the real files and its
  README names at least one error the data makes easy and quiet. A folder that
  is a README and a stub is worse than none, because it looks like coverage.
- **Nothing is listed before it is built.** Maintenance policy rule 1: a roadmap
  entry is a promise to a reader.

## Testing

`.github/workflows/tests.yml` runs everything on pull requests and pushes to
main. No schedule: nothing here touches an external service, so nothing rots
between commits.

```
cd data_starters/dhs-south-asia && python make_fixture.py --outdir fixtures
python test_load_dhs.py     # 30 checks
Rscript test_load_dhs.R     # 33: the same ones plus the survey design object

cd ../plfs-india && python make_fixture.py --outdir fixtures
python test_load_plfs.py    # 28 checks
Rscript test_load_plfs.R    # the same 28
```

Stata has no free runtime, so the `.do` files are the only untested ones. Each
carries a fixture check at the bottom naming the number to look for. Say so
plainly rather than implying otherwise.

## Watch out for

- **DHS weights** are `v005 / 1,000,000`, and the men's recode weights on
  `mv005`. Omitting the division leaves means intact and multiplies every
  weighted total by a million, so it survives casual checking.
- **DHS anthropometry** flags sit at 9990 and above and must be dropped *before*
  the values are divided by 100, not after. Getting this backwards turns flagged
  children into plausible z-scores and lowers your stunting rate.
- **PLFS weights** are not `MLTS/100`. For a combined estimate it is `MLTS/100`
  only where `NSS = NSC`, and `MLTS/200` otherwise. The blanket rule inflates the
  population wherever the sub-samples differ, silently, because ratios barely
  move.
- **Published tables are the check.** `data_starters/dhs-south-asia/benchmarks/`
  holds the figures DHS published. Reproducing them is the only cheap proof a
  pipeline is right end to end.

## network_effects_sni

Rewritten 2026-09-08 from four scripts that could not run as a chain: one wrote
its plot to a directory that does not exist, one duplicated it under different
column names, one read a CSV neither of them wrote, and the diffusion model
picked its seed with `random.choice` and no seed set.

Two things in the rewrite are the point of it and should survive a refactor.

**`peer_association` is deliberately not called `estimate_peer_effect`.** The
reflection problem (Manski 1993) means a positive coefficient is consistent with
endogenous influence, response to peers' characteristics, and simple shared
circumstances, and fully connected groups cannot separate them. The result
carries an `interpretation` string saying so and `print_result` prints it under
every estimate. A test asserts the string is there.

**Peer means are leave-one-out.** The version this replaced computed the group
mean including the member's own value on the line above the correct one and left
both in the frame. `test_including_your_own_value_would_manufacture_the_finding`
shows the cost: on pure noise the with-self version returns a large positive
coefficient, because the regressor contains the dependent variable.

Also: eigenvector centrality is computed by a dense symmetric solve rather than
through networkx, because both networkx routes fail on the graph shape a survey
of small groups produces. `eigenvector_centrality` raises
`PowerIterationFailedConvergence` and `eigenvector_centrality_numpy` goes through
ARPACK, which refuses a component of two nodes. A group of two members is
ordinary.

## Related repositories

The analysis half of the chain lives elsewhere, coupled through a CSV rather
than a dependency: [EquityStack](https://github.com/Varnasr/EquityStack)
`survey_estimation/` in Python, [FieldStack](https://github.com/Varnasr/FieldStack)
`survey_tools/dhs_stunting.R` in R.

## Design references

The house style now exists as a file: `assets/css/stack.css`. Its tokens, type and
border conventions are taken from **openstacks.dev**, which is the one page in the
family the owner considers well designed. Use it rather than writing new CSS, and
change it in one place if it needs changing.

The rules it encodes, so you do not undo them by accident: 2px borders and **no
shadows**, **no border-radius**, Bricolage Grotesque in uppercase for display,
Work Sans for prose, JetBrains Mono for labels and numbers, and colour bands
(`.band.white`, `.ash`, `.navy`, `.teal`, `.brick`, `.black`) rather than cards
floating on a page. Saffron `#f2a541` is the single accent and carries the focus
ring. No emoji anywhere.

For anything the house style does not already answer,
draw from **[kombai.com/gallery/web](https://kombai.com/gallery/web)** — the
owner's preferred reference for interface work that is genuinely well made. This
applies across all of Varna's repositories and sites, not only this one.

### Publishing traps, learned the hard way

**A folder only becomes a page if it holds a `README.md`.** GitHub Pages runs
`jekyll-readme-index`, which turns that README into the folder's index. A folder
without one returns 404.

**The nested duplicates are gone (2026-09-08).** Fourteen folders held a
directory of the same name, so clicking `taguette_coding` on GitHub showed one
folder called `taguette_coding` and nothing else, and the repository read as
empty. All flattened with `git mv`, with two exceptions worth knowing:
`stata_snippets/stata_snippets/` became `stata_snippets/stata_mel/`, because its
README described a distinct MEL set and would have collided with the top-level
one; and `spss_scripts/` was doubly nested, holding both `spss_scripts/` and
`spss_tools/spss_tools/`. Do not reintroduce the pattern by unzipping an archive
into a folder of its own name.

`miro/`, `network_effects_sni/` and `writing_guides/` had no README and now do.

**Do not link-check with `python -m http.server`.** It generates directory
listings, so every folder link returns 200 locally and a third of them 404 in
production. That mistake shipped once. Build with Jekyll and check that the
built output actually contains `<dir>/index.html`.

**Source folders link to GitHub, not to the site.** Uniform, never 404s, and
honest about what they are. The designed surface is the landing page, the
calculators and the data-starter guides; everything else is code.

**`_layouts/default.html` is why a click-through still looks like the site.**
Before it existed, `_config.yml` set `theme: minima` and any rendered README
opened in a stock theme. Keep the layout, keep `defaults` applying it, and do
not reintroduce a theme.

**Descriptions are visible, not hover titles.** A `title` attribute shows on no
touch device and is announced unreliably by screen readers.

**Check the landing page on a phone, not only in the link checker.** `.row span`
in `stack.css` carries `white-space: nowrap` so the short language tag ("Python,
R") keeps to one line. Adding a description as another span inside `.row` makes
it inherit that, and the page then scrolls sideways: 1384px against a 390px
viewport, invisible on a desktop and the first thing a phone shows. The nowrap is
now scoped to `.row .t span`. After any change to a landing page, load it at
390x844 and compare `documentElement.scrollWidth` against `clientWidth`.

**Write for the person with the problem, not for the folder.** "Causal inference:
DiD, PSM, IV/2SLS, RDD and sensitivity analysis" is accurate and tells a reader
nothing about when to open it. Lead with the question ("Did the programme work,
and can you defend the answer?"), then name the methods so someone who already
knows what they want can still find it.

What actually has an interface, counted rather than assumed (2026-09-08, after
all three landing pages shipped):

| Repository | HTML | Published at |
|---|---|---|
| InsightStack | 9 files: a root `index.html`, six calculators in `calculators/`, a Taguette export page, and `_layouts/default.html` | https://varnasr.github.io/InsightStack/ |
| FieldStack | a root `index.html` and `_layouts/default.html` | https://varnasr.github.io/FieldStack/ |
| EquityStack | a root `index.html` and `_layouts/default.html` | https://varnasr.github.io/EquityStack/ |

All three now run GitHub Pages with `jekyll-readme-index` and **no theme**. An
older version of this table said InsightStack used `minima` and EquityStack was
unpublished; both were true once and neither is now.

The six calculators are the largest design surface in the stack family and the
obvious place to start. Beyond the stacks: SignalStack, Experiments,
openstacks.dev and the ImpactMojo properties.

One constraint that catches people: `Experiments` serves under a strict Content
Security Policy allowlisting specific CDNs, so a design pulling fonts or scripts
from anywhere else fails there silently. Read its `netlify.toml` before adding
any external asset.
