def make_search_dict(students, groups):
    serialized_students = []
    for student in students:
        new_student = {
            "title": student.username,
            "url": "/students/%s" % student.username,
            "image": student.student.profile_pic.url
        }
        serialized_students.append(new_student)

    serialized_groups = []
    for group in groups:
        new_group = {
            "title": group.name,
            "url": "/groups/%s" % group.id,
            "image": group.profile_pic.url
        }
        serialized_groups.append(new_group)

    response_dict = {
        "results": {
            "category1": {
                "name": "Students",
                "results": serialized_students
            },
            "category2": {
                "name": "Groups",
                "results": serialized_groups
            }
        },

    }

    return response_dict


def make_dropdown_dict(students):
    serialized_students = []
    for student in students:
        new_student = {
            "name": student.username,
            "value": student.student.id
        }
        serialized_students.append(new_student)

    response_dict = {
        "success": "true",
        "results": serialized_students
    }

    return response_dict

