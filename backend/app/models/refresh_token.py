from sqlalchemy import Boolean, Column, ForeignKey,DateTime,Integer,String, false
from sqlalchemy.sql import func
from ..database import Base

class RefreshToken(Base):
    __tablename__="refresh_tokens"

    id = Column(Integer,primary_key=True,index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id",ondelete="CASCADE"),
        nullable= false,
        index = True
    )
    token_hash= Column(
        String(255),
        nullable= false,
        unique= True
    )

    expires_at = Column(
        DateTime,
        nullable= false
    )
    revoked = Column(
        Boolean,
        default= false,
        nullable= false 
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable= false
    )