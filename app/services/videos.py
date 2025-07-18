import os
from datetime import datetime
from typing import List
from typing import Optional, ClassVar, Tuple
import re

from fastapi import HTTPException, UploadFile
from pydantic import StrictStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.responses import JSONResponse, FileResponse

from app.database.tables.videos import InputVideo as input_video_table
from app.models.video import Video
from tests.utility.validation import validate_video
import uuid
from app.models.user import User

now = datetime.now()
path = "app\\database\\videos".replace("\\", os.sep)


from app.services.utility.video_file_handler import delete_video_file, store_video_file


class VideosService:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        VideosService.subclasses = VideosService.subclasses + (cls,)

    async def create_video(self, video: UploadFile,
                           title: Optional[StrictStr], format: Optional[StrictStr], frameRate: Optional[int],
                           resolution: Optional[StrictStr], description: Optional[StrictStr], bitDepth: Optional[int], current_user: User, db) -> Video:
        """Upload a new video to the infrastructure portal (Super User access required)."""

        if not bitDepth == 8 and not bitDepth == 10:
            raise HTTPException(status_code=400, detail="BitDepth must be either 8 or 10")

        if not format == "yuv" and not format == "y4m":
            raise HTTPException(status_code=400, detail="Accepted formats are: yuv, y4m")
        id = str(uuid.uuid4())

        res_pattern = r"[0-9]+x[0-9]+"
        if not re.fullmatch(res_pattern, resolution):
            raise HTTPException(status_code=400, detail="Resolution must follow the format widthxheight (Example 1920x1080)")

        # Create and save video
        data = {"id": id, "title": title, "path": path, "format": format,
                "frameRate": frameRate, "resolution": resolution, "description": description, "bitDepth": bitDepth, "createdDate": now.strftime("%m/%d/%Y, %H:%M:%S"), "lastUpdatedBy": current_user.username}

        db_obj = input_video_table(**data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        formatted_path = path.replace("\\", os.sep).replace("/", os.sep)
        store_video_file(video.file, formatted_path, f"{data["title"]}_{data["id"]}.{data["format"]}")
        return validate_video(db_obj)

    async def delete_video(self, video_id: StrictStr, db) -> JSONResponse:
        """Delete a specific video by ID (Super User access required)."""
        db_obj = await db.execute(select(input_video_table).filter(input_video_table.id == video_id))
        video_info = db_obj.scalars().first()

        if not video_info:
            raise HTTPException(status_code=404, detail="Video not found")

        stored_filename = f"{video_info.title}_{video_info.id}.{video_info.format}"
        file_path = f"{path}\\{stored_filename}".replace("\\", os.sep)

        delete_video_file(file_path)

        await db.delete(video_info)
        await db.commit()
        return JSONResponse(status_code=200, content={"message": "Video deleted"})

    async def get_video(self, video_id: StrictStr, db: AsyncSession):
        """Fetch a specific video by ID."""
        # todo user authentication
        db_obj = await db.execute(select(input_video_table).filter(input_video_table.id == video_id))
        video_info = db_obj.scalars().first()

        if not video_info:
            raise HTTPException(status_code=404, detail="Video not found")

        path = video_info.path
        returned_filename = f"{video_info.title}.{video_info.format}"
        stored_filename = f"{video_info.title}_{video_info.id}.{video_info.format}"
        file_path = f"{path}\\{stored_filename}".replace("\\", os.sep)

        if not file_path:
            raise HTTPException(status_code=404, detail="No video files found")

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Error Retrieving File")

        media_type = ""
        if video_info.format == "y4m":
            media_type = "video/x-yuv4mpeg"
        elif video_info.format == "yuv":
            media_type = "application/octet-stream"

        return FileResponse(path=file_path, media_type=media_type, filename=returned_filename)

    async def get_videos(self, db) -> List[Video]:
        """Fetch a list of all available videos."""
        db_obj = await db.execute(select(input_video_table))
        all_videos = db_obj.scalars()

        if not all_videos:
            return []

        return all_videos
