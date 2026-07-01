import json
import os

from scanners.sql_scan import scan_sql_injection
from scanners.xss_scan import scan_xss
from scanners.wordpress_scan import scan_wordpress

from core.app_classifier import classify_application
from core.app_context import AppContext
from core.schema.safe_wrap import safe_scanner_result

from core.llm.client import LLMClient
from core.llm.analyzer import LLMAnalyzer

from engines.pentestagent_engine import run_pentestagent

from workflow.attack_surface import build_attack_surface
from workflow.test_plan import generate_test_plan

from analysis.coverage_analyzer import analyze_coverage
from analysis.risk_analytics import analyze_risk
from analysis.posture_analyzer import analyze_posture
from analysis.validation_analytics import analyze_validation

from reports.json_report import generate_report


# =========================================================
# Scanner Orchestrator
# =========================================================
def run_scanners(url: str):
    return {
        "wordpress": safe_scanner_result(scan_wordpress(url)),
        "sql": safe_scanner_result(scan_sql_injection(url)),
        "xss": safe_scanner_result(scan_xss(url))
    }


# =========================================================
# Scan Pipeline Entry
# =========================================================
def scan():

    print("[WPCTF] scan pipeline started")

    # =========================================================
    # Load config
    # =========================================================
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    url = config["target_url"]

    # =========================================================
    # Run scanners
    # =========================================================
    scan_results = run_scanners(url)

    # =========================================================
    # 🔥 LLM INIT (FIXED - NOW INSIDE FUNCTION)
    # =========================================================
    llm_client = LLMClient()

    analyzer = LLMAnalyzer(llm_client)

    # =========================================================
    # 🔥 LLM ENRICHMENT LAYER
    # =========================================================
    llm_analysis = analyzer.analyze_scan(scan_results)

    # =========================================================
    # Context init
    # =========================================================
    ctx = AppContext(url)

    for name, result in scan_results.items():
        ctx.add_scan_result(name, result)

    # =========================================================
    # Classification
    # =========================================================
    classification = classify_application(scan_results)
    ctx.set_app_type(classification["app_type"])
    ctx.set_classification(classification)

    # =========================================================
    # Attack Surface
    # =========================================================
    surface_result = build_attack_surface(scan_results)

    surface_list = surface_result.get("surface_list", [])
    graph = surface_result.get("graph", {})

    ctx.update_metadata("attack_graph", graph)

    # =========================================================
    # Test Plan
    # =========================================================
    test_tasks = generate_test_plan(surface_list)

    # =========================================================
    # Analysis Input
    # =========================================================
    analysis_input = {
        "surface_list": surface_list,
        "test_tasks": test_tasks,
        "scan_results": scan_results,
        "llm_analysis": llm_analysis   # 🔥 NEW
    }

    # =========================================================
    # Analysis Execution
    # =========================================================
    risk_result = analyze_risk(analysis_input)
    coverage_result = analyze_coverage(surface_list, test_tasks)
    posture_result = analyze_posture(analysis_input, risk_result)
    validation_result = analyze_validation(analysis_input)

    analysis = {
        "coverage": coverage_result,
        "risk": risk_result,
        "posture": posture_result,
        "validation": validation_result,
        "llm_analysis": llm_analysis   # 🔥 NEW (for report visibility)
    }

    for k, v in analysis.items():
        ctx.add_analysis(k, v)

    # =========================================================
    # Aggregation Layer
    # =========================================================
    ctx.update_metadata("endpoints", surface_list)
    ctx.update_metadata("risk_profile", risk_result)
    ctx.update_metadata("findings", scan_results)
    ctx.update_metadata("attack_graph", graph)
    ctx.update_metadata("llm_analysis", llm_analysis)  # 🔥 NEW

    # =========================================================
    # Report
    # =========================================================
    report = generate_report(ctx.to_dict())

    os.makedirs("output", exist_ok=True)

    with open("output/report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    print("[+] Done -> output/report.json")