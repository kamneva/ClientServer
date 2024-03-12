from models.shared import Model, db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Department(db.Model, Model):
    __tablename__ = 'departments'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    institute_id = db.Column(UUID(as_uuid=True), db.ForeignKey('institutes.id', ondelete='cascade'), nullable=False)
    name = db.Column(db.String(), nullable=False)
    manager_name = db.Column(db.String(), nullable=False)
    group = db.relationship("Group", backref="department", cascade="all, delete, delete-orphan")

    def __init__(self, id, institute_id, name, manager_name):
        self.id = id
        self.institute_id = institute_id
        self.name = name
        self.manager_name = manager_name

    def __repr__(self) -> str:
        return f"<Department {self.id}>"

    def from_args(args):
        return Department(Model.get_id(args), args.get("institute_id"), args.get("name"), args.get("manager_name"))

    def copy(self, other):
        self.id = other.id
        self.institute_id = other.institute_id
        self.name = other.name
        self.manager_name = other.manager_name
        self.group = other.group

    def json(self) -> dict:
        return {
            "id" : self.id,
            "institute_id" : self.institute_id,
            "name" : self.name,
            "manager_name" : self.manager_name
        }