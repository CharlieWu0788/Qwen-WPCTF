def normalize_item(item):
    """
    Normalize scanner output into unified structure
    """

    if isinstance(item, str):
        return {
            "url": item,
            "raw": item
        }

    return {
        "url": item.get("url", ""),
        "raw": item
    }