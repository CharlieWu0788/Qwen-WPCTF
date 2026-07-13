class AnalysisEngine:

    def __init__(self):
        pass

    def run(self, scan_results, context):
        attack_surface = self._attack_surface(scan_results)
        risk = self._risk(attack_surface)
        coverage = self._coverage(attack_surface, context)
        posture = self._posture(coverage, risk)

        return {
            "attack_surface": attack_surface,
            "risk": risk,
            "coverage": coverage,
            "posture": posture,
            "exploitability": self._exploitability(attack_surface, scan_results)
        }

    # -------------------------
    # metrics layer
    # -------------------------
    def _attack_surface(self, scan_results):
        from workflow.attack_surface import build_attack_surface
        return build_attack_surface(scan_results)

    def _risk(self, attack_surface):
        from analysis.risk_analytics import analyze_risk
        return analyze_risk(attack_surface)

    def _coverage(self, attack_surface, context):
        from analysis.coverage_analyzer import analyze_coverage
        return analyze_coverage(
            attack_surface.get("surface_list", []),
            self._test_plan(context)
        )

    def _posture(self, coverage_result, risk_result):
        from analysis.posture_analyzer import analyze_posture
        return analyze_posture(coverage_result, risk_result)

    def _test_plan(self, context):
        metadata = (context or {}).get("metadata", {})
        attack_plan = metadata.get("attack_plan", {})

        if isinstance(attack_plan, list):
            return attack_plan

        if not isinstance(attack_plan, dict):
            return []

        test_plan = []

        for targets in attack_plan.values():
            if not isinstance(targets, list):
                continue

            for target in targets:
                if isinstance(target, dict):
                    item = dict(target)
                    item["target"] = self._target_key(target)
                    test_plan.append(item)
                else:
                    test_plan.append({"target": self._target_key(target)})

        return test_plan

    # -------------------------
    # reasoning layer (from engines)
    # -------------------------
    def _exploitability(self, attack_surface, scan_results):
        from analysis.exploitability_engine import analyze_exploitability
        return analyze_exploitability(
            attack_surface.get("surface_list", []),
            self._validation_results(scan_results)
        )

    def _validation_results(self, scan_results):
        validation_results = []

        for plugin_name, result in (scan_results or {}).items():
            if not isinstance(result, dict):
                continue

            if "error" in result and result.get("error"):
                continue

            validation_results.append({
                "target": self._target_key(result.get("target") or plugin_name),
                "validated": True,
                "evidence": result.get("evidence", [])
            })

        return validation_results

    def _target_key(self, target):
        if isinstance(target, dict):
            return str(
                target.get("id")
                or target.get("name")
                or target.get("target")
                or target.get("url")
                or target
            )

        return str(target)
