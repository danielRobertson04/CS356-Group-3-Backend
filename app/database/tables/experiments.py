from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship

from app.database.database import Base


class Experiment(Base):
    """
    Experiment details
    """
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    experiment_name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(250), nullable=False)
    owner_id = Column(String(250), nullable=False)
    status = Column(String(250), nullable=False)
    video_sources = Column(String(100))  # comma separated list
    encoding_parameters = Column(JSON, nullable=False)
    network_conditions = Column(JSON, nullable=False)
    metrics_requested = Column(String(128))  # comma separated list
    progress = Column(String(250))
    created_at = Column(String(250))

    result_files = relationship("ExperimentResult", back_populates="experiment", cascade="all, delete-orphan", lazy="selectin")
