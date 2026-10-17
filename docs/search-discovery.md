# Search discovery

The canonical website is [AI Can What?](https://aicanwhat.com/) and the public source is [reacher-z/AI-Can-What](https://github.com/reacher-z/AI-Can-What).

The site provides complete static HTML for the directory, categories, app-platform indexes, individual projects, and research bibliography in English and Chinese. Every canonical page is in the sitemap; language alternatives are reciprocal. Platform indexes have ordinary internal links and stable URLs such as `/apps/macos/`; query-string filters are a browsing convenience. Structured metadata describes the visible content. The original author remains the source of project claims.

Google's [AI search guidance](https://developers.google.com/search/docs/appearance/ai-features) uses ordinary search eligibility: crawlable pages that can be indexed and shown with a snippet. `llms.txt` is an optional navigation index, not a special eligibility requirement.

Homepage titles describe the catalog in each page's language, with the brand kept concise, following Google's [title-link guidance](https://developers.google.com/search/docs/appearance/title-link). `WebSite.sameAs` points to the corresponding public repository. Scoped browser observations add original steps and screenshots to selected project pages; they do not create ratings or imply that untested features work. These changes improve the information available to readers and crawlers; their ranking or citation effect is unmeasured.

The bilingual [selection guides](https://aicanwhat.com/guides/) answer concrete resource-selection questions, compare interaction settings and setup limits, and link both primary sources and project notes. Matching Markdown guides live in the public repository. This follows the purpose of Google's [helpful-content guidance](https://developers.google.com/search/docs/fundamentals/creating-helpful-content): provide a useful explanation and original organization for readers. Guide membership does not add independent projects, create a ranking, or imply full runtime testing. The method page explicitly discloses AI-assisted research, writing and site development.

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
