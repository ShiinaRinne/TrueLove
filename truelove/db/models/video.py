from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from truelove.db.base import Base

class Video(Base):
    __tablename__ = 'Video'

    id = Column(Integer, primary_key=True)
    w_id = Column(Integer, ForeignKey('Watching.w_id'), nullable=False)
    
    video_id = Column(Text, nullable=False, unique= True)
    video_name = Column(Text, nullable=False)
    video_cover = Column(Text)
    video_intro = Column(Text)
    video_pubdate = Column(Integer, default=0)
    video_num = Column(Integer, default=1)
    video_created = Column(Text, nullable=False)
    
    download_status = Column(Integer, default=0)
    download_path = Column(Text, default="")
    
    watch = relationship("Watching", back_populates="videos")



