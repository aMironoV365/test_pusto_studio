from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from models import Base, Player, Boost

engine = create_engine('sqlite:///sqlite_test.db')
Session = sessionmaker(bind=engine, expire_on_commit=False)


def initialize_database() -> None:
    """
    Инициализирует базу данных, удаляя и создавая таблицы.
    """
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def insert_data() -> None:
    """
    Вставляет начальные данные в базу данных: создает нового игрока и новый буст.
    """
    with Session() as session:
        player = Player(username="andrey")

        boost = Boost(boost_type="Усиление", description="Добыча золота увеличена на 20%")

        session.add_all([player, boost])
        session.commit()


def create_and_assign_boost() -> None:
    """
    Находит игрока и буст по их идентификаторам и присваивает буст игроку.
    Выполняет логин игрока и присваивает ему буст для увеличения добычи золота.
    """
    with Session() as session:
        player = session.execute(select(Player).where(Player.username == "andrey")).scalars().first()
        boost = session.execute(select(Boost).where(Boost.boost_type == "Усиление")).scalars().first()

        player.login()

        player.assign_boost(boost.description)

        session.commit()


if __name__ == '__main__':
    initialize_database()
    insert_data()
    create_and_assign_boost()
