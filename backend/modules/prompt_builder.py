"""
Prompt Builder Module
"""

def build_analysis_prompt(process_name: str) -> str:
    return f"""You are a business process analyst. Analyze the following business process and return ONLY the structured context below. No explanations, no markdown, no extra text.

BUSINESS PROCESS: {process_name}

Return this exact format:

DEPARTMENT:
[The primary department responsible for this process]

CONTEXT:
[Brief 2-3 sentence business context for this process]

KEY OBJECTIVES:
[3-4 bullet points of what this process aims to achieve, each on a new line starting with -]

KEY ROLES:
[3-4 roles involved, each on a new line starting with -]

KEY RISKS:
[3 main risks, each on a new line starting with -]

SPECIAL REQUIREMENTS:
[Any compliance, regulatory, or industry-specific requirements, each on a new line starting with -]"""

def build_sop_prompt(process_name: str, context: str) -> str:
    return f"""You are a senior enterprise SOP writer. Generate a professional, concise Standard Operating Procedure.

BUSINESS PROCESS: {process_name}

CONTEXT FROM ANALYSIS:
{context}

STRICT RULES:
- Return ONLY the SOP content in the exact format below
- No markdown (no **, no #, no -, no *)
- No tables
- No appendices
- No notes or explanations
- No version numbers or signatures
- Maximum 5 steps
- Maximum 3 KPIs
- Maximum 3 risk factors
- Maximum 2 tools
- Total response under 350 words
- Plain text only

Return EXACTLY this format (replace placeholder text):

PROCESS NAME:
{process_name}

OBJECTIVE:
[Single paragraph stating the purpose of this SOP]

SCOPE:
[Who and what this SOP applies to]

ROLES:
[List roles and responsibilities, one per line]

PREREQUISITES:
[Required conditions before starting, one per line]

STEPS:
[Numbered steps 1-5 maximum, each step on its own line]

KPIs:
[3 measurable key performance indicators, one per line]

RISK FACTORS:
[3 risks with brief mitigation, one per line]

TOOLS REQUIRED:
[2 tools maximum, one per line]

REVIEW FREQUENCY:
[How often this SOP should be reviewed]"""
