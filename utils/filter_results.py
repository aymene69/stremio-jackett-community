import re


def filter_language(torrents, language):
    print(f"Filtering torrents by language: {language}")
    filtered_torrents = []
    for torrent in torrents:
        if not torrent['language']:
            continue
        if torrent['language'] == language:
            filtered_torrents.append(torrent)
        if torrent['language'] == "multi":
            filtered_torrents.append(torrent)
        if torrent['language'] == "no":
            filtered_torrents.append(torrent)
    return filtered_torrents


def max_size(items, config):
    print("Started filtering size")
    if config is None:
        return items
    if config['maxSize'] is None:
        return items
    filtered_items = []
    size = int(config['maxSize']) * 1024 ** 3
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


def filter_season_episode(items, season, episode):
    filtered_items = []
    for item in items:
        if season + episode in item['title']:
            filtered_items.append(item)
        if re.search(r'\bS\d{2}\b', item['title']):
            filtered_items.append(item)
    return filtered_items


def filter_items(items, item_type=None, config=None, cached=False, season=None, episode=None):
    if config is None:
        return items
    if config['language'] is None:
        return items
    if cached and item_type == "series":
        items = filter_season_episode(items, season, episode)
    print("Started filtering torrents")
    items = filter_language(items, config['language'])
    if int(config['maxSize']) != 0:
        if item_type == "movie":
            items = max_size(items, config)
    if config['sort'] is not None:
        items = items_sort(items, config)
    if config['exclusion'] is not None:
        items = quality_exclusion(items, config)
    return items
