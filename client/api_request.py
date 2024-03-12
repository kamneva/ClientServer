import requests

from items.university import UniversityItem
from items.institute import InstituteItem
from items.department import DepartmentItem
from items.group import GroupItem
from items.subject import SubjectItem

class APIRequest:
    def __init__(self):
        self.base_url = "http://127.0.0.1:5000"

    def get_list(type, url, **kargs):
        response = requests.get(url, **kargs)

        if response.status_code != 200:
            return None

        return [type.from_json(item) for item in response.json()]

    def get_item(type, url):
        response = requests.get(url)

        if response.status_code != 200:
            return None

        return type.from_json(response.json())

    def post_item(url, params):
        response = requests.post(url, params=params)
        return response.status_code == 200

    def delete_item(url):
        response = requests.delete(url)
        return response.status_code == 200

    def get_universities(self):
        url = f"{self.base_url}/universities"
        return APIRequest.get_list(UniversityItem, url)

    def get_university(self, university_id):
        url = f"{self.base_url}/university/{university_id}"
        return APIRequest.get_item(UniversityItem, url)

    def add_university(self, params):
        url = f"{self.base_url}/university/add"
        return APIRequest.post_item(url, params)

    def modify_university(self, params):
        url = f"{self.base_url}/university/modify"
        return APIRequest.post_item(url, params)

    def delete_university(self, university_id):
        url = f"{self.base_url}/university/delete/{university_id}"
        return APIRequest.delete_item(url)

    def get_institutes(self, university_id):
        url = f"{self.base_url}/institutes/{university_id}"
        return APIRequest.get_list(InstituteItem, url)

    def get_institute(self, institute_id):
        url = f"{self.base_url}/institute/{institute_id}"
        return APIRequest.get_item(InstituteItem, url)

    def add_institute(self, params):
        url = f"{self.base_url}/institute/add"
        return APIRequest.post_item(url, params)

    def modify_institute(self, params):
        url = f"{self.base_url}/institute/modify"
        return APIRequest.post_item(url, params)

    def delete_institute(self, institute_id):
        url = f"{self.base_url}/institute/delete/{institute_id}"
        return APIRequest.delete_item(url)

    def get_departments(self, institute_id):
        url = f"{self.base_url}/departments/{institute_id}"
        return APIRequest.get_list(DepartmentItem, url)

    def get_department(self, department_id):
        url = f"{self.base_url}/department/{department_id}"
        return APIRequest.get_item(DepartmentItem, url)

    def add_department(self, params):
        url = f"{self.base_url}/department/add"
        return APIRequest.post_item(url, params)

    def modify_department(self, params):
        url = f"{self.base_url}/department/modify"
        return APIRequest.post_item(url, params)

    def delete_department(self, department_id):
        url = f"{self.base_url}/department/delete/{department_id}"
        return APIRequest.delete_item(url)

    def get_groups(self, department_id):
        url = f"{self.base_url}/groups/{department_id}"
        return APIRequest.get_list(GroupItem, url)

    def get_group(self, group_id):
        url = f"{self.base_url}/group/{group_id}"
        return APIRequest.get_item(GroupItem, url)

    def add_group(self, params):
        url = f"{self.base_url}/group/add"
        return APIRequest.post_item(url, params)

    def modify_group(self, params):
        url = f"{self.base_url}/group/modify"
        return APIRequest.post_item(url, params)

    def add_group_subject(self, params):
        url = f"{self.base_url}/group/add-subject"
        return APIRequest.post_item(url, params)

    def delete_group(self, group_id):
        url = f"{self.base_url}/group/delete/{group_id}"
        return APIRequest.delete_item(url)

    def delete_group_subject(self, group_id, subject_id):
        url = f"{self.base_url}/group/{group_id}/delete-subject/{subject_id}"
        return APIRequest.delete_item(url)

    def get_subjects(self):
        url = f"{self.base_url}/subjects"
        return APIRequest.get_list(SubjectItem, url)

    def get_subjects_for_group(self, group_id):
        url = f"{self.base_url}/subjects/{group_id}"
        params = { "type" : "include" }
        return APIRequest.get_list(SubjectItem, url, params=params)

    def get_subjects_exclude_group(self, group_id):
        url = f"{self.base_url}/subjects/{group_id}"
        params = { "type" : "exclude" }
        return APIRequest.get_list(SubjectItem, url, params=params)

    def add_subject(self, params):
        url = f"{self.base_url}/subject/add"
        return APIRequest.post_item(url, params)

    def modify_subject(self, params):
        url = f"{self.base_url}/subject/modify"
        return APIRequest.post_item(url, params)

    def delete_subject(self, subject_id):
        url = f"{self.base_url}/subject/delete/{subject_id}"
        return APIRequest.delete_item(url)

request = APIRequest()