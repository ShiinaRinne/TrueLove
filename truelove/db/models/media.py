from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from truelove.db.base import Base

class Media(Base):
    __tablename__ = 'Media'

    id = Column(Integer, primary_key=True)
    w_id = Column(Integer, ForeignKey('Watching.w_id'), nullable=False)
    

    media_id = Column(Text, nullable=False, unique= True)
    media_type = Column(Text, nullable=False)
    media_name = Column(Text, nullable=False)
    media_cover = Column(Text)
    media_intro = Column(Text)
    media_pubdate = Column(Integer, default=0)
    media_videos = Column(Integer, default=1)
    media_created = Column(Text, nullable=False)
    
    download_status = Column(Integer, default=0)
    download_path = Column(Text, default="")
    
    watch = relationship("Watching", back_populates="medias")



