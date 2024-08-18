import os

from sqlalchemy import create_engine, delete
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, Session
from sqlalchemy.types import Integer
import sys

sys.path.append('../')
from api.networks import NetworkType


class Base(DeclarativeBase):
    pass


class Config(Base):
    __tablename__ = "config"

    network: Mapped[NetworkType] = mapped_column("network", Integer(), primary_key=True)
    backend_uptime: Mapped[float] = mapped_column("BACKEND_UPTIME")

class Friend(Base):
    __tablename__ = "friends"

    friend_code: Mapped[str] = mapped_column("friendCode", primary_key=True, nullable=False, unique=True)
    network: Mapped[NetworkType] = mapped_column("network", Integer())
    online: Mapped[bool]
    title_id: Mapped[str] = mapped_column("titleID", nullable=False)
    upd_id: Mapped[str] = mapped_column("updID", nullable=False)
    last_accessed: Mapped[int] = mapped_column("lastAccessed", nullable=False)
    account_creation: Mapped[int] = mapped_column("accountCreation", nullable=False)
    username: Mapped[str]
    message: Mapped[str]
    mii: Mapped[str]
    joinable: Mapped[bool]
    game_description: Mapped[str] = mapped_column("gameDescription", nullable=False)
    last_online: Mapped[int] = mapped_column("lastOnline", nullable=False)
    favorite_game: Mapped[int] = mapped_column("jeuFavori", nullable=False)



class DiscordFriends(Base):
    __tablename__ = "discordFriends"

    id: Mapped[int] = mapped_column(primary_key=True)
    friend_code: Mapped[str] = mapped_column("friendCode", primary_key=True, nullable=False)
    network: Mapped[NetworkType] = mapped_column("network", Integer())
    active: Mapped[bool] = mapped_column(nullable=False)

class Discord(Base):
    __tablename__ = "discord"

    id: Mapped[int] = mapped_column("ID", primary_key=True, nullable=False, unique=True)
    refresh: Mapped[str] = mapped_column("refresh", nullable=False)
    bearer: Mapped[str] = mapped_column("bearer", nullable=False)
    session: Mapped[str] = mapped_column("session")
    token: Mapped[str] = mapped_column("token", unique=True)
    last_accessed: Mapped[int] = mapped_column("lastAccessed", nullable=False)
    generation_date: Mapped[int] = mapped_column("generationDate", nullable=False)
    show_profile_button: Mapped[bool] = mapped_column("showProfileButton", nullable=False, default=True)
    show_small_image: Mapped[bool] = mapped_column("showSmallImage", nullable=False, default=True)

def start_db_time(time: float, network_type: NetworkType):
    """Updates the database to track the starting time for the specific backend."""
    engine = create_engine('sqlite:///' + os.path.abspath('sqlite/fcLibrary.db'))
    with Session(engine) as session:
        # TODO: This should be an upsert, not a deletion and insertion.
        session.execute(delete(Config).where(Config.network == network_type))
        new_time = Config(network=network_type, backend_uptime=time)
        session.add(new_time)
        session.commit()
