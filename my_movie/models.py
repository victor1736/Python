from pydantic import BaseModel, Field
from typing import Optional
from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException, Body
from jwt_manager import validate_token


class JWTbearer(HTTPBearer):
    async def __call__(self, request : Request) :
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Las credenciales son invalidas")
        
    
class User (BaseModel):
    email:str
    password: str

class Movie(BaseModel):
    id : Optional[int] = None
    title : str = Field(min_length=5,max_length=15)
    overview : str = Field(min_length=15,max_length=50)
    year : int = Field(le=2023)
    rating : float = Field(default=10, ge=1, le=10)
    category : str = Field(default='Categoría', min_length=5, max_length=15)

    class Config :
        schema_extra = {
            "example" : {
            "id":1,
            "title": "Mi pelicula",
            "overview": "Descripcion de la pelicula",
            "year": 2023,
            "rating": 9.8,
            "category": "Acción"
            }
        }