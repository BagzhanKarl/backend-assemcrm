from fastapi import FastAPI

from assem.router.user import user_router

app = FastAPI(title='Assem', version='1.0.0')
app.include_router(user_router)