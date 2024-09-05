def test_get_assignments_student_1(client, h_student_1):
    """
    Test to get all assignments for student 1
    """
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_2(client, h_student_2):
    """
    Test to get all assignments for student 2
    """
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2


def test_post_assignment_null_content(client, h_student_1):
    """
    Failure case: Posting assignment with null content should return an error.
    """

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': None
        }
    )

    # Expect a 400 Bad Request status code when content is null
    assert response.status_code == 400

    error_response = response.json
    assert 'error' in error_response
    assert error_response['error'] == 'Content cannot be null'


def test_post_assignment_student_1(client, h_student_1):
    """
    Success case: Student 1 posts a new assignment in DRAFT state.
    """
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        }
    )

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_submit_assignment_student_1(client, h_student_1):
    """
    Test student 1 submitting an assignment to teacher 2.
    """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        }
    )

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2


def test_assignment_resubmit_error(client, h_student_1):
    """
    Test resubmission of an already submitted assignment should return an error.
    """
    # First submission
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        }
    )
    assert response.status_code == 200

    # Attempt to resubmit the same assignment
    resubmit_response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        }
    )

    # Expect a 400 Bad Request on resubmission attempt
    assert resubmit_response.status_code == 400

    error_response = resubmit_response.json
    assert 'error' in error_response
    assert error_response['error'] == 'Assignment has already been submitted'
