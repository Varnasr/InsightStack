#!/usr/bin/env python3
"""Checks for the published pages, as distinct from the code.

    python3 scripts/check_site.py

`tests.yml` runs the Python and R suites and says nothing about the nine HTML
files this repository serves at https://varnasr.github.io/InsightStack/. The
traps below are all written down in CLAUDE.md and none of them was checked by
anything.
"""

import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors = []
checks = 0


def check(name, ok, detail=''):
    global checks
    checks += 1
    if not ok:
        errors.append('%s: %s' % (name, detail))


def read(p):
    with open(os.path.join(ROOT, p), encoding='utf-8', errors='replace') as fh:
        return fh.read()


def tracked(pattern):
    out = subprocess.run(['git', 'ls-files', pattern], cwd=ROOT,
                         capture_output=True, text=True).stdout
    return sorted(f for f in out.split('\n') if f)


def main():
    pages = [p for p in tracked('*.html') if not p.startswith('_layouts/')]
    check('there are pages to check', pages, 'none tracked')

    for page in pages:
        body = read(page)
        # Without a viewport a phone lays the page out at desktop width and
        # zooms out, so the text arrives too small to read. It looks correct
        # on the machine it was built on and only a visitor on a phone sees it.
        check('%s sets a viewport' % page,
              re.search(r'<meta[^>]*name=["\']?viewport', body, re.I) is not None,
              'a phone lays this out at desktop width')
        check('%s declares a charset' % page,
              re.search(r'<meta[^>]*charset', body, re.I) is not None,
              'the curly quotes and en dashes in the exports depend on it')
        check('%s declares a language' % page,
              re.search(r'<html[^>]*\blang=', body, re.I) is not None,
              'a screen reader guesses the pronunciation')
        check('%s has a title' % page,
              re.search(r'<title>[^<]+</title>', body, re.I) is not None,
              'the browser tab and every search result show the URL instead')

    # GitHub Pages runs jekyll-readme-index, so a folder becomes a page only
    # if it holds a README.md. A folder link with no README is a 404 in
    # production and a 200 under `python -m http.server`, which generates a
    # directory listing. That mistake shipped once; CLAUDE.md records it.
    index = read('index.html')
    rels = [h for h in re.findall(r'href="([^"]+)"', index)
            if not h.startswith(('http', '#', 'mailto:'))]
    folder_links = [h for h in rels if h.endswith('/') and h not in ('./', '/')]
    check('the index links at least one folder, so this check is live',
          folder_links, 'none found; if that is deliberate, the check is moot')
    no_readme = [h for h in folder_links
                 if not os.path.exists(os.path.join(ROOT, h, 'README.md'))
                 and not os.path.exists(os.path.join(ROOT, h, 'index.html'))]
    check('every folder the index links holds a README.md', not no_readme,
          '%s would 404 in production and 200 under python -m http.server' % no_readme)

    missing = [h for h in rels
               if not os.path.exists(os.path.join(ROOT, h.split('#')[0]))
               and not os.path.exists(os.path.join(ROOT, h.split('#')[0].rstrip('/'), 'index.html'))
               and not os.path.exists(os.path.join(ROOT, h.split('#')[0].rstrip('/'), 'README.md'))]
    check('every relative link on the index resolves', not missing, '%s' % missing)

    # The house style is one file, shared verbatim across the stack
    # repositories. A page reaching for its own CSS is how that stops being
    # true, and the drift is invisible until two sites look different.
    styled = [p for p in pages if '<style' in read(p).lower()]
    check('no page carries its own <style> block',
          not styled or styled == ['taguette_coding/tag_summary_export.html'],
          '%s should use assets/css/stack.css' % styled)
    check('assets/css/stack.css is present',
          os.path.exists(os.path.join(ROOT, 'assets', 'css', 'stack.css')),
          'the house style file is the one every page loads')

    # _config.yml must keep applying the layout and must not reintroduce a
    # theme: before the layout existed, any rendered README opened in stock
    # minima and a click-through stopped looking like the site.
    config = read('_config.yml')
    check('_config.yml sets no theme',
          not re.search(r'^\s*(theme|remote_theme)\s*:', config, re.M),
          'a theme makes every rendered README open in stock styling')
    check('_config.yml still applies the default layout',
          'default' in config and 'defaults' in config,
          'without it a click-through stops looking like the site')

    if errors:
        print('FAIL: %d of %d checks' % (len(errors), checks))
        for e in errors:
            print('  - %s' % e)
        return 1
    print('PASS: %d checks (%d pages)' % (checks, len(pages)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
