from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from knox.models import AuthToken
from .models import Ticket

client = APIClient()


class CreateListTicketTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='Maxim', password='123qwe')
        self.admin = User.objects.create_superuser(username='Admin', password='123qwe')
        self.ticket = Ticket.objects.create(author=self.user, text='test text')

    def test_create_ticket(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + AuthToken.objects.create(self.user)[1])
        response = client.post('/ticket/', {"text": "Help please"})
        self.assertEqual(response.data, {'text': 'Help please'})
        self.assertEqual(response.status_code, 201)

    def test_list_ticket(self):
        client.credentials(HTTP_AUTHORIZATION='Token ' + AuthToken.objects.create(self.user)[1])
        response = client.get('/ticket/')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

