# lab5/main.py
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, select, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from config import DB_URL

engine = create_engine(DB_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    content = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")

def main():
    Base.metadata.create_all(engine)
    db = Session()
    
    # CRUD ORM
    u = User(username="petya", email="petya@test.com")
    db.add(u)
    db.commit()
    db.refresh(u)
    
    users = db.scalars(select(User).where(User.email.like("%@test.com"))).all()
    print(f"ORM filter: {[x.username for x in users]}")
    
    # Raw SQL
    with engine.connect() as conn:
        conn.execute(Post.__table__.insert().values(title="SQL Post", content="...", user_id=u.id))
        conn.commit()
        count = conn.scalar(select(func.count()).select_from(Post.__table__))
        print(f"SQL count: {count}")
    
    # Transaction
    try:
        nu = User(username="trx", email="trx@t.com")
        db.add(nu)
        db.flush()
        db.add(Post(title="Trx", content="Ok", user_id=nu.id))
        db.commit()
    except:
        db.rollback()
    finally:
        db.close()
    
    print("Done")

if __name__ == "__main__":
    main()