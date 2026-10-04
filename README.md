# AIToolsHub

- `site/` is the website. Upload the CONTENTS of this folder to the root of your GitHub repo.
- `build.py` regenerates `site/`. Keep it outside the repo root or delete it; the site does not need it.

## Set your real URL (do this before publishing)
Pages use the placeholder https://YOUR-USERNAME.github.io/YOUR-REPOSITORY in canonical tags, sitemap.xml and robots.txt.
Regenerate with your real address and contact email:

    python3 build.py https://USERNAME.github.io/REPOSITORY you@yourdomain.com

For a custom domain use https://yourdomain.com (no trailing slash).

## Publish
1. Upload everything inside `site/` to your repo root.
2. Repo > Settings > Pages > Deploy from a branch > main > / (root) > Save.
3. Google Search Console: add your URL, then Sitemaps > submit `sitemap.xml`.

## Edit
- Add tools: edit list `T` in build.py, then rebuild.
- Affiliate links: add `"Tool name": "your-affiliate-url"` to `AFF`. Only those links get rel="sponsored".
- Replace the "Hands-on notes" text on each review with your own testing and screenshots.
- Review the Privacy Policy and Terms for your situation before adding ads or analytics.
