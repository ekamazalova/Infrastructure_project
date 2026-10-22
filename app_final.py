import os
import logging

from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Book Catalog API", version="1.0.0")

LIBRARY_NAME = os.getenv("LIBRARY_NAME", "Моя библиотека")

BOOKS_DB = [
    {"id": 1, "title": "Мастер и Маргарита", "author": "Михаил Булгаков", "genre": "фантастика"},
    {"id": 2, "title": "Преступление и наказание", "author": "Фёдор Достоевский", "genre": "драма"},
    {"id": 3, "title": "1984", "author": "Джордж Оруэлл", "genre": "фантастика"},
    {"id": 4, "title": "Шерлок Холмс", "author": "Артур Конан Дойл", "genre": "детектив"}
]


@app.get("/health")
def health_check():
    logger.info("Проверка работоспособности")
    return {"status": "ok"}


@app.get("/version")
def get_version():
    return {"version": "1.0.0"}


@app.get("/books")
def get_books():
    logger.info("Получение списка книг")
    return {"books": BOOKS_DB}


@app.get("/books/genre/{genre}")
def get_books_by_genre(genre: str):
    logger.info(f"Поиск книг по жанру: {genre}")

    filtered = [
        book for book in BOOKS_DB
        if book["genre"].lower() == genre.lower()
    ]

    if not filtered:
        raise HTTPException(
            status_code=404,
            detail="Книги в таком жанре не найдены"
        )

    return {"genre": genre, "books": filtered}


@app.get("/library-info")
def get_library_info():
    return {
        "library_name": LIBRARY_NAME,
        "total_books": len(BOOKS_DB)
    }