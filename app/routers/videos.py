from typing import List, Optional, Tuple, Union

from fastapi import APIRouter, Form, HTTPException, Path, UploadFile
from pydantic import StrictBytes, StrictStr
from sqlalchemy.sql.annotation import Annotated
from sqlmodel import Field
from starlette.responses import JSONResponse, FileResponse, StreamingResponse

from app.database.database import get_db
from app.database.tables.videos import InputVideo
from app.models.video import Video
from app.services.videos import VideosService

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends, Path, Body, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.error import Error

router = APIRouter()


@router.post("/infrastructure/videos", responses={200: {"model": Video, "description": "Video created successfully"},
                                                  400: {"model": Error, "description": "Invalid video upload data"},
                                                  415: {"model": Error,
                                                        "description": "Unsupported media type for video upload."},
                                                  422: {"model": Error, "description": "Video file validation error."},
                                                  200: {"model": Error, "description": "Unexpected error"}, },
             tags=["videos"], summary="Create video", response_model_by_alias=True, )
async def create_video(
        video_file: UploadFile = File(..., description="Video file to upload"),
        id: Optional[int] = Form(None),
        groupId: Optional[int] = Form(None),
        filename: Optional[StrictStr] = Form(None),
        video_type: Optional[StrictStr] = Form(None),
        frame_rate: Optional[int] = Form(None),
        resolution: Optional[StrictStr] = Form(None),
        db: AsyncSession = Depends(get_db) ) -> Video:
    """Upload a new video to the infrastructure portal (Super User access required)."""
    return await VideosService().create_video(video_file, id, groupId, filename, video_type, frame_rate, resolution, db)


@router.delete("/infrastructure/videos/{id}", responses={200: {"model": Video, "description": "Video deleted"},
                                                         404: {"model": Error, "description": "Video not found"},
                                                         200: {"model": Error, "description": "Unexpected error"}, },
               tags=["videos"], summary="Delete video", response_model_by_alias=True, )
async def delete_video(id: StrictStr = Path(..., description=""), db: AsyncSession = Depends(get_db)) -> JSONResponse:
    """Delete a specific video by ID (Super User access required)."""
    return await VideosService().delete_video(id, db)


@router.get("/infrastructure/videos/{id}", responses={200: {"model": Video, "description": "Video details"},
                                                      404: {"model": Error, "description": "Video not found"},
                                                      200: {"model": Error, "description": "Unexpected error"}, },
            tags=["videos"], summary="Retrieve video", response_model_by_alias=True, response_class=FileResponse)
async def get_video(id: StrictStr = Path(..., description=""), db: AsyncSession = Depends(get_db)) -> FileResponse:
    """Fetch a specific video by ID."""
    return await VideosService().get_video(id, db)

@router.get("/infrastructure/videos", responses={200: {"model": List[StrictStr], "description": "A list of videos"},
                                                 200: {"model": Error, "description": "Unexpected error"}, },
            tags=["videos"], summary="Retrieve videos list", response_model_by_alias=True, )
async def get_videos(db: AsyncSession = Depends(get_db)) -> List[Video]:
    """Fetch a list of all available videos."""
    return await VideosService().get_videos(db)
