def format_memory(rss):
    """
    Konvertiert Bytes in Megabytes.
    """
    return round(rss / (1024 * 1024), 2)
