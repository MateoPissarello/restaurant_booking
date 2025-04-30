from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import status as response_status
from schemas.table_schemas import CreateTableBase, RetrieveTableBase, UpdateTableBase
from fastapi import HTTPException
from utils.RoleChecker import RoleChecker
from utils.get_current_user import get_current_user
from schemas.auth_schemas import TokenData
from utils.restaurant_utils import validate_restaurant_existence
from database import get_db
from daos.TableDAO import TableDAO
from models import Table
from typing import List

router = APIRouter(prefix="/table", tags=["Table"])

admin_only = RoleChecker(allowed_roles=["admin"])
client_or_admin = RoleChecker(allowed_roles=["admin", "client"])


@router.post("/create", status_code=response_status.HTTP_201_CREATED, response_model=RetrieveTableBase)
async def create_table(
    table: CreateTableBase,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(admin_only),
):
    table = Table(**table.model_dump(exclude_unset=True))
    dao = TableDAO(db)
    try:
        # Check if the restaurant exists
        if not validate_restaurant_existence(table.restaurant_id, db):
            raise HTTPException(
                status_code=response_status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found",
            )
        if dao.get_table_in_restaurant_by_number(restaurant_id=table.restaurant_id, number=table.number):
            raise HTTPException(
                status_code=response_status.HTTP_400_BAD_REQUEST,
                detail="Table with this number already exists in the restaurant",
            )
        create_table = dao.create_table(table)
        return create_table
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail,
        )
    except Exception as e:
        raise HTTPException(
            status_code=response_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/get_all/{restaurant_id}", status_code=response_status.HTTP_200_OK, response_model=List[RetrieveTableBase])
async def get_all_tables(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(client_or_admin),
) -> List[RetrieveTableBase]:
    dao = TableDAO(db)
    try:
        # Check if the restaurant exists
        if not validate_restaurant_existence(restaurant_id, db):
            raise HTTPException(
                status_code=response_status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found",
            )
        tables = dao.list_tables_by_restaurant(restaurant_id)
        return tables
    except Exception as e:
        raise HTTPException(
            status_code=response_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/get/{table_id}", status_code=response_status.HTTP_200_OK, response_model=RetrieveTableBase)
async def get_table_by_id(
    table_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(client_or_admin),
) -> RetrieveTableBase:
    dao = TableDAO(db)
    try:
        table = dao.get_table(table_id)
        if not table:
            raise HTTPException(
                status_code=response_status.HTTP_404_NOT_FOUND,
                detail="Table not found",
            )
        return table
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail,
        )
    except Exception as e:
        raise HTTPException(
            status_code=response_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.patch("/update/{table_id}", status_code=response_status.HTTP_200_OK, response_model=RetrieveTableBase)
async def update_table(
    table_id: int,
    updated_data: UpdateTableBase,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(admin_only),
) -> RetrieveTableBase:
    dao = TableDAO(db)
    updated_data = updated_data.model_dump(exclude_unset=True)
    table = dao.get_table(table_id)
    try:
        if updated_data.get("number") and dao.get_table_in_restaurant_by_number(
            restaurant_id=table.restaurant_id, number=updated_data["number"]
        ):
            raise HTTPException(
                status_code=response_status.HTTP_400_BAD_REQUEST,
                detail="Table with this number already exists in the restaurant",
            )
        table = dao.update_table(table_id, updated_data)
        if not table:
            raise HTTPException(
                status_code=response_status.HTTP_404_NOT_FOUND,
                detail="Table not found",
            )
        return table
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail,
        )
    except Exception as e:
        raise HTTPException(
            status_code=response_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.delete("/delete/{table_id}", status_code=response_status.HTTP_200_OK)
async def delete_table(
    table_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
    role_checker: RoleChecker = Depends(admin_only),
) -> dict:
    dao = TableDAO(db)
    try:
        if not dao.delete_table(table_id):
            raise HTTPException(
                status_code=response_status.HTTP_404_NOT_FOUND,
                detail="Table not found",
            )
        return {"detail": "Table deleted successfully"}
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.detail,
        )
    except Exception as e:
        raise HTTPException(
            status_code=response_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
