from models.shared import Model, db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class University(db.Model, Model):
    __tablename__ = 'universities'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False)
    address = db.Column(db.String(), nullable=False)
    institute = db.relationship("Institute", backref="universitiy", cascade="all, delete, delete-orphan")

    def __init__(self, id, name, address):
        self.id = id
        self.name = name
        self.address = address

    def __repr__(self) -> str:
        return f"<University {self.id}>"

    def from_args(args):
        return University(Model.get_id(args), args.get("name"), args.get("address"))

    def copy(self, other):
        self.id = other.id
        self.name = other.name
        self.address = other.address

    def json(self) -> dict:
        return {
            "id" : self.id,
            "name" : self.name,
            "address" : self.address
        }
