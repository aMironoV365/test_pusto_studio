import pytz
from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from datetime import datetime

Base = declarative_base()

moscow_tz = pytz.timezone('Europe/Moscow')


class Player(Base):
    """
    Модель игрока, содержащая информацию о пользователе, его последнем входе, баллах за день и назначенных бустах.

    Атрибуты:
        id (int): Уникальный идентификатор игрока (первичный ключ).
        username (str): Имя пользователя игрока, уникальное.
        first_login (datetime): Дата и время первого входа игрока.
        last_login (datetime): Дата и время последнего входа игрока.
        daily_points (int): Количество баллов, начисленных игроку за сегодняшний день.
        boosts (str): Описание активных бустов у игрока.

    Методы:
        login(): Обновляет дату последнего входа игрока, если это первый вход - также записывает первый.
        assign_boost(boost_description: str): Назначает буст игроку.
    """
    __tablename__ = 'players'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    first_login: Mapped[datetime] = mapped_column(default=lambda: datetime.now(moscow_tz))
    last_login: Mapped[datetime] = mapped_column(default=lambda: datetime.now(moscow_tz))
    daily_points: Mapped[int] = mapped_column(default=0)
    boosts: Mapped[str] = mapped_column(default="")

    def login(self) -> None:
        """
        Обновляет информацию о входе игрока.

        Если это первый вход, то устанавливает значение first_login в текущее время.
        Обновляет значение last_login на текущее время.
        Увеличивает количество баллов за сегодняшний день на 1.

        Возвращает:
            None
        """
        now = datetime.now(moscow_tz)
        if self.first_login is None:
            self.first_login = now
        self.last_login = now
        if self.daily_points is None:
            self.daily_points = 0

        self.daily_points += 1

    def assign_boost(self, boost_description) -> None:
        """
        Назначает буст игроку.

        Устанавливает значение поля boosts на описание переданного буста.

        Аргументы:
            boost_description (str): Описание буста.

        Возвращает:
            None
        """
        self.boosts = boost_description


class Boost(Base):
    """
    Модель буста, который может быть назначен игрокам.

    Атрибуты:
        id (int): Уникальный идентификатор буста (первичный ключ).
        boost_type (str): Тип буста (например, "Усиление").
        description (str): Описание буста, что он делает.
    """
    __tablename__ = 'boosts'

    id: Mapped[int] = mapped_column(primary_key=True)
    boost_type: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column()
