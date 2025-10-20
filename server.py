from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from random import random, choice

app = FastAPI(
    title="Gifts Battle Backend",
    description="Простой сервер для имитации рулетки, пополнения и инвентаря",
    version="1.0.0"
)

# -----------------------
# НАСТРОЙКИ CORS (для WebApp)
# -----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # при деплое замени на свой домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------
# МОДЕЛИ ДАННЫХ
# -----------------------
class SpinResult(BaseModel):
    prize: str
    balance: float

class BalanceRequest(BaseModel):
    amount: float
    currency: str

class WithdrawRequest(BaseModel):
    type: str  # "TON", "NFT" или "STARS"
    amount: float

# -----------------------
# ВРЕМЕННЫЕ ПЕРЕМЕННЫЕ (имитация базы)
# -----------------------
user_balance = {
    "TON": 10.0,
    "STARS": 5000,
}

user_inventory = []

# -----------------------
# РОУТЫ
# -----------------------

@app.get("/")
def root():
    return {"message": "🎁 Gifts Battle backend работает!"}


@app.get("/balance")
def get_balance():
    """Показать баланс пользователя"""
    return user_balance


@app.post("/topup")
def topup(req: BalanceRequest):
    """Имитация пополнения баланса"""
    if req.currency in user_balance:
        user_balance[req.currency] += req.amount
        return {"status": "ok", "balance": user_balance}
    return {"status": "error", "message": "неизвестная валюта"}


@app.post("/spin")
def spin():
    """Рулетка: шанс выпадения подарков и наград"""
    chance = random() * 100
    prize = None

    if chance < 45:
        prize = "🎁 Подарок: Мишка"
        user_inventory.append(prize)
    elif chance < 75:
        prize = "🚀 Подарок: Ракета"
        user_inventory.append(prize)
    elif chance < 100:
        # Случайный денежный приз
        options = [
            ("1 TON", 25),
            ("2 TON", 15),
            ("1000 STARS", 5),
            ("5000 STARS", 1)
        ]
        prizes = []
        for name, _ in options:
            prizes.append(name)
        prize = choice(prizes)
        if "TON" in prize:
            ton = int(prize.split()[0])
            user_balance["TON"] += ton
        else:
            stars = int(prize.split()[0])
            user_balance["STARS"] += stars
    else:
        prize = "😔 Ничего не выпало"

    return {"prize": prize, "balance": user_balance, "inventory": user_inventory}


@app.get("/inventory")
def get_inventory():
    """Показать предметы пользователя"""
    return {"inventory": user_inventory}


@app.post("/withdraw")
def withdraw(req: WithdrawRequest):
    """Имитация вывода TON, NFT или звёзд"""
    if req.type == "TON":
        if user_balance["TON"] >= req.amount:
            user_balance["TON"] -= req.amount
            return {"status": "ok", "message": f"Выведено {req.amount} TON"}
        else:
            return {"status": "error", "message": "Недостаточно TON"}
    elif req.type == "STARS":
        if user_balance["STARS"] >= req.amount:
            user_balance["STARS"] -= req.amount
            return {"status": "ok", "message": f"Выведено {req.amount} звёзд"}
        else:
            return {"status": "error", "message": "Недостаточно звёзд"}
    elif req.type == "NFT":
        return {"status": "ok", "message": "NFT передан менеджеру"}
    else:
        return {"status": "error", "message": "Неизвестный тип вывода"}
