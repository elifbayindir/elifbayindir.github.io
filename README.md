# elifbayindir.github.io

Personal academic site of Elif Bayındır, built with Jekyll and published by GitHub Pages.
No theme, no build tools: content lives in a few YAML and Markdown files.

| What | Where |
|---|---|
| About text, links, CV | `_data/profile.yml` |
| News | `_data/news.yml` |
| Publications | `_data/publications.yml` |
| Presentations | `_data/presentations.yml` |
| Experience | `_data/experience.yml` |
| Education | `_data/education.yml` |
| Earlier research, methods demos | `_data/earlier_research.yml`, `_data/demos.yml` |
| Gallery | `_data/gallery.yml`, `assets/img/gallery/` |
| Project pages | `_projects/*.md` |
| Styles | `assets/css/main.css` |

## Two ways to edit

- **In the browser.** Open the file on github.com, click the pencil icon, edit, then "Commit changes". The site updates about a minute later. Good for text changes.
- **On your computer.** Edit the files, preview locally (see below), then commit and push to `main`. Needed for new images and the CV PDF.

YAML is sensitive to indentation: keep two spaces, and put text that contains a colon in double quotes.

## Add a news item

Add it at the top of `_data/news.yml` (newest first). The home page shows the 8 most recent; older ones move into "Older news".

```yaml
- date: "2026-12"          # "YYYY-MM" shows as "Dec 2026"; "YYYY" shows as "2026"
  text: "Gave a talk on calibrated forecasting at …"
  link: /projects/cognitive-forecasting/   # optional
```

## Add a publication, or mark one as published

In `_data/publications.yml`, entries are grouped under `peer_reviewed:` and `under_review:`.
"Bayındır, E." is shown in bold as "E. Bayındır" automatically.

When a paper is accepted, move its entry from `under_review:` to the top of `peer_reviewed:` and add what is now known:

```yaml
  - year: 2027
    authors: "Bayındır, E., Arslan, S. Ş., & Atam, E."
    title: "Point Accuracy Saturation and Calibrated Uncertainty in Longitudinal Digital Cognitive Forecasting"
    venue: "IEEE Journal of Biomedical and Health Informatics"
    volume: "31(2)"            # optional
    pages: "100–112"           # optional
    links: { doi: "https://doi.org/…", code: "https://github.com/…" }
```

Only add `links` keys that have a real URL. Also update the project page's Outputs list and add a news item.

## Add a project page

1. Copy `_projects/_template.md` to `_projects/<short-name>.md` (no leading underscore). The page appears at `/projects/<short-name>/`.
2. Fill in the front matter: `title`, `description` (one sentence, shown on the home page and in search results), `meta`, `dates`, `role`, `status`, `order`, and optionally `repo` and `thumbnail`.
3. `featured: true` shows it as a row on the home page (keep 4–6 rows). `featured: false` lists it on one line under "More projects".
4. Write the sections in this order: Question, Approach, What I found, Outputs, and optionally Limitations.
5. Put figures in `assets/img/projects/<short-name>/` (max 1600 px wide) and insert them with:

```liquid
{% include figure.html src="/assets/img/projects/<short-name>/figure.png" width="1600" height="900" alt="What the figure shows" caption="One-sentence caption." %}
```

### Checklist for a new GitHub project

This can be followed step by step, or pasted as a request:

> Read the README of <repo URL>. Create a project page from `_projects/_template.md` using only facts stated there. Copy one or two figures from the repo into `assets/img/projects/<short-name>/`, resized to at most 1600 px wide. Set `featured` to true or false. Add a news item to `_data/news.yml`. Show me the page locally before committing.

## Add gallery photos

1. Put the original photos in `Website_Photos/` (git-ignored, never published).
2. Run the script. It removes all metadata, including GPS location, and writes a full-size copy and a thumbnail:

   ```sh
   python3 tools/optimise_images.py Website_Photos
   ```

3. Add one entry per photo to `_data/gallery.yml`, in display order:

   ```yaml
     - file: 16.jpg
       alt: "What the photo shows"
       position: "right center"   # optional: which part stays visible in the 4:5 tile
   ```

Photos open in a viewer when clicked; without JavaScript they open as a plain image.

## Replace the CV

Save the public CV (no phone number, no referee contact details) as `assets/pdf/Elif_Bayindir_CV.pdf`.
The first time, also set `cv: /assets/pdf/Elif_Bayindir_CV.pdf` in `_data/profile.yml`; the CV link then appears in the menu and under the about text.
Later updates only need the PDF replaced under the same name.

## Other links

In `_data/profile.yml`, a link with an empty `url:` is hidden. Fill in `url:` to show it (for example ResearchGate or Google Scholar).

## Preview locally

GitHub Pages uses Ruby 3.3-compatible gems, so the local preview uses Homebrew's `ruby@3.3`:

```sh
PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH" bundle install          # first time only
PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH" bundle exec jekyll serve --livereload
```

Open http://127.0.0.1:4000. Changes to `_config.yml` need a restart of the server.

## Publishing

Push to the `main` branch. GitHub Pages rebuilds the site in about a minute.
Check the build under the repository's "Actions" tab if a change does not appear.

## Regenerating images

```sh
python3 tools/make_og_image.py    # assets/img/og-image.png (link previews)
python3 tools/make_favicons.py    # favicon.svg, favicon-32.png, apple-touch-icon.png
```

Both download the font files they need into `tools/.cache/` (git-ignored).
