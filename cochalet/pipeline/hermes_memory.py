#!/usr/bin/env python3
"""
hermes_memory.py -- Persistent Knowledge Memory for COS Pipeline
Priority 4: Teach Hermes memory skills.

Structured memory store with read/write/search/recall capabilities.
Memory is stored as JSON docs in SQLite (same DB pattern as ledger).

Tables:
  memory_store: id, key, category, content, source, created_at, updated_at, ttl_days
  memory_index: id, memory_id, term (full-text search via LIKE)

Categories: canon, competitor, market, financial, legal, technical, persona, reference

Usage:
  from hermes_memory import MemoryStore
  mem = MemoryStore()
  mem.remember("cochalet_adr", "financial", "ADR is $771 per night", source="canon-v3.1")
  mem.recall("ADR")  # -> list of matching memories
  mem.forget("cochalet_adr")  # -> delete
  mem.list_category("financial")  # -> all financial memories

CLI:
  python3 hermes_memory.py remember <key> <category> <content> [--source X]
  python3 hermes_memory.py recall <query>
  python3 hermes_memory.py forget <key>
  python3 hermes_memory.py list [category]
  python3 hermes_memory.py stats
  python3 hermes_memory.py seed  # Load canon facts
"""

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

DB_PATH = Path('/var/lib/hermes/memory/hermes_memory.db')

CATEGORIES = [
    'canon', 'competitor', 'market', 'financial',
    'legal', 'technical', 'persona', 'reference',
]

# Canon seed data — the foundational facts every agent must know
CANON_SEEDS = [
    ("founder", "canon", "Justin Kausel is the Founder & CEO of CoChalet. 66+ months building, $425K sweat equity, 25 financial model iterations. Lost $120K over 3 years on Airbnb with zero ownership — built CoChalet as the solution.", "canon-v3.1"),
    ("product_definition", "canon", "CoChalet offers deeded co-ownership of luxury chalets in the Laurentians, Quebec. NOT timeshare. NOT fractional ownership. Owners hold real property title.", "canon-v3.1"),
    ("four_nevers", "canon", "FOUR NEVERS (zero tolerance): Never say 'timeshare' (use 'deeded co-ownership'). Never say 'fractional ownership' (use 'co-ownership'). Never say 'guaranteed returns' (use 'builds equity over time'). Never say 'Engine Room' (use 'internal operations').", "brand-voice-guard"),
    ("adr", "financial", "Average Daily Rate (ADR) is $771 per night.", "canon-v3.1"),
    ("fo_stake", "financial", "Fractional Owner stake is $112,300. Monthly payment is $2,634 ($759 P&I + $1,875 service fee).", "canon-v3.1"),
    ("cochalet_take", "financial", "CoChalet annual take is $28,200 (15.3% of revenue).", "canon-v3.1"),
    ("noi_margin", "financial", "NOI margin is 37.9%. DSCR is 1.95x.", "canon-v3.1"),
    ("flip_point", "financial", "Break-even (flip point) is at 45% occupancy.", "canon-v3.1"),
    ("ltv_cac", "financial", "LTV:CAC is 35.4:1 (referral) and 9.6:1 (paid). AOI is 44.4 (22x).", "canon-v3.1"),
    ("slogan_en", "canon", "English slogan: 'Use It. Own It. Love It.'", "brand-apr9"),
    ("slogan_fr", "canon", "French slogan: 'Arrivez et vivez'", "brand-apr9"),
    ("persona_pc", "persona", "PC (Property Candidate): Prospective buyer. Urban professional 35-55, dreams of chalet ownership but thinks it's out of reach. Messaging focuses on accessibility, real ownership, and lifestyle.", "persona-matrix"),
    ("persona_dw", "persona", "DW (Dream Weaver): Current co-owner. Already invested, experiencing the lifestyle. Messaging focuses on community, equity growth, and referral program.", "persona-matrix"),
    ("competitor_pacaso", "competitor", "Pacaso: US-based co-ownership company. Higher price point ($300K+), LLC structure (not deeded), focuses on luxury second homes. No Canadian operations.", "comp-intel"),
    ("competitor_ember", "competitor", "Ember: Canadian co-ownership. Similar model but different regions. Less operational history than CoChalet.", "comp-intel"),
    ("location", "canon", "Properties are in the Laurentians, Quebec, Canada. ~1 hour from Montreal. Four-season destination: skiing, hiking, lakes, fall foliage.", "canon-v3.1"),
    ("legal_status", "legal", "Securities classification pending. Need OSC/AMF legal opinion ($2-5K). Current model structured as real property co-ownership, not securities offering.", "legal-p0"),
    ("pipeline_models", "technical", "Pipeline uses 5 AI models: Opus 4.6 CLI ($0, director), Sonnet 4.6 CLI ($0, manager), Codex GPT-5.4 CLI ($0, specialist), Gemini 2.5 Flash (OpenRouter, $0.15-0.60/M), DeepSeek Chat (OpenRouter, $0.14-0.28/M).", "cos-audit-apr11"),
]


class MemoryStore:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_conn(self):
        conn = sqlite3.connect(str(self.db_path), timeout=5)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA busy_timeout=3000")
        return conn

    def _init_db(self):
        conn = self._get_conn()
        try:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS memory_store (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    category TEXT NOT NULL,
                    content TEXT NOT NULL,
                    source TEXT DEFAULT '',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    ttl_days INTEGER DEFAULT 0
                );
                CREATE INDEX IF NOT EXISTS idx_memory_category ON memory_store(category);
                CREATE INDEX IF NOT EXISTS idx_memory_key ON memory_store(key);

                CREATE TABLE IF NOT EXISTS memory_index (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    memory_id INTEGER NOT NULL,
                    term TEXT NOT NULL,
                    FOREIGN KEY (memory_id) REFERENCES memory_store(id) ON DELETE CASCADE
                );
                CREATE INDEX IF NOT EXISTS idx_memory_term ON memory_index(term);
            """)
            conn.commit()
        finally:
            conn.close()

    def _index_terms(self, conn, memory_id: int, content: str):
        """Extract and store searchable terms from content."""
        # Clean and tokenize
        import re
        words = re.findall(r'[a-zA-ZÀ-ÿ]{3,}', content.lower())
        unique_words = set(words)
        # Delete old terms
        conn.execute("DELETE FROM memory_index WHERE memory_id=?", (memory_id,))
        # Insert new terms
        for term in unique_words:
            conn.execute(
                "INSERT INTO memory_index (memory_id, term) VALUES (?, ?)",
                (memory_id, term)
            )

    def remember(self, key: str, category: str, content: str,
                 source: str = '', ttl_days: int = 0) -> dict:
        """Store or update a memory."""
        now = datetime.now(timezone.utc).isoformat()
        conn = self._get_conn()
        try:
            existing = conn.execute(
                "SELECT id FROM memory_store WHERE key=?", (key,)
            ).fetchone()

            if existing:
                conn.execute(
                    "UPDATE memory_store SET category=?, content=?, source=?, "
                    "updated_at=?, ttl_days=? WHERE key=?",
                    (category, content, source, now, ttl_days, key)
                )
                memory_id = existing['id']
                action = 'updated'
            else:
                cursor = conn.execute(
                    "INSERT INTO memory_store (key, category, content, source, "
                    "created_at, updated_at, ttl_days) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (key, category, content, source, now, now, ttl_days)
                )
                memory_id = cursor.lastrowid
                action = 'created'

            self._index_terms(conn, memory_id, f"{key} {category} {content}")
            conn.commit()
            return {'action': action, 'key': key, 'id': memory_id}
        finally:
            conn.close()

    def recall(self, query: str, limit: int = 10) -> list:
        """Search memories by query (matches key, content, and indexed terms)."""
        conn = self._get_conn()
        try:
            query_lower = query.lower().strip()
            # Multi-strategy search: exact key, LIKE content, indexed terms
            results = conn.execute("""
                SELECT DISTINCT m.key, m.category, m.content, m.source,
                       m.created_at, m.updated_at
                FROM memory_store m
                LEFT JOIN memory_index i ON m.id = i.memory_id
                WHERE m.key LIKE ? OR m.content LIKE ? OR i.term LIKE ?
                ORDER BY m.updated_at DESC
                LIMIT ?
            """, (
                f'%{query_lower}%',
                f'%{query_lower}%',
                f'%{query_lower}%',
                limit
            )).fetchall()

            return [dict(r) for r in results]
        finally:
            conn.close()

    def get(self, key: str) -> Optional[dict]:
        """Get a specific memory by key."""
        conn = self._get_conn()
        try:
            row = conn.execute(
                "SELECT * FROM memory_store WHERE key=?", (key,)
            ).fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def forget(self, key: str) -> bool:
        """Delete a memory by key."""
        conn = self._get_conn()
        try:
            row = conn.execute(
                "SELECT id FROM memory_store WHERE key=?", (key,)
            ).fetchone()
            if row:
                conn.execute("DELETE FROM memory_index WHERE memory_id=?", (row['id'],))
                conn.execute("DELETE FROM memory_store WHERE key=?", (key,))
                conn.commit()
                return True
            return False
        finally:
            conn.close()

    def list_category(self, category: str = None, limit: int = 50) -> list:
        """List memories, optionally filtered by category."""
        conn = self._get_conn()
        try:
            if category:
                rows = conn.execute(
                    "SELECT key, category, content, source, updated_at "
                    "FROM memory_store WHERE category=? ORDER BY updated_at DESC LIMIT ?",
                    (category, limit)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT key, category, content, source, updated_at "
                    "FROM memory_store ORDER BY updated_at DESC LIMIT ?",
                    (limit,)
                ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def stats(self) -> dict:
        """Memory store statistics."""
        conn = self._get_conn()
        try:
            total = conn.execute("SELECT COUNT(*) FROM memory_store").fetchone()[0]
            by_cat = conn.execute(
                "SELECT category, COUNT(*) as cnt FROM memory_store "
                "GROUP BY category ORDER BY cnt DESC"
            ).fetchall()
            terms = conn.execute("SELECT COUNT(*) FROM memory_index").fetchone()[0]
            return {
                'total_memories': total,
                'indexed_terms': terms,
                'by_category': {r['category']: r['cnt'] for r in by_cat},
            }
        finally:
            conn.close()

    def seed_canon(self) -> dict:
        """Seed the memory store with canonical CoChalet facts."""
        created = 0
        updated = 0
        for key, cat, content, source in CANON_SEEDS:
            result = self.remember(key, cat, content, source=source)
            if result['action'] == 'created':
                created += 1
            else:
                updated += 1
        return {'created': created, 'updated': updated, 'total': len(CANON_SEEDS)}

    def context_for_task(self, task: str, limit: int = 5) -> str:
        """Generate a context block for a pipeline task from relevant memories."""
        # Extract key terms from task
        import re
        terms = re.findall(r'[a-zA-ZÀ-ÿ]{4,}', task.lower())
        # Always include canon essentials
        results = set()
        # Search for task-relevant memories
        for term in terms[:10]:
            for mem in self.recall(term, limit=3):
                results.add((mem['key'], mem['content']))
        # Always include four nevers
        four_nevers = self.get('four_nevers')
        if four_nevers:
            results.add(('four_nevers', four_nevers['content']))

        if not results:
            return ""

        lines = ["## HERMES KNOWLEDGE CONTEXT"]
        for key, content in sorted(results)[:limit]:
            lines.append(f"- **{key}**: {content}")
        return "\n".join(lines)


# -- CLI ----------------------------------------------------------------
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Hermes Memory Store')
    sub = parser.add_subparsers(dest='command')

    p_remember = sub.add_parser('remember')
    p_remember.add_argument('key')
    p_remember.add_argument('category', choices=CATEGORIES)
    p_remember.add_argument('content')
    p_remember.add_argument('--source', default='')

    p_recall = sub.add_parser('recall')
    p_recall.add_argument('query')
    p_recall.add_argument('--limit', type=int, default=10)

    p_forget = sub.add_parser('forget')
    p_forget.add_argument('key')

    p_list = sub.add_parser('list')
    p_list.add_argument('category', nargs='?')

    sub.add_parser('stats')
    sub.add_parser('seed')

    p_context = sub.add_parser('context')
    p_context.add_argument('task')

    args = parser.parse_args()
    mem = MemoryStore()

    if args.command == 'remember':
        result = mem.remember(args.key, args.category, args.content, source=args.source)
        print(json.dumps(result, indent=2))
    elif args.command == 'recall':
        results = mem.recall(args.query, limit=args.limit)
        for r in results:
            print(f"  [{r['category']}] {r['key']}: {r['content'][:120]}")
        print(f"\n  {len(results)} results")
    elif args.command == 'forget':
        ok = mem.forget(args.key)
        print(f"{'Deleted' if ok else 'Not found'}: {args.key}")
    elif args.command == 'list':
        results = mem.list_category(args.category)
        for r in results:
            print(f"  [{r['category']}] {r['key']}: {r['content'][:100]}")
        print(f"\n  {len(results)} memories")
    elif args.command == 'stats':
        print(json.dumps(mem.stats(), indent=2))
    elif args.command == 'seed':
        result = mem.seed_canon()
        print(f"Seeded: {result['created']} created, {result['updated']} updated, {result['total']} total")
    elif args.command == 'context':
        ctx = mem.context_for_task(args.task)
        print(ctx if ctx else "(no relevant context found)")
    else:
        parser.print_help()
