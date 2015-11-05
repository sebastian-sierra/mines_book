def serialize_students(students):
    response = []

    for student in students:
        new_student = {
            "title": student.username,
            "url": "/students/%s" % student.username,
            "image": student.student.profile_pic.url
        }
        response.append(new_student)
    return response


def serialize_groups(groups):
    response = []

    for group in groups:
        new_group = {
            "title": group.name,
            "url": "/groups/%s" % group.id,
            "image": group.profile_pic.url
        }
        response.append(new_group)
    return response


def serialize_students_select(students):
    response = []

    for student in students:
        new_student = {
            "name": student.username,
            "value": student.student.id
        }
        response.append(new_student)
    return response
