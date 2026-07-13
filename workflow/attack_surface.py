from workflow.attack_graph import AttackGraph
from workflow.attack_node import AttackNode

from core.schema.capability_map import CAPABILITY_MAP
from core.utils.normalize import normalize_item

def build_attack_surface(scan_results: dict):
    """
    V1.2 Enhanced Scan-Based Attack Surface Builder

    Improvements:
    - structured graph topology (not linear chain)
    - capability scoring (not pure keyword match)
    - grouped surface layer
    """

    scan_results = scan_results or {}

    graph = AttackGraph()
    attack_surface = []

    node_index = 0

    # =========================================================
    # Capability scoring (NEW)
    # =========================================================
    def detect_capability_scored(text: str):
        """
        Returns:
            (capability, score)
        """
        if not isinstance(text, str):
            return "generic", 0.0

        text = text.lower()

        best_cap = "generic"
        best_score = 0.0

        for cap, keywords in CAPABILITY_MAP.items():
            score = sum(1 for k in keywords if k in text)

            if score > best_score:
                best_cap = cap
                best_score = score

        return best_cap, float(best_score)

    # =========================================================
    # Node registry (NEW)
    # =========================================================
    capability_groups = {}

    def add_node(source, items, surface_type_prefix):
        nonlocal node_index

        for item in items or []:

            item = normalize_item(item)

            capability, score = detect_capability_scored(item["url"])

            node_id = f"node_{node_index}_{surface_type_prefix}"

            node_type = f"{capability}_surface"

            node = AttackNode(
                node_id=node_id,
                node_type=node_type,
                target=item["url"]
            )

            node.add_attribute("capability", capability)
            node.add_attribute("capability_score", score)   # 🔥 NEW
            node.add_attribute("source", source)
            node.add_attribute("raw", item["raw"])

            graph.add_node(node)

            # =====================================================
            # NEW: group by capability (STRUCTURE UPGRADE)
            # =====================================================
            capability_groups.setdefault(capability, []).append(node_id)

            attack_surface.append({
                "id": node_id,
                "type": node_type,
                "capability": capability,
                "capability_score": score,
                "target": item["url"],
                "source_scanner": source,
                "metadata": item["raw"]
            })

            node_index += 1

    def scanner_result(name):
        result = scan_results.get(name) or scan_results.get(f"{name}_scan") or {}
        return result if isinstance(result, dict) else {}

    # =========================================================
    # 1. WordPress Surface
    # =========================================================
    wp = scanner_result("wordpress")

    if wp.get("wordpress_detected"):
        add_node(
            "wordpress",
            [{"url": wp.get("final_url", "")}],
            "wordpress"
        )

    # =========================================================
    # 2. Auth Surface
    # =========================================================
    auth = scanner_result("auth")

    add_node(
        "auth_login_urls",
        [{"url": u} for u in auth.get("login_urls", [])],
        "auth"
    )

    add_node(
        "auth_links",
        auth.get("discovered_links", []),
        "auth"
    )

    # =========================================================
    # 3. SQL Surface
    # =========================================================
    sql = scanner_result("sql")

    add_node(
        "sql_params",
        [{"url": "parameter_based_scan"}] if sql.get("tested_payloads") else [],
        "sql"
    )

    # =========================================================
    # 4. XSS Surface
    # =========================================================
    xss = scanner_result("xss")

    if xss.get("tested_payloads"):
        add_node(
            "xss_payloads",
            [{"url": "form_input_surface"}],
            "xss"
        )

    # =========================================================
    # 🔥 NEW: intra-capability graph linking
    # =========================================================
    for cap, nodes in capability_groups.items():
        for i in range(len(nodes) - 1):
            graph.add_edge(nodes[i], nodes[i + 1])

    # =========================================================
    # Final Output (ENHANCED CONTRACT)
    # =========================================================
    return {
        "schema_version": "v2.2.0",
        "graph": graph.to_dict(),
        "surface_list": attack_surface,
        "capability_groups": capability_groups   # 🔥 NEW
    }
