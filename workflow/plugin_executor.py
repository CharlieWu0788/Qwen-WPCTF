from core.plugins.registry import get_registry


def execute_plugin(plugin_name: str, context: dict):
    """
    Execute a single plugin by name.

    Args:
        plugin_name (str): Name of the plugin registered in registry
        context (dict): Runtime execution context

    Returns:
        dict | None: Plugin execution result
    """

    registry = get_registry()
    plugin = registry.get(plugin_name)

    if plugin is None:
        print(f"[PLUGIN_EXECUTOR] Plugin not found: {plugin_name}")
        return None

    try:
        result = plugin.run(context)

        return {
            "plugin": plugin_name,
            "status": "success",
            "result": result
        }

    except Exception as e:
        return {
            "plugin": plugin_name,
            "status": "error",
            "error": str(e)
        }


def execute_plugins(plugin_names: list, target: dict, context: dict = None):
    """
    Execute multiple plugins sequentially.

    Args:
        plugin_names (list): List of plugin names selected by plugin_selector
        target (dict): Target application info
        context (dict): Shared runtime context

    Returns:
        dict: Aggregated scan results
    """

    if context is None:
        context = {}

    results = {}

    for name in plugin_names:

        result = execute_plugin(
            plugin_name=name,
            context={
                "target": target,
                "runtime": context
            }
        )

        if result is not None:
            results[name] = result

    return results