from fastapi import FastAPI
from .api_routers import user_router, business_router, system_router, branch_router

app = FastAPI(title='Assem', version='1.0.0')
app.include_router(user_router)
app.include_router(business_router)
app.include_router(branch_router)



app.include_router(system_router)
