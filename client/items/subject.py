from dataclasses import dataclass

from items.item import Item, WidgetType, DialogLayout

@dataclass
class SubjectItem(Item):
    name : str
    hours : float

    def from_json(json):
        return SubjectItem(json["id"], json["name"], json["hours"])

    def caption(self) -> str:
        return self.name

    def view_btn_caption(self) -> str:
        return str()

    def description(self) -> str:
        return f"Количество часов: {self.hours}"

    def params(self) -> dict:
        return {
            "id" : self.id,
            "name" : self.name,
            "hours" : self.hours
        }

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_hours(self, hours):
        self.hours = hours

    def get_hours(self):
        return self.hours

    def dialog_layout(self) -> list:
        return [
            DialogLayout("ID", WidgetType.Label, self.set_id, self.get_id),
            DialogLayout("Наименование", WidgetType.LineEdit, self.set_name, self.get_name),
            DialogLayout("Количество часов", WidgetType.DoubleSpinBox, self.set_hours, self.get_hours)
        ]
