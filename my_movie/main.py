from fastapi import FastAPI, Body , Path, Query,Depends
from fastapi.responses import HTMLResponse, JSONResponse
from models import Movie,User, JWTbearer
from typing import  List
from config import create_configuration_fastapi
from data import movies
from jwt_manager import create_token


app = FastAPI()
create_configuration_fastapi(app)

@app.get('/',tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')

@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com"  and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)

@app.get('/movies', tags=['movies'], response_model=List[Movie],status_code=200 , dependencies=[Depends(JWTbearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)

@app.get('/movies/{id}',tags=['movies'],response_model=List[Movie])
def get_movie(id: int = Path(ge=1,le=2000)) ->Movie:
    for item in movies:
        if item["id"]==id:
            return JSONResponse(content=item)
    return JSONResponse(status_code=404,content=[])

@app.get('/movies/', tags=['movies'],response_model=List[Movie])
def get_movies_by_category(category : str = Query(min_length=5,max_length=15))->List [Movie]:
    data = [ item for item in movies if item['category']==category]
    return JSONResponse(content=data)

@app.post('/movies', tags=['movies'], response_model=dict,status_code=201)
def create_movie(movie: Movie)-> dict:
    movies.append(movie.dict())
    return JSONResponse(status_code=201, content={"message" : "Se ha registrado la pelicula"})

@app.put('/movies/{id}', tags=['movies'],response_model=dict,status_code=200)
def update_movie(id:int , movie: Movie) -> dict:
        try:
            index = [movie['id'] for movie in movies].index(id)
            movies[index] = movie.dict()
            return JSONResponse(status_code=200, content={"message" : "Se ha modificado la pelicula"})
        except ValueError:
            return {'error': 'Movie not found'}   


@app.delete('/movies/{id}', tags=['movies'],response_model=dict,status_code=200)
def delete__movie(id : int)-> dict:
    for item in movies:
        if item["id"]==id:
            movies.remove(item)
            return JSONResponse(status_code=200, content={"message" : "Se ha eliminado la pelicula"})
