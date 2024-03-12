from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPaintEvent, QPainter, QImage
from PySide6.QtCore import Qt

from enum import Enum

from gui.shared import header_font
from gui.control_panel import ControlPanel
from gui.items_container import ItemsContainer
from gui.home_page_navigation import HomePageNavigation
from gui.item_dialog import ItemDialog

from items.item import Item
from items.university import UniversityItem
from items.institute import InstituteItem
from items.department import DepartmentItem
from items.group import GroupItem
from items.subject import SubjectItem
from items.subject_list import SubjectListItem

from api_request import request

class MainWindow(QWidget):
    class Page(Enum):
        Home = 0
        Universities = 1
        Institutes = 2
        Departments = 3
        Groups = 4
        Subjects = 5

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.current_item = None
        self.current_page = MainWindow.Page.Home

        self.caption_label = QLabel("Caption", alignment=Qt.AlignCenter)
        self.caption_label.setFont(header_font)

        self.control_panel = ControlPanel()
        self.control_panel.back_btn_clicked.connect(self.on_back_btn_clicked)
        self.control_panel.home_btn_clicked.connect(self.on_home_btn_clicked)
        self.control_panel.add_btn_clicked.connect(self.on_add_btn_clicked)

        self.items_container = ItemsContainer()
        self.items_container.view_item_changed.connect(self.on_view_item_changed)
        self.items_container.modify_btn_clicked.connect(self.on_modify_btn_clicked)
        self.items_container.remove_btn_clicked.connect(self.on_remove_btn_clicked)

        self.home_page_navigation = HomePageNavigation()
        self.home_page_navigation.universities_btn_clicked.connect(self.on_universities_btn_clicked)
        self.home_page_navigation.subjects_btn_clicked.connect(self.on_subjects_btn_clicked)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.caption_label)
        self.main_layout.addWidget(self.control_panel)
        self.main_layout.addWidget(self.items_container, 1)
        self.main_layout.addWidget(self.home_page_navigation)
        self.main_layout.addStretch(0)

        self.show_home_page()

    def paintEvent(self, event: QPaintEvent):
        painter=QPainter(self)
        image = QImage("gui/img/загружено.jpg")
        painter.drawImage(self.rect(), image)
        super().paintEvent(event)

    def on_back_btn_clicked(self):
        if self.current_item is None:
            self.show_home_page()
            return

        if self.current_page is MainWindow.Page.Institutes:
            self.on_universities_btn_clicked()
            return

        items_func = lambda : None

        if self.current_page is MainWindow.Page.Departments:
            self.current_item = request.get_university(self.current_item.university_id)
            self.current_page = MainWindow.Page.Institutes
            items_func = request.get_institutes

        if self.current_page is MainWindow.Page.Groups:
            self.current_item = request.get_institute(self.current_item.institute_id)
            self.current_page = MainWindow.Page.Departments
            items_func = request.get_departments

        if self.current_page is MainWindow.Page.Subjects:
            self.current_item = request.get_department(self.current_item.department_id)
            self.current_page = MainWindow.Page.Groups
            items_func = request.get_groups

        self.set_caption(self.current_item.caption())
        self.show_content_page(items_func, self.current_item.id)

    def on_home_btn_clicked(self):
        self.current_item = None
        self.current_page = MainWindow.Page.Home
        self.show_home_page()

    def on_add_btn_clicked(self):
        item = Item(None)
        caption = "Add item"
        add_func = lambda *args: False

        if self.current_page is MainWindow.Page.Universities:
            item = UniversityItem(None, None, None)
            caption = "Добавить университет"
            add_func = request.add_university

        if self.current_page is MainWindow.Page.Institutes:
            item = InstituteItem(None, self.current_item.id, None, None)
            caption = "Добавить институт"
            add_func = request.add_institute

        if self.current_page is MainWindow.Page.Departments:
            item = DepartmentItem(None, self.current_item.id, None, None)
            caption = "Добавить кафедру"
            add_func = request.add_department

        if self.current_page is MainWindow.Page.Groups:
            item = GroupItem(None, self.current_item.id, None, None, None)
            caption = "Добавить группу"
            add_func = request.add_group

        if self.current_page is MainWindow.Page.Subjects:
            caption = "Добавить предмет"

            if self.current_item is None:
                item = SubjectItem(None, None, None)
                add_func = request.add_subject
            else:
                subject_list = request.get_subjects_exclude_group(self.current_item.id)
                item = SubjectListItem(self.current_item.id, subject_list, None)
                add_func = request.add_group_subject

        dialog = ItemDialog(item, caption, self)
        if not dialog.exec():
            return

        if not add_func(dialog.item.params()):
            return

        self.on_view_item_changed(self.current_item)

    def on_universities_btn_clicked(self):
        self.current_item = None
        self.current_page = MainWindow.Page.Universities

        self.set_caption("Университеты")
        self.show_content_page(request.get_universities)

    def on_subjects_btn_clicked(self):
        self.current_item = None
        self.current_page = MainWindow.Page.Subjects

        self.set_caption("Предметы")
        self.show_content_page(request.get_subjects)

    def on_view_item_changed(self, item):
        self.current_item = item

        if item is None:
            if self.current_page is MainWindow.Page.Universities:
                self.on_universities_btn_clicked()

            if self.current_page is MainWindow.Page.Subjects:
                self.on_subjects_btn_clicked()

            return

        items_func = lambda *args: None

        if type(item) is UniversityItem:
            self.current_page = MainWindow.Page.Institutes
            items_func = request.get_institutes

        if type(item) is InstituteItem:
            self.current_page = MainWindow.Page.Departments
            items_func = request.get_departments

        if type(item) is DepartmentItem:
            self.current_page = MainWindow.Page.Groups
            items_func = request.get_groups

        if type(item) is GroupItem:
            self.current_page = MainWindow.Page.Subjects
            items_func = request.get_subjects_for_group

        self.set_caption(item.caption())
        self.show_content_page(items_func, item.id)

    def on_modify_btn_clicked(self, item):
        caption = "Modify item"
        modify_func = lambda *args: False

        if self.current_page is MainWindow.Page.Universities:
            caption = "Редактирование университета"
            modify_func = request.modify_university

        if self.current_page is MainWindow.Page.Institutes:
            caption = "Редактирование института"
            modify_func = request.modify_institute

        if self.current_page is MainWindow.Page.Departments:
            caption = "Редактирование кафедры"
            modify_func = request.modify_department

        if self.current_page is MainWindow.Page.Groups:
            caption = "Редактирование группы"
            modify_func = request.modify_group

        if self.current_page is MainWindow.Page.Subjects:
            caption = "Редактирование предмета"
            modify_func = request.modify_subject

        dialog = ItemDialog(item, caption, self)
        if not dialog.exec():
            return

        if not modify_func(dialog.item.params()):
            return

        self.on_view_item_changed(self.current_item)

    def on_remove_btn_clicked(self, item):
        delete_success = False

        if type(item) == UniversityItem:
            delete_success = request.delete_university(item.id)

        if type(item) == InstituteItem:
            delete_success = request.delete_institute(item.id)

        if type(item) == DepartmentItem:
            delete_success = request.delete_department(item.id)

        if type(item) == GroupItem:
            delete_success = request.delete_group(item.id)

        if type(item) == SubjectItem:
            if self.current_item is None:
                delete_success = request.delete_subject(item.id)

            else:
                delete_success = request.delete_group_subject(self.current_item.id, item.id)

        if not delete_success:
            return

        self.items_container.remove_item_widget(item.id)

        if self.items_container.inside_layout.count() in [1, 2]:
            self.items_container.clear()

    def show_home_page(self):
        self.control_panel.setVisible(False)
        self.items_container.setVisible(False)
        self.home_page_navigation.setVisible(True)

        self.set_caption("Начальная страница")

    def show_content_page(self, items_func, *args):
        self.control_panel.setVisible(True)
        self.items_container.setVisible(True)
        self.home_page_navigation.setVisible(False)

        self.items_container.clear()
        self.items_container.set_items(items_func(*args))

    def set_caption(self, caption):
        self.caption_label.setText(caption)
