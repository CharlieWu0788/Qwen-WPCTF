class LLMAnalyzer:
    def __init__(self, llm_client):
        self.llm = llm_client

    def analyze_scan(self, scan_result: dict):
        prompt = f"""
You are a professional cybersecurity analyst.

Analyze the following scan result.

Scan Result:
{scan_result}

Return ONLY valid JSON.

The output format MUST be:

{{
    "english": {{
        "summary": "",
        "vulnerability_type": "",
        "risk_score": "",
        "attack_vectors": [],
        "exploitation": "",
        "mitigation": ""
    }},
    "chinese": {{
        "summary": "",
        "vulnerability_type": "",
        "risk_score": "",
        "attack_vectors": [],
        "exploitation": "",
        "mitigation": ""
    }}
}}

Do NOT output Markdown.
Do NOT explain.
Do NOT wrap the JSON in ```json.
Return JSON only.
"""
        return self.llm.chat(prompt)