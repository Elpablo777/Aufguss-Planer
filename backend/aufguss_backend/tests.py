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

@pytest.mark.django_db
def test_user_viewset_permissions_and_me_action():
    # Create admin user
    admin_user = User.objects.create_user(username='admin', password='testpass', is_staff=True)
    SaunaUser.objects.create(user=admin_user, full_name='Admin User')

    # Create normal user
    normal_user = User.objects.create_user(username='normaluser', password='testpass')
    sauna_user_normal = SaunaUser.objects.create(user=normal_user, full_name='Normal User')

    client = APIClient()

    # Test 'me' action for normal user
    token_normal = client.post(reverse('token_obtain_pair'), {'username': 'normaluser', 'password': 'testpass'}).data['access']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_normal)
    response_me = client.get(reverse('saunauser-me')) # 'saunauser-me' ist der basename + action
    assert response_me.status_code == 200
    assert response_me.data['full_name'] == 'Normal User'

    # Test list action (safe method) for normal user - should be allowed
    response_list_normal = client.get(reverse('saunauser-list'))
    assert response_list_normal.status_code == 200

    # Test create action (unsafe method) for normal user - should be forbidden
    user_data = {'user': normal_user.id, 'full_name': 'Attempted Create', 'color': '#123456'}
    response_create_normal = client.post(reverse('saunauser-list'), user_data, format='json')
    assert response_create_normal.status_code == 403 # Forbidden

    # Test retrieve action for another user by normal user (safe method) - should be allowed
    response_retrieve_other_normal = client.get(reverse('saunauser-detail', args=[sauna_user_normal.id]))
    assert response_retrieve_other_normal.status_code == 200

    # Test update action for another user by normal user (unsafe method) - should be forbidden
    response_update_other_normal = client.patch(reverse('saunauser-detail', args=[sauna_user_normal.id]), {'full_name': 'Updated Name'}, format='json')
    assert response_update_other_normal.status_code == 403

    # Test 'me' action for admin user
    client.credentials() # Clear previous credentials
    token_admin = client.post(reverse('token_obtain_pair'), {'username': 'admin', 'password': 'testpass'}).data['access']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + token_admin)
    response_me_admin = client.get(reverse('saunauser-me'))
    assert response_me_admin.status_code == 200
    assert response_me_admin.data['full_name'] == 'Admin User'

    # Test create action for admin user - should be allowed
    # We need to create a new underlying Django user first for the SaunaUser
    new_django_user = User.objects.create_user(username='newdjango', password='testpassword')
    admin_create_data = {'user': new_django_user.id, 'full_name': 'Created by Admin', 'color': '#ABCDEF'}
    response_create_admin = client.post(reverse('saunauser-list'), admin_create_data, format='json')
    assert response_create_admin.status_code == 201
    created_sauna_user_id = response_create_admin.data['id']

    # Test update action for another user by admin user - should be allowed
    response_update_other_admin = client.patch(reverse('saunauser-detail', args=[created_sauna_user_id]), {'full_name': 'Admin Was Here'}, format='json')
    assert response_update_other_admin.status_code == 200
    assert response_update_other_admin.data['full_name'] == 'Admin Was Here'

    # Test delete action by admin user - should be allowed
    response_delete_admin = client.delete(reverse('saunauser-detail', args=[created_sauna_user_id]))
    assert response_delete_admin.status_code == 204
