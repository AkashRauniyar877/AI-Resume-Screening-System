import re
from typing import Optional, List, Tuple

try:
    import spacy

    try:
        _nlp = spacy.load("en_core_web_sm")
    except Exception:
        _nlp = None

except ImportError:
    _nlp = None


# ---------------------------------------------------------
# Resume words that should not be treated as a name
# ---------------------------------------------------------

REJECTED_WORDS = {
    # Resume headings
    "summary",
    "experience",
    "education",
    "skills",
    "profile",
    "resume",
    "curriculum",
    "vitae",
    "cv",
    "contact",
    "objective",
    "work",
    "employment",
    "history",
    "projects",
    "project",
    "certifications",
    "certificates",
    "qualifications",
    "achievements",
    "awards",
    "references",
    "declaration",
    "hobbies",
    "languages",
    "interests",

    # Job titles
    "developer",
    "engineer",
    "manager",
    "analyst",
    "technician",
    "administrator",
    "specialist",
    "accountant",
    "consultant",
    "officer",
    "director",
    "assistant",
    "coordinator",
    "associate",
    "lead",
    "executive",
    "intern",
    "internship",
    "representative",
    "supervisor",
    "architect",
    "designer",
    "programmer",
    "operator",
    "instructor",
    "teacher",
    "professor",

    # Technical / professional words
    "information",
    "technology",
    "computer",
    "software",
    "hardware",
    "system",
    "systems",
    "data",
    "network",
    "web",
    "full",
    "stack",
    "frontend",
    "backend",
    "devops",
    "cloud",
    "senior",
    "junior",
    "head",
    "chief",

    # Contact
    "email",
    "phone",
    "tel",
    "mobile",
    "address",
    "location",
    "linkedin",
    "github",
    "portfolio",
    "website",
    "personal",
    "details",

    # Programming / technology
    "python",
    "java",
    "javascript",
    "typescript",
    "react",
    "fastapi",
    "sql",
    "mysql",
    "mongodb",
    "postgresql",
    "docker",
    "git",
    "aws",
    "azure",
    "linux",
    "c++",
    "html",
    "css",
    "node",
    "express",
    "django",
}


# ---------------------------------------------------------
# Indian states / UTs
# ---------------------------------------------------------

INDIAN_STATES = {
    "andhra pradesh",
    "arunachal pradesh",
    "assam",
    "bihar",
    "chhattisgarh",
    "goa",
    "gujarat",
    "haryana",
    "himachal pradesh",
    "jharkhand",
    "karnataka",
    "kerala",
    "madhya pradesh",
    "maharashtra",
    "manipur",
    "meghalaya",
    "mizoram",
    "nagaland",
    "odisha",
    "orissa",
    "punjab",
    "rajasthan",
    "sikkim",
    "tamil nadu",
    "telangana",
    "tripura",
    "uttar pradesh",
    "uttarakhand",
    "west bengal",

    # UTs
    "delhi",
    "new delhi",
    "jammu and kashmir",
    "ladakh",
    "chandigarh",
    "puducherry",
    "pondicherry",
    "lakshadweep",
    "andaman and nicobar islands",
    "dadra and nagar haveli",
    "daman and diu",
}


# ---------------------------------------------------------
# Common location names
# ---------------------------------------------------------

COMMON_LOCATIONS = {
    "delhi",
    "new delhi",
    "mumbai",
    "bombay",
    "pune",
    "bangalore",
    "bengaluru",
    "hyderabad",
    "chennai",
    "kolkata",
    "calcutta",
    "noida",
    "greater noida",
    "ghaziabad",
    "gurugram",
    "gurgaon",
    "lucknow",
    "kanpur",
    "agra",
    "jaipur",
    "indore",
    "bhopal",
    "patna",
    "ranchi",
    "surat",
    "vadodara",
    "ahmedabad",
    "chandigarh",
    "dehradun",
    "varanasi",
    "prayagraj",
    "allahabad",
    "meerut",
    "faridabad",
    "nagpur",
    "nashik",
    "kochi",
    "coimbatore",
    "mysore",
    "mysuru",
}


# ---------------------------------------------------------
# Address indicators
# ---------------------------------------------------------

ADDRESS_WORDS = {
    "road",
    "rd",
    "street",
    "st",
    "sector",
    "phase",
    "block",
    "near",
    "opposite",
    "district",
    "pin",
    "pincode",
    "postal",
    "india",
    "state",
    "city",
    "location",
    "address",
    "avenue",
    "lane",
    "nagar",
    "colony",
    "village",
    "town",
}


# ---------------------------------------------------------
# Basic helpers
# ---------------------------------------------------------

def _normalize_line(line: str) -> str:
    """Clean a resume line."""
    line = re.sub(r"\s+", " ", line).strip()

    # Remove common decorative characters.
    line = re.sub(r"^[|•·▪◦\-–—:]+", "", line)
    line = re.sub(r"[|•·▪◦\-–—:]+$", "", line)

    return line.strip()


def _get_lines(text: str) -> List[str]:
    """Get meaningful resume lines."""
    lines = []

    for raw_line in text.splitlines():
        line = _normalize_line(raw_line)

        if line:
            lines.append(line)

    return lines


def _is_email(text: str) -> bool:
    return bool(
        re.search(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
            text,
        )
    )


def _is_url(text: str) -> bool:
    lower = text.lower()

    return (
        "http://" in lower
        or "https://" in lower
        or "www." in lower
        or "linkedin.com" in lower
        or "github.com" in lower
    )


def _is_phone(text: str) -> bool:
    digits = re.sub(r"\D", "", text)

    return 10 <= len(digits) <= 15


def _is_location(text: str) -> bool:
    """
    Detect obvious location names without assuming
    that every unknown word is a location.
    """

    lower = text.lower().strip()

    if lower in INDIAN_STATES:
        return True

    if lower in COMMON_LOCATIONS:
        return True

    # If a state name occurs inside a short candidate,
    # it is almost certainly not the candidate's name.
    for state in INDIAN_STATES:
        if state in lower:
            return True

    # Typical Indian PIN code.
    if re.search(r"\b\d{6}\b", lower):
        return True

    # Multiple address indicators.
    words = set(re.findall(r"[a-z]+", lower))

    if len(words.intersection(ADDRESS_WORDS)) >= 2:
        return True

    return False


def _is_heading(text: str) -> bool:
    lower = text.lower().strip()

    return lower in {
        "summary",
        "experience",
        "education",
        "skills",
        "technical skills",
        "profile",
        "resume",
        "curriculum vitae",
        "cv",
        "contact",
        "objective",
        "projects",
        "certifications",
        "achievements",
        "references",
        "languages",
        "interests",
        "declaration",
    }


def _contains_rejected_word(text: str) -> bool:
    lower = text.lower()

    for word in REJECTED_WORDS:
        pattern = rf"(?<![a-z]){re.escape(word)}(?![a-z])"

        if re.search(pattern, lower):
            return True

    return False


def _looks_like_name(text: str) -> bool:
    """
    Structural name check.

    Allows:
        Ajay Chauhan
        Akhilesh Kumar Gautam
        Rahul Kumar Singh
        JOHN DOE
        john doe
    """

    text = text.strip()

    if not text:
        return False

    if len(text) > 60:
        return False

    # Names should not contain these.
    if any(char in text for char in "@:/\\|=<>[]{}"):
        return False

    # Allow:
    # John Doe
    # O'Connor
    # Mary-Jane
    cleaned = re.sub(r"[.'’\-]", "", text)

    words = cleaned.split()

    # 1-5 words.
    if not 1 <= len(words) <= 5:
        return False

    for word in words:
        if not word.isalpha():
            return False

    return True


def _name_format_score(text: str) -> float:
    """Score capitalization style."""

    words = text.split()

    if not words:
        return 0

    title_case = 0
    uppercase = 0

    for word in words:
        clean = re.sub(r"[^A-Za-z]", "", word)

        if not clean:
            continue

        if clean.isupper():
            uppercase += 1
        elif clean[0].isupper():
            title_case += 1

    if uppercase == len(words):
        return 8

    if title_case >= max(1, len(words) - 1):
        return 10

    # Lowercase names are still possible.
    if all(
        re.sub(r"[^A-Za-z]", "", w).islower()
        for w in words
    ):
        return 3

    return 5


# ---------------------------------------------------------
# Candidate validation
# ---------------------------------------------------------

def _valid_candidate(text: str) -> bool:
    """Reject obvious non-name candidates."""

    if not text:
        return False

    text = _normalize_line(text)

    if not text:
        return False

    if _is_email(text):
        return False

    if _is_url(text):
        return False

    if _is_phone(text):
        return False

    if _is_heading(text):
        return False

    if _is_location(text):
        return False

    if _contains_rejected_word(text):
        return False

    if not _looks_like_name(text):
        return False

    # Sentence-like text is usually not a name.
    lower_words = {
        word.lower()
        for word in text.split()
    }

    if lower_words.intersection(
        {
            "and",
            "with",
            "the",
            "to",
            "for",
            "of",
            "in",
            "on",
            "from",
            "as",
            "by",
        }
    ):
        return False

    return True


# ---------------------------------------------------------
# Candidate generation
# ---------------------------------------------------------

def _header_candidates(
    lines: List[str],
) -> List[Tuple[str, int, str]]:
    """
    Generate possible names from the top/header area.

    We intentionally inspect more than only the first
    3 lines because PDF extraction order can vary.
    """

    candidates = []

    # First 20 meaningful lines.
    for index, line in enumerate(lines[:20]):

        if _valid_candidate(line):
            candidates.append(
                (line, index, "header")
            )

    return candidates


def _spacy_candidates(
    text: str,
) -> List[Tuple[str, int, str]]:
    """
    Generate PERSON candidates using spaCy.

    spaCy is only supporting evidence.
    It is NOT trusted blindly.
    """

    if _nlp is None:
        return []

    try:
        doc = _nlp(text)
    except Exception:
        return []

    candidates = []

    for ent in doc.ents:

        if ent.label_ != "PERSON":
            continue

        value = _normalize_line(ent.text)

        if not _valid_candidate(value):
            continue

        # Approximate line position.
        before_entity = text[:ent.start_char]
        line_index = before_entity.count("\n")

        candidates.append(
            (value, line_index, "spacy")
        )

    return candidates


# ---------------------------------------------------------
# Candidate scoring
# ---------------------------------------------------------

def _score_candidate(
    candidate: str,
    line_index: int,
    lines: List[str],
    source: str,
) -> float:
    """
    Score a possible candidate name.

    Higher score = more likely to be the resume owner's name.
    """

    if not _valid_candidate(candidate):
        return -1000

    score = 0.0

    # -----------------------------------------------------
    # Position score
    # -----------------------------------------------------

    if line_index == 0:
        score += 30
    elif line_index == 1:
        score += 27
    elif line_index <= 3:
        score += 23
    elif line_index <= 5:
        score += 18
    elif line_index <= 10:
        score += 10
    elif line_index <= 20:
        score += 4
    else:
        score -= 5

    # -----------------------------------------------------
    # Name length
    # -----------------------------------------------------

    word_count = len(candidate.split())

    if word_count == 2:
        score += 18
    elif word_count == 3:
        score += 20
    elif word_count == 4:
        score += 17
    elif word_count == 5:
        score += 10
    elif word_count == 1:
        score += 4

    # -----------------------------------------------------
    # Capitalization
    # -----------------------------------------------------

    score += _name_format_score(candidate)

    # -----------------------------------------------------
    # Contact proximity
    # -----------------------------------------------------

    start = max(0, line_index - 2)
    end = min(len(lines), line_index + 3)

    nearby = " ".join(
        lines[start:end]
    ).lower()

    contact_words = {
        "email",
        "phone",
        "mobile",
        "contact",
        "linkedin",
        "github",
        "portfolio",
    }

    if any(word in nearby for word in contact_words):
        score += 8

    # -----------------------------------------------------
    # Name near beginning of actual resume content
    # -----------------------------------------------------

    if line_index <= 5:
        score += 8

    # -----------------------------------------------------
    # spaCy PERSON is supporting evidence only
    # -----------------------------------------------------

    if source == "spacy":
        score += 5

    # -----------------------------------------------------
    # If the candidate appears as both a header candidate
    # and PERSON entity, caller adds additional confidence.
    # -----------------------------------------------------

    return score


# ---------------------------------------------------------
# Main extraction function
# ---------------------------------------------------------

def extract_name(text: str) -> Optional[str]:
    """
    Generic candidate name extraction.

    Uses:
    - header position
    - candidate structure
    - location rejection
    - section rejection
    - contact proximity
    - capitalization
    - spaCy PERSON as supporting evidence

    Returns:
        Candidate name or None.
    """

    if not isinstance(text, str) or not text.strip():
        return None

    lines = _get_lines(text)

    if not lines:
        return None

    candidates = []

    # -----------------------------------------------------
    # Header candidates
    # -----------------------------------------------------

    candidates.extend(
        _header_candidates(lines)
    )

    # -----------------------------------------------------
    # spaCy candidates
    # -----------------------------------------------------

    candidates.extend(
        _spacy_candidates(text)
    )

    if not candidates:
        return None

    # -----------------------------------------------------
    # Merge identical candidates from different sources.
    # -----------------------------------------------------

    grouped = {}

    for candidate, line_index, source in candidates:

        key = candidate.lower().strip()

        if key not in grouped:
            grouped[key] = []

        grouped[key].append(
            (
                candidate,
                line_index,
                source,
            )
        )

    scored_candidates = []

    for group in grouped.values():

        best_item = None
        best_score = -1000

        sources = {
            item[2]
            for item in group
        }

        for candidate, line_index, source in group:

            score = _score_candidate(
                candidate,
                line_index,
                lines,
                source,
            )

            # Multiple independent signals.
            if len(sources) >= 2:
                score += 15

            if score > best_score:
                best_score = score
                best_item = candidate

        if best_item is not None:
            scored_candidates.append(
                (
                    best_item,
                    best_score,
                )
            )

    if not scored_candidates:
        return None

    # -----------------------------------------------------
    # Highest confidence candidate
    # -----------------------------------------------------

    scored_candidates.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    best_name, best_score = scored_candidates[0]

    # -----------------------------------------------------
    # Confidence threshold
    # -----------------------------------------------------

    # If evidence is weak, don't guess.
    if best_score < 35:
        return None

    return _normalize_line(best_name)