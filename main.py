import base64
import json
import logging
import re

import starlette.status as status
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from constants import NO_RESULTS
from debrid.alldebrid import get_stream_link_ad
from debrid.realdebrid import get_stream_link_rd
from utils.filter_results import filter_items
from utils.get_cached import search_cache
from utils.get_content import get_name
from utils.logger import setup_logger
from utils.process_results import process_results


app = FastAPI()


class LogFilterMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        request = Request(scope, receive)
        path = request.url.path
        sensible_path = re.sub(r'/ey.*?/', '/<SENSITIVE_DATA>/', path)
        logger.info(f"{request.method} - {sensible_path}")
        return await self.app(scope, receive, send)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LogFilterMiddleware)

templates = Jinja2Templates(directory=".")

logger = setup_logger(__name__)


@app.get("/")
async def root():
    return RedirectResponse(url="/configure")


@app.get("/configure")
async def configure(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/{config}/configure")
async def configure(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/{params}/manifest.json")
async def get_manifest():
    return {
        "id": "community.aymene69.jackett",
        "icon": "https://i.imgur.com/tVjqEJP.png",
        "version": "3.0.10",
        "catalogs": [],
        "resources": ["stream"],
        "types": ["movie", "series"],
        "name": "Jackett",
        "description": "Stremio Jackett Addon",
        "behaviorHints": {
            "configurable": True,
        }
    }


formatter = logging.Formatter('[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
                              '%m-%d %H:%M:%S')


logger.info("Started Jackett Addon")


@app.get("/{config}/stream/{stream_type}/{stream_id}")
async def get_results(config: str, stream_type: str, stream_id: str):
    stream_id = stream_id.replace(".json", "")
    config = json.loads(base64.b64decode(config).decode('utf-8'))
    logger.info(stream_type + " request")
    logger.info("Getting name and properties")
    name = get_name(stream_id, stream_type, config=config)
    logger.info("Got name and properties: " + str(name['title']))
    logger.info("Getting config")
    logger.info("Got config")
    logger.info("Getting cached results")
    cached_results = search_cache(name)
    logger.info("Got " + str(len(cached_results)) + " cached results")
    logger.info("Filtering cached results")
    filtered_cached_results = filter_items(cached_results, stream_type, config=config, cached=True,
                                           season=name['season'] if stream_type == "series" else None,
                                           episode=name['episode'] if stream_type == "series" else None)
    if len(filtered_cached_results) > 0:
        logger.info("Cached results found")
        logger.info("Processing cached results")
        stream_list = process_results(filtered_cached_results[:10], True, stream_type,
                                      name['season'] if stream_type == "series" else None,
                                      name['episode'] if stream_type == "series" else None, config=config)
        logger.info("Processed cached results")
        if len(stream_list) == 0:
            logger.info("No results found")
            return NO_RESULTS
        return {"streams": stream_list}
    else:
        return NO_RESULTS


@app.get("/playback/{config}/{query}/{title}")
async def get_playback(config: str, query: str, title: str):
    try:
        if not query or not title:
            raise HTTPException(status_code=400, detail="Query and title are required.")
        config = json.loads(base64.b64decode(config).decode('utf-8'))
        logger.info("Decoding query")
        query = base64.b64decode(query).decode('utf-8')
        logger.info(query)
        logger.info("Decoded query")

        service = config['service']
        if service == "realdebrid":
            logger.info("Getting Real-Debrid link")
            link = get_stream_link_rd(query, config=config)
        elif service == "alldebrid":
            logger.info("Getting All-Debrid link")
            link = get_stream_link_ad(query, config=config)
        else:
            raise HTTPException(status_code=500, detail="Invalid service configuration.")

        logger.info("Got link: " + link)
        return RedirectResponse(url=link, status_code=status.HTTP_301_MOVED_PERMANENTLY)

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")
