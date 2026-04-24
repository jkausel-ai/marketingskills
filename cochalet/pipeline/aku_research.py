#!/usr/bin/env python3
"""
aku_research.py -- Auto Knowledge Update (AKU) Research Pipeline
Priority 5: Automated web research + knowledge enrichment.

Pipeline: TOPIC → SEARCH → EXTRACT → VERIFY → STORE (to hermes_memory)

Uses DuckDuckGo HTML search (no API key needed) + urllib for fetching.
Stores findings in hermes_memory.db with source attribution.

Usage:
  python3 aku_research.py research "Pacaso pricing 2026"
  python3 aku_research.py research "Quebec co-ownership regulations"
  python3 aku_research.py competitor "Pacaso"
  python3 aku_research.py market "luxury chalet Laurentians 2026"
  python3 aku_research.py batch research_topics.txt
  python3 aku_research.py status
"""

import argparse
import html
import json
import os
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent))

DB_PATH = Path('/var/lib/hermes/memory/hermes_memory.db')
RESEARCH_LOG = Path('/var/lib/hermes/memory/aku_research.jsonl')
DELIVERABLES = Path('/mnt/hermes-output/deliverables/dept-strategy')

# DuckDuckGo HTML search (no API key)
DDG_URL = 'https://html.duckduckgo.com/html/'
USER_AGENT = 'Mozilla/5.0 (compatible; CoChalet-AKU/1.0)'
MAX_FETCH_SIZE = 50_000  # 50KB per page
FETCH_TIMEOUT = 15  # seconds


def web_search(query: str, max_results: int = 5) -> list:
    """Search DuckDuckGo and return list of {title, url, snippet}."""
    data = urllib.parse.urlencode({'q': query}).encode('utf-8')
    req = urllib.request.Request(DDG_URL, data=data)
    req.add_header('User-Agent', USER_AGENT)

    try:
        with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT) as resp:
            body = resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        return [{'error': str(e)}]

    results = []
    # Parse DDG HTML results (simplified regex extraction)
    # DDG uses <a class="result__a" href="...">title</a> and <a class="result__snippet">
    links = re.findall(
        r'<a[^>]+class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
        body, re.DOTALL
    )
    snippets = re.findall(
        r'<a[^>]+class="result__snippet"[^>]*>(.*?)</a>',
        body, re.DOTALL
    )

    for i, (url, title) in enumerate(links[:max_results]):
        # Decode DDG redirect URL
        if 'uddg=' in url:
            match = re.search(r'uddg=([^&]+)', url)
            if match:
                url = urllib.parse.unquote(match.group(1))

        snippet = ''
        if i < len(snippets):
            snippet = re.sub(r'<[^>]+>', '', snippets[i]).strip()
            snippet = html.unescape(snippet)

        title = re.sub(r'<[^>]+>', '', title).strip()
        title = html.unescape(title)

        results.append({
            'title': title,
            'url': url,
            'snippet': snippet,
        })

    return results


def fetch_page(url: str) -> Optional[str]:
    """Fetch a web page and return cleaned text content."""
    req = urllib.request.Request(url)
    req.add_header('User-Agent', USER_AGENT)

    try:
        with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT) as resp:
            raw = resp.read(MAX_FETCH_SIZE).decode('utf-8', errors='replace')
    except Exception:
        return None

    # Strip HTML tags, scripts, styles
    text = re.sub(r'<script[^>]*>.*?</script>', '', raw, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()

    return text[:10000]  # Cap at 10K chars


def summarize_with_model(content: str, topic: str, model: str = 'google/gemini-2.5-flash') -> Optional[str]:
    """Use OpenRouter API to summarize research content."""
    api_key = None
    env_path = Path('/root/.hermes/.env')
    if env_path.is_file():
        for line in env_path.read_text().splitlines():
            if line.startswith('OPENROUTER_API_KEY='):
                api_key = line.split('=', 1)[1].strip().strip("'\"")

    if not api_key:
        api_key = os.environ.get('OPENROUTER_API_KEY')
    if not api_key:
        return None

    prompt = f"""You are a research analyst for CoChalet, a luxury chalet co-ownership company in Quebec, Canada.

Extract ALL factual information from the content below that could be useful for understanding "{topic}".

Rules:
- Return bullet points starting with *
- Include: numbers, dates, prices, names, locations, regulations, requirements
- Include information that is even tangentially related to the topic
- ONLY say "NO RELEVANT FINDINGS" if the content is completely unrelated (e.g. a 404 page or spam)

Content:
{content[:8000]}"""

    payload = json.dumps({
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 1000,
        'temperature': 0.1,
    }).encode('utf-8')

    req = urllib.request.Request(
        'https://openrouter.ai/api/v1/chat/completions',
        data=payload
    )
    req.add_header('Authorization', f'Bearer {api_key}')
    req.add_header('Content-Type', 'application/json')
    req.add_header('HTTP-Referer', 'https://cochalet.co')

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode('utf-8'))
        return body.get('choices', [{}])[0].get('message', {}).get('content', '')
    except Exception as e:
        return f"[SUMMARY ERROR: {e}]"


def research_topic(topic: str, category: str = 'reference',
                   deep: bool = False) -> dict:
    """Full research pipeline: search → fetch → summarize → store."""
    now = datetime.now(timezone.utc)
    result = {
        'topic': topic,
        'category': category,
        'timestamp': now.isoformat(),
        'search_results': [],
        'findings': [],
        'stored_keys': [],
    }

    print(f"[AKU] Researching: {topic}")
    print(f"  [1/4] SEARCH...")
    search_results = web_search(topic)
    result['search_results'] = search_results
    print(f"  Found {len(search_results)} results")

    if not search_results or 'error' in search_results[0]:
        print(f"  ✗ Search failed")
        return result

    # Fetch top pages
    print(f"  [2/4] FETCH...")
    pages_content = []
    for sr in search_results[:3]:
        url = sr.get('url', '')
        if not url or url.startswith('#'):
            continue
        print(f"    Fetching: {url[:80]}")
        text = fetch_page(url)
        if text and len(text) > 100:
            pages_content.append({
                'url': url,
                'title': sr.get('title', ''),
                'text': text,
            })
        time.sleep(0.5)  # Rate limit

    if not pages_content:
        # Fall back to snippets
        combined = '\n'.join(
            f"- {sr['title']}: {sr['snippet']}"
            for sr in search_results if sr.get('snippet')
        )
        pages_content = [{'url': 'snippets', 'title': 'Search Snippets', 'text': combined}]

    # Summarize
    print(f"  [3/4] SUMMARIZE ({len(pages_content)} sources)...")
    combined_text = '\n\n---\n\n'.join(
        f"Source: {p['title']} ({p['url']})\n{p['text']}"
        for p in pages_content
    )
    summary = summarize_with_model(combined_text, topic)

    if summary and 'NO RELEVANT FINDINGS' not in summary:
        result['findings'] = summary.strip().split('\n')
        print(f"  Found {len(result['findings'])} findings")
    else:
        print(f"  No relevant findings extracted")
        return result

    # Store in memory
    print(f"  [4/4] STORE...")
    try:
        from hermes_memory import MemoryStore
        mem = MemoryStore()
        # Create a clean key from topic
        key = re.sub(r'[^a-z0-9]+', '_', topic.lower())[:60]
        key = f"aku_{key}"

        mem.remember(
            key=key,
            category=category,
            content=summary.strip(),
            source=f"aku-research {now.strftime('%Y-%m-%d')} | Sources: {', '.join(p['url'][:50] for p in pages_content[:3])}",
        )
        result['stored_keys'].append(key)
        print(f"  ✓ Stored as: {key}")
    except Exception as e:
        print(f"  ✗ Store failed: {e}")

    # Log to research journal
    try:
        with open(RESEARCH_LOG, 'a', encoding='utf-8') as f:
            f.write(json.dumps({
                'ts': now.isoformat(),
                'topic': topic,
                'category': category,
                'sources': len(pages_content),
                'findings': len(result['findings']),
                'stored': result['stored_keys'],
            }, ensure_ascii=False) + '\n')
    except Exception:
        pass

    return result


def research_competitor(name: str) -> dict:
    """Focused competitor research."""
    queries = [
        f"{name} co-ownership pricing 2026",
        f"{name} reviews customer experience",
        f"{name} business model how it works",
    ]
    all_findings = []
    for q in queries:
        result = research_topic(q, category='competitor')
        all_findings.extend(result.get('findings', []))

    # Consolidate into one memory entry
    if all_findings:
        try:
            from hermes_memory import MemoryStore
            mem = MemoryStore()
            key = f"competitor_{name.lower().replace(' ', '_')}_research"
            mem.remember(
                key=key,
                category='competitor',
                content='\n'.join(all_findings),
                source=f"aku-competitor-research {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
            )
            print(f"\n[AKU] Consolidated competitor research stored as: {key}")
        except Exception as e:
            print(f"\n[AKU] Consolidation failed: {e}")

    return {'competitor': name, 'total_findings': len(all_findings)}


def batch_research(filepath: str) -> dict:
    """Run research for each line in a topics file."""
    topics = Path(filepath).read_text().strip().splitlines()
    topics = [t.strip() for t in topics if t.strip() and not t.startswith('#')]
    results = []
    for i, topic in enumerate(topics):
        print(f"\n{'='*60}")
        print(f"[{i+1}/{len(topics)}] {topic}")
        print('='*60)
        parts = topic.split('|')
        if len(parts) == 2:
            result = research_topic(parts[0].strip(), category=parts[1].strip())
        else:
            result = research_topic(topic)
        results.append(result)
        time.sleep(1)  # Rate limit between topics
    return {
        'total_topics': len(topics),
        'successful': sum(1 for r in results if r.get('findings')),
        'stored': sum(len(r.get('stored_keys', [])) for r in results),
    }


# -- CLI ----------------------------------------------------------------
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='AKU Auto-Research Pipeline')
    sub = parser.add_subparsers(dest='command')

    p_research = sub.add_parser('research')
    p_research.add_argument('topic')
    p_research.add_argument('--category', default='reference', choices=[
        'canon', 'competitor', 'market', 'financial',
        'legal', 'technical', 'persona', 'reference',
    ])
    p_research.add_argument('--deep', action='store_true')

    p_comp = sub.add_parser('competitor')
    p_comp.add_argument('name')

    p_market = sub.add_parser('market')
    p_market.add_argument('query')

    p_batch = sub.add_parser('batch')
    p_batch.add_argument('filepath')

    sub.add_parser('status')

    args = parser.parse_args()

    if args.command == 'research':
        result = research_topic(args.topic, category=args.category, deep=args.deep)
        print(f"\nFindings: {len(result['findings'])}")
        print(f"Stored: {result['stored_keys']}")
    elif args.command == 'competitor':
        result = research_competitor(args.name)
        print(json.dumps(result, indent=2))
    elif args.command == 'market':
        result = research_topic(args.query, category='market')
        print(f"\nFindings: {len(result['findings'])}")
    elif args.command == 'batch':
        result = batch_research(args.filepath)
        print(json.dumps(result, indent=2))
    elif args.command == 'status':
        if RESEARCH_LOG.exists():
            lines = RESEARCH_LOG.read_text().strip().splitlines()
            print(f"Research log: {len(lines)} entries")
            for line in lines[-5:]:
                data = json.loads(line)
                print(f"  {data['ts'][:16]} | {data['topic'][:50]} | {data['findings']} findings")
        else:
            print("No research log yet")
    else:
        parser.print_help()
