from fastapi import FastAPI

from assem.router import user_router, categoryAPI, typesApi

app = FastAPI(title='Assem', version='1.0.0')
app.include_router(user_router)
app.include_router(categoryAPI)
app.include_router(typesApi)