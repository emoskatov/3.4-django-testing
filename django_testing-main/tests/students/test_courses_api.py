import pytest
from rest_framework.test import APIClient
from students.models import Course, Student
from model_bakery import baker

@pytest.fixture
def client():
    return APIClient()
@pytest.fixture
def customer_factory():
    def factory1(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory1

@pytest.fixture
def course_factory():
    def factory2(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory2

@pytest.mark.django_db
def test_the_receipt_of_the_first_course(client, course_factory):
    course = course_factory()
    response = client.get(f'/api/v1/courses/{course.id}/')
    data = response.json()
    assert response.status_code == 200
    assert course.name == data['name']

@pytest.mark.django_db
def test_to_get_a_list_of_courses(client, course_factory):
    course = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/')
    data = response.json()
    assert response.status_code == 200
    for i, k in enumerate(data):
        assert course[i].name == k['name']

@pytest.mark.django_db
def test_the_filtering_of_the_list_of_courses_by_id(client, course_factory):
    course = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/', {'id': course[6].id})
    data = response.json()
    assert response.status_code == 200
    assert course[6].id == data[0]['id']

@pytest.mark.django_db
def test_the_filtering_of_the_list_of_courses_by_name(client, course_factory):
    course = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/', {'name': course[7].name})
    data = response.json()
    assert response.status_code == 200
    assert course[7].name == data[0]['name']

@pytest.mark.django_db
def test_of_successful_course_creation(client):
    response = client.post('/api/v1/courses/', data={'name': 'C++', 'students_id': 1}, format='json')
    assert response.status_code == 201

@pytest.mark.django_db
def test_of_a_successful_course_update(client, course_factory):
    course = course_factory()
    response = client.patch(f'/api/v1/courses/{course.id}/', data={'name': 'Python'}, format='json')
    response1 = client.get(f'/api/v1/courses/{course.id}/', data={'name': 'Python'}, format='json')
    assert response.status_code == 200
    assert response1.status_code == 200

@pytest.mark.django_db
def test_of_successful_course_deletion(client, course_factory):
    course = course_factory()
    response = client.delete(f'/api/v1/courses/{course.id}/')
    response1 = client.get(f'/api/v1/courses/{course.id}/')
    assert response.status_code == 204
    assert response1.status_code == 404

