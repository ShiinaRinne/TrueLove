from truelove.process.platforms.bilibili import BiliAPI


async def main():
    asd = await BiliAPI.fetch_author_info(512313464)
    if asd is not None:
        print(asd)
        print(asd.name)
        assert asd.name == "GAMES-Webinar"
        
        
    qwe = await BiliAPI.fetch_author_video_list(512313464)
    if qwe is not None:
        print(qwe.list.vlist[0].title)
    
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())