# Dyslexia-Friendly Learning Material Converter

<p align="center">
  <img src="https://img.shields.io/badge/Skill-%23233-blueviolet" alt="Skill #233">
  <img src="https://img.shields.io/badge/Cluster-career--education-success" alt="Cluster: career-education">
  <img src="https://img.shields.io/badge/Status-production--ready-brightgreen" alt="Production ready">
  <img src="https://img.shields.io/badge/BDA%202023-compliant-informational" alt="BDA 2023 compliant">
  <img src="https://img.shields.io/badge/WCAG%202.1%20AA-passing-success" alt="WCAG 2.1 AA passing">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License: MIT">
</p>

<p align="center">
  <em>Automatically convert any learning material into a dyslexia-friendly format grounded in the latest neurocognitive research and BDA/IDA standards.</em>
</p>

---

## Table of Contents

- [Why this exists](#why-this-exists)
- [What it does](#what-it-does)
- [Research foundation](#research-foundation)
- [Architecture](#architecture)
- [Quick start](#quick-start)
- [Usage](#usage)
- [File map](#file-map)
- [Quality gates](#quality-gates)
- [Test results](#test-results)
- [Knowledge pipeline](#knowledge-pipeline)
- [Cluster integration](#cluster-integration)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Citation](#citation)

---

## Why this exists

Dyslexia affects **10–15% of the global population**—the most common specific learning difficulty. Despite decades of research, the majority of educational, corporate, and government documents are still produced in formats that actively impede dyslexic readers:

- Dense, justified text with uneven word spacing
- Serif fonts at small sizes
- Tight line spacing and cramped letters
- Long compound sentences and low-frequency vocabulary
- Pure black-on-white contrast that triggers visual stress

Manually reformatting materials is slow and requires specialist knowledge of the British Dyslexia Association (BDA) Style Guide, International Dyslexia Association (IDA) standards, WCAG 2.1 text-presentation criteria, and Universal Design for Learning (UDL).

This skill automates the entire conversion pipeline—from learner-profile intake through typography/layout transformation and sentence-level simplification to a scored accessibility report—so teachers, L&D teams, parents, and content creators can produce research-backed, dyslexia-friendly materials in minutes, not hours.

---

## What it does

Given a learner profile and a source text, the skill returns a complete conversion report containing:

1. **Typography specification sheet** — font, size, spacing, colour, margins, contrast ratio, and platform-specific implementation instructions
2. **Converted text** — simplified sentences, chunked paragraphs, explicit lists, glossary entries
3. **Before/after accessibility scorecard** — BDA 2023 checklist, WCAG 2.1 AA compliance, Flesch-Kincaid metrics
4. **Prioritised improvement roadmap** — remaining issues and research-backed tips
5. **Glossary** — definitions for retained technical / low-frequency terms

The pipeline respects safety-critical domains (legal, medical, fire-safety) and never alters meaning where accuracy is essential.

---

## Research foundation

Every numeric target and design decision is traceable to peer-reviewed research or authoritative guidelines:

| Standard / Study | Key finding | How it is used |
|------------------|-------------|----------------|
| **BDA Style Guide (2023)** | Sans-serif fonts, 1.5x line spacing, left-aligned ragged-right text, cream/yellow/blue backgrounds | Primary typography standard |
| **Rello & Baeza-Yates (2013)** | Arial, Verdana, Helvetica outperform serif fonts for dyslexic readers | Font selection logic |
| **Zorzi et al. (2012)** | Extra letter spacing improves reading speed and accuracy | `letter-spacing: +0.35em` |
| **Wilkins et al. (2004)** | ~20% of dyslexic readers benefit from coloured overlays | Background-colour advisory logic |
| **Wolf & Bowers (1999)** | Double-deficit hypothesis: phonological + naming-speed deficits | Subtype classification |
| **Shaywitz & Shaywitz (2005)** | Phonological deficit theory and left-hemisphere underactivation | Vocabulary simplification rationale |
| **WCAG 2.1 SC 1.4.3 / 1.4.12** | Contrast ≥ 4.5:1; line height ≥ 1.5x; letter spacing ≥ 0.12em | Accessibility scoring gates |
| **CAST UDL 2.2** | Multiple means of representation, action, and engagement | Structural aids and TTS advisory |

The full bibliography lives in [`SECOND-KNOWLEDGE-BRAIN.md`](./SECOND-KNOWLEDGE-BRAIN.md).

---

## Architecture

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    dyslexia-learning-material-converter                    │
│                              (main harness)                                  │
└───────────────────────────────┬────────────────────────────────────────────┘
                                │
        ┌───────────────────────▼────────────────────────┐
        │        STAGE 1: INTAKE                         │
        │    [sub-profile-intake]                        │
        │  age • subtype • severity • font • overlay     │
        │  reading context • output medium               │
        └───────────────────────┬────────────────────────┘
                                │
        ┌───────────────────────▼────────────────────────┐
        │        STAGE 2: TEXT ANALYSIS                  │
        │     [sub-text-analyzer]                        │
        │  Flesch-Kincaid • sentence length •            │
        │  low-frequency words • passive voice           │
        └───────────────────────┬────────────────────────┘
                                │
        ┌───────────────────────▼────────────────────────┐
        │      STAGE 3: TYPOGRAPHY & LAYOUT              │
        │   [sub-font-layout-converter]                  │
        │  font • size • spacing • colour • contrast     │
        └───────────────────────┬────────────────────────┘
                                │
        ┌───────────────────────▼────────────────────────┐
        │       STAGE 4: SENTENCE REWRITE                │
        │          [offline engine + LLM polish]           │
        │  split • substitute • chunk • bullet • active  │
        └───────────────────────┬────────────────────────┘
                                │
        ┌───────────────────────▼────────────────────────┐
        │      STAGE 5: ACCESSIBILITY SCORE              │
        │      [sub-readability-scorer]                    │
        │  BDA checklist • WCAG 1.4.x • grade rubric     │
        └───────────────────────┬────────────────────────┘
                                │
        ┌───────────────────────▼────────────────────────┐
        │         STAGE 6: FINAL OUTPUT                  │
        │    converted text • spec • scorecard • roadmap │
        └────────────────────────────────────────────────┘
```

### Two execution modes

| Mode | When to use | Entry point |
|------|-------------|-------------|
| **Claude Code skill** | Conversational, single-document conversion | `skills/main.md` |
| **Offline Python core** | Batch processing, CI/CD, reproducible scoring | `tools/dyslexia_converter.py` + `tools/test_harness.py` |

---

## Quick start

### 1. Clone the repository

```bash
git clone https://github.com/dungnotnull/dyslexia-learning-material-converter.git
cd dyslexia-learning-material-converter
```

### 2. Install dependencies

```bash
pip install textstat nltk langdetect wordfreq
python -m nltk.downloader punkt
```

Optional, for the knowledge crawler:

```bash
pip install crawl4ai beautifulsoup4 lxml requests python-dateutil
```

### 3. Run the validation harness

```bash
python tools/test_harness.py
```

You should see:

```
Summary: 7/7 scenarios passed
```

---

## Usage

### As a Claude Code skill

1. Copy the `skills/` directory into your Codex / Claude Code skill path.
2. Invoke `/dyslexia-learning-material-converter`.
3. Answer the 7 intake questions (or pre-fill them in your request).
4. Paste or upload the source text.
5. Receive the 5-section conversion report.

### As a Python library

```python
import sys
sys.path.insert(0, "tools")
from dyslexia_converter import (
    analyse_text,
    convert_text,
    generate_typography_spec,
    score_accessibility,
)

profile = {
    "age_band": "8-11",
    "dyslexia_subtype": "phonological",
    "severity": "moderate",
    "preferred_font": "Arial",
    "overlay_colour_hex": "#FAFAD2",
    "reading_context": "classroom",
    "output_medium": "print",
    "fk_reading_ease_target": 60,
    "max_sentence_length_words": 12,
}

text = """Photosynthesis is the process by which green plants utilise sunlight,
water, and carbon dioxide to manufacture glucose, which subsequently provides the
energy necessary for the organism's biological functioning."""

analysis = analyse_text(text)
converted = convert_text(text, profile)
spec = generate_typography_spec(profile)
score = score_accessibility(text, converted["converted_text"], spec, profile)

print("Original FKRE:", analysis["fkre"])
print("Converted FKRE:", converted["converted_analysis"]["fkre"])
print("BDA gates passed:", score["bda_pass_count"], "/ 14")
print("WCAG AA gates passed:", score["wcag_aa_pass_count"], "/ 3")
print("Grade:", score["original_grade"], "→", score["converted_grade"])
```

### Update the knowledge brain

```bash
python tools/knowledge_updater.py --brain SECOND-KNOWLEDGE-BRAIN.md --max-entries 20
```

Add `--dry-run` to preview what would be appended without writing.

---

## File map

| Path | Purpose |
|------|---------|
| [`skills/main.md`](./skills/main.md) | Main harness: 6-stage workflow, quality gates, final report template |
| [`skills/sub-profile-intake.md`](./skills/sub-profile-intake.md) | Learner profile intake with defaults and subtype logic |
| [`skills/sub-text-analyzer.md`](./skills/sub-text-analyzer.md) | Text analysis: FKRE, sentence length, vocabulary, passive voice |
| [`skills/sub-font-layout-converter.md`](./skills/sub-font-layout-converter.md) | BDA/IDA typography specification generator |
| [`skills/sub-readability-scorer.md`](./skills/sub-readability-scorer.md) | BDA/WCAG scoring and grade rubric |
| [`tools/dyslexia_converter.py`](./tools/dyslexia_converter.py) | Deterministic offline core engine |
| [`tools/test_harness.py`](./tools/test_harness.py) | Reference scenario validation |
| [`tools/knowledge_updater.py`](./tools/knowledge_updater.py) | Automated research crawler with optional crawl4ai |
| [`tools/data/`](./tools/data/) | High-frequency word lists, synonym map, helper lists |
| [`SECOND-KNOWLEDGE-BRAIN.md`](./SECOND-KNOWLEDGE-BRAIN.md) | Self-improving research knowledge base |
| [`PROJECT-detail.md`](./PROJECT-detail.md) | Full technical specification |
| [`PROJECT-DEVELOPMENT-PHASE-TRACKING.md`](./PROJECT-DEVELOPMENT-PHASE-TRACKING.md) | Phase-by-phase build roadmap |
| [`tests/test-scenarios.md`](./tests/test-scenarios.md) | Reference scenarios and execution report |
| [`tests/test-results.md`](./tests/test-results.md) | Detailed per-scenario scorecards |
| [`progression.json`](./progression.json) | Cluster completion tracker |

---

## Quality gates

Before any output is shown, every mandatory gate must pass:

| Gate | Criterion | Threshold |
|------|-----------|-----------|
| BDA-1 | Font on approved list | Arial / Verdana / OpenDyslexic / etc. |
| BDA-2 | Font size | ≥ 12pt adult, ≥ 14pt child |
| BDA-3 | Line spacing | ≥ 1.5x (2.0x for severe) |
| BDA-4 | Text alignment | Left-aligned only |
| BDA-5 | Paragraph length | ≤ 4 sentences |
| BDA-6 | ALL-CAPS passages | None > 3 words |
| BDA-7–B14 | Spacing, colour, headers, lists, letter spacing | Per BDA 2023 |
| WCAG-1 | Contrast ratio | ≥ 4.5:1 (SC 1.4.3) |
| WCAG-2 | Resize text | 200% zoom without loss (SC 1.4.4) |
| WCAG-3 | Text spacing | Per SC 1.4.12 |
| FK-1 | Flesch-Kincaid Reading Ease | ≥ target (60–70 depending on severity) |
| FK-2 | Average sentence length | ≤ target (10–15 words depending on severity) |

If a gate fails, the harness attempts an automatic fix (e.g., increase font size, change background colour, re-chunk paragraphs) and re-scores. The loop runs a maximum of two iterations.

---

## Test results

The offline validation harness runs seven representative scenarios:

| # | Scenario | FKRE before | FKRE after | ASL before | ASL after | Grade | Verdict |
|---|----------|-------------|------------|------------|-----------|-------|---------|
| 1 | Year 4 science worksheet | -5.7 | 71.7 | 31.0 | 9.8 | F → A | ✅ PASS |
| 2 | Adult legal contract | -44.7 | 72.0 | 114.0 | 11.2 | F → A | ✅ PASS |
| 3 | Corporate employee handbook | 31.0 | 73.1 | 19.6 | 12.8 | F → A | ✅ PASS |
| 4 | E-learning fire-safety script | 2.1 | 71.0 | 19.8 | 7.6 | F → A | ✅ PASS |
| 5 | Audit of existing "dyslexia-friendly" doc | 30.3 | 67.2 | 16.8 | 9.0 | F → B | ✅ PASS |
| 6 | Medical patient information leaflet | 34.3 | 77.1 | 16.7 | 9.1 | F → A | ✅ PASS |
| 7 | Multilingual handout (English + Welsh) | 75.7 | 78.6 | 13.2 | 9.0 | F → A | ✅ PASS |

**Summary: 7/7 scenarios passed all quality gates.**

Full details: [`tests/test-results.md`](./tests/test-results.md)

---

## Knowledge pipeline

[`tools/knowledge_updater.py`](./tools/knowledge_updater.py) keeps the skill current by crawling:

- **PubMed** via NCBI E-utilities
- **ArXiv** cs.CL preprints
- **Dyslexia** (Wiley Online Library)
- **Annals of Dyslexia** (Springer)
- **Journal of Learning Disabilities** (Sage)

It scores each entry by **recency (50%) + keyword relevance (50%)**, deduplicates using SHA-256 hashes of DOI/URL, and appends qualifying papers to [`SECOND-KNOWLEDGE-BRAIN.md`](./SECOND-KNOWLEDGE-BRAIN.md). The script degrades gracefully: if `crawl4ai` is installed it uses it for JavaScript-heavy sites; otherwise it falls back to `requests` + `BeautifulSoup`.

Recommended schedule: run weekly (e.g., cron at Sunday 02:00 UTC).

---

## Cluster integration

This skill belongs to the **career-education** cluster. Several components are designed for reuse:

| Component | Reuse opportunity |
|-----------|-------------------|
| `sub-profile-intake` | Generalise the learner-profile JSON schema for ADHD, ESL, low-vision, mature-learner cohorts |
| `sub-text-analyzer` | Feed the scoring engine of any text-optimisation skill |
| `sub-readability-scorer` | Extract as a shared `sub-scoring-engine` for accessibility auditing |
| `sub-font-layout-converter` | Reuse for document-remediation skills (visual impairment, PDF accessibility) |

Natural skill pairings:

- **CV / resume skills** — apply the same font/spacing rules to job-application documents
- **E-learning script skills** — run sentence simplification before LMS upload
- **Interview-prep skills** — convert dense legal/policy passages using the legal-text adjusted threshold

No circular dependencies are introduced; this skill only reads its own knowledge brain and writes its own deliverables.

---

## Roadmap

This repository represents the **v1.0 production release**. Future enhancements may include:

- [ ] Multilingual simplification support beyond English
- [ ] Integration with a dependency-parsing library for richer syntactic simplification
- [ ] Web UI for drag-and-drop document conversion
- [ ] Export plugins for Microsoft Word, Google Docs, and PDF
- [ ] Fine-grained user preference learning from feedback

---

## Contributing

Contributions are welcome. Priority areas:

1. Expand `tools/data/synonyms.json` for domain-specific jargon
2. Improve sentence-splitting heuristics with linguistically informed rules
3. Add more publisher crawlers to `tools/knowledge_updater.py`
4. Translate documentation and add non-English test scenarios

Please open an issue before large changes, and ensure `python tools/test_harness.py` still reports **7/7 scenarios passed**.

---

## License

MIT License — see [`LICENSE`](./LICENSE) (add a standard MIT `LICENSE` file to the repo if you want it to be fully open-source compliant).

---

## Citation

If you use this skill in research or education, please cite:

```bibtex
@software{dyslexia_learning_material_converter,
  author = {Dungnotnull},
  title = {Dyslexia-Friendly Learning Material Converter},
  year = {2026},
  url = {https://github.com/dungnotnull/dyslexia-learning-material-converter}
}
```

---

<p align="center">
  <strong>Built for inclusion. Research-backed. Production-ready.</strong>
</p>
