import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from aufguss_app.models import SaunaUser, AufgussSession
import datetime

@pytest.mark.django_db
def test_user_login_and_jwt():
    user = User.objects.create_user(username='testuser', password='testpass')
    SaunaUser.objects.create(user=user, full_name='Test User')
    client = APIClient()
    response = client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 200
    assert 'access' in response.data

@pytest.mark.django_db
def test_aufguss_crud():
    user = User.objects.create_user(username='testuser2', password='testpass')
    sauna_user = SaunaUser.objects.create(user=user, full_name='Test User2')
    client = APIClient()
    token = client.post(reverse('token_obtain_pair'), {'username': 'testuser2', 'password': 'testpass'}).data['access']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    # Create
    data = {
        'title': 'Test Aufguss',
        'description': 'Test Desc',
        'start_time': datetime.datetime.now().isoformat(),
        'end_time': (datetime.datetime.now() + datetime.timedelta(hours=1)).isoformat(),
        'created_by': sauna_user.id
    }
    response = client.post('/api/aufguesse/', data, format='json')
    assert response.status_code == 201
    aufguss_id = response.data['id']
    # Read
    response = client.get(f'/api/aufguesse/{aufguss_id}/')
    assert response.status_code == 200
    # Update
    response = client.put(f'/api/aufguesse/{aufguss_id}/', {**data, 'title': 'Updated'}, format='json')
    assert response.status_code == 200
    # Delete
    response = client.delete(f'/api/aufguesse/{aufguss_id}/')
    assert response.status_code == 204
