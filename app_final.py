
import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LIBRARY_NAME = os.getenv("LIBRARY_NAME", "Моя библиотека")
APP_VERSION = "1.1.0"

BOOKS_DB = [
    {
        "id": 1,
        "title": "Мастер и Маргарита",
        "author": "Михаил Булгаков",
        "genre": "фантастика"
    },
    {
        "id": 2,
        "title": "Преступление и наказание",
        "author": "Фёдор Достоевский",
        "genre": "драма"
    },
    {
        "id": 3,
        "title": "1984",
        "author": "Джордж Оруэлл",
        "genre": "фантастика"
    },
    {
        "id": 4,
        "title": "Шерлок Холмс",
        "author": "Артур Конан Дойл",
        "genre": "детектив"
    }
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Запуск каталога книг: %s", LIBRARY_NAME)
    yield
    logger.info("Остановка каталога книг")


app = FastAPI(
    title="Book Catalog API",
    description="Электронный каталог книг",
    version=APP_VERSION,
    lifespan=lifespan
)


@app.get("/health")
def health_check():
    logger.info("Проверка работоспособности")
    return {"status": "ok"}


@app.get("/version")
def get_version():
    logger.info("Запрос версии приложения")
    return {"version": APP_VERSION}


@app.get("/books")
def get_books():
    logger.info("Запрос полного списка книг")
    return {"books": BOOKS_DB}


@app.get("/books/search")
def search_books(query: str = Query(min_length=1)):
    logger.info("Поиск книг по запросу: %s", query)

    found = [
        book for book in BOOKS_DB
        if query.casefold() in book["title"].casefold()
        or query.casefold() in book["author"].casefold()
    ]

    logger.info("Найдено книг: %d", len(found))
    return {"query": query, "books": found}


@app.get("/books/genre/{genre}")
def get_books_by_genre(genre: str):
    logger.info("Поиск книг по жанру: %s", genre)

    found = [
        book for book in BOOKS_DB
        if book["genre"].casefold() == genre.casefold()
    ]

    if not found:
        logger.warning("Книги жанра %s не найдены", genre)
        raise HTTPException(
            status_code=404,
            detail="Книги в таком жанре не найдены"
        )

    logger.info("Найдено книг: %d", len(found))
    return {"genre": genre, "books": found}


@app.get("/books/{book_id}")
def get_book_by_id(book_id: int):
    logger.info("Поиск книги с ID: %d", book_id)

    for book in BOOKS_DB:
        if book["id"] == book_id:
            return book

    logger.warning("Книга с ID %d не найдена", book_id)
    raise HTTPException(
        status_code=404,
        detail="Книга не найдена"
    )


@app.get("/library-info")
def get_library_info():
    logger.info("Запрос информации о библиотеке")
    return {
        "library_name": LIBRARY_NAME,
        "total_books": len(BOOKS_DB)
    }
