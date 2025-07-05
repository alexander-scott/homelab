from typing import Annotated, Sequence

from fastapi import FastAPI, HTTPException
from fastapi.params import Depends, Query
from fastapi.responses import PlainTextResponse, RedirectResponse
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Generator


sqlite_url = "sqlite:///database.db"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


@app.on_event("startup")
def on_startup() -> None:
    SQLModel.metadata.create_all(engine)


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


@app.get("/{arg}")
def redirect_to_long_url(arg: str, session: SessionDep) -> RedirectResponse:
    url = session.get(URL, arg)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url.full_url)


@app.get("/")
def root() -> PlainTextResponse:
    return PlainTextResponse("bla")
