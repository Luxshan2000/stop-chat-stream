from sqlalchemy import Boolean, Column, String

from be.configs.database import Base


class AbortSignal(Base):
    __tablename__ = "abort"

    id = Column(String, primary_key=True, index=True)
    flag = Column(Boolean, default=False)
