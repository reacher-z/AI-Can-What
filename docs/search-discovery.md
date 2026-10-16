# Search discovery

The canonical website is [AI Can What?](https://aicanwhat.com/) and the public source is [reacher-z/AI-Can-What](https://github.com/reacher-z/AI-Can-What).

The site provides complete static HTML for the directory, categories, and individual projects in English and Chinese. Every canonical page is in the sitemap; language alternatives are reciprocal. Structured metadata describes the visible content. The original author remains the source of project claims.

Google's [AI search guidance](https://developers.google.com/search/docs/appearance/ai-features) uses ordinary search eligibility: crawlable pages that can be indexed and shown with a snippet. `llms.txt` is an optional navigation index, not a special eligibility requirement.

## After deploying

1. Confirm public HTTPS, the canonical URL, the correct sitemap origin, and a genuine HTTP 404 for an unknown page.
2. Verify `https://aicanwhat.com/` in Google Search Console with its issued file and submit `https://aicanwhat.com/sitemap.xml`.
3. Inspect a representative URL and record any requested indexing. Sitemap discovery is not proof that every page is indexed.
4. Notify IndexNow participants of newly published or meaningfully changed URLs. IndexNow does not submit to Google and does not guarantee AI citation.

For this site's first launch only:

```sh
python3 scripts/submit_indexnow.py --initial-launch
python3 scripts/submit_indexnow.py --initial-launch --submit
```

For later changes, pass only the affected canonical pages:

```sh
python3 scripts/submit_indexnow.py https://aicanwhat.com/projects/webarena/
python3 scripts/submit_indexnow.py https://aicanwhat.com/projects/webarena/ --submit
```

The script verifies that the live ownership file and sitemap match the build, then saves a private local receipt under `.cache/`. HTTP 200 means the URLs were received; HTTP 202 means key validation is pending. Avoid repeated unchanged batches. See the official [IndexNow protocol](https://www.indexnow.org/documentation) and [FAQ](https://www.indexnow.org/faq).

`static/indexnow.txt` and Google verification files are public ownership proofs, not account credentials. Keep private dashboard records and search receipts outside the public source. Track page indexing, search impressions, clicks, and actual cited URLs as separate outcomes.
