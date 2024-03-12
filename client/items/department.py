from dataclasses import dataclass

from items.item import Item, WidgetType, DialogLayout

@dataclass
class DepartmentItem(Item):
    institute_id : str
    name : str
    manager_name : str

    def from_json(json):
        return DepartmentItem(json["id"], json["institute_id"], json["name"], json["manager_name"])

    def caption(self) -> str:
        return self.name

    def view_btn_caption(self) -> str:
        return "Показать группы"

    def description(self) -> str:
        return f"ФИО заведующего: {self.manager_name}"

    def params(self) -> dict:
        return {
            "id" : self.id,
            "institute_id" : self.institute_id,
            "name" : self.name,
            "manager_name" : self.manager_name
        }

    def set_institute_id(self, institute_id):
        self.institute_id = institute_id

    def get_institute_id(self):
        return self.institute_id

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_manager_name(self, manager_name):
        self.manager_name = manager_name

    def get_manager_name(self):
        return self.manager_name

    def dialog_layout(self) -> list:
        return [
            DialogLayout("ID", WidgetType.Label, self.set_id, self.get_id),
            DialogLayout("ID института", WidgetType.Label, self.set_institute_id, self.get_institute_id),
            DialogLayout("Наименование", WidgetType.LineEdit, self.set_name, self.get_name),
            DialogLayout("ФИО заведующего", WidgetType.LineEdit, self.set_manager_name, self.get_manager_name)
        ]