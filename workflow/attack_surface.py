from workflow.attack_graph import AttackGraph
from workflow.attack_node import AttackNode

from core.schema.capability_map import CAPABILITY_MAP
from core.utils.normalize import normalize_item



def build_attack_surface(
    scan_results: dict
):
    """
    Build unified attack surface from scanner results.

    Supports:
    - native scanners
    - saturation scan mode
    - future external agents
    """

    scan_results = scan_results or {}


    graph = AttackGraph()

    attack_surface = []

    capability_groups = {}

    node_index = 0



    # ---------------------------------------------------------
    # Capability detection
    # ---------------------------------------------------------

    def detect_capability(
        text
    ):

        if not isinstance(
            text,
            str
        ):
            return (
                "generic",
                0.0
            )


        text = text.lower()


        best = "generic"

        score = 0


        for cap, keywords in CAPABILITY_MAP.items():

            current = sum(
                1
                for k in keywords
                if k in text
            )


            if current > score:

                best = cap

                score = current


        return (
            best,
            float(score)
        )



    # ---------------------------------------------------------
    # Add surface node
    # ---------------------------------------------------------

    def add_surface(
        source,
        target,
        raw=None,
        surface_type=None
    ):

        nonlocal node_index


        capability, score = detect_capability(
            str(target)
        )


        node_id = (
            f"node_{node_index}_"
            f"{surface_type or capability}"
        )


        node_type = (
            f"{capability}_surface"
        )


        node = AttackNode(

            node_id=node_id,

            node_type=node_type,

            target=target

        )


        node.add_attribute(
            "capability",
            capability
        )


        node.add_attribute(
            "capability_score",
            score
        )


        node.add_attribute(
            "source",
            source
        )


        node.add_attribute(
            "raw",
            raw or {}
        )


        graph.add_node(
            node
        )


        capability_groups.setdefault(
            capability,
            []
        ).append(
            node_id
        )


        attack_surface.append({

            "id":
                node_id,


            "type":
                node_type,


            "capability":
                capability,


            "capability_score":
                score,


            "target":
                target,


            "source_scanner":
                source,


            "metadata":
                raw or {}

        })


        node_index += 1



    # ---------------------------------------------------------
    # Generic scanner extraction
    # ---------------------------------------------------------

    for scanner, result in scan_results.items():


        if not isinstance(
            result,
            dict
        ):

            continue



        # target/url extraction

        target = result.get(
            "target"
        )


        if isinstance(
            target,
            dict
        ):

            target = (
                target.get("url")
                or target.get("target")
            )



        # -----------------------------------------------------
        # endpoints
        # -----------------------------------------------------

        for endpoint in result.get(
            "endpoints",
            []
        ):

            add_surface(

                scanner,

                endpoint,

                {
                    "type":
                        "endpoint"
                },

                scanner

            )



        # -----------------------------------------------------
        # URLs
        # -----------------------------------------------------

        for url in result.get(
            "urls",
            []
        ):

            add_surface(

                scanner,

                url,

                {
                    "type":
                        "url"
                },

                scanner

            )



        # -----------------------------------------------------
        # Findings
        # -----------------------------------------------------

        findings = result.get(
            "findings"
        )


        if findings:


            add_surface(

                scanner,

                f"{scanner}_finding",

                {
                    "findings":
                        findings
                },

                scanner

            )



        # -----------------------------------------------------
        # Vulnerability flag
        # -----------------------------------------------------

        vuln = result.get(
            "vuln"
        )


        if vuln:


            add_surface(

                scanner,

                f"{scanner}:{vuln}",

                {
                    "vulnerability":
                        vuln
                },

                scanner

            )



        # -----------------------------------------------------
        # Boolean detection
        # -----------------------------------------------------

        for key,value in result.items():

            if (
                key.endswith(
                    "_detected"
                )
                or
                key.endswith(
                    "_found"
                )
            ) and value is True:


                add_surface(

                    scanner,

                    key,

                    {
                        "signal":
                            key
                    },

                    scanner

                )



    # ---------------------------------------------------------
    # Link same capability nodes
    # ---------------------------------------------------------

    for cap,nodes in capability_groups.items():

        for i in range(
            len(nodes)-1
        ):

            graph.add_edge(
                nodes[i],
                nodes[i+1]
            )



    return {

        "schema_version":
            "v2.3.0",


        "graph":
            graph.to_dict(),


        "surface_list":
            attack_surface,


        "capability_groups":
            capability_groups

    }