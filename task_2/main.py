import csv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from models import Base, Player, Level, Prize, PlayerLevel, LevelPrize

engine = create_engine('sqlite:///sqlite_test.db')
Session = sessionmaker(bind=engine, expire_on_commit=False)
session = Session()


def export_to_csv(session: Session, csv_file_path: str, chunk_size: int = 1000):
    """
    Экспортирует данные о игроках, уровнях, статусе прохождения и призах в CSV.

    :param session: активная сессия SQLAlchemy
    :param csv_file_path: путь к CSV файлу для записи
    :param chunk_size: размер порции выборки данных, по умолчанию 1000 записей
    """
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['player_id', 'level_title', 'is_completed', 'prize_title'])

        offset = 0
        while True:
            query = (session.execute(
                select(Player.player_id, Level.title, PlayerLevel.is_completed, Prize.title)
                .join(PlayerLevel, PlayerLevel.player_id == Player.id)
                .join(Level, Level.id == PlayerLevel.level_id)
                .join(LevelPrize, LevelPrize.level_id == Level.id)
                .join(Prize, Prize.id == LevelPrize.prize_id)
                .offset(offset).limit(chunk_size)
            )).fetchall()

            if not query:
                break

            for row in query:
                writer.writerow([row.player_id, row.title, row.is_completed, row.title])

            offset += chunk_size

    print(f"Экспорт завершен! Данные записаны в '{csv_file_path}'.")


def initialize_database() -> None:
    """
    Инициализирует базу данных, удаляя и создавая таблицы.
    """
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def insert_data() -> None:
    """
    Вставляет начальные данные в базу: игрока, уровень, приз и запись о прохождении уровня.

    Эта функция создает нового игрока, уровень, приз и связывает их в таблице PlayerLevel,
    а затем сохраняет все данные в базе данных.
    """
    with Session() as session:
        player = Player(player_id=1)
        level = Level(title="Горы Айсрека")
        prize = Prize(title="Топор")
        player_level = PlayerLevel(player_id=1, level_id=1)

        session.add_all([player, level, prize, player_level])
        session.commit()


def create_assign_prize_and_export_csv() -> None:
    """
    Обновляет статус уровня игрока, присваивает приз и экспортирует данные в CSV файл.

    Эта функция извлекает уровень игрока и приз из базы данных, обновляет статус уровня
    на "пройден", присваивает игроку приз, если уровень пройден, и затем экспортирует данные
    в CSV файл.
    """
    with Session() as session:
        player_level = session.execute(select(PlayerLevel).where(PlayerLevel.id == 1)).scalars().first()
        prize = session.execute(select(Prize).where(Prize.title == "Топор")).scalars().first()

        player_level.is_completed = True

        if player_level.is_completed:
            player_level.assign_prize(prize, session)

        export_to_csv(session, 'exported_data.csv')


if __name__ == '__main__':
    initialize_database()
    insert_data()
    create_assign_prize_and_export_csv()
