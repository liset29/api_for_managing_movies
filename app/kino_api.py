import httpx
from fastapi import HTTPException
from const import URL_KINO,  HEADERS


async def find_movies(query: str):
    params = {"keyword": query}
    url = f'{URL_KINO}api/v2.1/films/search-by-keyword'

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS, params=params)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to get movie data."
            )

        data = response.json()

        return [
            {
                "kinopoisk_id": film.get("filmId"),
                "name": film.get("nameRu"),
                "year": film.get("year"),
                "rating": film.get("rating"),
            }
            for film in data.get("films", [])
        ]

async def find_detail_movies(kino_id):
    params = {"keyword": kino_id}
    url = f'{URL_KINO}/api/v2.2/films/{kino_id}'

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS, params=params)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to get movie data."
            )

        data = response.json()

        return data
