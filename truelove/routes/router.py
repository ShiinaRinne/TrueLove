from typing import List, Literal, Optional
from fastapi import HTTPException, status, APIRouter, BackgroundTasks

from truelove.process.manager import TrueLoveManager, task_in_progress

from truelove.routes.models import *
from truelove.logger import logger
from truelove.db.models import WatcheeSchema
from truelove.routes.utils import parse_uid



router = APIRouter()


@router.get("/watchee_info")
async def _get_watchee_info(uid: Optional[str] = None) -> List[WatcheeSchema]:
    """获取全部订阅的作者信息
    当有指定uid时, 则只获取指定作者的信息

    Returns:
        List[WatchingSchema]: _description_
    """
    return await TrueLoveManager.fetch_watchee_info(uid)


@router.get("/watchee_video")
async def _get_watchee_video(
    uid: Optional[str] = None,
    limit: int = 10,
    order_by: str = "video_created",
    order: Literal["asc", "desc"] = "desc",
):
    """获取全部订阅的作者的全部视频.
    当有指定uid时, 则只获取指定作者的全部视频

    Args:
        limit (int, optional): _description_. Defaults to 10.
        order_by (str, optional): _description_. Defaults to "video_created".
        order (Literal[&quot;asc&quot;, &quot;desc&quot;], optional): _description_. Defaults to "desc".

    Returns:
        _type_: _description_
    """

    return await TrueLoveManager.fetch_watchee_video_list(limit=limit, order_by=order_by, order=order, uid=uid)


@router.get("/refresh")
async def _refresh(background_tasks: BackgroundTasks ,w_id: Optional[int] = None, force_refresh:bool = False) -> dict:
    """刷新订阅的全部作者的内容.
    当指定uid时, 则只刷新指定作者的内容.
    默认检测到第一个内容已经存在时, 会直接跳过停止刷新, 当 force_refresh 为True时, 则会强制刷新全部

    Args:
        background_tasks (BackgroundTasks): _description_
        uid (Optional[str], optional): _description_. Defaults to None.
        force_refresh (bool, optional): _description_. Defaults to False.

    Returns:
        dict: _description_
    """
    if task_in_progress.get("refresh", False):
        return {"message": "任务正在进行中, 请稍后再试"}
    else:
        kwargs = {"force_refresh": force_refresh}
        if w_id == "": w_id = None
        await TrueLoveManager.trigger_job_manually("refresh", w_id, **kwargs)
        return {
            "message": "已提交任务, 可能需要一些时间才可以刷新完毕",
        }
        
@router.get("/download_video")
async def _download_video(uid: Optional[str] = None):
    # await download_video()

    return {
        "status": "success",
    }


@router.post("/add_watchee")
async def _add_watchee(request: AddWatcheeRequest) -> AddWatcheeResponse:
    uid = parse_uid(request.uid)

    w = await TrueLoveManager.add_watchee(uid, request.platform, request.core, request.watch_type)
    if not w:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Author {uid} already exists",
        )
        
    return AddWatcheeResponse(
        status="success",
        ret_code=0,
    )


@router.post("/remove_watchee")
async def _remove_watchee(request: RemoveSubscriptionRequest) -> None:
    """取消对某个作者的订阅

    Args:
        uid (str): 对应平台的uid
        delete_videos (bool, optional): 是否删除已经下载好的文件与视频

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    ok = await TrueLoveManager.remove_watchee(request.w_id, watch_type=request.watch_type, delete_downloads=request.delete_downloads)
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Author {request.w_id} not exists",
        )
    

    return {
        "status": "success",
        "message": f"Delete [{request.w_id}] from Watching",
        "ret_code": 0,
    }
