import json
import threading
import time

import schedule
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.DadosFlash import FlashAPI
from app.database import ApiCnpj
from app.insertBanco import DataBase
from app.config import settings


app = FastAPI(title="flashapi", description="busca dados", redoc_url="/")
banco = DataBase()
api_cnpj = ApiCnpj()
origins = settings.CORS_ORIGINS



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/dados-rastreio")
def flashApi(request: Request, id_rastreio: int):
    flash_api = FlashAPI()
    dados = flash_api.buscar_dados(id_rastreio)
    return dados


@app.get("/cnpj")
def pegaDados(request: Request, cnpj: int):
    dados = api_cnpj.retorna_lista_de_pedidos(cnpj)
    if dados:
        return dados


@app.on_event("startup")
def alimentaBanco():
    schedule.every(5).hours.do(banco.insert_banco)
    print("Jobs:", schedule.jobs)


def run_continuously(interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()

    return cease_continuous_run


stop_run_continuously = run_continuously()


@app.on_event("shutdown")
def stop_scheduler():
    stop_run_continuously.set()


if __name__ == "__main__":
    pegaDados()