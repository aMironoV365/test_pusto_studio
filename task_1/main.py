from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from models import Base, Player, Boost

engine = create_engine('sqlite:///sqlite_test.db')
Session = sessionmaker(bind=engine, expire_on_commit=False)
session = Session()

if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    player = Player(username="andrey")

    boost = Boost(boost_type="Усиление", description="Добыча золота увеличена на 20%")

    session.add(player)
    session.add(boost)
    session.commit()
    session.close()

    with Session() as ses:
        player = ses.execute(select(Player).where(Player.username == "andrey")).scalars().first()
        boost = ses.execute(select(Boost).where(Boost.boost_type == "Усиление")).scalars().first()
        player.login()

        player.assign_boost(boost.description)

        ses.commit()
