import asyncio
from fastapi import HTTPException, status, APIRouter, BackgroundTasks
from typing import List, Literal, Optional

from truelove.process.manager import TrueLoveManager, task_in_progress
from truelove.process.platforms.api.biliapi.models import AuthorInfo

from truelove.db.models import (
    WatcheeSchema,
    MediaSchema,
)
from truelove.logger import logger
from truelove.routes.models import *
from truelove.routes.utils import  parse_uid


router = APIRouter()


@router.get("/watchee_info")
async def _get_watchee_info(uid: Optional[str] = None) -> List[WatcheeSchema]:
    """获取全部订阅的作者信息
    当有指定uid时, 则只获取指定作者的信息

    Returns:
        List[WatchingSchema]: _description_
    """
    return await TrueLoveManager.fetch_watchee_info(uid)


@router.get("/watchee_content")
async def _get_watchee_content(
    uid: Optional[str] = None,
    limit: int = 10,
    order_by: str = "add_time",
    order: Literal["asc", "desc"] = "desc",
):
    """获取全部订阅的作者的全部内容.
    当有指定uid时, 则只获取指定作者的全部内容

    Args:
        limit (int, optional): _description_. Defaults to 10.
        order_by (str, optional): _description_. Defaults to "add_time".
        order (Literal[&quot;asc&quot;, &quot;desc&quot;], optional): _description_. Defaults to "desc".

    Returns:
        _type_: _description_
    """

    return await TrueLoveManager.fetch_watchee_content_from_db( limit=limit, order_by=order_by, order=order, uid=uid)



@router.get("/refresh")
async def _refresh(background_tasks: BackgroundTasks ,uid: Optional[str] = None) -> dict:
    print("refresh!!!!!")
    
    if task_in_progress.get("refresh", False):
        return {"message": "任务正在进行中, 请稍后再试"}
    else:    
        task_in_progress["refresh"] = True
        background_tasks.add_task(TrueLoveManager.refresh, uid=parse_uid(uid))
        return {
            "message": "已提交任务, 可能需要一些时间才可以刷新完毕",
        }
        
@router.get("/download_media")
async def _download_media(uid: Optional[str] = None):
    await download_media()

    return {
        "status": "success",
    }


@router.post("/add_watchee")
async def _add_watchee(request: AddWatcheeRequest) -> AddWatcheeResponse:
    uid = parse_uid(request.uid)

    author_info: AuthorInfo = await TrueLoveManager.add_watchee(uid, request.platform, request.core)
    if author_info is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Author {uid} not exists",
        )
        
    return AddWatcheeResponse(
        status="success",
        message=f"Add [{author_info.name}] to Watching",
        uid=author_info.mid,
        platform="bilibili",
        ret_code=0,
    )


@router.post("/remove_watchee")
async def _remove_watchee(request: RemoveSubscriptionRequest) -> None:
    """取消对某个作者的订阅

    Args:
        uid (str): 对应平台的uid
        delete_medias (bool, optional): 是否删除已经下载好的文件与视频

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    ok = await TrueLoveManager.remove_watchee(request.uid, request.delete_medias)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Author {request.uid} not exists",
        )
    

    return {
        "status": "success",
        "message": f"Delete [{request.uid}] from Watching",
        "ret_code": 0,
    }