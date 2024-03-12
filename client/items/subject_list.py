from items.item import Item, WidgetType, DialogLayout

class SubjectListItem(Item):
    def __init__(self, id, subject_list, current_subject) -> None:
        super().__init__(id)
        self.subject_list = subject_list
        self.current_subject = current_subject

        if current_subject is None and len(subject_list) != 0:
            self.current_subject = subject_list[0]

    def from_json(json):
        return SubjectListItem(json["id"], [])

    def caption(self) -> str:
        return str()

    def view_btn_caption(self) -> str:
        return str()

    def description(self) -> str:
        return str()

    def params(self) -> dict:
        subject_id = None
        if self.current_subject is not None:
            subject_id = self.current_subject.id

        return {
            "group_id" : self.id,
            "subject_id" : subject_id
        }

    def set_current_subject(self, current_subject_name):
        current_subject = self.subject_list[0]
        for subject in self.subject_list:
            if subject.name == current_subject_name:
                current_subject = subject

        self.current_subject = current_subject

    def get_subject_list(self):
        return [item.name for item in self.subject_list]

    def dialog_layout(self) -> list:
        return [
            DialogLayout("Список предметов", WidgetType.ComboBox, self.set_current_subject, self.get_subject_list)
        ]
