#!/usr/bin/env python3
"""Notify participating search engines after deployment; dry-run by default."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ENDPOINT = 'https://api.indexnow.org/indexnow'
USER_AGENT = 'Mozilla/5.0 (compatible; AICanWhat-IndexNow/1.0)'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('urls', nargs='*', help='Exact canonical URLs added or meaningfully changed in this deployment')
    parser.add_argument('--initial-launch', action='store_true', help='Include the complete sitemap only for the initial launch')
    parser.add_argument('--submit', action='store_true', help='Verify the public ownership file and submit the selected URLs')
    parser.add_argument('--receipt', type=Path, default=ROOT / '.cache/indexnow-receipt.json')
    args = parser.parse_args()
    origin = json.loads((ROOT / 'site.json').read_text())['origin'].rstrip('/')
    host = urlsplit(origin).netloc
    key = (ROOT / 'static/indexnow.txt').read_text().strip()
    if not re.fullmatch(r'[a-f0-9]{32}', key):
        parser.error('The public ownership key must be 32 hexadecimal characters.')
    sitemap = (ROOT / 'dist/sitemap.xml').read_bytes()
    canonical = [e.text for e in ET.fromstring(sitemap).findall('{*}url/{*}loc')]
    if args.initial_launch and args.urls:
        parser.error('Choose explicit changed URLs or the initial-launch sitemap, not both.')
    urls = canonical if args.initial_launch else list(dict.fromkeys(args.urls))
    if not urls or len(urls) > 10000:
        parser.error('Supply 1–10,000 changed URLs, or --initial-launch for a newly published site.')
    for url in urls:
        parsed = urlsplit(url)
        if parsed.scheme != 'https' or parsed.netloc != host or parsed.query or parsed.fragment or url not in canonical:
            parser.error('Only exact canonical URLs from this site’s sitemap may be submitted.')
    if not args.submit:
        print(json.dumps({'mode': 'dry-run', 'host': host, 'count': len(urls), 'urls': urls}, indent=2))
        return 0
    for path, expected in [('/indexnow.txt', key.encode()), ('/sitemap.xml', sitemap.strip())]:
        with urlopen(Request(origin + path, headers={'User-Agent': USER_AGENT}), timeout=30) as response:
            if response.status != 200 or response.read(2_000_000).strip() != expected:
                raise ValueError('The public ownership file or sitemap does not match this build.')
    payload = {'host': host, 'key': key, 'keyLocation': origin + '/indexnow.txt', 'urlList': urls}
    request = Request(ENDPOINT, data=json.dumps(payload).encode(), method='POST',
                      headers={'Content-Type': 'application/json; charset=utf-8', 'User-Agent': USER_AGENT})
    try:
        with urlopen(request, timeout=30) as response:
            status, body = response.status, response.read(20000).decode('utf-8', 'replace')
    except HTTPError as error:
        status, body = error.code, error.read(20000).decode('utf-8', 'replace')
    receipt = {'submitted_at': datetime.now(timezone.utc).isoformat(), 'endpoint': ENDPOINT, 'host': host,
               'urls': urls, 'http_status': status, 'response_body': body,
               'meaning': {200: 'URLs received; indexing is not confirmed', 202: 'URLs received; key validation pending'}.get(status, 'Request was not accepted')}
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'http_status': status, 'count': len(urls), 'meaning': receipt['meaning'], 'receipt': str(args.receipt)}))
    return 0 if status in (200, 202) else 1


if __name__ == '__main__':
    raise SystemExit(main())
