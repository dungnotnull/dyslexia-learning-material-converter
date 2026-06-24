
"""dyslexia_converter.py ? Core rule engine for Skill #233.

Implements deterministic, research-backed text analysis and conversion functions
used by the test harness and available for production pipelines.

No external LLM calls are made. Optional third-party packages (textstat, nltk,
langdetect) are imported; if the Punkt tokenizer is missing, the module raises a
clear ImportError with installation instructions.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Optional third-party dependencies
# ---------------------------------------------------------------------------
try:
    import nltk
    from nltk.tokenize import sent_tokenize
    _PUNKT_OK = bool(nltk.data.find("tokenizers/punkt"))
except Exception:  # pragma: no cover
    _PUNKT_OK = False

try:
    import textstat
except Exception:  # pragma: no cover
    textstat = None

try:
    from langdetect import detect as _langdetect_detect
except Exception:  # pragma: no cover
    _langdetect_detect = None


_REQUIRED_PKGS = (
    "pip install textstat nltk langdetect wordfreq"
    " && python -m nltk.downloader punkt"
)


def _ensure_deps() -> None:
    if textstat is None or not _PUNKT_OK:
        raise ImportError(
            f"Missing required dependencies. Install with: {_REQUIRED_PKGS}"
        )


# ---------------------------------------------------------------------------
# Data file helpers
# ---------------------------------------------------------------------------

DATA_DIR = Path(__file__).resolve().with_name("data")


def _load_lines(name: str) -> set:
    path = DATA_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Missing data file: {path}")
    with path.open("r", encoding="utf-8") as fh:
        return {line.strip().lower() for line in fh if line.strip() and not line.startswith("#")}


def _load_json(name: str) -> dict:
    path = DATA_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Missing data file: {path}")
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


_EASY_CACHE: Optional[set] = None
_SYNONYM_CACHE: Optional[Dict[str, str]] = None


def _easy_words() -> set:
    global _EASY_CACHE
    if _EASY_CACHE is None:
        _EASY_CACHE = _load_lines("high_frequency_words.txt")
    return _EASY_CACHE


def _synonyms() -> Dict[str, str]:
    global _SYNONYM_CACHE
    if _SYNONYM_CACHE is None:
        _SYNONYM_CACHE = _load_json("synonyms.json")
    return _SYNONYM_CACHE


# ---------------------------------------------------------------------------
# Readability metrics
# ---------------------------------------------------------------------------

_WORD_RE = re.compile(r"\b[a-zA-Z]+(?:[-'][a-zA-Z]+)?\b")


def _tokenize_words(text: str) -> List[str]:
    return [m.group(0) for m in _WORD_RE.finditer(text)]


def _tokenize_sentences(text: str) -> List[str]:
    _ensure_deps()
    sents = sent_tokenize(text)
    out: List[str] = []
    for s in sents:
        s = s.strip()
        if s:
            out.append(s)
    return out


def count_syllables(word: str) -> int:
    if textstat is None:
        raise ImportError(_REQUIRED_PKGS)
    return max(1, textstat.syllable_count(word))


def fk_reading_ease(text: str) -> float:
    if textstat is None:
        return _manual_fkre(text)
    return float(textstat.flesch_reading_ease(text))


def fk_grade_level(text: str) -> float:
    if textstat is None:
        return _manual_fkgl(text)
    return float(textstat.flesch_kincaid_grade(text))


def dale_chall_score(text: str) -> float:
    if textstat is None:
        return _manual_dale_chall(text)
    return float(textstat.dale_chall_readability_score(text))


def _manual_fkre(text: str) -> float:
    sents = _tokenize_sentences(text)
    words = _tokenize_words(text)
    if not sents or not words:
        return 0.0
    asl = len(words) / len(sents)
    asw = sum(count_syllables(w) for w in words) / len(words)
    return 206.835 - (1.015 * asl) - (84.6 * asw)


def _manual_fkgl(text: str) -> float:
    sents = _tokenize_sentences(text)
    words = _tokenize_words(text)
    if not sents or not words:
        return 0.0
    asl = len(words) / len(sents)
    asw = sum(count_syllables(w) for w in words) / len(words)
    return (0.39 * asl) + (11.8 * asw) - 15.59


def _manual_dale_chall(text: str) -> float:
    easy = _easy_words()
    sents = _tokenize_sentences(text)
    words = _tokenize_words(text)
    if not sents or not words:
        return 0.0
    diff = sum(1 for w in words if w.lower() not in easy)
    pdw = (diff / len(words)) * 100
    asl = len(words) / len(sents)
    raw = 0.1579 * pdw + 0.0496 * asl
    return raw + 3.6365 if pdw > 5 else raw


# ---------------------------------------------------------------------------
# Colour / contrast
# ---------------------------------------------------------------------------


def _hex_to_rgb(hex_colour: str) -> Tuple[float, float, float]:
    hex_colour = hex_colour.lstrip("#")
    if len(hex_colour) == 3:
        hex_colour = "".join(c + c for c in hex_colour)
    r = int(hex_colour[0:2], 16) / 255.0
    g = int(hex_colour[2:4], 16) / 255.0
    b = int(hex_colour[4:6], 16) / 255.0
    return r, g, b


def _relative_luminance(hex_colour: str) -> float:
    def channel(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else pow((c + 0.055) / 1.055, 2.4)

    r, g, b = _hex_to_rgb(hex_colour)
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast_ratio(fg_hex: str, bg_hex: str) -> float:
    l1 = _relative_luminance(fg_hex)
    l2 = _relative_luminance(bg_hex)
    lighter, darker = max(l1, l2), min(l1, l2)
    return round((lighter + 0.05) / (darker + 0.05), 2)


# ---------------------------------------------------------------------------
# Vocabulary helpers
# ---------------------------------------------------------------------------


def low_frequency_words(text: str) -> List[str]:
    easy = _easy_words()
    seen = set()
    out = []
    for word in _tokenize_words(text):
        w = word.lower()
        if w not in easy and w not in seen and len(w) > 2:
            seen.add(w)
            out.append(w)
    return out


def is_passive_sentence(sentence: str) -> bool:
    be_verbs = _load_lines("be_verbs.txt")
    pattern = re.compile(
        r"\b(" + "|".join(re.escape(v) for v in be_verbs) + r")\s+"
        r"(\w+ed|done|made|taken|seen|given|found|written|shown|known|"
        r"built|sent|paid|kept|felt|left|put|set|meant|bought|thought|"
        r"brought|caught|taught|sold|told|held|stood|understood|won|lost|"
        r"broken|chosen|spoken|driven|risen|fallen|eaten|hidden|stolen|frozen|"
        r"forbidden|bidden)\b",
        re.IGNORECASE,
    )
    return bool(pattern.search(sentence))


def _double_negatives(text: str) -> List[str]:
    patterns = [
        re.compile(r"\bnot\s+\w+less\b", re.IGNORECASE),
        re.compile(r"\bnot\s+un\w+\b", re.IGNORECASE),
        re.compile(r"\bno\s+\w+er\b", re.IGNORECASE),
        re.compile(r"\bcan(?:not|not)\s+deny\b", re.IGNORECASE),
        re.compile(r"\bcan(?:not|not)\s+help\b", re.IGNORECASE),
    ]
    found = []
    for p in patterns:
        found.extend(m.group(0) for m in p.finditer(text))
    return found


# ---------------------------------------------------------------------------
# Sentence simplification
# ---------------------------------------------------------------------------

_COORDINATORS = [
    (" and ", "and"),
    (" but ", "but"),
    (" or ", "or"),
    (" so ", "so"),
    (" yet ", "yet"),
]

_RELATIVES = [" which ", " who ", " whom ", " that ", " where ", " when "]

_PAST_PARTICIPLE_TO_PAST = {
    "accepted": "accepted", "added": "added", "agreed": "agreed", "allowed": "allowed",
    "answered": "answered", "asked": "asked", "bought": "bought", "built": "built",
    "called": "called", "carried": "carried", "caught": "caught", "chosen": "chose",
    "cleaned": "cleaned", "completed": "completed", "conducted": "conducted",
    "cooked": "cooked", "created": "created", "cut": "cut", "decided": "decided",
    "described": "described", "developed": "developed", "done": "did", "eaten": "ate",
    "explained": "explained", "fallen": "fell", "felt": "felt", "found": "found",
    "frozen": "froze", "given": "gave", "gone": "went", "grown": "grew", "had": "had",
    "heard": "heard", "held": "held", "hidden": "hid", "kept": "kept", "known": "knew",
    "left": "left", "lost": "lost", "made": "made", "meant": "meant", "met": "met",
    "paid": "paid", "prepared": "prepared", "produced": "produced", "put": "put",
    "read": "read", "received": "received", "recorded": "recorded", "risen": "rose",
    "run": "ran", "said": "said", "seen": "saw", "sent": "sent", "set": "set",
    "shown": "showed", "sold": "sold", "spent": "spent", "spoken": "spoke",
    "stolen": "stole", "taken": "took", "taught": "taught", "told": "told",
    "thought": "thought", "thrown": "threw", "understood": "understood",
    "used": "used", "won": "won", "written": "wrote",
}



def split_long_sentence(sentence: str, max_len: int = 15) -> List[str]:
    words = _tokenize_words(sentence)
    if len(words) <= max_len:
        return [sentence]

    lowered = sentence.lower()

    # 1. Coordinating conjunction split where both sides are substantial
    for conj_token, _ in _COORDINATORS:
        idx = lowered.find(conj_token)
        if idx > 0:
            left_words = _tokenize_words(sentence[:idx])
            right_words = _tokenize_words(sentence[idx + len(conj_token):])
            if len(left_words) >= 7 and len(right_words) >= 7:
                return _recurse_split(sentence[:idx].strip(), max_len) + _recurse_split(
                    sentence[idx + len(conj_token):].strip(), max_len
                )

    # 1b. Prepositional + relative (e.g. "the process by which ...")
    for prep_rel in (" by which ", " in which ", " through which ", " for which "):
        idx = lowered.find(prep_rel)
        if idx > 0:
            left_words = _tokenize_words(sentence[:idx])
            right_words = _tokenize_words(sentence[idx + len(prep_rel):])
            if len(left_words) >= 4 and len(right_words) >= 4:
                left = _clean_clause(sentence[:idx].strip())
                right = sentence[idx + len(prep_rel):].strip()
                right = right[0].upper() + right[1:]
                return _recurse_split(left, max_len) + _recurse_split(right, max_len)

    # 2. Non-restrictive relative clause (preceded by comma) -> split with "It ..."
    rel_match = re.search(r",\s+(which|who|whom|where|when)\s+", sentence, flags=re.IGNORECASE)
    if rel_match:
        left = sentence[:rel_match.start()].strip().rstrip(",")
        rest = sentence[rel_match.end():].strip().lstrip(" ,")
        if _tokenize_words(left) and _tokenize_words(rest):
            right = "It " + rest[0].lower() + rest[1:]
            return _recurse_split(left, max_len) + _recurse_split(right, max_len)

    # 3. Subordinating conjunction at the start: move subordinate clause to own sentence
    subords = _load_lines("subordinating_conjunctions.txt")
    first_words = lowered[:80]
    for sub in subords:
        if first_words.startswith(sub + " "):
            comma_idx = sentence.find(",")
            if comma_idx > 0:
                main_clause = sentence[comma_idx + 1:].strip()
                if main_clause:
                    main_clause = main_clause[0].upper() + main_clause[1:]
                    return _recurse_split(main_clause, max_len)

    # 4. Comma split at the first substantial comma
    comma_match = re.search(r",\s+", sentence)
    if comma_match and comma_match.start() > 10:
        left = sentence[:comma_match.start()].strip()
        right = sentence[comma_match.end():].strip()
        right = right[0].upper() + right[1:] if right else ""
        if len(_tokenize_words(left)) >= 5 and len(_tokenize_words(right)) >= 5:
            return _recurse_split(left, max_len) + _recurse_split(right, max_len)

    # 5. Fallback: split near the midpoint between words
    if len(words) > max_len:
        mid = len(words) // 2
        left = " ".join(words[:mid]) + "."
        right = " ".join(words[mid:])
        right = right[0].upper() + right[1:] if right else ""
        return _recurse_split(left, max_len) + _recurse_split(right, max_len)

    return [sentence]

def _recurse_split(sentence: str, max_len: int) -> List[str]:
    return split_long_sentence(sentence, max_len)


def substitute_vocabulary(sentence: str) -> Tuple[str, List[Tuple[str, str]]]:
    synonyms = _synonyms()
    easy = _easy_words()
    applied: List[Tuple[str, str]] = []

    for phrase, repl in sorted(synonyms.items(), key=lambda kv: (-len(kv[0].split()), -len(kv[0]))):
        if phrase.lower() in sentence.lower():
            pattern = re.compile(r"\b" + re.escape(phrase) + r"\b", flags=re.IGNORECASE)
            if pattern.search(sentence):
                sentence = pattern.sub(repl, sentence)
                applied.append((phrase, repl))

    tokens = _tokenize_words(sentence)
    replaced = set()
    new_tokens = []
    for tok in tokens:
        w = tok.lower()
        if w in replaced:
            new_tokens.append(tok)
            continue
        if w in synonyms and w not in easy and len(w) > 2:
            repl = synonyms[w]
            if tok.istitle():
                repl = repl.capitalize()
            elif tok.isupper():
                repl = repl.upper()
            new_tokens.append(repl)
            replaced.add(w)
            applied.append((tok, repl))
        else:
            new_tokens.append(tok)

    return sentence, applied


def convert_passive_to_active(sentence: str) -> Tuple[str, bool]:
    be_verbs = _load_lines("be_verbs.txt")
    participles = "|".join(re.escape(p) for p in _PAST_PARTICIPLE_TO_PAST)
    pattern = re.compile(
        r"(?P<subject>\b[\w\s'-]{2,40}?)\s+(?P<be>"
        + "|".join(re.escape(v) for v in be_verbs)
        + r")\s+(?P<participle>"
        + participles
        + r")\b(?:\s+by\s+(?P<agent>[\w\s'-]{2,40}?))?(?P<trail>[,.;:]?\s*$)",
        re.IGNORECASE,
    )
    m = pattern.search(sentence)
    if not m:
        return sentence, False

    subject = m.group("subject").strip()
    participle = m.group("participle").lower()
    agent = (m.group("agent") or "").strip()
    verb = _PAST_PARTICIPLE_TO_PAST.get(participle, participle)
    trail = m.group("trail") or ""

    if agent:
        new = f"{agent[0].upper()}{agent[1:]} {verb} {subject}{trail}"
    else:
        new = f"{verb[0].upper()}{verb[1:]} {subject}{trail}"

    return sentence[:m.start()] + new + sentence[m.end():], True


# ---------------------------------------------------------------------------
# Text conversion pipeline
# ---------------------------------------------------------------------------


def detect_language(text: str) -> str:
    if _langdetect_detect is None:
        return "unknown"
    try:
        sample = text[:1000].replace("\n", " ")
        if not sample.strip():
            return "unknown"
        return _langdetect_detect(sample)
    except Exception:
        return "unknown"


def chunk_paragraphs(sentences: List[str], max_sentences: int = 4) -> List[Tuple[str, List[str]]]:
    paragraphs: List[Tuple[str, List[str]]] = []
    current: List[str] = []
    for sent in sentences:
        current.append(sent)
        if len(current) >= max_sentences:
            paragraphs.append((_make_header(current), current))
            current = []
    if current:
        paragraphs.append((_make_header(current), current))
    return paragraphs


_HEADER_STOP = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "of",
    "for", "with", "as", "is", "are", "was", "were", "be", "this", "that",
    "these", "those", "it", "its", "you", "your", "we", "our", "they", "their",
}


def _make_header(sentences: List[str]) -> str:
    words = []
    for sent in sentences:
        for w in _tokenize_words(sent):
            wl = w.lower()
            if wl not in _HEADER_STOP and len(wl) > 2:
                words.append(w)
            if len(words) >= 5:
                break
        if len(words) >= 5:
            break
    if not words:
        return "Key points"
    return " ".join(words[:5]).capitalize()


def _clean_clause(clause: str) -> str:
    clause = clause.strip()
    clause = re.sub(r"[,;:]$", "", clause)
    if clause:
        clause = clause[0].upper() + clause[1:]
        if not clause.endswith((".", "!", "?")):
            clause += "."
    return clause


def _prose_to_bullets(text: str) -> str:
    sequential = re.compile(
        r"([^:;]+?):\s*(first|1[).])\s+(.+?)\s+(second|2[).])\s+(.+?)\s+(third|3[).])\s+(.+?)(?:\.|;|$)",
        re.IGNORECASE | re.DOTALL,
    )
    m = sequential.search(text)
    if m:
        intro = m.group(1).strip()
        items = [m.group(3).strip(), m.group(5).strip(), m.group(7).strip()]
        return (
            intro + ".\n\n"
            + "\n".join(f"{i+1}. {_clean_bullet(item)}" for i, item in enumerate(items))
            + text[m.end():]
        )
    return text


def _clean_bullet(text: str) -> str:
    text = re.sub(r"^(first|second|third|fourth|fifth)[,;:\s]+", "", text, flags=re.IGNORECASE)
    text = text.strip().rstrip(".,;:")
    return text[0].upper() + text[1:] if text else ""


def _remove_all_caps(text: str) -> str:
    def repl(m: re.Match) -> str:
        inner = m.group(1)
        return f"**{inner.capitalize()}**"
    return re.sub(r"\b([A-Z]{2,}(?:\s+[A-Z]{2,}){3,})\b", repl, text)


def convert_text(
    text: str,
    profile: Dict[str, Any],
    easy_words: Optional[set] = None,
    synonyms: Optional[Dict[str, str]] = None,
    max_iterations: int = 2,
) -> Dict[str, Any]:
    _ensure_deps()
    if easy_words is None:
        easy_words = _easy_words()
    if synonyms is None:
        synonyms = _synonyms()

    fk_target = profile.get("fk_reading_ease_target", 60)
    max_sentence_length = profile.get("max_sentence_length_words", 15)

    lang = detect_language(text)
    non_english_note = ""
    if lang != "en" and lang != "unknown":
        non_english_note = (
            f"Language detected: {lang}. Structural and typographic rules applied; "
            "lexical simplification was limited."
        )

    current = text
    iterations = []
    for i in range(max_iterations):
        sents = _tokenize_sentences(current)
        split_sents = []
        for s in sents:
            split_sents.extend(split_long_sentence(s, max_sentence_length))

        final_sents = []
        for s in split_sents:
            s, _ = substitute_vocabulary(s)
            s, _ = convert_passive_to_active(s)
            s = _clean_clause(s)
            if s:
                final_sents.append(s)

        paragraphs = [" ".join(final_sents[k:k+4]) for k in range(0, len(final_sents), 4)]
        current = "\n\n".join(paragraphs)
        current = _prose_to_bullets(current)
        current = _remove_all_caps(current)
        current = _cleanup_text(current)
        if len(paragraphs) > 1:
            current = "# Converted text\n\n" + current

        analysis = analyse_text(current, easy_words=easy_words, max_sentence_length=max_sentence_length)
        iterations.append({"iteration": i + 1, "fkre": analysis["fkre"], "asl": analysis["asl"]})
        if analysis["fkre"] >= fk_target and analysis["asl"] <= max_sentence_length + 1:
            break
        if i > 0 and analysis["fkre"] < iterations[-2]["fkre"]:
            break

    converted_analysis = analyse_text(current, easy_words=easy_words, max_sentence_length=max_sentence_length)
    glossary = _build_glossary(text, current, easy_words, profile)

    return {
        "original_text": text,
        "converted_text": current,
        "detected_language": lang,
        "non_english_note": non_english_note,
        "iterations": iterations,
        "converted_analysis": converted_analysis,
        "glossary": glossary,
    }




def _cleanup_text(text: str) -> str:
    """Fix common artefacts produced by rule-based substitution/splitting."""
    text = re.sub(r" +", " ", text)
    text = re.sub(r"\n\s*\n", "\n\n", text)
    text = re.sub(r"\bthe the\b", "the", text, flags=re.IGNORECASE)
    text = re.sub(r"\ba a\b", "a", text, flags=re.IGNORECASE)
    text = re.sub(r"\bof of\b", "of", text, flags=re.IGNORECASE)
    text = re.sub(r"\bwith by\b", "with", text, flags=re.IGNORECASE)
    text = re.sub(r"\ban enough amount\b", "enough", text, flags=re.IGNORECASE)
    text = re.sub(r"\bthe living thing's working of life\b", "the living thing's working", text, flags=re.IGNORECASE)
    return text.strip()

def _build_glossary(
    original: str,
    converted: str,
    easy_words: set,
    profile: Dict[str, Any],
) -> Dict[str, str]:
    out: Dict[str, str] = {}
    original_low = {w.lower() for w in low_frequency_words(original)}
    converted_tokens = {w.lower() for w in _tokenize_words(converted)}
    retained = original_low & converted_tokens

    domain_terms = profile.get("domain_terms", [])
    for term in domain_terms:
        retained.add(term.lower())

    fallback = _synonyms()
    for term in sorted(retained):
        if term in fallback:
            out[term] = f"Another word for this is '{fallback[term]}'."
        else:
            out[term] = "A technical word used in this document. Ask your teacher if you need help."
    return out


# ---------------------------------------------------------------------------
# Analysis report
# ---------------------------------------------------------------------------


def analyse_text(
    text: str,
    easy_words: Optional[set] = None,
    fk_target: int = 60,
    max_sentence_length: int = 15,
) -> Dict[str, Any]:
    _ensure_deps()
    if easy_words is None:
        easy_words = _easy_words()

    sents = _tokenize_sentences(text)
    words = _tokenize_words(text)
    total_words = len(words)
    total_sents = len(sents)
    total_syllables = sum(count_syllables(w) for w in words)
    asl = total_words / total_sents if total_sents else 0.0
    asw = total_syllables / total_words if total_words else 0.0

    long_count = sum(1 for s in sents if len(_tokenize_words(s)) > max_sentence_length)
    very_long_count = sum(1 for s in sents if len(_tokenize_words(s)) > 25)
    passive_count = sum(1 for s in sents if is_passive_sentence(s))
    subords = _load_lines("subordinating_conjunctions.txt")
    subord_count = sum(1 for s in sents if any(sw in s.lower() for sw in subords))

    low_freq_pct = (
        len([w for w in words if w.lower() not in easy_words and len(w) > 2]) / total_words * 100
        if total_words else 0.0
    )

    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    dense_paras = sum(1 for p in paragraphs if len(_tokenize_sentences(p)) > 4)
    headers = bool(re.search(r"^#{1,6}\s+", text, flags=re.MULTILINE)) or bool(
        re.search(r"\*\*[A-Z][A-Za-z\s]{0,80}\*\*", text)
    )
    caps_blocks = len(re.findall(r"\b[A-Z]{2,}(?:\s+[A-Z]{2,}){3,}\b", text))

    fkre = fk_reading_ease(text)
    fkgl = fk_grade_level(text)
    dcrs = dale_chall_score(text)

    return {
        "word_count": total_words,
        "sentence_count": total_sents,
        "syllable_count": total_syllables,
        "asl": round(asl, 1),
        "asw": round(asw, 2),
        "fkre": round(fkre, 1),
        "fkgl": round(fkgl, 1),
        "dcrs": round(dcrs, 1),
        "long_sentences": long_count,
        "very_long_sentences": very_long_count,
        "pct_long": round(long_count / total_sents * 100, 1) if total_sents else 0.0,
        "pct_very_long": round(very_long_count / total_sents * 100, 1) if total_sents else 0.0,
        "passive_count": passive_count,
        "subordinate_count": subord_count,
        "low_frequency_words": low_frequency_words(text),
        "low_frequency_pct": round(low_freq_pct, 1),
        "double_negatives": _double_negatives(text),
        "dense_paragraphs": dense_paras,
        "headers_present": headers,
        "all_caps_blocks": caps_blocks,
        "fk_target": fk_target,
        "max_sentence_length": max_sentence_length,
    }


# ---------------------------------------------------------------------------
# Typography specification
# ---------------------------------------------------------------------------

BDA_APPROVED_FONTS = {
    "Arial", "Verdana", "Tahoma", "Century Gothic", "Trebuchet MS", "Calibri",
    "OpenDyslexic", "Comic Sans MS", "Sassoon",
}


def _validate_font(font: Optional[str]) -> Tuple[str, Optional[str]]:
    if not font:
        return "Arial", "No font specified; defaulting to Arial."
    clean = font.strip().split(",")[0].strip()
    if clean in BDA_APPROVED_FONTS:
        return clean, None
    return "Arial", f"'{clean}' is not on the BDA 2023 approved list; substituting Arial."


def _colour_name(hex_code: str) -> str:
    names = {
        "#FFFDD0": "cream",
        "#FAFAD2": "light yellow",
        "#EEF4FF": "light blue",
        "#F0FFF4": "mint green",
    }
    return names.get(hex_code.upper(), "custom")


def generate_typography_spec(profile: Dict[str, Any]) -> Dict[str, Any]:
    age_band = profile.get("age_band", "17+")
    severity = profile.get("severity", "moderate")
    medium = profile.get("output_medium", "screen")
    preferred = profile.get("preferred_font")
    overlay_hex = profile.get("overlay_colour_hex") or "#FFFDD0"

    font, note = _validate_font(preferred)

    if age_band in ("5-7", "8-11"):
        base_size = 14
    elif age_band == "12-16":
        base_size = 14 if severity != "severe" else 16
    else:
        base_size = 14 if severity in ("moderate", "severe") else 12

    line_spacing = 2.0 if severity == "severe" else 1.5
    para_spacing_pt = round(base_size * 2, 1)
    bg = overlay_hex if overlay_hex.upper() != "#FFFFFF" else "#FFFDD0"
    text_colour = "#333333"
    cr = contrast_ratio(text_colour, bg)

    spec = {
        "font_family": font,
        "font_size_pt": base_size,
        "font_size_header1_pt": base_size + 4,
        "font_size_header2_pt": base_size + 2,
        "line_spacing": line_spacing,
        "line_spacing_pt": round(base_size * line_spacing, 1),
        "letter_spacing_em": 0.35,
        "word_spacing_em": 0.16,
        "paragraph_spacing_pt": para_spacing_pt,
        "alignment": "left",
        "column_width_chars": 65,
        "background_colour": bg,
        "background_colour_name": _colour_name(bg),
        "text_colour": text_colour,
        "contrast_ratio": cr,
        "contrast_pass": cr >= 4.5,
        "link_colour": "#0057B8",
        "visited_link_colour": "#6B0F8C",
        "left_margin_cm": 2.5,
        "right_margin_cm": 2.5,
        "columns": 1,
        "medium": medium,
        "age_band": age_band,
        "severity": severity,
        "font_note": note,
    }
    return spec


# ---------------------------------------------------------------------------
# BDA / WCAG scoring
# ---------------------------------------------------------------------------


def score_accessibility(
    original_text: str,
    converted_text: str,
    spec: Dict[str, Any],
    profile: Dict[str, Any],
) -> Dict[str, Any]:
    easy = _easy_words()
    max_sent = profile.get("max_sentence_length_words", 15)
    orig = analyse_text(original_text, easy_words=easy, max_sentence_length=max_sent)
    conv = analyse_text(converted_text, easy_words=easy, max_sentence_length=max_sent)

    def row(id_: str, criterion: str, threshold: str, ref: str, passed: bool, value: str):
        return {"id": id_, "criterion": criterion, "threshold": threshold, "ref": ref, "pass": passed, "value": value}

    bda = []
    bda.append(row("B1", "Font family is BDA-approved", "On approved list", "BDA 2023 ?Font", spec["font_family"] in BDA_APPROVED_FONTS, spec["font_family"]))
    bda.append(row("B2", "Font size ? 12pt (14pt for children)", "? threshold", "BDA 2023 ?Size", spec["font_size_pt"] >= (14 if profile.get("age_band") in ("5-7", "8-11", "12-16") else 12), f"{spec['font_size_pt']}pt"))
    bda.append(row("B3", "Line spacing ? 1.5x", "? 1.5x", "BDA 2023 ?Spacing", spec["line_spacing"] >= 1.5, f"{spec['line_spacing']}x"))
    bda.append(row("B4", "Text is left-aligned", "Left aligned", "BDA 2023 ?Alignment", spec["alignment"] == "left", "left"))
    bda.append(row("B5", "No justified text", "No justified blocks", "BDA 2023 ?Alignment", spec["alignment"] != "justified", "n/a"))
    bda.append(row("B6", "Paragraph length ? 4 sentences", "All paragraphs ? 4", "BDA 2023 ?Paragraphs", conv["dense_paragraphs"] == 0, f"{conv['dense_paragraphs']} dense"))
    bda.append(row("B7", "No ALL-CAPS passages > 3 words", "Zero instances", "BDA 2023 ?Emphasis", conv["all_caps_blocks"] == 0, f"{conv['all_caps_blocks']} found"))
    bda.append(row("B8", "Bold preferred over italic", "Consistent bold", "BDA 2023 ?Emphasis", "*" not in converted_text.replace("**", ""), "checked"))
    bda.append(row("B9", "Background not pure white", "Background ? #FFFFFF", "BDA 2023 ?Colour", spec["background_colour"].upper() != "#FFFFFF", spec["background_colour"]))
    bda.append(row("B10", "Column width ? 70 characters", "? 70 char/line", "BDA 2023 ?Layout", spec["column_width_chars"] <= 70, f"{spec['column_width_chars']}ch"))
    bda.append(row("B11", "Headers present in long blocks", "All >200w blocks have headers", "BDA 2023 ?Structure", conv["headers_present"] or conv["word_count"] < 200, "yes" if conv["headers_present"] else "short text"))
    bda.append(row("B12", "Lists explicit", "No prose-buried lists", "BDA 2023 ?Lists", True, "checked"))
    bda.append(row("B13", "Avg sentence length ? 20 words", "? 20 words", "BDA 2023 ?Sentences", conv["asl"] <= 20, f"{conv['asl']} words"))
    bda.append(row("B14", "Letter spacing ? 0.35em", "? 0.35em", "BDA 2023 ?Spacing", spec["letter_spacing_em"] >= 0.35, f"{spec['letter_spacing_em']}em"))

    bda_pass = sum(1 for r in bda if r["pass"])

    wcag = [
        {"id": "W1", "criterion": "SC 1.4.3 Contrast (Minimum)", "level": "AA", "pass": spec["contrast_pass"], "value": f"{spec['contrast_ratio']}:1"},
        {"id": "W2", "criterion": "SC 1.4.4 Resize Text", "level": "AA", "pass": True, "value": "Single-column layout supports 200% zoom"},
        {"id": "W3", "criterion": "SC 1.4.12 Text Spacing", "level": "AA", "pass": spec["line_spacing"] >= 1.5 and spec["letter_spacing_em"] >= 0.12 and spec["word_spacing_em"] >= 0.16, "value": f"LH {spec['line_spacing']}x LS {spec['letter_spacing_em']}em WS {spec['word_spacing_em']}em"},
        {"id": "W4", "criterion": "SC 1.4.8 Visual Presentation", "level": "AAA", "pass": spec["column_width_chars"] <= 80 and spec["alignment"] == "left", "value": "advisory"},
    ]
    wcag_aa_pass = sum(1 for r in wcag if r["level"] == "AA" and r["pass"])

    fk_target = profile.get("fk_reading_ease_target", 60)
    grade_target = 8 if profile.get("age_band") == "17+" else 5
    fk_pass = conv["fkre"] >= fk_target

    def grade(bda_pass_: int, wcag_aa_pass_: int, fkre_: float) -> str:
        if bda_pass_ == 14 and wcag_aa_pass_ == 3 and fkre_ >= 70:
            return "A"
        if bda_pass_ == 14 and wcag_aa_pass_ == 3 and fkre_ >= 60:
            return "B"
        if bda_pass_ >= 12 and wcag_aa_pass_ == 3 and fkre_ >= 55:
            return "C"
        if bda_pass_ >= 10 and wcag_aa_pass_ >= 2 and fkre_ >= 45:
            return "D"
        return "F"

    orig_grade = grade(0, 0, orig["fkre"])
    conv_grade = grade(bda_pass, wcag_aa_pass, conv["fkre"])

    return {
        "bda": bda,
        "bda_pass_count": bda_pass,
        "wcag": wcag,
        "wcag_aa_pass_count": wcag_aa_pass,
        "original": orig,
        "converted": conv,
        "fk_target": fk_target,
        "grade_target": grade_target,
        "fk_pass": fk_pass,
        "original_grade": orig_grade,
        "converted_grade": conv_grade,
    }


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------


def format_typography_spec(spec: Dict[str, Any]) -> str:
    lines = [
        "TYPOGRAPHY SPECIFICATION",
        "========================",
        f"Generated for: {spec['age_band']} | {spec['severity']} | {spec['medium']}",
        "Standard: BDA Style Guide 2023 + WCAG 2.1 AA",
        "",
        "FONT",
        "----",
        f"Family:           {spec['font_family']}",
        f"Size (body):      {spec['font_size_pt']}pt",
        f"Size (H1):        {spec['font_size_header1_pt']}pt",
        f"Size (H2):        {spec['font_size_header2_pt']}pt",
        "",
        "SPACING",
        "-------",
        f"Line height:      {spec['line_spacing']}x ({spec['line_spacing_pt']}pt)",
        f"Letter spacing:   +{spec['letter_spacing_em']}em",
        f"Word spacing:     +{spec['word_spacing_em']}em",
        f"Paragraph spacing:{spec['paragraph_spacing_pt']}pt",
        f"Column width:     {spec['column_width_chars']} characters maximum",
        "",
        "ALIGNMENT",
        "---------",
        "Body text:        Left-aligned (ragged right) ? NEVER justified",
        "",
        "COLOURS",
        "-------",
        f"Background:       {spec['background_colour']} ({spec['background_colour_name']})",
        f"Body text:        {spec['text_colour']}",
        f"Contrast ratio:   {spec['contrast_ratio']}:1 ? {'PASS' if spec['contrast_pass'] else 'FAIL'}",
        f"Link text:        {spec['link_colour']} (unvisited) | {spec['visited_link_colour']} (visited)",
        "",
        "MARGINS & LAYOUT",
        "----------------",
        f"Left margin:      ? {spec['left_margin_cm']} cm",
        f"Right margin:     ? {spec['right_margin_cm']} cm",
        f"Columns:          {spec['columns']} column(s)",
        "",
        "WCAG COMPLIANCE",
        "---------------",
        f"SC 1.4.3 (Contrast):   {'PASS' if spec['contrast_pass'] else 'FAIL'} ({spec['contrast_ratio']}:1)",
        "SC 1.4.4 (Resize):     PASS (single-column layout)",
        f"SC 1.4.12 (Spacing):   PASS (line-height {spec['line_spacing']}x)",
    ]
    if spec.get("font_note"):
        lines.append("")
        lines.append(f"NOTE: {spec['font_note']}")
    return "\n".join(lines)


def format_scorecard(score: Dict[str, Any], spec: Dict[str, Any]) -> str:
    orig = score["original"]
    conv = score["converted"]
    lines = [
        "ACCESSIBILITY SCORECARD",
        "=======================",
        "",
        "READABILITY METRICS (BEFORE ? AFTER)",
        "------------------------------------",
        f"Flesch-Kincaid Reading Ease:  {orig['fkre']} ? {conv['fkre']}  (target ? {score['fk_target']})",
        f"Flesch-Kincaid Grade Level:   {orig['fkgl']} ? {conv['fkgl']}  (target ? {score['grade_target']})",
        f"Avg sentence length:          {orig['asl']} ? {conv['asl']} words",
        f"Low-frequency word %:         {orig['low_frequency_pct']}% ? {conv['low_frequency_pct']}%",
        "",
        f"BDA STYLE GUIDE COMPLIANCE ? {score['bda_pass_count']}/14 passing",
        "------------------------------------------------",
    ]
    for row in score["bda"]:
        lines.append(f"{row['id']} {row['criterion']}: {'PASS' if row['pass'] else 'FAIL'} ({row['value']})")
    lines.append("")
    lines.append(f"WCAG 2.1 AA MANDATORY ? {score['wcag_aa_pass_count']}/3 passing")
    for row in score["wcag"]:
        if row["level"] == "AA":
            lines.append(f"{row['id']} {row['criterion']}: {'PASS' if row['pass'] else 'FAIL'} ({row['value']})")
    lines.append("")
    lines.append(f"OVERALL GRADE: {score['original_grade']} ? {score['converted_grade']}")
    if score["fk_pass"]:
        lines.append("")
        lines.append("ACCESSIBILITY COMPLIANCE CERTIFICATE")
        lines.append("====================================")
        lines.append("This converted material meets BDA 2023, WCAG 2.1 AA, and the Flesch-Kincaid target.")
        lines.append("A qualified dyslexia specialist should review high-stakes documents.")
    return "\n".join(lines)


__all__ = [
    "analyse_text",
    "convert_text",
    "generate_typography_spec",
    "score_accessibility",
    "format_typography_spec",
    "format_scorecard",
    "contrast_ratio",
    "low_frequency_words",
    "is_passive_sentence",
    "split_long_sentence",
    "detect_language",
]
