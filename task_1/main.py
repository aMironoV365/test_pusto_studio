import pytz
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column, declarative_base
from datetime import datetime

Base = declarative_base()

moscow_tz = pytz.timezone('Europe/Moscow')


class Player(Base):
    __tablename__ = 'players'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    first_login: Mapped[DateTime] = mapped_column(default=datetime.now(moscow_tz))
    last_login: Mapped[DateTime] = mapped_column()
    daily_points: Mapped[int] = mapped_column(default=0)

    boosts: Mapped['PlayerBoost'] = relationship('PlayerBoost', back_populates='player')

    def login(self):
        """Обновление информации о входе игрока."""
        now = datetime.now(moscow_tz)
        if self.first_login is None:
            self.first_login = now
        self.last_login = now
        self.daily_points += 1  # Начисляем баллы за вход


class Boost(Base):
    __tablename__ = 'boosts'

    id: Mapped[int] = mapped_column(primary_key=True)
    boost_type: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column()




class PlayerBoost(Base):
    __tablename__ = 'player_boosts'

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey('players.id'), ondelete='CASCADE')
    boost_id: Mapped[int] = mapped_column(ForeignKey('boosts.id'))
    assigned_at: Mapped[DateTime] = mapped_column(default=datetime.now(moscow_tz))

    player = relationship("Player", back_populates="boosts")
    boost = relationship("Boost")

    def assign_boost(self, player, boost):
        """Назначение буста игроку."""
        self.player = player
        self.boost = boost
        self.assigned_at = datetime.now(moscow_tz)


print(datetime.now(moscow_tz))
