import json
import os

from core.app_classifier import classify_application
from core.app_context import AppContext

from core.llm.client import LLMClient
from core.llm.analyzer import LLMAnalyzer

from workflow.attack_surface import build_attack_surface
from workflow.test_plan import generate_test_plan

from workflow.preflight import prepare_target

from analysis.coverage_analyzer import analyze_coverage
from analysis.risk_analytics import analyze_risk
from analysis.posture_analyzer import analyze_posture
from analysis.validation_analytics import analyze_validation

from reports.json_report import generate_report
from reports.llm_report import generate_llm_markdown

from scanners.registry import execute_scanners


def scan():

    print("[WPCTF] Scan pipeline started")

    # --------------------------------------------------
    # Preflight
    # --------------------------------------------------
    target_context = prepare_target()

    target = target_context["target"]
    profile = target_context["profile"]
    url = target_context["url"]
    environment = target_context["environment"]

    print(f"[Target] {target['name']}")
    print(f"[Profile] {profile['name']}")

    # --------------------------------------------------
    # Scanner Registry
    # --------------------------------------------------
    scan_results = execute_scanners(
        url,
        profile["scanners"]
    )

    # --------------------------------------------------
    # LLM
    # --------------------------------------------------
    llm_client = LLMClient()

    analyzer = LLMAnalyzer(llm_client)

    llm_analysis = analyzer.analyze_scan(
        scan_results
    )

    # --------------------------------------------------
    # Context
    # --------------------------------------------------
    ctx = AppContext(url)

    for name, result in scan_results.items():
        ctx.add_scan_result(name, result)

    classification = classify_application(
        scan_results
    )

    ctx.set_app_type(
        classification["app_type"]
    )

    ctx.set_classification(
        classification
    )

    # --------------------------------------------------
    # Attack Surface
    # --------------------------------------------------
    surface_result = build_attack_surface(
        scan_results
    )

    surface_list = surface_result.get(
        "surface_list",
        []
    )

    graph = surface_result.get(
        "graph",
        {}
    )

    ctx.update_metadata(
        "attack_graph",
        graph
    )

    # --------------------------------------------------
    # Test Plan
    # --------------------------------------------------
    test_tasks = generate_test_plan(
        surface_list
    )

    analysis_input = {

        "surface_list": surface_list,

        "test_tasks": test_tasks,

        "scan_results": scan_results,

        "llm_analysis": llm_analysis

    }

    # --------------------------------------------------
    # Analysis
    # --------------------------------------------------
    risk_result = analyze_risk(
        analysis_input
    )

    coverage_result = analyze_coverage(
        surface_list,
        test_tasks
    )

    posture_result = analyze_posture(
        analysis_input,
        risk_result
    )

    validation_result = analyze_validation(
        analysis_input
    )

    analysis = {

        "coverage": coverage_result,

        "risk": risk_result,

        "posture": posture_result,

        "validation": validation_result,

        "llm_analysis": llm_analysis

    }

    for k, v in analysis.items():
        ctx.add_analysis(k, v)

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------
    ctx.update_metadata(
        "endpoints",
        surface_list
    )

    ctx.update_metadata(
        "risk_profile",
        risk_result
    )

    ctx.update_metadata(
        "findings",
        scan_results
    )

    ctx.update_metadata(
        "attack_graph",
        graph
    )

    ctx.update_metadata(
        "llm_analysis",
        llm_analysis
    )

    ctx.update_metadata(
        "environment",
        environment
    )

    # --------------------------------------------------
    # Report
    # --------------------------------------------------
    report = generate_report(
        ctx.to_dict()
    )

    os.makedirs(
        "output",
        exist_ok=True
    )

    with open(
        "output/report.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            report,
            f,
            indent=4,
            ensure_ascii=False
        )

    llm_md = generate_llm_markdown(
        llm_analysis,
        metadata=ctx.to_dict().get("metadata", {}),
        scan_results=scan_results
    )

    with open(
        "output/llm_analysis.md",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(llm_md)

    print("[+] Done -> output/report.json")