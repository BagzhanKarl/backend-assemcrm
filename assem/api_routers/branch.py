from fastapi import APIRouter, Cookie, Depends
from sqlalchemy.orm import Session

from assem.db.database import get_db
from assem.models import Branch
from assem.schemas import CreateBranchSchema

branch_router = APIRouter(prefix='/api/v1/publuc/branch', tags=['Филиалы'])

@branch_router.get('/{branch_id}')
async def get_branch_info(branch: CreateBranchSchema, db: Session = Depends(get_db)):
    return branch;
