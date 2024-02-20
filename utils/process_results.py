import base64
import json
from utils.get_availability import get_availability_cached
from utils.get_quality import detect_quality, detect_quality_spec
import concurrent.futures

def get_emoji(language):
    emoji_dict = {
        "fr": "🇫🇷",
        "en": "🇬🇧",
        "es": "🇪🇸",
        "de": "🇩🇪",
        "it": "🇮🇹",
        "pt": "🇵🇹",
        "multi": "🌍"
    }
    return emoji_dict.get(language, "🇬🇧")


def process_results(items, cached, stream_type, season=None, episode=None, config=None):
    stream_list = []

    # Définir une fonction pour traiter chaque élément de manière concurrente
    def process_stream(stream):
        try:
            if "availability" not in stream and not cached:
                return None
        except:
            return None

        if cached:
            if season is None and episode is None:
                availability = get_availability_cached(stream, stream_type, config=config)
            else:
                availability = get_availability_cached(stream, stream_type, season + episode, config=config)
        else:
            availability = stream.get('availability', False)

        query = {"magnet": stream['magnet'], "type": stream_type}
        if stream_type == "series":
            query['season'] = season
            query['episode'] = episode

        if availability:
            indexer = stream.get('indexer', 'Cached')
            name = f"+{indexer} ({detect_quality(stream['title'])} - {detect_quality_spec(stream['title'])})"
        else:
            indexer = stream.get('indexer', 'Cached')
            name = f"-{indexer} ({detect_quality(stream['title'])} - {detect_quality_spec(stream['title'])})"

        return {
            "name": name,
            "title": f"{stream['title']}\r\n{get_emoji(stream['language'])}👥{stream['seeders']}📂"
                     f"{round(int(stream['size']) / 1024 / 1024 / 1024, 2)}GB",
            "url": f"{config['addonHost']}/{base64.b64encode(json.dumps(config).encode('utf-8')).decode('utf-8')}/playback/"
                   f"{base64.b64encode(json.dumps(query).encode('utf-8')).decode('utf-8')}/{stream['title']}"
        }

    # Utiliser un context manager pour gérer les threads/processus
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Exécuter le traitement de chaque élément de manière concurrente
        # La méthode map exécute la fonction process_stream pour chaque élément de la liste items
        # et retourne les résultats dans l'ordre où ils ont été soumis
        results = executor.map(process_stream, items)

        # Ajouter les résultats traités non nuls à la liste de résultats
        for result in results:
            if result is not None:
                stream_list.append(result)

    return stream_list