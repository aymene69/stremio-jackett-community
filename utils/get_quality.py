import re


def detect_quality(torrent_name):
    quality_patterns = {
        "4k": r'\b(2160P|2160P|UHD|4K)\b',
        "1080p": r'\b(1080P|1080P|FHD|FULLHD|HD|HIGHDEFINITION)\b',
        "720p": r'\b(720P|720P|HD|HIGHDEFINITION)\b',
        "480p": r'\b(480P|480P|SD|STANDARDDEFINITION)\b'
    }

    for quality, pattern in quality_patterns.items():
        if re.search(pattern, torrent_name, re.IGNORECASE):
            return quality
    return "Unknown"


def detect_quality_spec(torrent_name):
    quality_patterns = {
        "HDR": r'\b(HDR|HDRIP|HDR10)\b',
        "DTS": r'\b(DTS|DTS-HD)\b',
        "DDP": r'\b(DDP|DDP5.1|DDP7.1)\b',
        "DD": r'\b(DD|DD5.1|DD7.1)\b',
        "SDR": r'\b(SDR|SDRIP)\b',
        "WEBDL": r'\b(WEBDL|WEB-DL|WEB)\b',
        "BLURAY": r'\b(BLURAY|BLU-RAY|BD)\b',
        "DVDRIP": r'\b(DVDRIP|DVDR)\b',
        "CAM": r'\b(CAM|CAMRIP|CAM-RIP)\b',
        "TS": r'\b(TS|TELESYNC|TELESYNC)\b',
        "TC": r'\b(TC|TELECINE|TELECINE)\b',
        "R5": r'\b(R5|R5LINE|R5-LINE)\b',
        "DVDSCR": r'\b(DVDSCR|DVD-SCR)\b',
        "HDTV": r'\b(HDTV|HDTVRIP|HDTV-RIP)\b',
        "PDTV": r'\b(PDTV|PDTVRIP|PDTV-RIP)\b',
        "DSR": r'\b(DSR|DSRRIP|DSR-RIP)\b',
        "WORKPRINT": r'\b(WORKPRINT|WP)\b',
        "VHSRIP": r'\b(VHSRIP|VHS-RIP)\b',
        "VODRIP": r'\b(VODRIP|VOD-RIP)\b',
        "TVRIP": r'\b(TVRIP|TV-RIP)\b',
        "WEBRIP": r'\b(WEBRIP|WEB-RIP)\b',
        "BRRIP": r'\b(BRRIP|BR-RIP)\b',
        "BDRIP": r'\b(BDRIP|BD-RIP)\b',
        "HDCAM": r'\b(HDCAM|HD-CAM)\b',
    }

    qualities = []
    for quality, pattern in quality_patterns.items():
        if re.search(pattern, torrent_name, re.IGNORECASE):
            qualities.append(quality)
    return "/".join(qualities) if qualities else "Unknown"