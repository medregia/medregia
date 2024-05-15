from django.test import TestCase
from authentication.models import StateModel, DistrictModel, CustomUser, Person, Notification


class StateModelTestCase(TestCase):
    def setUp(self):
        self.state = StateModel.objects.create(Pid=1, LocationType='State', Pname='Test State')

    def test_state_creation(self):
        self.assertEqual(self.state.Pname, 'Test State')

class DistrictModelTestCase(TestCase):
    def setUp(self):
        self.state = StateModel.objects.create(Pid=1, LocationType='State', Pname='Test State')
        self.district = DistrictModel.objects.create(id=1, state=self.state, Pid=1, LocationType='District', districtname='Test District')

    def test_district_creation(self):
        self.assertEqual(self.district.districtname, 'Test District')

class CustomUserTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='testuser', email='test@example.com')

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')

class PersonTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username='testuser', email='test@example.com')
        self.state = StateModel.objects.create(Pid=1, LocationType='State', Pname='Test State')
        self.district = DistrictModel.objects.create(id=1, state=self.state, Pid=1, LocationType='District', districtname='Test District')
        self.person = Person.objects.create(user=self.user, MedicalShopName='Test Shop', state=self.state, district=self.district)

    def test_person_creation(self):
        self.assertEqual(self.person.MedicalShopName, 'Test Shop')

class NotificationTestCase(TestCase):
    def setUp(self):
        self.sender = CustomUser.objects.create(username='sender', email='sender@example.com')
        self.receiver = CustomUser.objects.create(username='receiver', email='receiver@example.com')
        self.notification = Notification.objects.create(sender=self.sender, receiver=self.receiver, message='Test Message')

    def test_notification_creation(self):
        self.assertEqual(self.notification.message, 'Test Message')

