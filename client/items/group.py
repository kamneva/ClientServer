from dataclasses import dataclass

from items.item import Item, WidgetType, DialogLayout

@dataclass
class GroupItem(Item):
    department_id : str
    name : str
    year : int
    quantity : int

    def from_json(json):
        return GroupItem(json["id"], json["department_id"], json["name"], json["year"], json["quantity"])

    def caption(self) -> str:
        return self.name

    def view_btn_caption(self) -> str:
        return "Показать предметы"

    def description(self) -> str:
        return f"Год поступления: {self.year}\nКоличество студентов группы: {self.quantity}"

    def params(self) -> dict:
        return {
            "id" : self.id,
            "department_id" : self.department_id,
            "name" : self.name,
            "year" : self.year,
            "quantity" : self.quantity
        }

    def set_department_id(self, department_id):
        self.department_id = department_id

    def get_department_id(self):
        return self.department_id

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_year(self, year):
        self.year = year

    def get_year(self):
        return self.year

    def set_quantity(self, quantity):
        self.quantity = quantity

    def get_quantity(self):
        return self.quantity

    def dialog_layout(self) -> list:
        return [
            DialogLayout("ID", WidgetType.Label, self.set_id, self.get_id),
            DialogLayout("ID кафедры", WidgetType.Label, self.set_department_id, self.get_department_id),
            DialogLayout("Наименование", WidgetType.LineEdit, self.set_name, self.get_name),
            DialogLayout("Год поступления", WidgetType.SpinBox, self.set_year, self.get_year),
            DialogLayout("Количество студентов группы", WidgetType.SpinBox, self.set_quantity, self.get_quantity)
        ]