import datetime
import random

from fastapi import FastAPI, APIRouter, HTTPException
from starlette.status import HTTP_404_NOT_FOUND

app = FastAPI()
bases = APIRouter(prefix="/bases")

cache = {}
pdn_eles = {}
"""
2. Информация об обязательствах:
1. Вид обязательств
2. Даты (открытия, плановое закрытие, фактическое закрытие)
3. Роль (заемщик, поручитель, созаемщик)
4. Статус (текущий, завершенный)
5. Сумма
6. % ставка
5. Остаток к выплате
8. Просрочка в разрезе срока (1-30, 31-60, 61-90, 91-150, 151-180, >180) 
9. Сумма просрочки"""


def generator_date(old_date=None):
    gen = datetime.date(2023, random.randint(1, 12), random.randint(1, 28))

    if not old_date:
        return gen

    if gen <= old_date:
        return generator_date(old_date)

    return gen


def generator_bki():
    open_date = generator_date()
    close_plan = generator_date(open_date)
    close_real = generator_date(close_plan)
    status = random.choice(["текущий", "завершенный"])
    summ = random.randint(100, 10000000)
    rel = None
    pros = 0
    pros_summ = 0

    if status == "текущий":
        rel = random.randint(100, summ)
        close_real = None
        pros = random.choice(["0", "1-30", "31-60", "61-90", "91-150", "151-180", ">180"])

    if pros != "0" or pros is not None:
        pros_summ = random.randint(100, summ)

    return {
        "type": random.choice(["кредит", "облигация", "аренда"]),
        "dates": {
            "открытия": open_date,
            "закрытия": close_real,
            "ожидаемо": close_plan
        },
        "role": random.choice(["заемщик", "поручитель", "созаемщик"]),
        "status": status,
        "amount": summ,
        "rate": random.random() * 100,
        "repayment": rel,
        "interval": pros,
        "debt_amount": pros_summ
    }


@app.get("/bki")
async def get_bki(passport_series, passport_number):
    string = f"{passport_series} {passport_number}"
    result = cache.get(string)
    if result:
        return cache[string]

    score = random.randint(300, 900)

    bki_obligations = []
    for i in range(random.randint(0, 5)):
        bki_obligations.append(generator_bki())

    cache[string] = {
        "score": score,
        "obligations": bki_obligations
    }

    return cache[string]


@app.get("/pdn")
async def get_pdn(passport_series, passport_number):
    string = f"{passport_series} {passport_number}"
    result = cache.get(string)
    pdn = pdn_eles.get(string)
    if pdn:
        return pdn

    if not result:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="bki not found")

    salary = random.randint(10000, 1000000)
    elements_sum = sum(element["repayment"] or 0 for element in result["obligations"])
    pdn = elements_sum / salary * 100
    pdn_eles[string] = pdn
    return pdn_eles[string]


@bases.get("/mvd")
async def get_mvd(first_name, middle_name, last_name, passport_series, passport_number):
    string = f"{passport_series} {passport_number}"
    result = cache.get(string)
    if not result:
        cache[string] = random.choice([True, False])

    return cache[string]


@bases.get("/bankruptcy")
async def get_bankruptcy(first_name, middle_name, last_name, passport_series, passport_number):
    string = f"{passport_series} {passport_number}"
    result = cache.get(string)
    if not result:
        cache[string] = random.choice([True, False])

    return cache[string]


@bases.get("/enforcement")
async def get_enforcement(first_name, middle_name, last_name, passport_series, passport_number):
    string = f"{passport_series} {passport_number}"
    result = cache.get(string)
    if not result:
        cache[string] = random.choice([True, False])

    return cache[string]
