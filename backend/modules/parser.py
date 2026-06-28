"""
SOP Parser Module
"""
import re

FIELD_PATTERNS = {
    "process_name": r"PROCESS NAME:\s*(.*?)(?=\n[A-Z ]+:|$)",
    "objective": r"OBJECTIVE:\s*(.*?)(?=\nSCOPE:|$)",
    "scope": r"SCOPE:\s*(.*?)(?=\nROLES:|$)",
    "roles": r"ROLES:\s*(.*?)(?=\nPREREQUISITES:|$)",
    "prerequisites": r"PREREQUISITES:\s*(.*?)(?=\nSTEPS:|$)",
    "steps": r"STEPS:\s*(.*?)(?=\nKPIs:|$)",
    "kpis": r"KPIs:\s*(.*?)(?=\nRISK FACTORS:|$)",
    "risk_factors": r"RISK FACTORS:\s*(.*?)(?=\nTOOLS REQUIRED:|$)",
    "tools_required": r"TOOLS REQUIRED:\s*(.*?)(?=\nREVIEW FREQUENCY:|$)",
    "review_frequency": r"REVIEW FREQUENCY:\s*(.*?)(?=$)",
}

def _clean_text(text: str) -> str:
    if not text:
        return ""
    lines = [line.strip() for line in text.strip().splitlines()]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)

def parse_sop(raw_text: str) -> dict:
    result = {}
    for field, pattern in FIELD_PATTERNS.items():
        match = re.search(pattern, raw_text, re.DOTALL | re.IGNORECASE)
        if match:
            result[field] = _clean_text(match.group(1))
        else:
            result[field] = ""
    return result

def parse_context(raw_context: str) -> dict:
    result = {}
    dept_match = re.search(
        r"DEPARTMENT:\s*(.*?)(?=\nCONTEXT:|$)", raw_context, re.DOTALL | re.IGNORECASE
    )
    result["department"] = _clean_text(dept_match.group(1)) if dept_match else "General"
    result["full_context"] = raw_context.strip()
    return result
