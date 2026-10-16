#!/usr/bin/env python3
"""Check source records, rendered content, internal links, languages, and metadata."""
from html.parser import HTMLParser
import json
from pathlib import Path
import struct
from urllib.parse import unquote, urlsplit
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET

from build import OUT, PLATFORMS, read_inputs, lang_path, project_path
from papers import read_papers


class Page(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.hrefs, self.links, self.ids, self.projects, self.papers, self.graphs = [], [], set(), [], [], []
        self.meta, self.language, self.h1 = {}, '', 0
        self.json_parts, self.json_open = [], False
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'html': self.language = a.get('lang')
        if tag == 'h1': self.h1 += 1
        if tag == 'a' and a.get('href'): self.hrefs.append(a['href'])
        if tag == 'link': self.links.append(a)
        if tag == 'meta': self.meta[a.get('name') or a.get('property')] = a.get('content', '')
        if a.get('id'): self.ids.add(a['id'])
        if a.get('data-project'): self.projects.append(a['data-project'])
        if a.get('data-paper'): self.papers.append(a['data-paper'])
        if tag == 'script' and a.get('type') == 'application/ld+json': self.json_open, self.json_parts = True, []

    def handle_data(self, text):
        if self.json_open: self.json_parts.append(text)

    def handle_endtag(self, tag):
        if tag == 'script' and self.json_open:
            self.graphs.append(json.loads(''.join(self.json_parts)))
            self.json_open = False


def main():
    config, _, entries = read_inputs()
    _, papers = read_papers(OUT.parent, entries)
    origin = config['origin'].rstrip('/')
    urls = [node.text for node in ET.parse(OUT / 'sitemap.xml').findall('{*}url/{*}loc')]
    assert len(urls) == len(set(urls))
    assert len(urls) == len(list(OUT.rglob('index.html')))
    pages = {}
    for url in urls:
        parsed = urlsplit(url)
        assert url.startswith(origin + '/') and not parsed.query and not parsed.fragment, url
        page = Page((OUT / parsed.path.lstrip('/') / 'index.html').read_text())
        pages[parsed.path] = page
        assert page.h1 == 1 and page.meta.get('description') and page.graphs, url
        assert page.language == ('zh-CN' if parsed.path.startswith('/zh/') else 'en'), url
        assert [l.get('href') for l in page.links if l.get('rel') == 'canonical'] == [url], url
        assert 'noindex' not in page.meta.get('robots', ''), url
        assert page.meta.get('og:image') == page.meta.get('twitter:image') == origin + '/social-card.png', url
        for graph in page.graphs:
            assert graph['@context'] == 'https://schema.org'
            for item in graph['@graph']:
                if item['@type'] == 'ItemList':
                    assert item['numberOfItems'] == len(item['itemListElement']) == len(page.projects or page.papers), url
                    visible_links = {href if urlsplit(href).scheme else origin + href for href in page.hrefs}
                    for element in item['itemListElement']:
                        destination = element.get('url') or element['item']['url']
                        assert destination in visible_links, (url, destination)
    for path, page in pages.items():
        for link in page.links:
            if link.get('rel') == 'alternate' and link.get('hreflang'):
                other = pages[urlsplit(link['href']).path]
                assert any(l.get('rel') == 'alternate' and l.get('href') == origin + path for l in other.links), path
        for href in page.hrefs:
            parsed = urlsplit(href)
            if parsed.scheme or parsed.netloc:
                continue
            target = parsed.path or path
            if target in pages:
                if parsed.fragment: assert unquote(parsed.fragment) in pages[target].ids, href
            else:
                assert (OUT / target.lstrip('/')).is_file(), (path, href)
    expected = {e['id'] for e in entries}
    for language in ('en', 'zh'):
        assert set(pages[lang_path(language)].projects) == expected
        for platform in PLATFORMS:
            members = {e['id'] for e in entries if e['content_type'] == 'app' and platform in e['platforms']}
            if members:
                assert set(pages[lang_path(language, '/apps/' + platform + '/')].projects) == members, platform
        for entry in entries:
            page = pages[project_path(language, entry)]
            assert entry['primary_url'] in page.hrefs, entry['id']
        assert set(pages[lang_path(language, '/papers/')].papers) == {paper['id'] for paper in papers}
    robots = RobotFileParser()
    robots.parse((OUT / 'robots.txt').read_text().splitlines())
    for crawler in ('Googlebot', 'bingbot', 'OAI-SearchBot', 'PerplexityBot'):
        assert all(robots.can_fetch(crawler, url) for url in urls)
    assert (OUT / 'llms.txt').is_file()
    image = (OUT / 'social-card.png').read_bytes()
    assert image[:8] == b'\x89PNG\r\n\x1a\n' and struct.unpack('>II', image[16:24]) == (1200, 630), 'Invalid sharing image'
    assert 'noindex' in (OUT / '404.html').read_text()
    assert (OUT / 'references.bib').read_text().count('@misc{') == len(papers)
    print(f'Validated {len(entries)} source-backed records, {len(papers)} papers, {len(urls)} static pages, internal links, bilingual alternates, JSON-LD, citations, and crawler access.')


if __name__ == '__main__':
    main()
