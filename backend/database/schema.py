CREATE_SOPS_TABLE = """
CREATE TABLE IF NOT EXISTS sops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department TEXT,
    process_name TEXT UNIQUE COLLATE NOCASE,
    objective TEXT,
    scope TEXT,
    roles TEXT,
    prerequisites TEXT,
    steps TEXT,
    kpis TEXT,
    risk_factors TEXT,
    tools_required TEXT,
    review_frequency TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
