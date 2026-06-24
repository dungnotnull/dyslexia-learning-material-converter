# CLAUDE.md — Skill: dyslexia-learning-material-converter

## Identity

- **Skill name:** dyslexia-learning-material-converter
- **Tagline:** Automatically convert and optimize any learning material into a dyslexia-friendly format grounded in the latest neurocognitive research and BDA/IDA standards.
- **Current phase:** Phase 0 — Research & Skill Architecture
- **Source idea:** #233
- **Cluster:** career-education

---

## Problem This Skill Solves

An estimated 10–15% of the global population has dyslexia, yet the vast majority of educational, corporate, and government documents are produced in formats that actively impede dyslexic readers: dense justified text, serif fonts at small sizes, tight line spacing, and long compound sentences. Manually reformatting materials is time-consuming and requires specialist knowledge of neurocognitive accessibility guidelines (BDA Style Guide, IDA standards, WCAG 1.4.x, UDL). This skill automates the entire conversion pipeline — from learner-profile intake through typography/layout transformation and sentence-level simplification to a scored accessibility report — enabling teachers, L&D teams, parents, and content creators to produce research-backed dyslexia-friendly materials in minutes, not hours.

---

## Harness Flow Summary

```
1. [sub-profile-intake]        Gather learner profile (age, dyslexia subtype, severity, font/overlay preferences, context)
2. [sub-text-analyzer]         Analyse input text: Flesch-Kincaid, sentence length, vocab complexity, structural issues
3. [sub-font-layout-converter] Apply BDA/IDA typography rules: font, size, spacing, colour, margins
4. [internal: sentence-rewrite] Simplify sentences, replace low-frequency words, chunk paragraphs, add headers/bullets
5. [sub-readability-scorer]    Score converted material vs BDA checklist + WCAG 1.4.x + Flesch-Kincaid ≥ 60
6. [main harness]              Synthesise final deliverable: converted material + before/after comparison + improvement roadmap
```

---

## Sub-Skills List

| File | Description |
|------|-------------|
| `skills/sub-profile-intake.md` | Collects learner age, dyslexia subtype (phonological/surface/mixed), severity, preferred font, colour overlay preference, and reading context |
| `skills/sub-text-analyzer.md` | Analyses source text for readability metrics, sentence complexity, vocabulary difficulty, and structural weaknesses |
| `skills/sub-font-layout-converter.md` | Outputs specific typography and layout recommendations aligned with BDA Style Guide and WCAG 1.4.x |
| `skills/sub-readability-scorer.md` | Scores both original and converted material; produces before/after comparison and compliance report |

---

## Tools Required

- **WebSearch** — fetch latest neuroscience research, BDA/IDA guideline updates, OpenDyslexic effectiveness studies
- **WebFetch** — retrieve full papers from PubMed, Dyslexia journal, Annals of Dyslexia, Journal of Learning Disabilities
- **Read** — read source documents and skill files
- **Write** — write converted materials, reports, and knowledge-brain updates

---

## Knowledge Sources

| Source | URL / Access |
|--------|-------------|
| British Dyslexia Association (BDA) | https://www.bdadyslexia.org.uk/advice/employers/creating-a-dyslexia-friendly-workplace/dyslexia-friendly-style-guide |
| International Dyslexia Association (IDA) | https://dyslexiaida.org/ |
| Dyslexia journal (Wiley) | https://onlinelibrary.wiley.com/journal/10990909 |
| Annals of Dyslexia | https://link.springer.com/journal/11881 |
| Journal of Learning Disabilities | https://journals.sagepub.com/home/ldx |
| PubMed — dyslexia + font/accessibility | https://pubmed.ncbi.nlm.nih.gov/?term=dyslexia+font+readability |
| ArXiv cs.CL — text simplification | https://arxiv.org/search/?searchtype=all&query=text+simplification+accessibility |
| WCAG 2.1 (W3C) | https://www.w3.org/TR/WCAG21/ |
| UDL Guidelines | https://udlguidelines.cast.org/ |
| Rose Report (UK Government) | https://webarchive.nationalarchives.gov.uk/+/http://www.standards.dcsf.gov.uk/phonics/report.pdf |

---

## Supporting Python Tools

| File | Purpose |
|------|---------|
| `tools/dyslexia_converter.py` | Deterministic text analysis, sentence simplification, BDA/WCAG scoring, and typography spec generation used by the test harness and available for production pipelines |
| `tools/test_harness.py` | Runs the 7 reference scenarios, validates quality gates, and writes `tests/test-results.md` |
| `tools/knowledge_updater.py` | crawl4ai-aware pipeline: fetches latest papers from PubMed, Dyslexia (Wiley), Annals of Dyslexia, JLD, and ArXiv; deduplicates by DOI/URL hash; appends scored entries to SECOND-KNOWLEDGE-BRAIN.md |
| `tools/data/high_frequency_words.txt` | Combined Dale-Chall + wordfreq 5K high-frequency word list for low-frequency detection |
| `tools/data/synonyms.json` | Production synonym map for low-frequency vocabulary substitution |
| `progression.json` | Local completion tracker for Skill #233 in the career-education cluster |

---

## Active Development Tasks

- [x] Phase 0: Finalize skill architecture and sub-skill interface contracts
- [x] Phase 1: Implement sub-profile-intake (dyslexia subtype classification logic)
- [x] Phase 1: Implement sub-text-analyzer (Flesch-Kincaid + sentence segmentation)
- [x] Phase 1: Implement sub-font-layout-converter (BDA/IDA rule engine)
- [x] Phase 1: Implement sub-readability-scorer (BDA checklist + WCAG compliance)
- [x] Phase 2: Build main harness with quality gates
- [x] Phase 2: Implement sentence simplification engine (replace low-frequency words, break compound sentences)
- [x] Phase 3: Deploy knowledge_updater.py and seed SECOND-KNOWLEDGE-BRAIN.md
- [x] Phase 4: Run 5+ test scenarios and validate output quality
- [x] Phase 5: Wire shared sub-skills to cluster (career-education) shared library

---


## Cluster Integration (career-education)

This skill contributes reusable sub-skill patterns to the career-education cluster shared library:

| Sub-skill | Reusable asset | How to reuse |
|-----------|----------------|--------------|
| `sub-profile-intake` | Learner-profile JSON schema (age band, severity, context, medium) | Generalise field names for any learner cohort beyond dyslexia (e.g., ADHD, ESL, low-vision) |
| `sub-text-analyzer` | Readability metrics pipeline + high-frequency word filter | Use as `sub-scoring-engine` input for any text-optimisation skill |
| `sub-readability-scorer` | BDA/WCAG checklist + grade rubric | Extract as `sub-scoring-engine` for accessibility auditing skills |
| `sub-font-layout-converter` | Typography spec generator | Reuse for any document-accessibility skill (visual-impairment, print-to-PDF) |

### Cross-skill references
- Pair with CV/resume accessibility skills: apply the same font/spacing rules to job-application documents.
- Pair with e-learning script skills: use the sentence-simplification engine before uploading content to an LMS.
- Pair with interview-prep skills: convert dense policy/compliance passages using the legal-text adjusted threshold documented in `tests/test-scenarios.md`.

### Dependencies
- No circular dependencies: this skill reads `SECOND-KNOWLEDGE-BRAIN.md` and writes its own deliverables only.
- External cluster shared sub-skills are referenced conceptually; this skill remains self-contained if the shared library is not present.

## Reference Documents

- `PROJECT-detail.md` — full technical specification
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` — phase-by-phase build roadmap
- `SECOND-KNOWLEDGE-BRAIN.md` — self-improving domain knowledge base
