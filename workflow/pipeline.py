import json
import os

from core.app_classifier import classify_application
from core.app_context import AppContext

from core.llm.client import LLMClient
from core.llm.analyzer import LLMAnalyzer

from core.plugins.auto_loader import auto_load_plugins
from core.plugins.registry import get_registry

from workflow.preflight import prepare_target

from workflow.control.scan_orchestrator import run_full_scan
from workflow.control.intelligence_hub import build_intelligence
from workflow.control.routing_engine import generate_attack_plan
from workflow.control.agent_dispatcher import dispatch_agents

from analysis.engine import AnalysisEngine

from reports.json_report import generate_report
from reports.llm_report import generate_llm_markdown



def scan():

    print("[WPCTF v2] START FULL SATURATION MODE")


    # -----------------------------
    # Target preparation
    # -----------------------------

    target_context = prepare_target()


    target = target_context["target"]

    url = target_context["url"]


    print(
        f"[Target] {target['name']}"
    )



    # -----------------------------
    # Plugin loading
    # -----------------------------

    registry = get_registry()


    auto_load_plugins()


    print(
        f"[Registry] plugins loaded: {len(registry.get_all_plugins())}"
    )



    # -----------------------------
    # Scanner execution
    # -----------------------------

    scan_results = run_full_scan(
        registry,
        target,
        context=target_context
    )


    print(
        f"[Scan Complete] {len(scan_results)} modules executed"
    )



    # -----------------------------
    # LLM analysis
    # -----------------------------

    llm_client = LLMClient()

    analyzer = LLMAnalyzer(
        llm_client
    )


    llm_analysis = analyzer.analyze_scan(
        scan_results
    )



    # -----------------------------
    # Application context
    # -----------------------------

    ctx = AppContext(
        url
    )


    ctx.scan_results = scan_results



    classification = classify_application(
        scan_results
    )


    ctx.set_app_type(
        classification["app_type"]
    )


    ctx.set_classification(
        classification
    )



    # ==================================================
    # PentestAgent execution
    #
    # External AI agent must execute before
    # intelligence construction.
    # ==================================================

    agent_plan = {

        "agent_tasks": [

            {

                "target": url,

                "mode": "full"

            }

        ]

    }



    agent_results = dispatch_agents(
        agent_plan,
        pentest_agent=target_context.get(
            "pentest_agent"
        )
    )



    ctx.update_metadata(
        "agent_results",
        agent_results
    )



    # -----------------------------
    # Merge scanner + agent results
    # -----------------------------

    combined_results = {}


    combined_results.update(
        scan_results
    )



    for key, value in agent_results.items():


        combined_results[
            f"agent_{key}"
        ] = value



    ctx.scan_results = combined_results



    # -----------------------------
    # Intelligence construction
    # -----------------------------

    intelligence = build_intelligence(
        combined_results,
        llm_analysis
    )


    ctx.update_metadata(
        "intelligence",
        intelligence
    )



    # -----------------------------
    # Attack planning
    # -----------------------------

    attack_plan = generate_attack_plan(
        intelligence
    )


    ctx.update_metadata(
        "attack_plan",
        attack_plan
    )



    # -----------------------------
    # Analysis engine
    # -----------------------------

    engine = AnalysisEngine()


    analysis = engine.run(
        combined_results,
        ctx.to_dict()
    )



    for key, value in analysis.items():

        ctx.add_analysis(
            key,
            value
        )



    # -----------------------------
    # JSON report
    # -----------------------------

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



    # -----------------------------
    # LLM markdown report
    # -----------------------------

    llm_md = generate_llm_markdown(
        llm_analysis,
        metadata=ctx.to_dict().get(
            "metadata",
            {}
        ),
        scan_results=combined_results
    )



    with open(
        "output/llm_analysis.md",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            llm_md
        )



    print(
        "[+] DONE -> output/report.json"
    )