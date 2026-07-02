import re
from typing import Any, Dict, List

try:
    import spacy  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    spacy = None


class ResumeParser:
    """Extract basic resume fields from free-form text."""

    EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    PHONE_PATTERN = re.compile(r"(?:\+?\d[\d\s().-]{7,}\d)")
    SECTION_PATTERN = re.compile(r"(?i)\b(skills|education|experience)\b\s*:\s*(.+)")

    def parse(self, text: str) -> Dict[str, Any]:
        if not text:
            return {"name": "", "email": "", "phone": "", "skills": [], "education": "", "experience": ""}

        normalized = text.replace("\r\n", "\n").strip()
        return {
            "name": self._extract_name(normalized),
            "email": self._extract_email(normalized),
            "phone": self._extract_phone(normalized),
            "skills": self._extract_skills(normalized),
            "education": self._extract_section(normalized, "education"),
            "experience": self._extract_section(normalized, "experience"),
        }

    def _extract_name(self, text: str) -> str:
        if spacy is not None:
            try:
                nlp = spacy.load("en_core_web_sm")
                doc = nlp(text)
                for ent in doc.ents:
                    if ent.label_ in {"PERSON"}:
                        return ent.text.strip()
            except OSError:
                pass

        for line in text.splitlines():
            candidate = line.strip()
            if not candidate:
                continue
            if self.EMAIL_PATTERN.search(candidate) or self.PHONE_PATTERN.search(candidate):
                continue
            if candidate.lower().startswith(("skills:", "education:", "experience:", "summary:")):
                continue
            if len(candidate.split()) <= 6:
                return candidate
        return ""

    def _extract_email(self, text: str) -> str:
        match = self.EMAIL_PATTERN.search(text)
        return match.group(0) if match else ""

    def _extract_phone(self, text: str) -> str:
        match = self.PHONE_PATTERN.search(text)
        return match.group(0).strip() if match else ""

    def _extract_skills(self, text: str) -> List[str]:
        match = self.SECTION_PATTERN.search(text)
        if match and match.group(1).lower() == "skills":
            raw = match.group(2)
            parts = re.split(r"[,;|/]+", raw)
            return [part.strip() for part in parts if part.strip()]

        for line in text.splitlines():
            if re.search(r"(?i)\bskills\b", line):
                raw = line.split(":", 1)[-1].strip()
                parts = re.split(r"[,;|/]+", raw)
                return [part.strip() for part in parts if part.strip()]
        return []

    def _extract_section(self, text: str, heading: str) -> str:
        pattern = re.compile(rf"(?i)\b{heading}\b\s*:\s*(.+)")
        match = pattern.search(text)
        if match:
            return match.group(1).strip()
        return ""


def parse_resume(text: str) -> Dict[str, Any]:
    return ResumeParser().parse(text)
