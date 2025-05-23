from datetime import datetime

from sqlalchemy import Column, Integer, String

from app.database.database import Base


class InputVideo(Base):
    """
    Location of result files for a given parent experiment.

    :id: Unique identifier
    :filename: Filename passed by the user and that which shall be returned
    :path: The path of where this file is stored on system (actual filename will have been modified to avoid conflict)
    """
    __tablename__ = "input_videos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    filename = Column(String, nullable=False)
    path = Column(String)
    video_type = Column(String)
    frame_rate = Column(Integer)
    resolution = Column(String)
    created_date = Column(String)
