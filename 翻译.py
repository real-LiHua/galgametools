import asyncio
import json
import logging
import sys
from json.decoder import JSONDecodeError
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
fy = sorted(list(json.load(open(sys.argv[1])).items()), key=lambda x: -len(x[0]))


async def task(path):
    with open(path) as f:
        s = f.read()
        old = s
    for k, v in fy:
        s = s.replace(k, v)
    try:
        json.loads(s)
    except JSONDecodeError:
        logger.error(path)
        s = old
        for k, v in fy:
            new = s.replace(k, v)
            try:
                json.loads(new)
                if s != new:
                    logger.info(f"已翻译：{path} {k} => {v}")
                    s = new
            except JSONDecodeError:
                logger.error(f"{path} {k} {v}")
    path.write_text(s)
    logger.info(f"已翻译：{path}")


async def main():
    await asyncio.gather(*[task(path) for path in Path("data").glob("*.json")])


asyncio.run(main())
