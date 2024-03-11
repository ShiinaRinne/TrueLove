from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

from truelove.db.base import Base

class Dynamic(Base):
    __tablename__ = 'Dynamic'

    id = Column(Integer, primary_key=True)
    w_id = Column(Integer, ForeignKey('Watching.w_id'), nullable=False)
    
    dynamic_id = Column(Text, nullable=False, unique= True)
    dynamic_pub_ts = Column(Integer, default=0)
    dynamic_pub_time = Column(Text, nullable=False)
    
    download_status = Column(Integer, default=0)
    download_path = Column(Text, default="")
    
    watch = relationship("Watching", back_populates="dynamics")

