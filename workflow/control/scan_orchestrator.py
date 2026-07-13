def run_full_scan(registry, target, context=None):

    results = {}

    for plugin in registry.get_all_plugins():

        try:
            # 🔥 SAFE WRAP (fix crash)
            if hasattr(plugin, "run"):

                # normalize input (VERY IMPORTANT)
                if hasattr(plugin.run, "__code__"):
                    try:
                        results[plugin.name] = plugin.run({
                            "target": target,
                            "context": context or {}
                        })
                    except TypeError:
                        # fallback for old signature
                        results[plugin.name] = plugin.run(context or {})

            else:
                results[plugin.name] = {
                    "error": "no run() method"
                }

        except Exception as e:
            results[plugin.name] = {
                "error": str(e),
                "plugin": plugin.name
            }

    return results