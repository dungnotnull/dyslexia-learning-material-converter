# PROJECT-DEVELOPMENT-PHASE-TRACKING.md — Skill #233: dyslexia-learning-material-converter

---

## Overview

| Phase | Name | Status | Target Completion |
|-------|------|--------|------------------|
| 0 | Research & Skill Architecture | Complete | Week 1 |
| 1 | Core Sub-Skills Implementation | Complete | Week 2–3 |
| 2 | Main Harness + Quality Gates | Complete | Week 4 |
| 3 | SECOND-KNOWLEDGE-BRAIN Pipeline | Complete | Week 5 |
| 4 | Testing & Validation | Complete | Week 6 |
| 5 | Integration & Cross-Skill Wiring | Complete | Week 7 |

---

## Phase 0: Research & Skill Architecture

### Goal
Establish the complete skill architecture, validate the framework choices against current research, and produce all planning documents before writing a single line of skill code.

### Task List
- [x] Read BDA Style Guide (2023) — extract all numeric typography targets
- [x] Read IDA standards documentation — map to BDA where overlapping
- [x] Review Rello & Baeza-Yates (2013) — font effectiveness RCT
- [x] Review Zorzi et al. (2012) — letter/line spacing RCT
- [x] Define dyslexia subtype taxonomy (phonological / surface / mixed)
- [x] Map WCAG 2.1 Success Criteria relevant to text presentation (1.4.3, 1.4.4, 1.4.12)
- [x] Design harness architecture (ASCII diagram)
- [x] Define sub-skill interface contracts (inputs/outputs for all 4 sub-skills)
- [x] Define quality gate thresholds (see PROJECT-detail.md)
- [x] Write CLAUDE.md, PROJECT-detail.md, this document, SECOND-KNOWLEDGE-BRAIN.md
- [x] Write skills/main.md skeleton

### Deliverables
- CLAUDE.md (complete)
- PROJECT-detail.md (complete)
- PROJECT-DEVELOPMENT-PHASE-TRACKING.md (this file)
- SECOND-KNOWLEDGE-BRAIN.md (seeded with 10+ papers)
- skills/main.md (full harness)
- skills/sub-*.md (4 sub-skills)

### Success Criteria
- All numeric BDA/IDA/WCAG targets documented with source citations
- Harness flow covers all 6 stages with no gaps
- Every sub-skill has defined inputs, outputs, and quality gate
- SECOND-KNOWLEDGE-BRAIN.md seeded with minimum 10 research papers

### Estimated Effort
3–4 hours of research + 2 hours of documentation

---

## Phase 1: Core Sub-Skills Implementation

### Goal
Implement the 4 core sub-skills as fully functional skill files with complete workflow instructions, branching logic, and internal quality gates.

### Task List

#### sub-profile-intake.md
- [x] Write structured intake questionnaire (7 fields)
- [x] Define default values per BDA age-band (5–7, 8–11, 12–16, 17+, adult)
- [x] Add severity scale definition (mild / moderate / severe) with observable indicators
- [x] Add reading context taxonomy (classroom, self-study, workplace, assessment, recreational)
- [x] Add font preference elicitation (show examples, ask which feels easiest)
- [x] Add colour overlay preference logic (reference Wilkins 2004 screening)
- [x] Write intake validation logic (flag missing fields, apply defaults)

#### sub-text-analyzer.md
- [x] Implement Flesch-Kincaid Reading Ease formula: 206.835 − (1.015 × ASL) − (84.6 × ASW)
- [x] Implement Flesch-Kincaid Grade Level formula
- [x] Define long sentence threshold (> 15 words = flag; > 20 words = critical flag)
- [x] Build low-frequency word detection against Dale-Chall 3,000 word list
- [x] Add passive voice detection pattern (to be + past participle)
- [x] Add structural issue detection (no headers in >300-word block; paragraph > 4 sentences)
- [x] Add double-negative detection (cognitive load amplifier)
- [x] Output formatted analysis report template

#### sub-font-layout-converter.md
- [x] Build decision tree: digital screen vs print vs PDF
- [x] Build age-band × severity → font/size/spacing lookup table
- [x] Add contrast ratio computation guidance (WCAG 1.4.3 formula)
- [x] Add platform-specific CSS/Word/Google Docs implementation snippets
- [x] Add coloured background hex codes with rationale (cream, yellow, light blue, mint green)
- [x] Add column width guidance (60–70 characters/line for all contexts)
- [x] Add hyperlink formatting guidance (no underline alone; colour + underline)

#### sub-readability-scorer.md
- [x] Build BDA checklist (all criteria from Phase 0 research)
- [x] Build WCAG 1.4.x checklist (SC 1.4.3, 1.4.4, 1.4.12)
- [x] Define before/after comparison table format
- [x] Define overall accessibility grade rubric (A: all pass + FK ≥ 70; B: all mandatory pass + FK ≥ 60; C: ≥ 80% mandatory pass; D: < 80% mandatory; F: < 60%)
- [x] Add improvement delta computation (% improvement per dimension)
- [x] Add research-backed rationale for each criterion

### Deliverables
- 4 complete sub-skill .md files (fully functional, not skeleton)

### Success Criteria
- Each sub-skill file can be read in isolation and executed by Claude without the main harness
- All sub-skills have defined quality gates
- sub-font-layout-converter produces a complete typography spec for any profile × medium combination

### Estimated Effort
6–8 hours

---

## Phase 2: Main Harness + Quality Gates

### Goal
Build the main harness (skills/main.md) that orchestrates all sub-skills, implements the sentence-rewrite engine, and enforces all quality gates.

### Task List
- [x] Complete skills/main.md with full workflow (Steps 1–13 from E2E Execution Flow)
- [x] Implement sentence segmentation logic (Step 8a)
- [x] Implement sentence splitting heuristic (Step 8b — 4 splitting rules)
- [x] Implement low-frequency word substitution (Step 8c — with glossary generation)
- [x] Implement active voice conversion (Step 8d — with flag-for-review on unresolvable cases)
- [x] Implement paragraph chunking with descriptive headers (Step 8e)
- [x] Implement prose-to-bullet conversion (Step 8f)
- [x] Implement quality gate enforcement loop (Step 10 — max 2 iterations)
- [x] Write final output template (Sections A–E)
- [x] Write implementation notes for Word, Google Docs, PDF, HTML/CSS
- [x] Add graceful degradation paths (WebSearch unavailable, non-English text, short text)
- [x] Add UDL Principle 1 advisory (alt-text suggestions, TTS compatibility)

### Deliverables
- skills/main.md (fully functional harness)
- Quality gate enforcement documented inside main.md

### Success Criteria
- Harness correctly routes through all 6 stages for any valid profile
- Quality gate loop terminates correctly (max 2 iterations)
- Final output always contains all 5 sections (A–E)
- Graceful degradation tested for all 3 error paths

### Estimated Effort
4–5 hours

---

## Phase 3: SECOND-KNOWLEDGE-BRAIN Pipeline

### Goal
Deploy the automated knowledge crawler and validate that SECOND-KNOWLEDGE-BRAIN.md grows correctly with each run.

### Task List
- [x] Complete tools/knowledge_updater.py (crawl4ai implementation — PubMed, Dyslexia Wiley, Annals, JLD)
- [x] Add SHA-256 deduplication logic
- [x] Add relevance scoring algorithm (recency 0.5 + keyword match 0.5)
- [x] Test crawl against PubMed API (search: dyslexia font readability)
- [x] Test crawl against Dyslexia journal (Wiley Online Library)
- [x] Test append logic (verify correct table row format)
- [x] Test deduplication (run twice, verify no duplicate entries)
- [x] Set up cron schedule recommendation in SECOND-KNOWLEDGE-BRAIN.md Self-Update Protocol
- [x] Seed initial 10+ papers manually into SECOND-KNOWLEDGE-BRAIN.md
- [x] Document knowledge_updater.py usage in CLAUDE.md

### Deliverables
- tools/knowledge_updater.py (complete, runnable)
- SECOND-KNOWLEDGE-BRAIN.md (seeded with 10+ papers, update log entry for 2026-06-18)

### Success Criteria
- knowledge_updater.py runs without error on a machine with Python 3.10+ and crawl4ai installed
- At least 3 new paper entries appended on first clean run
- No duplicate entries after 2 consecutive runs
- Knowledge Update Log entry added with correct date

### Estimated Effort
3–4 hours

---

## Phase 4: Testing & Validation

### Goal
Execute all test scenarios in tests/test-scenarios.md, validate output quality against quality gates, and document any failures.

### Task List
- [x] Execute Scenario 1: Year 4 science worksheet (phonological, age 9)
- [x] Execute Scenario 2: Adult legal contract (mixed, moderate)
- [x] Execute Scenario 3: Corporate employee handbook (surface, age 32)
- [x] Execute Scenario 4: E-learning script (phonological, age 16)
- [x] Execute Scenario 5: Existing dyslexia-friendly document audit
- [x] Execute Scenario 6: Medical patient information leaflet (dyslexia + low literacy, age 45)
- [x] Execute Scenario 7: Multilingual handout (English sections only)
- [x] For each scenario: document quality gate results (pass/fail per gate)
- [x] For each scenario: measure FK Reading Ease before/after
- [x] For each scenario: measure FK Grade Level before/after
- [x] Document any quality gate failures and root causes
- [x] Fix identified issues in skill files (sub-skills or harness)
- [x] Re-run failed scenarios after fixes
- [x] Write final test report in tests/test-scenarios.md

### Deliverables
- tests/test-scenarios.md (completed with all 7 scenario results)
- Updated skill files (any fixes from testing)

### Success Criteria
- All 7 scenarios complete without harness failure
- FK Reading Ease improves by ≥ 15 points in at least 5 of 7 scenarios
- All mandatory BDA quality gates pass in final output for all scenarios
- WCAG 1.4.3 contrast passes for all typography specs generated

### Estimated Effort
4–6 hours

---

## Phase 5: Integration & Cross-Skill Wiring

### Goal
Connect this skill's sub-skills to the cluster-wide shared sub-skill library (career-education cluster) and document reuse opportunities for other skills in the cluster.

### Task List
- [x] Review career-education cluster shared sub-skills: sub-profile-intake (shared pattern), sub-framework-selector, sub-scoring-engine, sub-improvement-roadmap
- [x] Identify overlap: sub-profile-intake can be generalised for learner profiles beyond dyslexia
- [x] Identify overlap: sub-readability-scorer scoring engine can be extracted as sub-scoring-engine
- [x] Document cluster-reusable interfaces in CLAUDE.md
- [x] Cross-reference with any other accessibility-focused skills in the library
- [x] Add cross-skill references in SECOND-KNOWLEDGE-BRAIN.md (related skills, shared knowledge)
- [x] Update progression.json (move #233 to completed)

### Deliverables
- Updated CLAUDE.md with cluster integration notes
- Cross-skill reference documentation

### Success Criteria
- At least 2 sub-skills documented as reusable for other career-education cluster skills
- No circular dependencies between this skill and cluster shared library
- progression.json updated to mark #233 as completed

### Estimated Effort
1–2 hours
