# PROJECT-detail.md — Dyslexia-Friendly Learning Material Converter (Skill #233)

---

## Executive Summary

The **dyslexia-learning-material-converter** is a Claude Code skill that accepts any text-based learning material and automatically transforms it into a format optimised for dyslexic readers. The conversion applies evidence-based typography rules (BDA Style Guide, IDA standards), WCAG 1.4.x text-presentation guidelines, and sentence-level readability improvements grounded in phonological deficit theory and visual-stress neuroscience. The skill outputs the fully converted material alongside a before/after accessibility scorecard and a prioritised improvement roadmap. It is designed to serve teachers, L&D designers, parents, corporate training teams, and accessibility specialists without requiring any prior knowledge of dyslexia research.

---

## Problem Statement

### Prevalence and Impact
Dyslexia affects an estimated **10–15% of the global population** (Shaywitz, 1998; IDA, 2022), making it the most common specific learning difficulty. It is characterised by unexpected difficulty with accurate and/or fluent word recognition, poor spelling and decoding abilities, reflecting a deficit in the phonological component of language (Lyon, Shaywitz & Shaywitz, 2003). Secondary characteristics include visual stress (Irlen syndrome overlap), working-memory limitations, and difficulties processing rapid sequences of visual stimuli (magnocellular pathway deficit — Stein & Walsh, 1997).

### Typography and Format as Barriers
Research confirms that typographic choices significantly affect reading performance for dyslexic readers:
- **Font:** Sans-serif fonts (Arial, Verdana, OpenDyslexic) outperform serif fonts (Times New Roman) in reading speed and error rate (Rello & Baeza-Yates, 2013).
- **Text size:** Minimum 12–14 pt is recommended; 14 pt is the BDA default.
- **Line spacing:** 1.5x line height significantly reduces crowding effects (Zorzi et al., 2012).
- **Justification:** Left-aligned (ragged right) prevents uneven word spacing that disrupts saccadic eye movement (BDA, 2023).
- **Colour contrast and overlays:** ~20% of dyslexic readers report benefit from coloured overlays that reduce visual stress (Wilkins et al., 2004).
- **Sentence length:** Average sentence length ≤ 15 words and Flesch-Kincaid Reading Ease ≥ 60 significantly reduce cognitive load (Klare, 1963).

### The Gap
Despite extensive research, the overwhelming majority of educational documents, e-learning modules, employee handbooks, and assessment materials are produced in formats that violate every guideline above. Manual reformatting requires specialist knowledge and takes hours per document. No automated, research-grounded, end-to-end conversion tool exists in the Claude ecosystem.

---

## Target Users and Use Cases

| User | Trigger | Expected Output |
|------|---------|----------------|
| Primary school teacher | "Convert this science worksheet for my Year 4 student who has phonological dyslexia" | Reformatted worksheet with font/spacing changes and simplified sentences |
| Corporate L&D team | "Make our employee onboarding handbook dyslexia-friendly" | Fully converted handbook with accessibility scorecard |
| Parent | "Help my 12-year-old understand this history chapter" | Chunked, simplified version with structural aids |
| University disability officer | "Audit this exam paper for dyslexia accessibility" | BDA/WCAG compliance report with specific remediation steps |
| EdTech content creator | "Optimise this e-learning script for a mixed audience including dyslexic learners" | Revised script with UDL-aligned formatting guidance |
| Adult dyslexic learner | "I struggle to read this legal document" | Plain-language conversion with structural aids and font recommendations |

---

## Harness Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                  dyslexia-learning-material-converter                │
│                         (main harness)                               │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
              ┌────────────────▼────────────────┐
              │        STAGE 1: INTAKE           │
              │    [sub-profile-intake]          │
              │ - Learner age, subtype, severity │
              │ - Font/overlay preference        │
              │ - Reading context/purpose        │
              └────────────────┬────────────────┘
                               │
              ┌────────────────▼────────────────┐
              │      STAGE 2: TEXT ANALYSIS      │
              │     [sub-text-analyzer]          │
              │ - Flesch-Kincaid score           │
              │ - Avg sentence length            │
              │ - Low-frequency word list        │
              │ - Structural weaknesses          │
              └────────────────┬────────────────┘
                               │
              ┌────────────────▼────────────────┐
              │    STAGE 3: TYPOGRAPHY & LAYOUT  │
              │  [sub-font-layout-converter]     │
              │ - Font family + size             │
              │ - Line/letter/para spacing       │
              │ - Background colour              │
              │ - Margin & column width          │
              └────────────────┬────────────────┘
                               │
              ┌────────────────▼────────────────┐
              │   STAGE 4: SENTENCE REWRITE      │
              │      [main harness — internal]   │
              │ - Break long sentences (≤15 wds) │
              │ - Replace low-freq vocabulary    │
              │ - Add headers, bullets, chunking │
              │ - Active voice conversion        │
              └────────────────┬────────────────┘
                               │
              ┌────────────────▼────────────────┐
              │    STAGE 5: ACCESSIBILITY SCORE  │
              │    [sub-readability-scorer]      │
              │ - BDA Style Guide checklist      │
              │ - WCAG 1.4.x compliance          │
              │ - Flesch-Kincaid ≥ 60 check      │
              │ - Before/after comparison        │
              └────────────────┬────────────────┘
                               │
              ┌────────────────▼────────────────┐
              │       STAGE 6: FINAL OUTPUT      │
              │      [main harness — output]     │
              │ - Converted material (full text) │
              │ - Typography spec sheet          │
              │ - Accessibility scorecard        │
              │ - Prioritised improvement roadmap│
              └─────────────────────────────────┘
```

---

## Full Sub-Skill Catalog

### sub-profile-intake

| Attribute | Value |
|-----------|-------|
| **Purpose** | Collect all learner profile variables needed to personalise the conversion |
| **Inputs** | User-provided description or structured intake form |
| **Outputs** | Structured profile JSON: `{age, dyslexia_subtype, severity, preferred_font, overlay_colour, reading_context, purpose}` |
| **Tools** | Read (if profile file provided), conversational intake otherwise |
| **Quality Gate** | All 7 fields populated; if missing, apply defaults from BDA age-band recommendations |

**Dyslexia subtype classification:**
- **Phonological dyslexia:** Difficulty decoding new words via grapheme-phoneme rules; benefits most from high-frequency word replacement, chunking, and phonics-aligned vocabulary.
- **Surface dyslexia:** Difficulty with sight-word recognition of irregular words; benefits from consistent spelling patterns and glossaries.
- **Mixed/Double-deficit:** Both phonological and naming-speed deficits; requires comprehensive intervention across all dimensions.

### sub-text-analyzer

| Attribute | Value |
|-----------|-------|
| **Purpose** | Quantify the accessibility barriers in the source text |
| **Inputs** | Raw source text (string) |
| **Outputs** | Analysis report: FK grade level, FK reading ease, avg sentence length, % long sentences (>20 words), % low-frequency words (outside Dale-Chall 3000 list), passive-voice count, structural issues (no headers, dense paragraphs >4 sentences) |
| **Tools** | Read (source document), Bash (optional textstat library invocation) |
| **Quality Gate** | All metrics computed; at least 3 specific "barrier flags" identified |

### sub-font-layout-converter

| Attribute | Value |
|-----------|-------|
| **Purpose** | Produce a complete typography and layout specification for the converted document |
| **Inputs** | Learner profile (from sub-profile-intake), target output medium (print/screen/PDF) |
| **Outputs** | Typography spec: font family, font size, line height, letter spacing, word spacing, paragraph spacing, text alignment, column width, margin, background colour hex, text colour hex, contrast ratio |
| **Tools** | Read (BDA guidelines from SECOND-KNOWLEDGE-BRAIN.md) |
| **Quality Gate** | WCAG 1.4.3 contrast ratio ≥ 4.5:1 for normal text; all BDA mandatory fields populated |

**BDA/IDA mandatory typography targets:**
- Font: OpenDyslexic, Arial, Verdana, or Comic Sans (avoid Times New Roman, Helvetica)
- Size: minimum 12pt; recommended 14pt for primary-age learners
- Line spacing: minimum 1.5x (150%); recommended 2.0x for severe cases
- Letter spacing: 0.35em additional
- Word spacing: 0.16em additional
- Paragraph spacing: ≥ 2.0x line height
- Text alignment: left-aligned only (never justified)
- Column width: maximum 60–70 characters per line
- Background: cream (#FFFDD0), light yellow (#FAFAD2), or light blue (#EEF4FF) over pure white

### sub-readability-scorer

| Attribute | Value |
|-----------|-------|
| **Purpose** | Score both original and converted text against all applicable accessibility standards |
| **Inputs** | Original text, converted text, typography spec |
| **Outputs** | Scorecard: BDA compliance (pass/fail per criterion), WCAG 1.4.x compliance (pass/fail per SC), Flesch-Kincaid Reading Ease (before/after), Flesch-Kincaid Grade Level (before/after), overall accessibility grade (A/B/C/D/F), improvement delta |
| **Tools** | Read (SECOND-KNOWLEDGE-BRAIN.md for framework reference) |
| **Quality Gate** | Flesch-Kincaid Reading Ease ≥ 60; all BDA mandatory items pass; WCAG 1.4.3 contrast passes |

---

## E2E Execution Flow

```
Step 1:  User invokes /dyslexia-learning-material-converter
Step 2:  Harness greets user and explains the process (1 sentence)
Step 3:  INVOKE sub-profile-intake → await profile JSON
Step 4:  User provides source text (paste or file path)
Step 5:  INVOKE sub-text-analyzer → receive analysis report
Step 6:  Harness displays analysis summary: "Your text has FK Grade X, avg sentence Y words, Z% low-frequency words — here are the top 3 accessibility barriers."
Step 7:  INVOKE sub-font-layout-converter (using profile + medium) → receive typography spec
Step 8:  Harness performs sentence rewrite:
           a. Segment text by sentence
           b. Flag sentences > 15 words → split at conjunctions/relative clauses
           c. Flag low-frequency words → substitute from high-frequency synonym list
           d. Convert passive voice to active where possible
           e. Group every 3–4 sentences into a paragraph with a descriptive header
           f. Convert long lists in prose to bullet points
Step 9:  INVOKE sub-readability-scorer (original + converted + typography spec)
Step 10: If Flesch-Kincaid < 60 on converted text → loop back to Step 8 (max 2 iterations)
Step 11: If all quality gates pass → proceed to output
Step 12: Harness generates final deliverable:
           - Section A: Typography Specification Sheet
           - Section B: Converted Text (full)
           - Section C: Before/After Accessibility Scorecard
           - Section D: Prioritised Improvement Roadmap
           - Section E: Implementation Notes (how to apply the spec in Word/Google Docs/InDesign)
Step 13: Harness offers to search for latest dyslexia research relevant to the learner's profile
         (WebSearch: PubMed, Dyslexia journal) and appends 2–3 research-backed tips
```

**Error handling:**
- Source text < 50 words: warn user that scoring will be unreliable; proceed with conversion
- Unknown dyslexia subtype: default to phonological (most common) and note assumption
- WebSearch unavailable: fall back to SECOND-KNOWLEDGE-BRAIN.md; signal limitation clearly
- FK score cannot be computed (non-English text): note limitation; apply structural rules only

---

## SECOND-KNOWLEDGE-BRAIN Integration

The skill reads from `SECOND-KNOWLEDGE-BRAIN.md` at two points:
1. **sub-font-layout-converter** — reads the Analytical Frameworks section to verify current BDA/IDA targets
2. **sub-readability-scorer** — reads Key Research Papers for citation backing in the scorecard

The `tools/knowledge_updater.py` script runs weekly (or on demand) to:
- Fetch new papers from PubMed (dyslexia + font/overlay/readability), Annals of Dyslexia, JLD
- Score by recency (days since publication, weight 0.5) + relevance (keyword match score, weight 0.5)
- Append new entries to the Key Research Papers table with date stamp
- Skip entries with DOI/URL already present (SHA-256 hash check)
- Update the Knowledge Update Log

---

## Quality Gates

Before the final deliverable is shown, ALL of the following must be true:

| Gate | Criterion | Pass Threshold |
|------|-----------|---------------|
| BDA-1 | Font is from BDA-approved list | Pass / Fail |
| BDA-2 | Font size ≥ 12pt (14pt for children) | Pass / Fail |
| BDA-3 | Line spacing ≥ 1.5x | Pass / Fail |
| BDA-4 | Text is left-aligned (not justified) | Pass / Fail |
| BDA-5 | Paragraph length ≤ 4 sentences | Pass / Fail |
| BDA-6 | No ALL-CAPS passages > 3 words | Pass / Fail |
| WCAG-1 | Text contrast ratio ≥ 4.5:1 (SC 1.4.3) | Pass / Fail |
| WCAG-2 | Text can be resized 200% without loss (SC 1.4.4) | Advisory |
| WCAG-3 | Line height ≥ 1.5x font size (SC 1.4.12) | Pass / Fail |
| FK-1 | Flesch-Kincaid Reading Ease ≥ 60 | Numeric |
| FK-2 | Average sentence length ≤ 15 words | Numeric |
| FK-3 | FK Grade Level ≤ 8 (general adult audience) | Numeric |

If any mandatory gate fails, the harness must note the failure, explain what must be corrected, and (if possible) apply an automatic fix before presenting output.

---

## Test Scenarios

See `tests/test-scenarios.md` for full details. Summary:

1. Dense Year 4 science worksheet (phonological dyslexia, age 9)
2. Adult legal contract (mixed dyslexia, severity moderate)
3. Corporate employee handbook (surface dyslexia, age 32)
4. E-learning script with bullet points (phonological, age 16)
5. Existing "dyslexia-friendly" document — audit for compliance gaps
6. Medical patient information leaflet (dyslexia + low literacy, age 45)
7. Multilingual classroom handout (English sections only; note limitation on non-English)

---

## Key Design Decisions

1. **Font family priority order:** OpenDyslexic (if digital) > Arial > Verdana > Trebuchet MS. Comic Sans is included on the BDA list but is often professionally inappropriate — offer as an option, not a default.
2. **No justified text ever:** Justified text creates uneven word rivers that are demonstrably harmful for dyslexic readers (BDA, 2023). This is a hard constraint — never output justified text.
3. **Colour overlays as advisory, not enforced:** Colour overlay preferences are highly individual (~20% benefit, ~10% experience worsening — Wilkins, 2004). The skill recommends based on profile but always presents as a suggestion with instructions to test.
4. **Sentence splitting heuristic:** Split at: (a) coordinating conjunctions (and, but, or, so, yet) where both clauses > 7 words; (b) relative clauses (which, who, that) introducing a new idea; (c) subordinating conjunctions (although, because, however) at sentence start.
5. **Active voice conversion:** Passive voice ("The experiment was conducted by") is converted to active ("The researcher conducted") using subject-verb-object reordering. Cannot be automated perfectly — harness flags remaining passive constructions for manual review.
6. **Glossary generation:** For every replaced low-frequency word, the skill generates a glossary entry (original term → plain-language definition) appended to the converted document.
7. **Platform-specific implementation notes:** The skill always appends instructions for applying the typography spec in the most common platforms: Microsoft Word, Google Docs, PDF (CSS/InDesign), and HTML/CSS.
8. **Severity scaling:** Severe dyslexia profiles receive more aggressive intervention (higher FK ease target: ≥ 70, line spacing 2.0x, larger font 16pt+). Mild profiles use standard BDA targets.
9. **UDL alignment:** The conversion also applies UDL Principle 1 (Multiple Means of Representation): adds alt-text suggestions for any images referenced, recommends audio/text-to-speech compatibility.
10. **Evidence hierarchy:** All framework citations follow the evidence hierarchy: Systematic Review > RCT > Cohort > Expert guidance. The BDA Style Guide (expert consensus) is the floor; RCT evidence from Rello & Baeza-Yates (2013) and Zorzi et al. (2012) takes precedence where it conflicts.
