from models.shared import Model, db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class GroupSubjectLink(db.Model, Model):
    __tablename__ = 'group_subject_links'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    group_id = db.Column(UUID(as_uuid=True), db.ForeignKey('groups.id', ondelete='cascade'), nullable=False, default=uuid.uuid4)
    subject_id = db.Column(UUID(as_uuid=True), db.ForeignKey('subjects.id', ondelete='cascade'), nullable=False, default=uuid.uuid4)

    def __init__(self, id, group_id, subject_id):
        self.id = id
        self.group_id = group_id
        self.subject_id = subject_id

    def __repr__(self) -> str:
        return f"<GroupSubjectLink {self.group_id}:{self.subject_id}>"

    def from_args(args):
        return GroupSubjectLink(Model.get_id(args), args.get("group_id"), args.get("subject_id"))

    def copy(self, other):
        self.id = other.id
        self.group_id = other.group_id
        self.subject_id = other.subject_id

    def json(self) -> dict:
        return {
            "id" : self.id,
            "group_id" : self.group_id,
            "subject_id" : self.subject_id
        }