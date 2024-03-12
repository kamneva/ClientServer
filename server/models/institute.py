from models.shared import Model, db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Institute(db.Model, Model):
    __tablename__ = 'institutes'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    university_id = db.Column(UUID(as_uuid=True), db.ForeignKey('universities.id', ondelete='cascade'), nullable=False)
    name = db.Column(db.String(), nullable=False)
    cabinet = db.Column(db.Integer(), nullable=False)
    department = db.relationship("Department", backref="institute", cascade="all, delete, delete-orphan")

    def __init__(self, id, university_id, name, cabinet):
        self.id = id
        self.university_id = university_id
        self.name = name
        self.cabinet = cabinet

    def __repr__(self) -> str:
        return f"<Institute {self.id}>"

    def from_args(args):
        return Institute(Model.get_id(args), args.get("university_id"), args.get("name"), args.get("cabinet"))

    def copy(self, other):
        self.id = other.id
        self.university_id = other.university_id
        self.name = other.name
        self.cabinet = other.cabinet

    def json(self) -> dict:
        return {
            "id" : self.id,
            "university_id" : self.university_id,
            "name" : self.name,
            "cabinet" : self.cabinet
        }