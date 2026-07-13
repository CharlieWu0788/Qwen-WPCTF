import json


def generate_llm_markdown(llm_analysis, metadata=None, scan_results=None):
    """
    Convert LLM analysis into human-readable markdown report
    """

    md = []

    md.append("# 🧠 LLM Security Analysis Report\n")

    # -----------------------------
    # Summary Section
    # -----------------------------
    try:
        if isinstance(llm_analysis, str):
            llm_analysis = json.loads(llm_analysis)
    except Exception:
        llm_analysis = {}

    if not isinstance(llm_analysis, dict):
        llm_analysis = {}

    md.append("## 📌 Summary\n")

    eng = llm_analysis.get("english", {})
    chi = llm_analysis.get("chinese", {})

    md.append(f"### English\n")
    md.append(f"- Summary: {eng.get('summary', 'N/A')}")
    md.append(f"- Risk Score: {eng.get('risk_score', 'N/A')}")
    md.append(f"- Vulnerability Type: {eng.get('vulnerability_type', 'N/A')}\n")

    md.append(f"### 中文\n")
    md.append(f"- 总结：{chi.get('summary', 'N/A')}")
    md.append(f"- 风险评分：{chi.get('risk_score', 'N/A')}")
    md.append(f"- 漏洞类型：{chi.get('vulnerability_type', 'N/A')}\n")

    # -----------------------------
    # Attack Vectors
    # -----------------------------
    md.append("## 🚨 Attack Vectors\n")

    attack_vectors = eng.get("attack_vectors", [])
    if attack_vectors:
        for v in attack_vectors:
            md.append(f"- {v}")
    else:
        md.append("- No attack vectors identified")

    md.append("")

    # -----------------------------
    # Exploitation
    # -----------------------------
    md.append("## ⚔️ Exploitation\n")
    md.append(eng.get("exploitation", "N/A"))
    md.append("")

    # -----------------------------
    # Mitigation
    # -----------------------------
    md.append("## 🛡️ Mitigation\n")
    md.append(eng.get("mitigation", "N/A"))
    md.append("")

    # -----------------------------
    # Scan Context (optional)
    # -----------------------------
    if scan_results:
        md.append("## 🔍 Scan Context\n")
        md.append("Summary of scanners executed:\n")

        for k, v in scan_results.items():
            md.append(f"- **{k}**: success={v.get('success')}")

    return "\n".join(md)
