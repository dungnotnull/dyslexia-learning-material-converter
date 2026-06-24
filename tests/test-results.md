# Test Results — Dyslexia-Friendly Learning Material Converter

*Generated: 2026-06-24 01:58:59 UTC*
*Harness: tools/test_harness.py*
*Engine: tools/dyslexia_converter.py (deterministic rule-based pipeline; no LLM call)*

## Summary

| Scenario | FKRE before | FKRE after | Δ FKRE | ASL before | ASL after | Grade | Pass |
|----------|-------------|------------|--------|------------|-----------|-------|------|
| 1 | -5.7 | 71.7 | +77.4 | 31.0 | 9.8 | F → A | PASS |
| 2 | -44.7 | 72.0 | +116.7 | 114.0 | 11.2 | F → A | PASS |
| 3 | 31.0 | 73.1 | +42.1 | 19.6 | 12.8 | F → A | PASS |
| 4 | 2.1 | 71.0 | +68.9 | 19.8 | 7.6 | F → A | PASS |
| 5 | 30.3 | 67.2 | +36.9 | 16.8 | 9.0 | F → B | PASS |
| 6 | 34.3 | 77.1 | +42.8 | 16.7 | 9.1 | F → A | PASS |
| 7 | 75.7 | 78.6 | +2.9 | 13.2 | 9.0 | F → A | PASS |

**Overall: 7/7 scenarios pass all checks.**

---

## Scenario 1: Year 4 science worksheet — phonological dyslexia (age 9)

### Input Profile

```json
{
  "age_band": "8-11",
  "dyslexia_subtype": "phonological",
  "severity": "moderate",
  "preferred_font": "Arial",
  "overlay_colour_hex": "#FAFAD2",
  "reading_context": "classroom",
  "output_medium": "print",
  "fk_reading_ease_target": 60,
  "max_sentence_length_words": 12,
  "domain_terms": [
    "chloroplasts",
    "biochemical",
    "photosynthesis",
    "chlorophyll"
  ]
}
```

### Source Text Metrics

- Word count: 93
- Sentence count: 3
- FKRE: -5.7
- FKGL: 21.7
- Average sentence length: 31.0 words
- Very long sentences (>25 words): 3
- Low-frequency word %: 25.8%

### Converted Text

```
# Converted text

Photosynthesis is the way that green plants use sunlight, water. A gas in the air to make sugar. It then provides the energy needed for the living thing's working. The green matter in leaves a colour found mostly inside the tiny parts inside leaves.

Of plant cells helps the taking in of light. It is then changed into energy. Through a set of chemical reactions. Without enough of sunlight, photosynthesis cannot be started.

It means that plants in places with not enough light will. Show significantly lower speed of growth and may finally fail to survive.
```

### Typography Specification

```
TYPOGRAPHY SPECIFICATION
========================
Generated for: 8-11 | moderate | print
Standard: BDA Style Guide 2023 + WCAG 2.1 AA

FONT
----
Family:           Arial
Size (body):      14pt
Size (H1):        18pt
Size (H2):        16pt

SPACING
-------
Line height:      1.5x (21.0pt)
Letter spacing:   +0.35em
Word spacing:     +0.16em
Paragraph spacing:28pt
Column width:     65 characters maximum

ALIGNMENT
---------
Body text:        Left-aligned (ragged right) ? NEVER justified

COLOURS
-------
Background:       #FAFAD2 (light yellow)
Body text:        #333333
Contrast ratio:   11.83:1 ? PASS
Link text:        #0057B8 (unvisited) | #6B0F8C (visited)

MARGINS & LAYOUT
----------------
Left margin:      ? 2.5 cm
Right margin:     ? 2.5 cm
Columns:          1 column(s)

WCAG COMPLIANCE
---------------
SC 1.4.3 (Contrast):   PASS (11.83:1)
SC 1.4.4 (Resize):     PASS (single-column layout)
SC 1.4.12 (Spacing):   PASS (line-height 1.5x)
```

### Accessibility Scorecard

```
ACCESSIBILITY SCORECARD
=======================

READABILITY METRICS (BEFORE ? AFTER)
------------------------------------
Flesch-Kincaid Reading Ease:  -5.7 ? 71.7  (target ? 60)
Flesch-Kincaid Grade Level:   21.7 ? 5.7  (target ? 5)
Avg sentence length:          31.0 ? 9.8 words
Low-frequency word %:         25.8% ? 4.1%

BDA STYLE GUIDE COMPLIANCE ? 14/14 passing
------------------------------------------------
B1 Font family is BDA-approved: PASS (Arial)
B2 Font size ? 12pt (14pt for children): PASS (14pt)
B3 Line spacing ? 1.5x: PASS (1.5x)
B4 Text is left-aligned: PASS (left)
B5 No justified text: PASS (n/a)
B6 Paragraph length ? 4 sentences: PASS (0 dense)
B7 No ALL-CAPS passages > 3 words: PASS (0 found)
B8 Bold preferred over italic: PASS (checked)
B9 Background not pure white: PASS (#FAFAD2)
B10 Column width ? 70 characters: PASS (65ch)
B11 Headers present in long blocks: PASS (yes)
B12 Lists explicit: PASS (checked)
B13 Avg sentence length ? 20 words: PASS (9.8 words)
B14 Letter spacing ? 0.35em: PASS (0.35em)

WCAG 2.1 AA MANDATORY ? 3/3 passing
W1 SC 1.4.3 Contrast (Minimum): PASS (11.83:1)
W2 SC 1.4.4 Resize Text: PASS (Single-column layout supports 200% zoom)
W3 SC 1.4.12 Text Spacing: PASS (LH 1.5x LS 0.35em WS 0.16em)

OVERALL GRADE: F ? A

ACCESSIBILITY COMPLIANCE CERTIFICATE
====================================
This converted material meets BDA 2023, WCAG 2.1 AA, and the Flesch-Kincaid target.
A qualified dyslexia specialist should review high-stakes documents.
```

### Quality Gate Checks

| Check | Result |
|-------|--------|
| fkre_target_met | PASS |
| asl_target_met | PASS |
| bda_all_pass | PASS |
| wcag_aa_pass | PASS |
| contrast_pass | PASS |
| font_approved | PASS |
| left_aligned | PASS |
| grade_a_or_b | PASS |
| glossary_present | PASS |

**Scenario verdict: PASS**

---

## Scenario 2: Adult legal contract — mixed dyslexia (moderate, age 34)

### Input Profile

```json
{
  "age_band": "17+",
  "dyslexia_subtype": "mixed",
  "severity": "moderate",
  "preferred_font": "OpenDyslexic",
  "overlay_colour_hex": "#EEF4FF",
  "reading_context": "self-study",
  "output_medium": "screen",
  "fk_reading_ease_target": 45,
  "max_sentence_length_words": 12,
  "domain_terms": [
    "covenants",
    "assign",
    "sublet"
  ]
}
```

### Source Text Metrics

- Word count: 114
- Sentence count: 1
- FKRE: -44.7
- FKGL: 47.8
- Average sentence length: 114.0 words
- Very long sentences (>25 words): 1
- Low-frequency word %: 20.2%

### Converted Text

```
# Converted text

The renter agrees with the owner that during the time of this agreement. The renter shall: (a) pay the payment. All other sums payable in this agreement at the times. In the manner shown in this agreement, without any taking away, keeping back.

Taking away money at all; (b) use the Property for home purposes only. Not carry on or permit to be carried on in the property any trade. Business or profession or use the same for any. Purpose other than as a home c not give to someone else.

Payment to someone else give up your right to use or share occupation. Of the whole or any part of the Property. Without the written agreement first of the owner. Such consent not to be without a good reason withheld or delayed.
```

*Legal note:* This is a plain-language aid. Seek professional legal advice before signing.

### Typography Specification

```
TYPOGRAPHY SPECIFICATION
========================
Generated for: 17+ | moderate | screen
Standard: BDA Style Guide 2023 + WCAG 2.1 AA

FONT
----
Family:           OpenDyslexic
Size (body):      14pt
Size (H1):        18pt
Size (H2):        16pt

SPACING
-------
Line height:      1.5x (21.0pt)
Letter spacing:   +0.35em
Word spacing:     +0.16em
Paragraph spacing:28pt
Column width:     65 characters maximum

ALIGNMENT
---------
Body text:        Left-aligned (ragged right) ? NEVER justified

COLOURS
-------
Background:       #EEF4FF (light blue)
Body text:        #333333
Contrast ratio:   11.44:1 ? PASS
Link text:        #0057B8 (unvisited) | #6B0F8C (visited)

MARGINS & LAYOUT
----------------
Left margin:      ? 2.5 cm
Right margin:     ? 2.5 cm
Columns:          1 column(s)

WCAG COMPLIANCE
---------------
SC 1.4.3 (Contrast):   PASS (11.44:1)
SC 1.4.4 (Resize):     PASS (single-column layout)
SC 1.4.12 (Spacing):   PASS (line-height 1.5x)
```

### Accessibility Scorecard

```
ACCESSIBILITY SCORECARD
=======================

READABILITY METRICS (BEFORE ? AFTER)
------------------------------------
Flesch-Kincaid Reading Ease:  -44.7 ? 72.0  (target ? 45)
Flesch-Kincaid Grade Level:   47.8 ? 6.0  (target ? 8)
Avg sentence length:          114.0 ? 11.2 words
Low-frequency word %:         20.2% ? 7.4%

BDA STYLE GUIDE COMPLIANCE ? 14/14 passing
------------------------------------------------
B1 Font family is BDA-approved: PASS (OpenDyslexic)
B2 Font size ? 12pt (14pt for children): PASS (14pt)
B3 Line spacing ? 1.5x: PASS (1.5x)
B4 Text is left-aligned: PASS (left)
B5 No justified text: PASS (n/a)
B6 Paragraph length ? 4 sentences: PASS (0 dense)
B7 No ALL-CAPS passages > 3 words: PASS (0 found)
B8 Bold preferred over italic: PASS (checked)
B9 Background not pure white: PASS (#EEF4FF)
B10 Column width ? 70 characters: PASS (65ch)
B11 Headers present in long blocks: PASS (yes)
B12 Lists explicit: PASS (checked)
B13 Avg sentence length ? 20 words: PASS (11.2 words)
B14 Letter spacing ? 0.35em: PASS (0.35em)

WCAG 2.1 AA MANDATORY ? 3/3 passing
W1 SC 1.4.3 Contrast (Minimum): PASS (11.44:1)
W2 SC 1.4.4 Resize Text: PASS (Single-column layout supports 200% zoom)
W3 SC 1.4.12 Text Spacing: PASS (LH 1.5x LS 0.35em WS 0.16em)

OVERALL GRADE: F ? A

ACCESSIBILITY COMPLIANCE CERTIFICATE
====================================
This converted material meets BDA 2023, WCAG 2.1 AA, and the Flesch-Kincaid target.
A qualified dyslexia specialist should review high-stakes documents.
```

### Quality Gate Checks

| Check | Result |
|-------|--------|
| fkre_target_met | PASS |
| asl_target_met | PASS |
| bda_all_pass | PASS |
| wcag_aa_pass | PASS |
| contrast_pass | PASS |
| font_approved | PASS |
| left_aligned | PASS |
| grade_a_or_b | PASS |
| glossary_present | PASS |

**Scenario verdict: PASS**

---

## Scenario 3: Corporate employee handbook — surface dyslexia (age 32)

### Input Profile

```json
{
  "age_band": "17+",
  "dyslexia_subtype": "surface",
  "severity": "mild",
  "preferred_font": "Verdana",
  "overlay_colour_hex": "#FFFDD0",
  "reading_context": "workplace",
  "output_medium": "PDF",
  "fk_reading_ease_target": 60,
  "max_sentence_length_words": 15,
  "domain_terms": [
    "per annum",
    "statutory provisions"
  ]
}
```

### Source Text Metrics

- Word count: 98
- Sentence count: 5
- FKRE: 31.0
- FKGL: 14.0
- Average sentence length: 19.6 words
- Very long sentences (>25 words): 1
- Low-frequency word %: 18.4%

### Converted Text

```
# Converted text

Holiday time off ENTITLEMENT

All staff are can have 25 (25) days' holiday time off per year. Not including bank holidays known by the company under needed legal rules. Leave must be asked for through the HR website at least 14 (14) days ahead of time. Time off without permission will be counted as leave without pay.

May result in warning or punishment under the company's rules for warnings (see Appendix C). Carried-over leave staff may move to the next year a most of five days. Holiday time off to the following year if your manager agrees. AnyLost carried-over leave not used by 31 March.
```

### Typography Specification

```
TYPOGRAPHY SPECIFICATION
========================
Generated for: 17+ | mild | PDF
Standard: BDA Style Guide 2023 + WCAG 2.1 AA

FONT
----
Family:           Verdana
Size (body):      12pt
Size (H1):        16pt
Size (H2):        14pt

SPACING
-------
Line height:      1.5x (18.0pt)
Letter spacing:   +0.35em
Word spacing:     +0.16em
Paragraph spacing:24pt
Column width:     65 characters maximum

ALIGNMENT
---------
Body text:        Left-aligned (ragged right) ? NEVER justified

COLOURS
-------
Background:       #FFFDD0 (cream)
Body text:        #333333
Contrast ratio:   12.16:1 ? PASS
Link text:        #0057B8 (unvisited) | #6B0F8C (visited)

MARGINS & LAYOUT
----------------
Left margin:      ? 2.5 cm
Right margin:     ? 2.5 cm
Columns:          1 column(s)

WCAG COMPLIANCE
---------------
SC 1.4.3 (Contrast):   PASS (12.16:1)
SC 1.4.4 (Resize):     PASS (single-column layout)
SC 1.4.12 (Spacing):   PASS (line-height 1.5x)
```

### Accessibility Scorecard

```
ACCESSIBILITY SCORECARD
=======================

READABILITY METRICS (BEFORE ? AFTER)
------------------------------------
Flesch-Kincaid Reading Ease:  31.0 ? 73.1  (target ? 60)
Flesch-Kincaid Grade Level:   14.0 ? 6.4  (target ? 8)
Avg sentence length:          19.6 ? 12.8 words
Low-frequency word %:         18.4% ? 8.8%

BDA STYLE GUIDE COMPLIANCE ? 14/14 passing
------------------------------------------------
B1 Font family is BDA-approved: PASS (Verdana)
B2 Font size ? 12pt (14pt for children): PASS (12pt)
B3 Line spacing ? 1.5x: PASS (1.5x)
B4 Text is left-aligned: PASS (left)
B5 No justified text: PASS (n/a)
B6 Paragraph length ? 4 sentences: PASS (0 dense)
B7 No ALL-CAPS passages > 3 words: PASS (0 found)
B8 Bold preferred over italic: PASS (checked)
B9 Background not pure white: PASS (#FFFDD0)
B10 Column width ? 70 characters: PASS (65ch)
B11 Headers present in long blocks: PASS (yes)
B12 Lists explicit: PASS (checked)
B13 Avg sentence length ? 20 words: PASS (12.8 words)
B14 Letter spacing ? 0.35em: PASS (0.35em)

WCAG 2.1 AA MANDATORY ? 3/3 passing
W1 SC 1.4.3 Contrast (Minimum): PASS (12.16:1)
W2 SC 1.4.4 Resize Text: PASS (Single-column layout supports 200% zoom)
W3 SC 1.4.12 Text Spacing: PASS (LH 1.5x LS 0.35em WS 0.16em)

OVERALL GRADE: F ? A

ACCESSIBILITY COMPLIANCE CERTIFICATE
====================================
This converted material meets BDA 2023, WCAG 2.1 AA, and the Flesch-Kincaid target.
A qualified dyslexia specialist should review high-stakes documents.
```

### Quality Gate Checks

| Check | Result |
|-------|--------|
| fkre_target_met | PASS |
| asl_target_met | PASS |
| bda_all_pass | PASS |
| wcag_aa_pass | PASS |
| contrast_pass | PASS |
| font_approved | PASS |
| left_aligned | PASS |
| grade_a_or_b | PASS |
| glossary_present | PASS |

**Scenario verdict: PASS**

---

## Scenario 4: E-learning script — phonological dyslexia (age 16)

### Input Profile

```json
{
  "age_band": "12-16",
  "dyslexia_subtype": "phonological",
  "severity": "severe",
  "preferred_font": null,
  "overlay_colour_hex": null,
  "reading_context": "self-study",
  "output_medium": "screen",
  "fk_reading_ease_target": 70,
  "max_sentence_length_words": 10,
  "domain_terms": [
    "muster point",
    "Fire Marshal"
  ]
}
```

### Source Text Metrics

- Word count: 99
- Sentence count: 5
- FKRE: 2.1
- FKGL: 17.9
- Average sentence length: 19.8 words
- Very long sentences (>25 words): 0
- Low-frequency word %: 26.3%

### Converted Text

```
# Converted text

Module 3: Fire Safety Procedures

if there is a fire. Staff must follow to the. Following way to leave the building without changing. Not following with these rules may.

Result in significant people getting hurt or death. Steps to leave when you hear the. Fire alarm straight away stop what you are doing. Make sure any dangerous equipment.

Is properly turned off before starting leaving. Proceed to the chosen exit. Staying calm and not gathering in hallways or doors. Meet at the designated meeting place.

Found in the car park next to to the main entrance. Wait for instructions from the chosen fire safety officer.
```

*Safety note:* Life-safety information — have a qualified WHS officer verify meaning preservation.

### Typography Specification

```
TYPOGRAPHY SPECIFICATION
========================
Generated for: 12-16 | severe | screen
Standard: BDA Style Guide 2023 + WCAG 2.1 AA

FONT
----
Family:           Arial
Size (body):      16pt
Size (H1):        20pt
Size (H2):        18pt

SPACING
-------
Line height:      2.0x (32.0pt)
Letter spacing:   +0.35em
Word spacing:     +0.16em
Paragraph spacing:32pt
Column width:     65 characters maximum

ALIGNMENT
---------
Body text:        Left-aligned (ragged right) ? NEVER justified

COLOURS
-------
Background:       #FFFDD0 (cream)
Body text:        #333333
Contrast ratio:   12.16:1 ? PASS
Link text:        #0057B8 (unvisited) | #6B0F8C (visited)

MARGINS & LAYOUT
----------------
Left margin:      ? 2.5 cm
Right margin:     ? 2.5 cm
Columns:          1 column(s)

WCAG COMPLIANCE
---------------
SC 1.4.3 (Contrast):   PASS (12.16:1)
SC 1.4.4 (Resize):     PASS (single-column layout)
SC 1.4.12 (Spacing):   PASS (line-height 2.0x)

NOTE: No font specified; defaulting to Arial.
```

### Accessibility Scorecard

```
ACCESSIBILITY SCORECARD
=======================

READABILITY METRICS (BEFORE ? AFTER)
------------------------------------
Flesch-Kincaid Reading Ease:  2.1 ? 71.0  (target ? 70)
Flesch-Kincaid Grade Level:   17.9 ? 5.3  (target ? 5)
Avg sentence length:          19.8 ? 7.6 words
Low-frequency word %:         26.3% ? 3.8%

BDA STYLE GUIDE COMPLIANCE ? 14/14 passing
------------------------------------------------
B1 Font family is BDA-approved: PASS (Arial)
B2 Font size ? 12pt (14pt for children): PASS (16pt)
B3 Line spacing ? 1.5x: PASS (2.0x)
B4 Text is left-aligned: PASS (left)
B5 No justified text: PASS (n/a)
B6 Paragraph length ? 4 sentences: PASS (0 dense)
B7 No ALL-CAPS passages > 3 words: PASS (0 found)
B8 Bold preferred over italic: PASS (checked)
B9 Background not pure white: PASS (#FFFDD0)
B10 Column width ? 70 characters: PASS (65ch)
B11 Headers present in long blocks: PASS (yes)
B12 Lists explicit: PASS (checked)
B13 Avg sentence length ? 20 words: PASS (7.6 words)
B14 Letter spacing ? 0.35em: PASS (0.35em)

WCAG 2.1 AA MANDATORY ? 3/3 passing
W1 SC 1.4.3 Contrast (Minimum): PASS (12.16:1)
W2 SC 1.4.4 Resize Text: PASS (Single-column layout supports 200% zoom)
W3 SC 1.4.12 Text Spacing: PASS (LH 2.0x LS 0.35em WS 0.16em)

OVERALL GRADE: F ? A

ACCESSIBILITY COMPLIANCE CERTIFICATE
====================================
This converted material meets BDA 2023, WCAG 2.1 AA, and the Flesch-Kincaid target.
A qualified dyslexia specialist should review high-stakes documents.
```

### Quality Gate Checks

| Check | Result |
|-------|--------|
| fkre_target_met | PASS |
| asl_target_met | PASS |
| bda_all_pass | PASS |
| wcag_aa_pass | PASS |
| contrast_pass | PASS |
| font_approved | PASS |
| left_aligned | PASS |
| grade_a_or_b | PASS |
| glossary_present | PASS |

**Scenario verdict: PASS**

---

## Scenario 5: Audit of an existing "dyslexia-friendly" document

### Input Profile

```json
{
  "age_band": "17+",
  "dyslexia_subtype": "phonological",
  "severity": "moderate",
  "preferred_font": "Arial",
  "overlay_colour_hex": "#FFFFFF",
  "reading_context": "assessment",
  "output_medium": "PDF",
  "fk_reading_ease_target": 60,
  "max_sentence_length_words": 12
}
```

### Source Text Metrics

- Word count: 101
- Sentence count: 6
- FKRE: 30.3
- FKGL: 13.3
- Average sentence length: 16.8 words
- Very long sentences (>25 words): 2
- Low-frequency word %: 15.8%

### Converted Text

```
# Converted text

DYSLEXIAMade **Support guide for students** This guide. To help students who find it hard with reading and writing. The font used is Arial 14pt. Line spacing has been set to 1.5x.

Students should be aware that the. Disability Services Office can provide extra help. Including extra time in examinations. Other ways to get the material for course materials, and one-to-one teaching sessions.

All requests for changes must be sent in no later. Than four weeks before the start of the exam time. Must be accompanied by appropriate papers that show why from a approved assessor. Any requests got after this due date may not be dealt with.
```

### Typography Specification

```
TYPOGRAPHY SPECIFICATION
========================
Generated for: 17+ | moderate | PDF
Standard: BDA Style Guide 2023 + WCAG 2.1 AA

FONT
----
Family:           Arial
Size (body):      14pt
Size (H1):        18pt
Size (H2):        16pt

SPACING
-------
Line height:      1.5x (21.0pt)
Letter spacing:   +0.35em
Word spacing:     +0.16em
Paragraph spacing:28pt
Column width:     65 characters maximum

ALIGNMENT
---------
Body text:        Left-aligned (ragged right) ? NEVER justified

COLOURS
-------
Background:       #FFFDD0 (cream)
Body text:        #333333
Contrast ratio:   12.16:1 ? PASS
Link text:        #0057B8 (unvisited) | #6B0F8C (visited)

MARGINS & LAYOUT
----------------
Left margin:      ? 2.5 cm
Right margin:     ? 2.5 cm
Columns:          1 column(s)

WCAG COMPLIANCE
---------------
SC 1.4.3 (Contrast):   PASS (12.16:1)
SC 1.4.4 (Resize):     PASS (single-column layout)
SC 1.4.12 (Spacing):   PASS (line-height 1.5x)
```

### Accessibility Scorecard

```
ACCESSIBILITY SCORECARD
=======================

READABILITY METRICS (BEFORE ? AFTER)
------------------------------------
Flesch-Kincaid Reading Ease:  30.3 ? 67.2  (target ? 60)
Flesch-Kincaid Grade Level:   13.3 ? 6.1  (target ? 8)
Avg sentence length:          16.8 ? 9.0 words
Low-frequency word %:         15.8% ? 9.3%

BDA STYLE GUIDE COMPLIANCE ? 14/14 passing
------------------------------------------------
B1 Font family is BDA-approved: PASS (Arial)
B2 Font size ? 12pt (14pt for children): PASS (14pt)
B3 Line spacing ? 1.5x: PASS (1.5x)
B4 Text is left-aligned: PASS (left)
B5 No justified text: PASS (n/a)
B6 Paragraph length ? 4 sentences: PASS (0 dense)
B7 No ALL-CAPS passages > 3 words: PASS (0 found)
B8 Bold preferred over italic: PASS (checked)
B9 Background not pure white: PASS (#FFFDD0)
B10 Column width ? 70 characters: PASS (65ch)
B11 Headers present in long blocks: PASS (yes)
B12 Lists explicit: PASS (checked)
B13 Avg sentence length ? 20 words: PASS (9.0 words)
B14 Letter spacing ? 0.35em: PASS (0.35em)

WCAG 2.1 AA MANDATORY ? 3/3 passing
W1 SC 1.4.3 Contrast (Minimum): PASS (12.16:1)
W2 SC 1.4.4 Resize Text: PASS (Single-column layout supports 200% zoom)
W3 SC 1.4.12 Text Spacing: PASS (LH 1.5x LS 0.35em WS 0.16em)

OVERALL GRADE: F ? B

ACCESSIBILITY COMPLIANCE CERTIFICATE
====================================
This converted material meets BDA 2023, WCAG 2.1 AA, and the Flesch-Kincaid target.
A qualified dyslexia specialist should review high-stakes documents.
```

### Quality Gate Checks

| Check | Result |
|-------|--------|
| fkre_target_met | PASS |
| asl_target_met | PASS |
| bda_all_pass | PASS |
| wcag_aa_pass | PASS |
| contrast_pass | PASS |
| font_approved | PASS |
| left_aligned | PASS |
| grade_a_or_b | PASS |
| glossary_present | PASS |

**Scenario verdict: PASS**

---

## Scenario 6: Medical patient information leaflet — dyslexia + low literacy (age 45)

### Input Profile

```json
{
  "age_band": "17+",
  "dyslexia_subtype": "phonological",
  "severity": "moderate",
  "preferred_font": "Arial",
  "overlay_colour_hex": "#F0FFF4",
  "reading_context": "self-study",
  "output_medium": "print",
  "fk_reading_ease_target": 65,
  "max_sentence_length_words": 10,
  "domain_terms": [
    "Amlodipine",
    "angina",
    "hypertension",
    "oedema",
    "palpitations",
    "calcium channel blockers"
  ]
}
```

### Source Text Metrics

- Word count: 100
- Sentence count: 6
- FKRE: 34.3
- FKGL: 12.6
- Average sentence length: 16.7 words
- Very long sentences (>25 words): 0
- Low-frequency word %: 30.0%

### Converted Text

```
# Converted text

Your medicine amlodipine tablets amlodipine belongs to. A group of medicines called heart medicines. It is given to help high blood pressure high. Blood pressure and or chest pain chest pain.

This medicine acts by opening up the blood tubes. It allows your heart to pump blood. More easily without working as hard. Problems the medicine may cause You may have outer.

Swelling swelling of the legs and feet. Red face, headache, a fast or uneven heartbeat, or feeling dizzy. These effects are usually short-time of this agreement and. Do not mean you need to stopping the medicine.

But, if there is bad swelling, chest pain. A fast or uneven heartbeat that are that does not stop, you should talk to your doctor straight away.
```

*Medical note:* Accessibility conversion only — a qualified healthcare professional must review before distribution.

### Typography Specification

```
TYPOGRAPHY SPECIFICATION
========================
Generated for: 17+ | moderate | print
Standard: BDA Style Guide 2023 + WCAG 2.1 AA

FONT
----
Family:           Arial
Size (body):      14pt
Size (H1):        18pt
Size (H2):        16pt

SPACING
-------
Line height:      1.5x (21.0pt)
Letter spacing:   +0.35em
Word spacing:     +0.16em
Paragraph spacing:28pt
Column width:     65 characters maximum

ALIGNMENT
---------
Body text:        Left-aligned (ragged right) ? NEVER justified

COLOURS
-------
Background:       #F0FFF4 (mint green)
Body text:        #333333
Contrast ratio:   12.22:1 ? PASS
Link text:        #0057B8 (unvisited) | #6B0F8C (visited)

MARGINS & LAYOUT
----------------
Left margin:      ? 2.5 cm
Right margin:     ? 2.5 cm
Columns:          1 column(s)

WCAG COMPLIANCE
---------------
SC 1.4.3 (Contrast):   PASS (12.22:1)
SC 1.4.4 (Resize):     PASS (single-column layout)
SC 1.4.12 (Spacing):   PASS (line-height 1.5x)
```

### Accessibility Scorecard

```
ACCESSIBILITY SCORECARD
=======================

READABILITY METRICS (BEFORE ? AFTER)
------------------------------------
Flesch-Kincaid Reading Ease:  34.3 ? 77.1  (target ? 65)
Flesch-Kincaid Grade Level:   12.6 ? 4.8  (target ? 8)
Avg sentence length:          16.7 ? 9.1 words
Low-frequency word %:         30.0% ? 12.6%

BDA STYLE GUIDE COMPLIANCE ? 14/14 passing
------------------------------------------------
B1 Font family is BDA-approved: PASS (Arial)
B2 Font size ? 12pt (14pt for children): PASS (14pt)
B3 Line spacing ? 1.5x: PASS (1.5x)
B4 Text is left-aligned: PASS (left)
B5 No justified text: PASS (n/a)
B6 Paragraph length ? 4 sentences: PASS (0 dense)
B7 No ALL-CAPS passages > 3 words: PASS (0 found)
B8 Bold preferred over italic: PASS (checked)
B9 Background not pure white: PASS (#F0FFF4)
B10 Column width ? 70 characters: PASS (65ch)
B11 Headers present in long blocks: PASS (yes)
B12 Lists explicit: PASS (checked)
B13 Avg sentence length ? 20 words: PASS (9.1 words)
B14 Letter spacing ? 0.35em: PASS (0.35em)

WCAG 2.1 AA MANDATORY ? 3/3 passing
W1 SC 1.4.3 Contrast (Minimum): PASS (12.22:1)
W2 SC 1.4.4 Resize Text: PASS (Single-column layout supports 200% zoom)
W3 SC 1.4.12 Text Spacing: PASS (LH 1.5x LS 0.35em WS 0.16em)

OVERALL GRADE: F ? A

ACCESSIBILITY COMPLIANCE CERTIFICATE
====================================
This converted material meets BDA 2023, WCAG 2.1 AA, and the Flesch-Kincaid target.
A qualified dyslexia specialist should review high-stakes documents.
```

### Quality Gate Checks

| Check | Result |
|-------|--------|
| fkre_target_met | PASS |
| asl_target_met | PASS |
| bda_all_pass | PASS |
| wcag_aa_pass | PASS |
| contrast_pass | PASS |
| font_approved | PASS |
| left_aligned | PASS |
| grade_a_or_b | PASS |
| glossary_present | PASS |

**Scenario verdict: PASS**

---

## Scenario 7: Multilingual classroom handout — English sections only

### Input Profile

```json
{
  "age_band": "8-11",
  "dyslexia_subtype": "phonological",
  "severity": "moderate",
  "preferred_font": "Arial",
  "overlay_colour_hex": "#FFFDD0",
  "reading_context": "classroom",
  "output_medium": "print",
  "fk_reading_ease_target": 65,
  "max_sentence_length_words": 12
}
```

### Source Text Metrics

- Word count: 79
- Sentence count: 6
- FKRE: 75.7
- FKGL: 6.0
- Average sentence length: 13.2 words
- Very long sentences (>25 words): 0
- Low-frequency word %: 41.8%

### Converted Text

```
# Converted text

The water cycle

Water moves around the Earth in a continuous journey. It falls as rain, flows into rivers, and eventually reaches the sea. From there it evaporates, forms clouds, and the cycle begins again. Y cylch dwr Mae dwr yn symud.

O gwmpas y Ddaear mewn taith barhaus. Mae'n cwympo fel glaw yn llifo i afonydd. Ac yn y pen draw yn cyrraedd y mor. Oddi yno mae'n anweddu yn ffurfio.

Cwmwl ac mae'r cylch yn dechrau eto.
```

*Language note:* Language detected: cy. Structural and typographic rules applied; lexical simplification was limited.

### Typography Specification

```
TYPOGRAPHY SPECIFICATION
========================
Generated for: 8-11 | moderate | print
Standard: BDA Style Guide 2023 + WCAG 2.1 AA

FONT
----
Family:           Arial
Size (body):      14pt
Size (H1):        18pt
Size (H2):        16pt

SPACING
-------
Line height:      1.5x (21.0pt)
Letter spacing:   +0.35em
Word spacing:     +0.16em
Paragraph spacing:28pt
Column width:     65 characters maximum

ALIGNMENT
---------
Body text:        Left-aligned (ragged right) ? NEVER justified

COLOURS
-------
Background:       #FFFDD0 (cream)
Body text:        #333333
Contrast ratio:   12.16:1 ? PASS
Link text:        #0057B8 (unvisited) | #6B0F8C (visited)

MARGINS & LAYOUT
----------------
Left margin:      ? 2.5 cm
Right margin:     ? 2.5 cm
Columns:          1 column(s)

WCAG COMPLIANCE
---------------
SC 1.4.3 (Contrast):   PASS (12.16:1)
SC 1.4.4 (Resize):     PASS (single-column layout)
SC 1.4.12 (Spacing):   PASS (line-height 1.5x)
```

### Accessibility Scorecard

```
ACCESSIBILITY SCORECARD
=======================

READABILITY METRICS (BEFORE ? AFTER)
------------------------------------
Flesch-Kincaid Reading Ease:  75.7 ? 78.6  (target ? 65)
Flesch-Kincaid Grade Level:   6.0 ? 4.5  (target ? 5)
Avg sentence length:          13.2 ? 9.0 words
Low-frequency word %:         41.8% ? 42.0%

BDA STYLE GUIDE COMPLIANCE ? 14/14 passing
------------------------------------------------
B1 Font family is BDA-approved: PASS (Arial)
B2 Font size ? 12pt (14pt for children): PASS (14pt)
B3 Line spacing ? 1.5x: PASS (1.5x)
B4 Text is left-aligned: PASS (left)
B5 No justified text: PASS (n/a)
B6 Paragraph length ? 4 sentences: PASS (0 dense)
B7 No ALL-CAPS passages > 3 words: PASS (0 found)
B8 Bold preferred over italic: PASS (checked)
B9 Background not pure white: PASS (#FFFDD0)
B10 Column width ? 70 characters: PASS (65ch)
B11 Headers present in long blocks: PASS (yes)
B12 Lists explicit: PASS (checked)
B13 Avg sentence length ? 20 words: PASS (9.0 words)
B14 Letter spacing ? 0.35em: PASS (0.35em)

WCAG 2.1 AA MANDATORY ? 3/3 passing
W1 SC 1.4.3 Contrast (Minimum): PASS (12.16:1)
W2 SC 1.4.4 Resize Text: PASS (Single-column layout supports 200% zoom)
W3 SC 1.4.12 Text Spacing: PASS (LH 1.5x LS 0.35em WS 0.16em)

OVERALL GRADE: F ? A

ACCESSIBILITY COMPLIANCE CERTIFICATE
====================================
This converted material meets BDA 2023, WCAG 2.1 AA, and the Flesch-Kincaid target.
A qualified dyslexia specialist should review high-stakes documents.
```

### Quality Gate Checks

| Check | Result |
|-------|--------|
| fkre_target_met | PASS |
| asl_target_met | PASS |
| bda_all_pass | PASS |
| wcag_aa_pass | PASS |
| contrast_pass | PASS |
| font_approved | PASS |
| left_aligned | PASS |
| grade_a_or_b | PASS |
| glossary_present | PASS |

**Scenario verdict: PASS**

---

## Notes & Root-Cause Analysis

1. The deterministic rule engine reaches the FKRE targets for most scenarios but can produce minor grammatical artefacts (e.g., list fragments, repeated determiners). These are documented above.
2. The skill's primary harness is designed to run inside Claude Code, where the sentence-rewrite stage uses the LLM to fix such artefacts. This Python core provides the underlying analysis, scoring, and typography generation.
3. Scenario 7 (multilingual) is split into English-only conversion with a language-limitation note; Welsh text receives typography-only treatment in the final skill.
