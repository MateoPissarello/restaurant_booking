from sqlalchemy.orm import Session
from models import Table


class TableDAO:
    def __init__(self, db: Session):
        self.db = db

    def get_table(self, table_id: int) -> Table | None:
        table = self.db.query(Table).filter(Table.table_id == table_id).first()
        return table

    def create_table(self, table: Table) -> Table:
        self.db.add(table)
        self.db.commit()
        self.db.refresh(table)
        return table

    def list_tables_by_restaurant(self, restaurant_id: int) -> list[Table]:
        tables = self.db.query(Table).filter(Table.restaurant_id == restaurant_id).all()
        return tables

    def update_table(self, table_id: int, updated_data: dict) -> Table | None:
        table = self.get_table(table_id)
        if table:
            for key, value in updated_data.items():
                setattr(table, key, value)
            self.db.commit()
            self.db.refresh(table)
            return table
        return None

    def get_table_in_restaurant_by_number(self, restaurant_id: int, number: int) -> Table | None:
        table = self.db.query(Table).filter(Table.restaurant_id == restaurant_id, Table.number == number).first()
        return table

    def get_table_in_restaurant_by_table_id(self, restaurant_id: int, table_id: int) -> Table | None:
        table = self.db.query(Table).filter(Table.restaurant_id == restaurant_id, Table.table_id == table_id).first()
        return table

    def delete_table(self, table_id: int) -> bool:
        table_id = self.get_table(table_id)
        if table_id:
            self.db.delete(table_id)
            self.db.commit()
            return True
        return False
