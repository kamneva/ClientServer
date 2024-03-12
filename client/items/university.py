from dataclasses import dataclass

from items.item import Item, WidgetType, DialogLayout

@dataclass
class UniversityItem(Item):
    name : str
    address : str

    def from_json(json):
        return UniversityItem(json["id"], json["name"], json["address"])

    def caption(self) -> str:
        return self.name


    def view_btn_caption(self) -> str:
        return "Показать институты"

    def description(self) -> str:
        return f"Адрес: {self.address}"

    def params(self) -> dict:
        return {
            "id" : self.id,
            "name" : self.name,
            "address" : self.address
        }

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name
    
    def set_address(self, address):
        self.address = address

    def get_address(self):
        return self.address

    def dialog_layout(self) -> list:
        return [
            DialogLayout("ID", WidgetType.Label, self.set_id, self.get_id),
            DialogLayout("Наименование", WidgetType.LineEdit, self.set_name, self.get_name),
            DialogLayout("Адрес", WidgetType.LineEdit, self.set_address, self.get_address)
        ]