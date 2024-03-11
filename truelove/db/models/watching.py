from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Text
from sqlalchemy.schema import UniqueConstraint
from truelove.db.base import Base


class Watching(Base):
    __tablename__ = 'Watching'
    
    w_id = Column(Integer, primary_key=True)  # watching id
    author = Column(Text, nullable=False)
    uid = Column(Text, nullable=False)
    platform = Column(Text, nullable=False)
    core = Column(Text, nullable=False)  # 使用的core
    add_time = Column(Text, nullable=False)  # 添加到关注的时间
    watch_type = Column(Text, nullable=False)  # 关注的类型
    

    videos = relationship("Video", back_populates="watch") 
    dynamics = relationship("Dynamic", back_populates="watch")
    
    __table_args__ = (UniqueConstraint('uid', 'watch_type', name='_uid_watch_type_uc'),)