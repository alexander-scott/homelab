from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator, Generator, Sequence

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Depends, Query
from fastapi.responses import PlainTextResponse, RedirectResponse
from sqlmodel import Field, Session, SQLModel, create_engine, select

sqlite_url = "sqlite:///database.db"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "localhost:5173"],  # Our web app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class URL(SQLModel, table=True):  # type: ignore
    short_url: str = Field(index=True, primary_key=True)
    full_url: str = Field(index=True)


@app.get("/get")
def read_all_urls(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> Sequence[URL]:
    urls = session.exec(select(URL).offset(offset).limit(limit)).all()
    return urls


@app.post("/create")
def create_url(new_url: URL, session: SessionDep) -> URL:
    session.add(new_url)
    session.commit()
    session.refresh(new_url)
    return new_url


urls = [{"id": "1", "item": "www.google.com"}, {"id": "2", "item": "www.youtube.com"}]


@app.get("/url", tags=["urls"])
async def get_urls() -> dict[str, list[dict[str, str]]]:
    return {"data": urls}


@app.post("/url", tags=["urls"])
async def add_url(url: dict[str, str]) -> dict[str, set[str]]:
    urls.append(url)
    return {"data": {"URL added."}}


@app.put("/url/{id}", tags=["urls"])
async def update_url(id: int, body: dict[str, str]) -> dict[str, str]:
    for url in urls:
        if int(url["id"]) == id:
            url["item"] = body["item"]
            return {"data": f"URL with id {id} has been updated."}

    return {"data": f"URL with id {id} not found."}


@app.delete("/url/{id}", tags=["urls"])
async def delete_url(id: int) -> dict[str, str]:
    for url in urls:
        if int(url["id"]) == id:
            urls.remove(url)
            return {"data": f"URL with id {id} has been removed."}

    return {"data": f"URL with id {id} not found."}


@app.get("/{arg}")
def redirect_to_long_url(arg: str, session: SessionDep) -> RedirectResponse:
    url = session.get(URL, arg)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url.full_url)


@app.get("/")
def root() -> PlainTextResponse:
    return PlainTextResponse("bla")
