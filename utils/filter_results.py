def max_size(items, config):
    print("Started filtering size")
    if config is None:
        return items
    if config['maxSize'] is None:
        return items
    filtered_items = []
    size = config['maxSize'] * 1024 ** 3
    for item in items:
        if int(item['size']) <= size:
            filtered_items.append(item)
    return filtered_items


def quality_exclusion(items, config):
    print("Started filtering quality")
    if config is None:
        return items
    if config['exclusion'] is None:
        return items
    filtered_items = []
    for item in items:
        if item['quality'] not in config['exclusion']:
            filtered_items.append(item)
    return filtered_items


def sort_quality(item):
    order = {"4k": 0, "1080p": 1, "720p": 2, "480p": 3}
    return order.get(item.get("quality"), float('inf')), item.get("quality") is None


def items_sort(items, config):
    if config is None:
        return items
    if config['sort'] is None:
        return items
    if config['sort'] == "quality":
        return sorted(items, key=sort_quality)
    if config['sort'] == "sizeasc":
        return sorted(items, key=lambda x: int(x['size']))
    if config['sort'] == "sizedesc":
        return sorted(items, key=lambda x: int(x['size']), reverse=True)


def filter_items(items, item_type=None, config=None):
    if config is None:
        return items
    if config['maxSize'] != 0:
        if item_type == "movie":
            items = max_size(items, config)
    if config['sort'] is not None:
        items = items_sort(items, config)
    if config['exclusion'] is not None:
        items = quality_exclusion(items, config)
    return items
