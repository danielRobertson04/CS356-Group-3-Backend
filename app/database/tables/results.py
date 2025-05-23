from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base

class ExperimentResult(Base):
    """
    Location of result files for a given parent experiment.

    :id: Unique identifier
    :filename: Filename passed by the user and that which shall be returned
    :path: The path of where this file is stored on system (actual filename will have been modified to avoid conflict)
    """
    __tablename__ = "experiment_results"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    filename = Column(String, nullable=False)
    path = Column(String)

    experiment_id = Column(Integer, ForeignKey("experiments.id"), nullable=False)
    experiment = relationship("Experiment", back_populates="result_files")