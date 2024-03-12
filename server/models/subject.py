from models.shared import Model, db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Subject(db.Model, Model):
    __tablename__ = 'subjects'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False)
    hours = db.Column(db.Float(), nullable=False)
    room_link = db.relationship("GroupSubjectLink", backref="subject", cascade="all, delete, delete-orphan")

    def __init__(self, id, name, hours):
        self.id = id
        self.name = name
        self.hours = hours

    def __repr__(self) -> str:
        return f"<Subject {self.id}>"

    def from_args(args):
        return Subject(Model.get_id(args), args.get("name"), float(args.get("hours")))

    def copy(self, other):
        self.id = other.id
        self.name = other.name
        self.hours = other.hours

    def json(self) -> dict:
        return {
            "id" : self.id,
            "name" : self.name,
            "hours" : self.hours
        }