import pytz
from sqlalchemy.orm import Mapped, mapped_column, declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()

moscow_tz = pytz.timezone('Europe/Moscow')


class Player(Base):
    __tablename__ = 'players'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    first_login: Mapped[datetime] = mapped_column(default=lambda: datetime.now(moscow_tz))
    last_login: Mapped[datetime] = mapped_column(default=lambda: datetime.now(moscow_tz))
    daily_points: Mapped[int] = mapped_column(default=0)
    boosts: Mapped[str] = mapped_column(default="")

    def login(self):
        """Обновление информации о входе игрока."""
        now = datetime.now(moscow_tz)
        if self.first_login is None:
            self.first_login = now
        self.last_login = now
        if self.daily_points is None:
            self.daily_points = 0

        self.daily_points += 1

    def assign_boost(self, boost_description):
        """Назначение буста игроку."""
        self.boosts = boost_description


class Boost(Base):
    __tablename__ = 'boosts'

    id: Mapped[int] = mapped_column(primary_key=True)
    boost_type: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column()
