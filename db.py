python
# Simple SQLite models + helper
from sqlalchemy import (create_engine, MetaData, Table, Column,
                        Integer, String, JSON, Float, Boolean, DateTime)
from sqlalchemy.sql import func
from sqlalchemy import select
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./gifts_battle.db')
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('tg_id', Integer, unique=True, nullable=False),
    Column('balance_ton', Float, default=0.0),
    Column('balance_stars', Integer, default=0),
    Column('balance_nft_credit', Integer, default=0),
    Column('created_at', DateTime, server_default=func.now()),
)

inventory = Table(
    'inventory', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, nullable=False),
    Column('item_type', String, nullable=False), # e.g. 'bear','rocket','1ton','2ton','1000stars','5000stars','nft'
    Column('metadata', JSON, nullable=True),
    Column('created_at', DateTime, server_default=func.now()),
)

withdrawals = Table(
    'withdrawals', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, nullable=False),
    Column('kind', String, nullable=False), # 'ton','stars','nft'
    Column('amount', Float, nullable=True),
    Column('nft_info', JSON, nullable=True),
    Column('status', String, default='pending'),
    Column('created_at', DateTime, server_default=func.now()),
)

metadata.create_all(engine)

# Helper functions
from sqlalchemy import insert, update
from sqlalchemy.engine import Result

conn = engine.connect()

def get_or_create_user(tg_id:int):
    q = select(users).where(users.c.tg_id==tg_id)
    r = conn.execute(q).first()
    if r:
        return dict(r)
    else:
        ins = insert(users).values(tg_id=tg_id, balance_ton=0.0, balance_stars=0, balance_nft_credit=0)
        res = conn.execute(ins)
        uid = res.inserted_primary_key[0]
        q2 = select(users).where(users.c.id==uid)
        return dict(conn.execute(q2).first())

def add_balance(tg_id:int, ton:float=0.0, stars:int=0, nft_credit:int=0):
    u = get_or_create_user(tg_id)
    upd = update(users).where(users.c.tg_id==tg_id).values(
        balance_ton = users.c.balance_ton + ton,
        balance_stars = users.c.balance_stars + stars,
        balance_nft_credit = users.c.balance_nft_credit + nft_credit
    )
    # SQLAlchemy can't use column objects in values with this simple approach, so read and write manually:
    new_ton = u['balance_ton'] + ton
    new_stars = u['balance_stars'] + stars
    new_nft = u['balance_nft_credit'] + nft_credit
    conn.execute(update(users).where(users.c.tg_id==tg_id).values(balance_ton=new_ton, balance_stars=new_stars, balance_nft_credit=new_nft))
    return get_or_create_user(tg_id)

def get_user_by_tg(tg_id:int):
    q = select(users).where(users.c.tg_id==tg_id)
    r = conn.execute(q).first()
    return dict(r) if r else None

def add_inventory(user_id:int, item_type:str, metadata:dict=None):
    res = conn.execute(insert(inventory).values(user_id=user_id, item_type=item_type, metadata=metadata or {}))
    return res.inserted_primary_key[0]

def list_inventory(user_id:int):
    q = select(inventory).where(inventory.c.user_id==user_id)
    rows = conn.execute(q).fetchall()
    return [dict(r) for r in rows]

def create_withdrawal(user_id:int, kind:str, amount:float=None, nft_info:dict=None):
    res = conn.execute(insert(withdrawals).values(user_id=user_id, kind=kind, amount=amount, nft_info=nft_info, status='pending'))
    return res.inserted_primary_key[0]

def list_withdrawals():
    q = select(withdrawals).order_by(withdrawals.c.created_at.desc())
    rows = conn.execute(q).fetchall()
    return [dict(r) for r in rows]

def set_withdrawal_status(wid:int, status:str):
    conn.execute(update(withdrawals).where(withdrawals.c.id==wid).values(status=status))
