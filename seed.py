# seed.py
from db import SessionLocal, engine, Base
from models import Category, Product, User
from passlib.context import CryptContext

pwd = CryptContext(schemes=['bcrypt'], deprecated='auto')

def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(Category).count() == 0:
        c1 = Category(name='Almacén', icon='package', color='text-purple-700')
        c2 = Category(name='Bebidas', icon='cup-soda', color='text-purple-700')
        db.add_all([c1,c2]); db.commit()
    if db.query(User).filter(User.email=='admin@example.com').count() == 0:
        user = User(name='Admin', email='admin@example.com', hashed_password=pwd.hash('password123'), is_admin=True)
        db.add(user); db.commit()
    db.close()
    print('Seed complete')

if __name__ == '__main__':
    run()
