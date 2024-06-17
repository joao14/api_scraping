from fastapi import FastAPI
from app.api import endpoints
import uvicorn
#Instanciamos FastAPI
app = FastAPI()

#Incluimos url de enpoint a validar
app.include_router(endpoints.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)