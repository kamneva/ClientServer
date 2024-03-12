from models.shared import Model, db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Group(db.Model, Model):
    __tablename__ = 'groups'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    department_id = db.Column(UUID(as_uuid=True), db.ForeignKey('departments.id', ondelete='cascade'), nullable=False)
    name = db.Column(db.String(), nullable=False)
    year = db.Column(db.Integer(), nullable=False)
    quantity = db.Column(db.Integer(), nullable=False)
    subject_link = db.relationship("GroupSubjectLink", backref="room", cascade="all, delete, delete-orphan")

    def __init__(self, id, department_id, name, year, quantity):
        self.id = id
        self.department_id = department_id
        self.name = name
        self.year = year
        self.quantity = quantity

    def __repr__(self) -> str:
        return f"<Group {self.id}>"

    def from_args(args):
        return Group(Model.get_id(args), args.get("department_id"), args.get("name"), int(args.get("year")), int(args.get("quantity")))

    def copy(self, other):
        self.id = other.id
        self.department_id = other.department_id
        self.name = other.name
        self.year = other.year
        self.quantity = other.quantity

    def json(self) -> dict:
        return {
            "id" : self.id,
            "department_id" : self.department_id,
            "name" : self.name,
            "year" : self.year,
            "quantity" : self.quantity
        }