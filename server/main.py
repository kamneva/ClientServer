from flask import Flask, jsonify, request

import uuid

from models.shared import Model, db
from models.university import University
from models.institute import Institute
from models.department import Department
from models.group_subject_link import GroupSubjectLink
from models.group import Group
from models.subject import Subject

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:7151@localhost:5432/postgres"

db.init_app(app)
with app.app_context():
    db.create_all()

def get_list(type, **kargs):
    query = type.query.filter_by(**kargs).all()
    return jsonify([item.json() for item in query])

def get_item(type, **kargs):
    query = type.query.filter_by(**kargs).first()
    if query is None:
        return jsonify(None), 404

    return jsonify(query.json())

def add_item(type):
    item = type.from_args(request.args)
    if not item.valid():
        return jsonify(), 400

    db.session.add(item)
    db.session.commit()

    return jsonify()

def modify_item(type):
    new_item = type.from_args(request.args)
    if not new_item.valid():
        return jsonify(), 400

    current_item = type.query.filter_by(id=new_item.id).first()
    if current_item is None:
        return jsonify(), 400

    current_item.copy(new_item)
    db.session.commit()

    return jsonify()

def delete_item(type, **kargs):
    delete_count = type.query.filter_by(**kargs).delete()
    db.session.commit()

    if delete_count == 0:
        return jsonify(), 404
    
    return jsonify()

@app.route("/universities", methods=['GET'])
def universities():
    return get_list(University)

@app.route("/university/<university_id>", methods=['GET'])
def university(university_id):
    return get_item(University, id=university_id)

@app.route("/university/add", methods=['POST'])
def university_add():
    return add_item(University)

@app.route("/university/modify", methods=['POST'])
def university_modify():
    return modify_item(University)

@app.route("/university/delete/<university_id>", methods=['DELETE'])
def university_delete(university_id):
    return delete_item(University, id=university_id)

@app.route("/institutes/<university_id>", methods=['GET'])
def institutes(university_id):
    return get_list(Institute, university_id=university_id)

@app.route("/institute/<institute_id>", methods=['GET'])
def institute(institute_id):
    return get_item(Institute, id=institute_id)

@app.route("/institute/add", methods=['POST'])
def institute_add():
    return add_item(Institute)

@app.route("/institute/modify", methods=['POST'])
def institute_modify():
    return modify_item(Institute)

@app.route("/institute/delete/<institute_id>", methods=['DELETE'])
def institute_delete(institute_id):
    return delete_item(Institute, id=institute_id)

@app.route("/departments/<institute_id>", methods=['GET'])
def departments(institute_id):
    return get_list(Department, institute_id=institute_id)

@app.route("/department/<department_id>", methods=['GET'])
def department(department_id):
    return get_item(Department, id=department_id)

@app.route("/department/add", methods=['POST'])
def department_add():
    return add_item(Department)

@app.route("/department/modify", methods=['POST'])
def department_modify():
    return modify_item(Department)

@app.route("/department/delete/<department_id>", methods=['DELETE'])
def department_delete(department_id):
    return delete_item(Department, id=department_id)

@app.route("/groups/<department_id>", methods=['GET'])
def groups(department_id):
    return get_list(Group, department_id=department_id)

@app.route("/group/<group_id>", methods=['GET'])
def group(group_id):
    return get_item(Group, id=group_id)

@app.route("/group/add", methods=['POST'])
def group_add():
    return add_item(Group)

@app.route("/group/modify", methods=['POST'])
def group_modify():
    return modify_item(Group)

@app.route("/group/add-subject", methods=['POST'])
def group_add_subject():
    group_subject_link = GroupSubjectLink.from_args(request.args)
    if not group_subject_link.valid():
        return jsonify(), 400

    existed_link_query = GroupSubjectLink.query \
        .filter_by(group_id=group_subject_link.group_id, subject_id=group_subject_link.subject_id) \
        .all()

    if len(existed_link_query) != 0:
        return jsonify(), 404

    db.session.add(group_subject_link)
    db.session.commit()

    return jsonify()

@app.route("/group/delete/<group_id>", methods=['DELETE'])
def group_delete(group_id):
    return delete_item(Group, id=group_id)

@app.route("/group/<group_id>/delete-subject/<subject_id>", methods=['DELETE'])
def group_delete_subject(group_id, subject_id):
    return delete_item(GroupSubjectLink, group_id=group_id, subject_id=subject_id)

@app.route("/subjects", methods=['GET'])
def subjects():
    return get_list(Subject)

@app.route("/subjects/<group_id>", methods=['GET'])
def subjects_by_group_id(group_id):
    subject_ids_query = GroupSubjectLink.query.filter_by(group_id=group_id).all()
    subject_ids = [link.subject_id for link in subject_ids_query]

    type = request.args.get("type")
    if type not in ["include", "exclude"]:
        return jsonify(), 400
    
    filter = Subject.id.in_(subject_ids) if type == "include" else ~Subject.id.in_(subject_ids)
    return jsonify([subject.json() for subject in Subject.query.filter(filter).all()])

@app.route("/subject/add", methods=['POST'])
def subject_add():
    return add_item(Subject)

@app.route("/subject/modify", methods=['POST'])
def subject_modify():
    return modify_item(Subject)

@app.route("/subject/delete/<subject_id>", methods=['DELETE'])
def subject_delete(subject_id):
    return delete_item(Subject, id=subject_id)

if __name__ == "__main__":
    app.run()