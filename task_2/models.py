import pytz
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from datetime import datetime

Base = declarative_base()

moscow_tz = pytz.timezone('Europe/Moscow')


class Player(Base):
    """
    Модель игрока, представляющая пользователя системы.

    Атрибуты:
        id (int): Уникальный идентификатор игрока (первичный ключ).
        player_id (str): Уникальный идентификатор игрока (например, имя пользователя).
        player_levels (list[PlayerLevel]): Связь с уровнями игрока (список объектов PlayerLevel).
    """
    __tablename__ = 'players'

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[str] = mapped_column(String(100), nullable=False)

    player_levels: Mapped[list['PlayerLevel']] = relationship("PlayerLevel", back_populates="player")


class Level(Base):
    """
    Модель уровня игры, представляющая один из этапов игры.

    Атрибуты:
        id (int): Уникальный идентификатор уровня (первичный ключ).
        title (str): Название уровня.
        order (int): Порядковый номер уровня (по умолчанию 0).
        level_prizes (list[LevelPrize]): Связь с призами уровня (список объектов LevelPrize).
    """
    __tablename__ = 'levels'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    order: Mapped[int] = mapped_column(default=0)

    level_prizes: Mapped[list['LevelPrize']] = relationship("LevelPrize", back_populates="level")


class Prize(Base):
    """
    Модель приза, который игрок может получить за выполнение уровней.

    Атрибуты:
        id (int): Уникальный идентификатор приза (первичный ключ).
        title (str): Название приза.
    """
    __tablename__ = 'prizes'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)


class PlayerLevel(Base):
    """
    Модель для хранения информации о прохождении игроком уровня.

    Атрибуты:
        id (int): Уникальный идентификатор записи (первичный ключ).
        player_id (int): Внешний ключ, связывающий с игроком.
        level_id (int): Внешний ключ, связывающий с уровнем.
        completed (datetime): Дата и время завершения уровня.
        is_completed (bool): Статус завершения уровня.
        score (int): Очки, набранные игроком на уровне.
        player (Player): Связь с игроком.
        level (Level): Связь с уровнем.

    Методы:
        assign_prize(prize, session): Присваивает приз игроку за выполнение уровня.
    """
    __tablename__ = 'player_levels'

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey('players.id', ondelete='CASCADE'))
    level_id: Mapped[int] = mapped_column(ForeignKey('levels.id', ondelete='CASCADE'))
    completed: Mapped[datetime] = mapped_column(default=lambda: datetime.now(moscow_tz))
    is_completed: Mapped[bool] = mapped_column(default=False)
    score: Mapped[int] = mapped_column(default=0)

    player: Mapped['Player'] = relationship("Player", back_populates="player_levels")
    level: Mapped['Level'] = relationship("Level")

    def assign_prize(self, prize, session):
        """
        Присваивает приз игроку за прохождение уровня.

        :param prize: Приз, который должен быть присвоен.
        :param session: Сессия SQLAlchemy для выполнения операций с базой данных.
        """
        level_prize = LevelPrize(level=self.level, prize=prize, received=datetime.now(moscow_tz))
        session.add(level_prize)
        session.commit()
        print(f"Приз '{prize.title}' присвоен игроку за прохождение уровня '{self.level.title}'.")


class LevelPrize(Base):
    """
    Модель, представляющая приз, который был получен на уровне.

    Атрибуты:
        id (int): Уникальный идентификатор записи (первичный ключ).
        level_id (int): Внешний ключ, связывающий с уровнем.
        prize_id (int): Внешний ключ, связывающий с призом.
        received (datetime): Дата и время получения приза.
    """
    __tablename__ = 'level_prizes'

    id: Mapped[int] = mapped_column(primary_key=True)
    level_id: Mapped[int] = mapped_column(ForeignKey('levels.id', ondelete='CASCADE'))
    prize_id: Mapped[int] = mapped_column(ForeignKey('prizes.id'))
    received: Mapped[datetime] = mapped_column(default=lambda: datetime.now(moscow_tz))

    level: Mapped['Level'] = relationship("Level", back_populates="level_prizes")
    prize: Mapped['Prize'] = relationship("Prize")
