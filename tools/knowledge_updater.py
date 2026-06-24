#!/usr/bin/env python3
"""
knowledge_updater.py — Dyslexia-Friendly Learning Material Converter (Skill #233)
===================================================================================
Crawls PubMed, Dyslexia journal (Wiley), Annals of Dyslexia (Springer), and
Journal of Learning Disabilities (Sage) for new research on dyslexia typography,
font effectiveness, visual stress, text simplification, and UDL accessibility.

Scores each entry by recency + relevance, deduplicates by DOI/URL hash, and
appends qualifying new entries to SECOND-KNOWLEDGE-BRAIN.md.

Usage:
    python knowledge_updater.py
    python knowledge_updater.py --brain ../SECOND-KNOWLEDGE-BRAIN.md --max-entries 20
    python knowledge_updater.py --dry-run   # Show what would be appended without writing

Requirements:
    pip install crawl4ai requests beautifulsoup4 lxml python-dateutil

Schedule: Run weekly (e.g., cron: 0 2 * * 0)
"""

import argparse
import hashlib
import json
import logging
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.parse import urlencode, urljoin, quote_plus

import requests
from bs4 import BeautifulSoup
from dateutil import parser as dateparser

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DEFAULT_BRAIN_PATH = Path(__file__).parent.parent / "SECOND-KNOWLEDGE-BRAIN.md"

SEARCH_CONFIG = {
    "pubmed": {
        "base_url": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/",
        "search_terms": [
            "dyslexia font readability",
            "dyslexia letter spacing reading",
            "visual stress dyslexia overlay intervention",
            "OpenDyslexic font effectiveness dyslexia",
            "text simplification dyslexia accessibility",
            "Universal Design for Learning reading disability",
            "dyslexia typography accommodation",
            "phonological dyslexia intervention reading",
            "dyslexia sentence length comprehension",
        ],
        "max_results_per_query": 10,
        "retmax": 10,
        "sort": "pub_date",
        "datetype": "pdat",
        "reldate": 730,  # Papers from last 2 years
    },
    "arxiv": {
        "base_url": "https://export.arxiv.org/api/query",
        "search_terms": [
            "text simplification accessibility dyslexia",
            "readability NLP learning disabilities",
            "automatic text adaptation dyslexia",
        ],
        "max_results": 10,
    },
    "wiley": {
        "queries": ["dyslexia", "reading disability", "visual stress"],
        "max_results": 10,
    },
    "springer": {
        "queries": ["dyslexia", "phonological dyslexia", "reading intervention"],
        "max_results": 10,
    },
    "sage": {
        "queries": ["dyslexia", "learning disabilities reading", "text accessibility"],
        "max_results": 10,
    },
}

RELEVANCE_KEYWORDS = [
    "dyslexia", "dyslexic", "reading disability", "specific learning disability",
    "font", "typography", "typeface", "OpenDyslexic", "Arial", "Verdana",
    "letter spacing", "line spacing", "line height", "visual stress",
    "colored overlay", "colour overlay", "Irlen", "meares",
    "phonological", "phonological deficit", "phonological awareness",
    "magnocellular", "saccade", "eye tracking", "reading speed",
    "text simplification", "sentence simplification", "readability",
    "Flesch-Kincaid", "accessibility", "Universal Design for Learning", "UDL",
    "Orton-Gillingham", "BDA", "IDA", "learning difficulty",
    "working memory", "crowding effect", "word recognition",
]

SCORE_WEIGHTS = {
    "recency": 0.5,    # 1.0 = published today; decays by 1/365 per day old
    "relevance": 0.5,  # keyword match fraction
}

MIN_SCORE_THRESHOLD = 0.30
MAX_ENTRIES_DEFAULT = 20

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("knowledge_updater")


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def compute_doi_hash(doi: Optional[str], url: Optional[str]) -> str:
    """Compute a stable SHA-256 hash for deduplication based on DOI or URL."""
    identifier = doi.strip().lower() if doi else (url.strip().lower() if url else "")
    return hashlib.sha256(identifier.encode("utf-8")).hexdigest()


def extract_existing_hashes(brain_path: Path) -> set:
    """Extract all DOI/URL hashes already present in SECOND-KNOWLEDGE-BRAIN.md."""
    if not brain_path.exists():
        log.warning(f"Brain file not found: {brain_path}")
        return set()

    content = brain_path.read_text(encoding="utf-8")
    existing_hashes = set()

    # Extract DOIs from markdown table rows (pattern: https://doi.org/... or doi.org/...)
    doi_pattern = re.compile(r"https?://(?:dx\.)?doi\.org/[\S]+", re.IGNORECASE)
    url_pattern = re.compile(r"https?://\S+", re.IGNORECASE)

    for match in doi_pattern.finditer(content):
        url = match.group(0).rstrip(").,|")
        existing_hashes.add(compute_doi_hash(url, None))

    for match in url_pattern.finditer(content):
        url = match.group(0).rstrip(").,|")
        if "doi.org" not in url:
            existing_hashes.add(compute_doi_hash(None, url))

    log.info(f"Found {len(existing_hashes)} existing entries in knowledge brain")
    return existing_hashes


def compute_recency_score(pub_date_str: Optional[str]) -> float:
    """Compute a recency score [0.0, 1.0] based on days since publication."""
    if not pub_date_str:
        return 0.1  # Unknown date — assign low baseline
    try:
        pub_date = dateparser.parse(pub_date_str, default=datetime(2000, 1, 1))
        pub_date = pub_date.replace(tzinfo=timezone.utc) if pub_date.tzinfo is None else pub_date
        now = datetime.now(timezone.utc)
        days_old = (now - pub_date).days
        # Decay: 1.0 = today; 0.5 = 365 days ago; 0.0 = ~730 days ago
        score = max(0.0, 1.0 - (days_old / 730.0))
        return round(score, 4)
    except Exception:
        return 0.1


def compute_relevance_score(title: str, abstract: str) -> float:
    """Compute a relevance score [0.0, 1.0] based on keyword match density."""
    text = (title + " " + abstract).lower()
    matched = sum(1 for kw in RELEVANCE_KEYWORDS if kw.lower() in text)
    score = min(1.0, matched / max(1, len(RELEVANCE_KEYWORDS) * 0.3))
    return round(score, 4)


def compute_composite_score(recency: float, relevance: float) -> float:
    """Compute weighted composite score."""
    return round(
        SCORE_WEIGHTS["recency"] * recency + SCORE_WEIGHTS["relevance"] * relevance,
        4,
    )


def format_authors_short(authors: list) -> str:
    """Format authors list as 'FirstAuthor et al.' or 'A & B' for ≤ 2 authors."""
    if not authors:
        return "Unknown"
    if len(authors) == 1:
        return authors[0]
    if len(authors) == 2:
        return f"{authors[0]} & {authors[1]}"
    return f"{authors[0]} et al."


def format_doi_link(doi: Optional[str], url: Optional[str]) -> str:
    """Format DOI as a markdown link, or fall back to URL."""
    if doi:
        clean_doi = doi.lstrip("https://doi.org/").lstrip("https://dx.doi.org/")
        return f"https://doi.org/{clean_doi}"
    return url or "No URL"


def build_table_row(entry: dict, row_id: int) -> str:
    """Build a markdown table row for SECOND-KNOWLEDGE-BRAIN.md."""
    authors_short = format_authors_short(entry.get("authors", []))
    doi_link = format_doi_link(entry.get("doi"), entry.get("url"))
    title = entry.get("title", "Unknown title")[:120]  # Truncate very long titles
    year = entry.get("year", "N/A")
    journal = entry.get("journal", "N/A")[:60]
    relevance_note = entry.get("relevance_note", "Dyslexia typography/accessibility research")

    return f"| {row_id} | {title} | {authors_short} | {year} | {journal} | {doi_link} | {relevance_note} |"


# ---------------------------------------------------------------------------
# PubMed crawler
# ---------------------------------------------------------------------------

class PubMedCrawler:
    """Fetch papers from PubMed via NCBI E-utilities API."""

    def __init__(self, config: dict):
        self.config = config
        self.base_url = config["base_url"]
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "DyslexiaKnowledgeUpdater/1.0 (skill-233; educational research tool)"
        })

    def search_papers(self, query: str, max_results: int = 10) -> list:
        """Search PubMed and return a list of paper dicts."""
        papers = []

        # Step 1: ESearch — get PMIDs
        search_params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "sort": self.config.get("sort", "pub_date"),
            "retmode": "json",
            "datetype": self.config.get("datetype", "pdat"),
            "reldate": self.config.get("reldate", 730),
        }
        try:
            response = self.session.get(
                f"{self.base_url}esearch.fcgi",
                params=search_params,
                timeout=15,
            )
            response.raise_for_status()
            search_data = response.json()
            pmids = search_data.get("esearchresult", {}).get("idlist", [])
            log.info(f"PubMed: '{query}' → {len(pmids)} PMIDs")
        except Exception as e:
            log.warning(f"PubMed ESearch failed for '{query}': {e}")
            return []

        if not pmids:
            return []

        # Step 2: EFetch — get paper details
        time.sleep(0.4)  # Respect NCBI rate limit (3 requests/second without API key)
        fetch_params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "xml",
            "rettype": "abstract",
        }
        try:
            response = self.session.get(
                f"{self.base_url}efetch.fcgi",
                params=fetch_params,
                timeout=30,
            )
            response.raise_for_status()
            papers = self._parse_pubmed_xml(response.text)
        except Exception as e:
            log.warning(f"PubMed EFetch failed: {e}")

        return papers

    def _parse_pubmed_xml(self, xml_text: str) -> list:
        """Parse PubMed XML response into structured paper dicts."""
        soup = BeautifulSoup(xml_text, "lxml-xml")
        papers = []

        for article in soup.find_all("PubmedArticle"):
            try:
                # Title
                title_el = article.find("ArticleTitle")
                title = title_el.get_text(strip=True) if title_el else "Unknown"

                # Authors
                authors = []
                for author in article.find_all("Author"):
                    last = author.find("LastName")
                    first = author.find("ForeName")
                    if last:
                        name = last.get_text()
                        if first:
                            name += f" {first.get_text()[0]}."
                        authors.append(name)

                # Year
                year_el = article.find("PubDate")
                year = "N/A"
                if year_el:
                    year_tag = year_el.find("Year")
                    medline_date = year_el.find("MedlineDate")
                    if year_tag:
                        year = year_tag.get_text()
                    elif medline_date:
                        year = medline_date.get_text()[:4]

                # Journal
                journal_el = article.find("ISOAbbreviation") or article.find("Title")
                journal = journal_el.get_text(strip=True) if journal_el else "N/A"

                # DOI
                doi = None
                for id_el in article.find_all("ArticleId"):
                    if id_el.get("IdType") == "doi":
                        doi = id_el.get_text(strip=True)
                        break

                # PMID for URL fallback
                pmid_el = article.find("PMID")
                pmid = pmid_el.get_text() if pmid_el else None
                url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else None

                # Abstract
                abstract_parts = []
                for ab_text in article.find_all("AbstractText"):
                    abstract_parts.append(ab_text.get_text(strip=True))
                abstract = " ".join(abstract_parts)[:500]

                # Pub date string for recency
                pub_date_str = f"{year}-01-01"

                papers.append({
                    "title": title,
                    "authors": authors,
                    "year": year,
                    "journal": journal,
                    "doi": doi,
                    "url": url,
                    "abstract": abstract,
                    "pub_date_str": pub_date_str,
                    "source": "PubMed",
                })
            except Exception as e:
                log.debug(f"Could not parse PubMed article: {e}")
                continue

        return papers

    def fetch_all(self) -> list:
        """Run all configured search queries and return deduplicated papers."""
        all_papers = []
        seen_titles = set()

        for query in self.config["search_terms"]:
            papers = self.search_papers(query, self.config["max_results_per_query"])
            for paper in papers:
                title_key = paper["title"].lower()[:80]
                if title_key not in seen_titles:
                    seen_titles.add(title_key)
                    all_papers.append(paper)
            time.sleep(0.4)

        log.info(f"PubMed: {len(all_papers)} unique papers fetched")
        return all_papers


# ---------------------------------------------------------------------------
# ArXiv crawler
# ---------------------------------------------------------------------------

class ArXivCrawler:
    """Fetch papers from ArXiv cs.CL / cs.AI on text simplification + dyslexia."""

    def __init__(self, config: dict):
        self.config = config
        self.base_url = config["base_url"]
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "DyslexiaKnowledgeUpdater/1.0 (skill-233; educational research tool)"
        })

    def fetch_all(self) -> list:
        """Fetch papers from ArXiv for all configured search terms."""
        all_papers = []
        seen_ids = set()

        for query in self.config["search_terms"]:
            params = {
                "search_query": f"all:{quote_plus(query)}",
                "start": 0,
                "max_results": self.config["max_results"],
                "sortBy": "submittedDate",
                "sortOrder": "descending",
            }
            try:
                response = self.session.get(self.base_url, params=params, timeout=20)
                response.raise_for_status()
                papers = self._parse_arxiv_atom(response.text)
                for paper in papers:
                    arxiv_id = paper.get("arxiv_id", "")
                    if arxiv_id and arxiv_id not in seen_ids:
                        seen_ids.add(arxiv_id)
                        all_papers.append(paper)
                log.info(f"ArXiv: '{query}' → {len(papers)} results")
            except Exception as e:
                log.warning(f"ArXiv fetch failed for '{query}': {e}")
            time.sleep(1.0)

        log.info(f"ArXiv: {len(all_papers)} unique papers fetched")
        return all_papers

    def _parse_arxiv_atom(self, xml_text: str) -> list:
        """Parse ArXiv Atom feed XML."""
        soup = BeautifulSoup(xml_text, "lxml-xml")
        papers = []

        for entry in soup.find_all("entry"):
            try:
                title_el = entry.find("title")
                title = title_el.get_text(strip=True) if title_el else "Unknown"

                authors = [a.find("name").get_text() for a in entry.find_all("author") if a.find("name")]

                published_el = entry.find("published")
                pub_str = published_el.get_text()[:10] if published_el else "2020-01-01"
                year = pub_str[:4]

                id_el = entry.find("id")
                arxiv_url = id_el.get_text(strip=True) if id_el else None
                arxiv_id = arxiv_url.split("/abs/")[-1] if arxiv_url else None

                summary_el = entry.find("summary")
                abstract = summary_el.get_text(strip=True)[:500] if summary_el else ""

                papers.append({
                    "title": title,
                    "authors": authors,
                    "year": year,
                    "journal": "ArXiv",
                    "doi": None,
                    "url": arxiv_url,
                    "arxiv_id": arxiv_id,
                    "abstract": abstract,
                    "pub_date_str": pub_str,
                    "source": "ArXiv",
                })
            except Exception as e:
                log.debug(f"Could not parse ArXiv entry: {e}")
                continue

        return papers


# ---------------------------------------------------------------------------
# Scoring and filtering
# ---------------------------------------------------------------------------

def score_and_filter(papers: list, existing_hashes: set, min_score: float) -> list:
    """Score all papers, skip duplicates, return filtered and sorted list."""
    scored = []

    for paper in papers:
        # Deduplicate
        doi_hash = compute_doi_hash(paper.get("doi"), paper.get("url"))
        if doi_hash in existing_hashes:
            log.debug(f"SKIP (duplicate): {paper.get('title', '')[:60]}")
            continue

        # Score
        recency = compute_recency_score(paper.get("pub_date_str"))
        relevance = compute_relevance_score(
            paper.get("title", ""),
            paper.get("abstract", ""),
        )
        composite = compute_composite_score(recency, relevance)

        if composite < min_score:
            log.debug(f"SKIP (score {composite:.2f} < {min_score}): {paper.get('title', '')[:60]}")
            continue

        paper["_recency_score"] = recency
        paper["_relevance_score"] = relevance
        paper["_composite_score"] = composite
        paper["_doi_hash"] = doi_hash

        # Generate relevance note
        title_lower = paper.get("title", "").lower()
        abstract_lower = paper.get("abstract", "").lower()
        text = title_lower + " " + abstract_lower
        note_parts = []
        if any(kw in text for kw in ["font", "typeface", "typography", "opendyslexic"]):
            note_parts.append("font/typography research")
        if any(kw in text for kw in ["letter spacing", "line spacing", "crowding"]):
            note_parts.append("spacing intervention")
        if any(kw in text for kw in ["visual stress", "overlay", "irlen", "meares"]):
            note_parts.append("visual stress/overlay research")
        if any(kw in text for kw in ["simplif", "readability", "flesch"]):
            note_parts.append("text simplification/readability")
        if any(kw in text for kw in ["udl", "universal design", "accessibility"]):
            note_parts.append("UDL/accessibility research")
        if not note_parts:
            note_parts.append("dyslexia reading research")
        paper["relevance_note"] = "; ".join(note_parts[:2])

        scored.append(paper)
        log.info(f"INCLUDE (score {composite:.2f}): {paper.get('title', '')[:70]}")

    # Sort by composite score descending
    scored.sort(key=lambda p: p["_composite_score"], reverse=True)
    return scored


# ---------------------------------------------------------------------------
# Brain updater
# ---------------------------------------------------------------------------

def find_table_insert_position(content: str) -> int:
    """Find the line index of the last row in the Key Research Papers table."""
    lines = content.split("\n")
    last_table_row = -1
    in_papers_section = False

    for i, line in enumerate(lines):
        if "## 2. Key Research Papers" in line or "Key Research Papers" in line:
            in_papers_section = True
        if in_papers_section and line.startswith("| ") and not line.startswith("| #") and not line.startswith("| ---"):
            last_table_row = i
        if in_papers_section and last_table_row > 0 and line.strip() == "" and i > last_table_row + 2:
            break

    return last_table_row


def get_next_row_id(content: str) -> int:
    """Determine the next sequential row ID for the papers table."""
    pattern = re.compile(r"^\|\s*(\d+)\s*\|", re.MULTILINE)
    matches = [int(m.group(1)) for m in pattern.finditer(content)]
    return max(matches) + 1 if matches else 16


def append_to_brain(brain_path: Path, new_papers: list, dry_run: bool = False) -> int:
    """Append new paper rows to SECOND-KNOWLEDGE-BRAIN.md. Returns count appended."""
    if not new_papers:
        log.info("No new papers to append.")
        return 0

    content = brain_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    last_row_idx = find_table_insert_position(content)
    next_id = get_next_row_id(content)
    rows_to_insert = []

    for paper in new_papers:
        row = build_table_row(paper, next_id)
        rows_to_insert.append(row)
        next_id += 1

    if last_row_idx < 0:
        log.warning("Could not find Key Research Papers table — appending at end of file")
        new_content = content.rstrip() + "\n\n" + "\n".join(rows_to_insert) + "\n"
    else:
        lines.insert(last_row_idx + 1, "\n".join(rows_to_insert))
        new_content = "\n".join(lines)

    # Update Knowledge Update Log
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    sources = ", ".join(set(p.get("source", "Unknown") for p in new_papers))
    log_entry = f"| {today} | {sources} | {len(new_papers)} | 0 | Automated crawl (knowledge_updater.py) |"

    if "## 7. Knowledge Update Log" in new_content:
        # Find the last row in the update log table and insert after it
        log_section_idx = new_content.find("## 7. Knowledge Update Log")
        table_header_idx = new_content.find("| Date |", log_section_idx)
        if table_header_idx > 0:
            separator_idx = new_content.find("\n", table_header_idx)
            separator_end_idx = new_content.find("\n", separator_idx + 1)
            # Insert after the separator row
            new_content = (
                new_content[: separator_end_idx + 1]
                + log_entry + "\n"
                + new_content[separator_end_idx + 1:]
            )

    if dry_run:
        log.info(f"DRY RUN — would append {len(new_papers)} rows to {brain_path}")
        for paper in new_papers:
            print(f"  + [{paper['_composite_score']:.2f}] {paper['title'][:80]}")
        return len(new_papers)

    brain_path.write_text(new_content, encoding="utf-8")
    log.info(f"Appended {len(new_papers)} new entries to {brain_path}")
    return len(new_papers)




# ---------------------------------------------------------------------------
# Optional crawl4ai fetcher (used when available)
# ---------------------------------------------------------------------------

_CRAWL4AI_AVAILABLE = False
try:
    from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
    _CRAWL4AI_AVAILABLE = True
except Exception:
    pass


async def _crawl4ai_fetch_html(url: str, timeout: int = 30) -> Optional[str]:
    """Fetch page HTML using crawl4ai if installed; otherwise return None."""
    if not _CRAWL4AI_AVAILABLE:
        return None
    try:
        browser_config = BrowserConfig(headless=True, verbose=False)
        run_config = CrawlerRunConfig(cache_mode=CacheMode.DISABLED)
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(url=url, config=run_config)
            return result.html if result else None
    except Exception as e:
        log.warning(f"crawl4ai fetch failed for {url}: {e}")
        return None


def _fetch_html(url: str, timeout: int = 30) -> Optional[str]:
    """Fetch HTML using requests; fall back to crawl4ai if requests fails."""
    try:
        response = requests.get(url, timeout=timeout, headers={
            "User-Agent": "DyslexiaKnowledgeUpdater/1.0 (educational research tool)"
        })
        response.raise_for_status()
        return response.text
    except Exception as e:
        log.warning(f"requests fetch failed for {url}: {e}")

    if _CRAWL4AI_AVAILABLE:
        import asyncio
        try:
            return asyncio.get_event_loop().run_until_complete(_crawl4ai_fetch_html(url, timeout))
        except Exception:
            pass
    return None


# ---------------------------------------------------------------------------
# Publisher-specific crawlers
# ---------------------------------------------------------------------------

class WileyCrawler:
    """Crawl Dyslexia journal (Wiley Online Library) search results."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "DyslexiaKnowledgeUpdater/1.0 (educational research tool)"
        })

    def fetch_all(self, query: str = "dyslexia", max_results: int = 10) -> list:
        url = f"https://onlinelibrary.wiley.com/action/doSearch?AllField={quote_plus(query)}"
        html = _fetch_html(url)
        if not html:
            return []
        papers = self._parse_search(html)
        log.info(f"Wiley: '{query}' ? {len(papers)} papers")
        return papers[:max_results]

    def _parse_search(self, html: str) -> list:
        soup = BeautifulSoup(html, "html.parser")
        papers = []
        for item in soup.select(".items .item, .search-result, .article-item"):
            try:
                title_el = item.select_one(".item-title a, .article-title a, a[href*='/doi/']")
                if not title_el:
                    continue
                title = title_el.get_text(strip=True)
                href = title_el.get("href", "")
                doi_url = urljoin("https://onlinelibrary.wiley.com", href)
                authors = [a.get_text(strip=True) for a in item.select(".item-author, .author-name")]
                year_el = item.select_one(".item-year, .year")
                year = year_el.get_text(strip=True)[:4] if year_el else "N/A"
                journal_el = item.select_one(".item-journal, .journal")
                journal = journal_el.get_text(strip=True) if journal_el else "Dyslexia (Wiley)"
                abstract_el = item.select_one(".item-abstract, .abstract")
                abstract = abstract_el.get_text(strip=True)[:500] if abstract_el else ""
                papers.append({
                    "title": title,
                    "authors": authors,
                    "year": year,
                    "journal": journal,
                    "doi": None,
                    "url": doi_url,
                    "abstract": abstract,
                    "pub_date_str": f"{year}-01-01" if year.isdigit() else "2020-01-01",
                    "source": "Wiley",
                })
            except Exception:
                continue
        return papers


class SpringerCrawler:
    """Crawl Annals of Dyslexia (Springer) search results."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "DyslexiaKnowledgeUpdater/1.0 (educational research tool)"
        })

    def fetch_all(self, query: str = "dyslexia", max_results: int = 10) -> list:
        url = f"https://link.springer.com/search?query={quote_plus(query)}&facet-journal-id=11881"
        html = _fetch_html(url)
        if not html:
            return []
        papers = self._parse_search(html)
        log.info(f"Springer: '{query}' ? {len(papers)} papers")
        return papers[:max_results]

    def _parse_search(self, html: str) -> list:
        soup = BeautifulSoup(html, "html.parser")
        papers = []
        for item in soup.select(".title, .content-item, .result-item"):
            try:
                title_el = item if item.name == "a" else item.select_one("a[href*='/article/']")
                if not title_el:
                    continue
                title = title_el.get_text(strip=True)
                href = title_el.get("href", "")
                url = urljoin("https://link.springer.com", href)
                authors = [a.get_text(strip=True) for a in item.parent.select(".authors .author")] if item.parent else []
                year_el = item.parent.select_one(".year") if item.parent else None
                year = year_el.get_text(strip=True)[:4] if year_el else "N/A"
                papers.append({
                    "title": title,
                    "authors": authors,
                    "year": year,
                    "journal": "Annals of Dyslexia",
                    "doi": None,
                    "url": url,
                    "abstract": "",
                    "pub_date_str": f"{year}-01-01" if year.isdigit() else "2020-01-01",
                    "source": "Springer",
                })
            except Exception:
                continue
        return papers


class SageCrawler:
    """Crawl Journal of Learning Disabilities (Sage) search results."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "DyslexiaKnowledgeUpdater/1.0 (educational research tool)"
        })

    def fetch_all(self, query: str = "dyslexia", max_results: int = 10) -> list:
        url = f"https://journals.sagepub.com/action/doSearch?AllField={quote_plus(query)}&SeriesKey=ldx"
        html = _fetch_html(url)
        if not html:
            return []
        papers = self._parse_search(html)
        log.info(f"Sage: '{query}' ? {len(papers)} papers")
        return papers[:max_results]

    def _parse_search(self, html: str) -> list:
        soup = BeautifulSoup(html, "html.parser")
        papers = []
        for item in soup.select(".searchResultItem, .result"):
            try:
                title_el = item.select_one(".art_title a, a[href*='/doi/']")
                if not title_el:
                    continue
                title = title_el.get_text(strip=True)
                href = title_el.get("href", "")
                doi_url = urljoin("https://journals.sagepub.com", href)
                authors = [a.get_text(strip=True) for a in item.select(".authors a, .contrib")]
                year_el = item.select_one(".year")
                year = year_el.get_text(strip=True)[:4] if year_el else "N/A"
                papers.append({
                    "title": title,
                    "authors": authors,
                    "year": year,
                    "journal": "Journal of Learning Disabilities",
                    "doi": None,
                    "url": doi_url,
                    "abstract": "",
                    "pub_date_str": f"{year}-01-01" if year.isdigit() else "2020-01-01",
                    "source": "Sage",
                })
            except Exception:
                continue
        return papers


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Update SECOND-KNOWLEDGE-BRAIN.md with latest dyslexia research papers."
    )
    parser.add_argument(
        "--brain",
        type=Path,
        default=DEFAULT_BRAIN_PATH,
        help="Path to SECOND-KNOWLEDGE-BRAIN.md (default: ../SECOND-KNOWLEDGE-BRAIN.md)",
    )
    parser.add_argument(
        "--max-entries",
        type=int,
        default=MAX_ENTRIES_DEFAULT,
        help=f"Maximum new entries to append per run (default: {MAX_ENTRIES_DEFAULT})",
    )
    parser.add_argument(
        "--min-score",
        type=float,
        default=MIN_SCORE_THRESHOLD,
        help=f"Minimum composite score threshold (default: {MIN_SCORE_THRESHOLD})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be appended without writing to file",
    )
    parser.add_argument(
        "--sources",
        nargs="+",
        choices=["pubmed", "arxiv", "wiley", "springer", "sage", "all"],
        default=["all"],
        help="Which sources to crawl (default: all)",
    )
    args = parser.parse_args()

    brain_path = args.brain.resolve()
    if not brain_path.exists() and not args.dry_run:
        log.error(f"Brain file not found: {brain_path}")
        sys.exit(1)

    log.info(f"Starting knowledge update for Skill #233 — dyslexia-learning-material-converter")
    log.info(f"Brain file: {brain_path}")
    log.info(f"Max entries: {args.max_entries} | Min score: {args.min_score} | Dry run: {args.dry_run}")

    # Load existing hashes for deduplication
    existing_hashes = extract_existing_hashes(brain_path) if brain_path.exists() else set()

    # Collect papers from all sources
    all_papers = []
    sources = args.sources if "all" not in args.sources else list(SEARCH_CONFIG.keys())
    # Run publisher crawlers when "all" or individually requested
    publisher_map = {
        "wiley": (WileyCrawler, "wiley"),
        "springer": (SpringerCrawler, "springer"),
        "sage": (SageCrawler, "sage"),
    }
    for src in list(sources):
        if src in publisher_map:
            cls, key = publisher_map[src]
            log.info(f"Crawling {src}...")
            try:
                crawler = cls()
                papers = []
                for query in SEARCH_CONFIG[src].get("queries", ["dyslexia"]):
                    papers.extend(crawler.fetch_all(query, SEARCH_CONFIG[src].get("max_results", 10)))
                all_papers.extend(papers)
                log.info(f"{src}: {len(papers)} papers")
            except Exception as e:
                log.error(f"{src} crawler failed: {e}")
            sources.remove(src)

    if "pubmed" in sources:
        log.info("Crawling PubMed...")
        try:
            pubmed = PubMedCrawler(SEARCH_CONFIG["pubmed"])
            pubmed_papers = pubmed.fetch_all()
            all_papers.extend(pubmed_papers)
            log.info(f"PubMed raw: {len(pubmed_papers)} papers")
        except Exception as e:
            log.error(f"PubMed crawler failed: {e}")

    if "arxiv" in sources:
        log.info("Crawling ArXiv...")
        try:
            arxiv = ArXivCrawler(SEARCH_CONFIG["arxiv"])
            arxiv_papers = arxiv.fetch_all()
            all_papers.extend(arxiv_papers)
            log.info(f"ArXiv raw: {len(arxiv_papers)} papers")
        except Exception as e:
            log.error(f"ArXiv crawler failed: {e}")

    log.info(f"Total raw papers collected: {len(all_papers)}")

    # Score, deduplicate, filter
    filtered = score_and_filter(all_papers, existing_hashes, args.min_score)
    log.info(f"After dedup + scoring: {len(filtered)} qualifying papers")

    # Limit to max entries
    to_append = filtered[: args.max_entries]
    log.info(f"Will append: {len(to_append)} papers")

    # Append to brain
    count = append_to_brain(brain_path, to_append, dry_run=args.dry_run)

    log.info(f"Knowledge update complete. {count} new entries added.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
