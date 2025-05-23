import os
from io import BytesIO
from typing import ClassVar
from typing import List, Optional, Tuple, Union

from dulwich.web import send_file
from multipart import file_path
from pydantic import StrictBytes, StrictStr

from pathlib import Path

from starlette.responses import JSONResponse, FileResponse

from app.database.tables.videos import InputVideo as input_video_table
from app.models.video import Video

from typing import Optional, ClassVar, Tuple

from fastapi import HTTPException
from pydantic import Field, StrictStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.services.utility.video_file_handler import delete_video_file


class VideosService:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        VideosService.subclasses = VideosService.subclasses + (cls,)

    async def create_video(self, video: Optional[Union[StrictBytes, StrictStr, Tuple[StrictStr, StrictBytes]]],
                           frame_rate: Optional[StrictStr], resolution: Optional[StrictStr], ) -> Video:
        """Upload a new video to the infrastructure portal (Super User access required)."""
        ...

    async def delete_video(self, video_id: StrictStr, db) -> JSONResponse:
        """Delete a specific video by ID (Super User access required)."""
        db_obj = await db.execute(select(input_video_table).filter(input_video_table.id == video_id))
        video_info = db_obj.scalars().first()
        file = video_info.path + video_info.filename

        if not video_info:
            raise HTTPException(status_code=404, detail="Video not found")

        delete_video_file(file)

        await db.delete(db_obj)
        await db.commit()
        return JSONResponse(status_code=200, content={"message": "Video deleted"})

    async def get_video(self, video_id: StrictStr, db: AsyncSession) -> FileResponse:
        """Fetch a specific video by ID."""
        # todo user authentication
        db_obj = await db.execute(select(input_video_table).filter(input_video_table.id == video_id))
        video_info = db_obj.scalars().first()
        path = video_info.path
        file = video_info.filename
        file_path = path + '/' + file

        if not video_info:
            raise HTTPException(status_code=404, detail="Video not found")

        if not file_path:
            raise HTTPException(status_code=404, detail="No video files found")

        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail="Error Retrieving File")

        return FileResponse(path = file_path, media_type=video_info.video_type, filename = file)


    async def get_videos(self) -> List[Video]:
        """Fetch a list of all available videos."""
        return [file.name for file in Path("app/database/videos").iterdir() if file.is_file()]
