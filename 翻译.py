import asyncio
import json
import logging
import sys
from json.decoder import JSONDecodeError
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
fy = sorted(list(json.load(open(sys.argv[1])).items()), key=lambda x: -len(x[0]))


async def task(path: Path):
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
    _ = path.write_text(s)
    logger.info(f"已翻译：{path}")


async def link(path: Path):
    old_name = path.name
    for k, v in fy:
        new_name = old_name.replace(k, v)
        if new_name == old_name:
            continue
        new_path = path.parents[0] / new_name
        try:
            new_path.symlink_to(path.name)
            logger.info(f"已翻译：{path}")
        except:
            pass


async def main():
    logger.info("正在翻译游戏数据")
    _ = await asyncio.gather(*[task(path) for path in Path("data").glob("*.json")])
    logger.info("正在翻译图片文件名")
    _ = await asyncio.gather(*[link(path) for path in Path("img").glob("**/*")])
    logger.info("正在翻译音频文件名")
    _ = await asyncio.gather(*[link(path) for path in Path("audio").glob("**/*.ogg_")])


asyncio.run(main())
