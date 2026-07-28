def build_intelligence(
    scan_results,
    llm_analysis=None
):
    """
    Normalize scanner outputs and external agent results
    into intelligence layer.
    """

    intelligence = {

        "target_url": None,

        "urls": [],

        "endpoints": [],

        "inputs": [],

        "auth_points": [],

        "high_risk_modules": [],

        "findings": [],

        "raw": scan_results,

        "llm": llm_analysis or {}

    }


    def append_unique(target_list, value):

        if value and value not in target_list:

            target_list.append(value)



    def add_high_risk(name):

        if name not in intelligence["high_risk_modules"]:

            intelligence["high_risk_modules"].append(name)



    for name, result in scan_results.items():


        if not isinstance(result, dict):

            continue



        # ==================================================
        # Target extraction
        # ==================================================

        if intelligence["target_url"] is None:


            target = result.get(
                "target"
            )


            if isinstance(target, dict):

                intelligence["target_url"] = (
                    target.get("url")
                )


            elif isinstance(target, str):

                intelligence["target_url"] = target



        # ==================================================
        # Generic URL collection
        # ==================================================

        for url in result.get(
            "urls",
            []
        ):

            append_unique(
                intelligence["urls"],
                url
            )



        # ==================================================
        # Endpoint collection
        # ==================================================

        for endpoint in result.get(
            "endpoints",
            []
        ):

            append_unique(
                intelligence["endpoints"],
                endpoint
            )



        # ==================================================
        # Parameter collection
        # ==================================================

        for parameter in result.get(
            "parameters",
            []
        ):

            append_unique(
                intelligence["inputs"],
                parameter
            )



        # ==================================================
        # PentestAgent support
        # ==================================================

        if result.get(
            "engine"
        ) == "pentestagent":


            for endpoint in result.get(
                "endpoints",
                []
            ):

                append_unique(
                    intelligence["endpoints"],
                    endpoint
                )



            vulnerabilities = result.get(
                "vulnerabilities",
                []
            )


            if isinstance(
                vulnerabilities,
                list
            ):


                for vuln in vulnerabilities:


                    if not isinstance(
                        vuln,
                        dict
                    ):

                        continue


                    finding = {

                        "scanner": "pentestagent",

                        "type": vuln.get(
                            "name",
                            vuln.get(
                                "id",
                                "unknown"
                            )
                        ),

                        "severity": vuln.get(
                            "severity",
                            "unknown"
                        ),

                        "details": vuln

                    }


                    intelligence["findings"].append(
                        finding
                    )


                    if vuln.get(
                        "severity"
                    ) in (
                        "critical",
                        "high"
                    ):

                        add_high_risk(
                            "pentestagent"
                        )



        # ==================================================
        # Authentication points
        # ==================================================

        if result.get(
            "auth_detected"
        ):

            append_unique(
                intelligence["auth_points"],
                name
            )



        if result.get(
            "login_page_found"
        ):

            append_unique(
                intelligence["auth_points"],
                name
            )



        # ==================================================
        # Finding normalization
        # ==================================================

        finding = None



        # Simple vulnerability result

        if result.get(
            "vuln"
        ):


            finding = {

                "scanner": name,

                "type": result.get(
                    "vuln"
                ),

                "severity": "high"

            }



        # Existing findings field

        elif result.get(
            "findings"
        ):


            raw_findings = result.get(
                "findings"
            )


            finding = {

                "scanner": name,

                "type": "scanner_finding",

                "details": raw_findings

            }



        # Boolean detection fields

        else:


            for key, value in result.items():


                if (

                    key.endswith(
                        "_detected"
                    )

                    or

                    key.endswith(
                        "_found"
                    )

                ) and value is True:


                    finding = {

                        "scanner": name,

                        "type": key,

                        "severity": "medium"

                    }


                    break



        if finding:


            intelligence["findings"].append(
                finding
            )


            add_high_risk(
                name
            )



        # ==================================================
        # Risk score support
        # ==================================================

        if result.get(
            "risk_score",
            0
        ) > 0.7:


            add_high_risk(
                name
            )



        # ==================================================
        # Scanner specific nested findings
        # ==================================================

        nested = result.get(
            "findings"
        )


        if isinstance(
            nested,
            dict
        ):


            for key, value in nested.items():


                if isinstance(
                    value,
                    list
                ) and value:


                    intelligence["findings"].append({

                        "scanner": name,

                        "type": key,

                        "details": value

                    })



    return intelligence