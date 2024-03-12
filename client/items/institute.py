from dataclasses import dataclass

from items.item import Item, WidgetType, DialogLayout

@dataclass
class InstituteItem(Item):
    university_id : str
    name : str
    cabinet : int

    def from_json(json):
        return InstituteItem(json["id"], json["university_id"], json["name"], json["cabinet"])

    def caption(self) -> str:
        return self.name

    def view_btn_caption(self) -> str:
        return "Показать кафедры"

    def description(self) -> str:
        return f"Кабинет: {self.cabinet}"

    def params(self) -> dict:
        return {
            "id" : self.id,
            "university_id" : self.university_id,
            "name" : self.name,
            "cabinet" : self.cabinet
        }

    def set_university_id(self, university_id):
        self.university_id = university_id

    def get_university_id(self):
        return self.university_id

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_cabinet(self, cabinet):
        self.cabinet = cabinet

    def get_cabinet(self):
        return self.cabinet

    def dialog_layout(self) -> list:
        return [
            DialogLayout("ID", WidgetType.Label, self.set_id, self.get_id),
            DialogLayout("ID университета", WidgetType.Label, self.set_university_id, self.get_university_id),
            DialogLayout("Наименование", WidgetType.LineEdit, self.set_name, self.get_name),
            DialogLayout("Кабинет", WidgetType.SpinBox, self.set_cabinet, self.get_cabinet)
        ]