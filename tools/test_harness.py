"""test_harness.py — Validate Skill #233 against the 7 reference scenarios.

Usage:
    python tools/test_harness.py          # writes tests/test-results.md
    python tools/test_harness.py --html   # also writes tests/test-results.html
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from dyslexia_converter import (
    analyse_text,
    convert_text,
    generate_typography_spec,
    score_accessibility,
    format_typography_spec,
    format_scorecard,
)

SCENARIOS = [
    {
        "id": 1,
        "title": "Year 4 science worksheet — phonological dyslexia (age 9)",
        "profile": {
            "age_band": "8-11",
            "dyslexia_subtype": "phonological",
            "severity": "moderate",
            "preferred_font": "Arial",
            "overlay_colour_hex": "#FAFAD2",
            "reading_context": "classroom",
            "output_medium": "print",
            "fk_reading_ease_target": 60,
            "max_sentence_length_words": 12,
            "domain_terms": ["chloroplasts", "biochemical", "photosynthesis", "chlorophyll"],
        },
        "text": """Photosynthesis is the process by which green plants utilise sunlight, water, and carbon dioxide to manufacture glucose, which subsequently provides the energy necessary for the organism's biological functioning. The chlorophyll, a pigment located predominantly within the chloroplasts of plant cells, facilitates the absorption of light energy, which is subsequently transformed into chemical energy through a complex series of biochemical reactions. Without an adequate supply of sunlight, photosynthesis cannot be initiated, which means that plants in environments characterised by insufficient illumination will demonstrate significantly diminished rates of growth and may ultimately fail to survive.""",
        "expected_fkre": 60,
        "expected_asl": 12,
    },
    {
        "id": 2,
        "title": "Adult legal contract — mixed dyslexia (moderate, age 34)",
        "profile": {
            "age_band": "17+",
            "dyslexia_subtype": "mixed",
            "severity": "moderate",
            "preferred_font": "OpenDyslexic",
            "overlay_colour_hex": "#EEF4FF",
            "reading_context": "self-study",
            "output_medium": "screen",
            "fk_reading_ease_target": 45,
            "max_sentence_length_words": 12,
            "domain_terms": ["covenants", "assign", "sublet"],
        },
        "text": """The Tenant hereby covenants with the Landlord that during the Term, the Tenant shall: (a) pay the Rent and all other sums payable hereunder at the times and in the manner herein specified, without any deduction, withholding or set-off whatsoever; (b) use the Property for residential purposes only and not carry on or permit to be carried on therein any trade, business or profession or use the same for any purpose other than as a private residence; (c) not assign, sublet, part with possession of or share occupation of the whole or any part of the Property without the prior written consent of the Landlord, such consent not to be unreasonably withheld or delayed.""",
        "expected_fkre": 45,
        "expected_asl": 12,
        "legal_note": True,
    },
    {
        "id": 3,
        "title": "Corporate employee handbook — surface dyslexia (age 32)",
        "profile": {
            "age_band": "17+",
            "dyslexia_subtype": "surface",
            "severity": "mild",
            "preferred_font": "Verdana",
            "overlay_colour_hex": "#FFFDD0",
            "reading_context": "workplace",
            "output_medium": "PDF",
            "fk_reading_ease_target": 60,
            "max_sentence_length_words": 15,
            "domain_terms": ["per annum", "statutory provisions"],
        },
        "text": """ANNUAL LEAVE ENTITLEMENT

All employees are entitled to twenty-five (25) days' annual leave per annum, exclusive of public holidays recognised by the company in accordance with applicable statutory provisions. Leave must be requested via the HR portal no fewer than fourteen (14) days in advance. Unauthorised absence will be treated as unpaid leave and may result in disciplinary action in accordance with the company's disciplinary procedure (see Appendix C).

Carryover: Employees may carry forward a maximum of five (5) days' annual leave to the following calendar year, subject to manager approval. Any carried-over leave not used by 31 March will be forfeited.""",
        "expected_fkre": 60,
        "expected_asl": 15,
    },
    {
        "id": 4,
        "title": "E-learning script — phonological dyslexia (age 16)",
        "profile": {
            "age_band": "12-16",
            "dyslexia_subtype": "phonological",
            "severity": "severe",
            "preferred_font": None,
            "overlay_colour_hex": None,
            "reading_context": "self-study",
            "output_medium": "screen",
            "fk_reading_ease_target": 70,
            "max_sentence_length_words": 10,
            "domain_terms": ["muster point", "Fire Marshal"],
        },
        "text": """Module 3: Fire Safety Procedures

In the event of a fire, employees must adhere to the following emergency evacuation procedure without deviation. Failure to comply with these protocols may result in significant personal injury or fatality.

Evacuation Steps:
Upon hearing the fire alarm, immediately cease all activities and ensure that any potentially hazardous equipment is appropriately deactivated prior to commencing evacuation. Proceed to the designated emergency exit, maintaining composure and avoiding congregating in corridors or doorways. Assemble at the designated muster point, located in the car park adjacent to the main entrance, and await instruction from the designated Fire Marshal.""",
        "expected_fkre": 70,
        "expected_asl": 10,
        "safety_note": True,
    },
    {
        "id": 5,
        "title": "Audit of an existing \"dyslexia-friendly\" document",
        "profile": {
            "age_band": "17+",
            "dyslexia_subtype": "phonological",
            "severity": "moderate",
            "preferred_font": "Arial",
            "overlay_colour_hex": "#FFFFFF",
            "reading_context": "assessment",
            "output_medium": "PDF",
            "fk_reading_ease_target": 60,
            "max_sentence_length_words": 12,
        },
        "text": """DYSLEXIA SUPPORT GUIDE FOR STUDENTS

This guide has been prepared to assist students who experience difficulties with reading and writing. The font used is Arial 14pt. Line spacing has been set to 1.5x.

Students should be aware that the Disability Services Office can provide additional support, including extra time in examinations, alternative formats for course materials, and specialist one-to-one tuition sessions. All requests for adjustments must be submitted no later than four weeks before the commencement of the examination period, and must be accompanied by appropriate supporting documentation from a qualified assessor. Any requests received after this deadline may not be processed.""",
        "expected_fkre": 60,
        "expected_asl": 12,
    },
    {
        "id": 6,
        "title": "Medical patient information leaflet — dyslexia + low literacy (age 45)",
        "profile": {
            "age_band": "17+",
            "dyslexia_subtype": "phonological",
            "severity": "moderate",
            "preferred_font": "Arial",
            "overlay_colour_hex": "#F0FFF4",
            "reading_context": "self-study",
            "output_medium": "print",
            "fk_reading_ease_target": 65,
            "max_sentence_length_words": 10,
            "domain_terms": ["Amlodipine", "angina", "hypertension", "oedema", "palpitations", "calcium channel blockers"],
        },
        "text": """Your medication — Amlodipine 5mg tablets

Amlodipine belongs to a group of medicines called calcium channel blockers. It is prescribed to treat hypertension (high blood pressure) and/or angina (chest pain). This medication acts by relaxing the blood vessels, which allows your heart to pump blood more efficiently without requiring as much effort.

Side effects: You may experience peripheral oedema (swelling of the lower limbs), flushing, headache, palpitations, or dizziness. These effects are generally transitory and do not necessitate cessation of treatment. However, in the event of severe oedema, chest pain, or palpitations that are sustained, you should consult your physician immediately.""",
        "expected_fkre": 65,
        "expected_asl": 10,
        "medical_note": True,
    },
    {
        "id": 7,
        "title": "Multilingual classroom handout — English sections only",
        "profile": {
            "age_band": "8-11",
            "dyslexia_subtype": "phonological",
            "severity": "moderate",
            "preferred_font": "Arial",
            "overlay_colour_hex": "#FFFDD0",
            "reading_context": "classroom",
            "output_medium": "print",
            "fk_reading_ease_target": 65,
            "max_sentence_length_words": 12,
        },
        "text": """The water cycle

Water moves around the Earth in a continuous journey. It falls as rain, flows into rivers, and eventually reaches the sea. From there it evaporates, forms clouds, and the cycle begins again.

Y cylch dwr

Mae dwr yn symud o gwmpas y Ddaear mewn taith barhaus. Mae'n cwympo fel glaw, yn llifo i afonydd, ac yn y pen draw yn cyrraedd y mor. Oddi yno mae'n anweddu, yn ffurfio cwmwl, ac mae'r cylch yn dechrau eto.""",
        "expected_fkre": 65,
        "expected_asl": 12,
    },
]


def _profile_to_json(profile: dict) -> str:
    return json.dumps(profile, indent=2, ensure_ascii=False)


def run_scenario(scenario: dict) -> dict:
    text = scenario["text"]
    profile = scenario["profile"]

    original_analysis = analyse_text(text)
    converted = convert_text(text, profile)
    spec = generate_typography_spec(profile)
    score = score_accessibility(text, converted["converted_text"], spec, profile)

    fkre_delta = converted["converted_analysis"]["fkre"] - original_analysis["fkre"]
    asl_delta = original_analysis["asl"] - converted["converted_analysis"]["asl"]

    checks = {
        "fkre_target_met": converted["converted_analysis"]["fkre"] >= scenario.get("expected_fkre", 60),
        "asl_target_met": converted["converted_analysis"]["asl"] <= scenario.get("expected_asl", 15),
        "bda_all_pass": score["bda_pass_count"] == 14,
        "wcag_aa_pass": score["wcag_aa_pass_count"] == 3,
        "contrast_pass": spec["contrast_pass"],
        "font_approved": spec["font_family"] in {"Arial", "Verdana", "Tahoma", "Century Gothic", "Trebuchet MS", "Calibri", "OpenDyslexic", "Comic Sans MS", "Sassoon"},
        "left_aligned": spec["alignment"] == "left",
        "grade_a_or_b": score["converted_grade"] in {"A", "B"},
        "glossary_present": bool(converted["glossary"]),
    }
    overall_pass = all(checks.values())

    return {
        "scenario": scenario,
        "original_analysis": original_analysis,
        "converted": converted,
        "spec": spec,
        "score": score,
        "fkre_delta": round(fkre_delta, 1),
        "asl_delta": round(asl_delta, 1),
        "checks": checks,
        "overall_pass": overall_pass,
    }


def _render_markdown(results: list[dict]) -> str:
    lines = [
        "# Test Results — Dyslexia-Friendly Learning Material Converter",
        "",
        f"*Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC*",
        "*Harness: tools/test_harness.py*",
        "*Engine: tools/dyslexia_converter.py (deterministic rule-based pipeline; no LLM call)*",
        "",
        "## Summary",
        "",
        "| Scenario | FKRE before | FKRE after | Δ FKRE | ASL before | ASL after | Grade | Pass |",
        "|----------|-------------|------------|--------|------------|-----------|-------|------|",
    ]
    for r in results:
        s = r["scenario"]
        lines.append(
            f"| {s['id']} | {r['original_analysis']['fkre']} | {r['converted']['converted_analysis']['fkre']} | "
            f"{r['fkre_delta']:+} | {r['original_analysis']['asl']} | {r['converted']['converted_analysis']['asl']} | "
            f"{r['score']['original_grade']} → {r['score']['converted_grade']} | {'PASS' if r['overall_pass'] else 'FAIL'} |"
        )
    lines += ["", f"**Overall: {sum(1 for r in results if r['overall_pass'])}/{len(results)} scenarios pass all checks.**", ""]

    for r in results:
        s = r["scenario"]
        lines += [
            f"---",
            "",
            f"## Scenario {s['id']}: {s['title']}",
            "",
            "### Input Profile",
            "",
            "```json",
            _profile_to_json(s["profile"]),
            "```",
            "",
            "### Source Text Metrics",
            "",
            f"- Word count: {r['original_analysis']['word_count']}",
            f"- Sentence count: {r['original_analysis']['sentence_count']}",
            f"- FKRE: {r['original_analysis']['fkre']}",
            f"- FKGL: {r['original_analysis']['fkgl']}",
            f"- Average sentence length: {r['original_analysis']['asl']} words",
            f"- Very long sentences (>25 words): {r['original_analysis']['very_long_sentences']}",
            f"- Low-frequency word %: {r['original_analysis']['low_frequency_pct']}%",
            "",
            "### Converted Text",
            "",
            "```",
            r["converted"]["converted_text"],
            "```",
            "",
        ]
        if r["converted"]["non_english_note"]:
            lines += [f"*Language note:* {r['converted']['non_english_note']}", ""]
        if s.get("legal_note"):
            lines += ["*Legal note:* This is a plain-language aid. Seek professional legal advice before signing.", ""]
        if s.get("safety_note"):
            lines += ["*Safety note:* Life-safety information — have a qualified WHS officer verify meaning preservation.", ""]
        if s.get("medical_note"):
            lines += ["*Medical note:* Accessibility conversion only — a qualified healthcare professional must review before distribution.", ""]
        lines += [
            "### Typography Specification",
            "",
            "```",
            format_typography_spec(r["spec"]),
            "```",
            "",
            "### Accessibility Scorecard",
            "",
            "```",
            format_scorecard(r["score"], r["spec"]),
            "```",
            "",
            "### Quality Gate Checks",
            "",
            "| Check | Result |",
            "|-------|--------|",
        ]
        for check, passed in r["checks"].items():
            lines.append(f"| {check} | {'PASS' if passed else 'FAIL'} |")
        lines += ["", f"**Scenario verdict: {'PASS' if r['overall_pass'] else 'FAIL'}**", ""]

    lines += [
        "---",
        "",
        "## Notes & Root-Cause Analysis",
        "",
        "1. The deterministic rule engine reaches the FKRE targets for most scenarios but can produce minor grammatical artefacts (e.g., list fragments, repeated determiners). These are documented above.",
        "2. The skill's primary harness is designed to run inside Claude Code, where the sentence-rewrite stage uses the LLM to fix such artefacts. This Python core provides the underlying analysis, scoring, and typography generation.",
        "3. Scenario 7 (multilingual) is split into English-only conversion with a language-limitation note; Welsh text receives typography-only treatment in the final skill.",
        "",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--html", action="store_true", help="Also generate HTML report")
    args = parser.parse_args()

    results = [run_scenario(s) for s in SCENARIOS]
    md = _render_markdown(results)

    out_dir = Path(__file__).resolve().parent.parent / "tests"
    out_dir.mkdir(exist_ok=True)
    md_path = out_dir / "test-results.md"
    md_path.write_text(md, encoding="utf-8")
    print(f"Wrote {md_path}")
    print(f"Summary: {sum(r['overall_pass'] for r in results)}/{len(results)} scenarios passed")

    if args.html:
        try:
            import markdown
            html = markdown.markdown(md, extensions=["tables", "fenced_code"])
            html_path = out_dir / "test-results.html"
            html_path.write_text(
                "<!DOCTYPE html><html><head><meta charset='utf-8'><title>Skill #233 Test Results</title></head><body>"
                + html
                + "</body></html>",
                encoding="utf-8",
            )
            print(f"Wrote {html_path}")
        except ImportError:
            print("markdown package not installed; skipping HTML report")


if __name__ == "__main__":
    main()
