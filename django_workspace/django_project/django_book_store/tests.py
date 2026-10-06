from django.test import Client, TestCase
from django.urls import reverse

from .models import Employee


class EmployeeLoginTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Employee.objects.create(
            employee_no='T00001', employee_name='試験従業員', password='test1234',
        )

    def setUp(self):
        self.login_url = reverse('django_book_store:login')
        self.logout_url = reverse('django_book_store:logout')

    def login(self, client=None):
        client = client or self.client
        return client.post(self.login_url, {
            'employee_no': 'T00001', 'password': 'test1234',
        })

    def test_valid_login_keeps_session_and_rotates_key(self):
        session = self.client.session
        session['other_data'] = 'keep'
        session.save()
        old_key = session.session_key
        response = self.login()
        self.assertRedirects(response, self.login_url)
        session = self.client.session
        self.assertNotEqual(session.session_key, old_key)
        self.assertEqual(session['book_store_employee_no'], 'T00001')
        self.assertEqual(session['other_data'], 'keep')
        self.assertNotIn('test1234', str(dict(session)))
        response = self.client.get(self.login_url)
        self.assertContains(response, '試験従業員')
        self.assertContains(response, 'ログインしました。')
        self.assertNotContains(response, 'test1234')

    def test_invalid_credentials_have_same_error_and_no_login(self):
        for employee_no, password in [('T00001', 'wrong'), ('T99999', 'test1234')]:
            with self.subTest(employee_no=employee_no):
                response = self.client.post(self.login_url, {
                    'employee_no': employee_no, 'password': password,
                })
                self.assertContains(response, '従業員番号またはパスワードが違います。')
                self.assertNotIn('book_store_employee_no', self.client.session)
                self.assertNotContains(response, f'value="{password}"')

    def test_empty_fields_do_not_login(self):
        response = self.client.post(self.login_url, {})
        self.assertContains(response, '従業員番号を入力してください。')
        self.assertContains(response, 'パスワードを入力してください。')
        self.assertNotIn('book_store_employee_no', self.client.session)

    def test_password_whitespace_is_not_discarded(self):
        response = self.client.post(self.login_url, {
            'employee_no': 'T00001', 'password': 'test1234 ',
        })
        self.assertContains(response, '従業員番号またはパスワードが違います。')
        self.assertNotIn('book_store_employee_no', self.client.session)

    def test_logout_requires_post_and_preserves_unrelated_session(self):
        session = self.client.session
        session['other_data'] = 'keep'
        session.save()
        self.login()
        self.assertEqual(self.client.get(self.logout_url).status_code, 405)
        self.assertIn('book_store_employee_no', self.client.session)
        response = self.client.post(self.logout_url)
        self.assertRedirects(response, self.login_url)
        self.assertNotIn('book_store_employee_no', self.client.session)
        self.assertEqual(self.client.session['other_data'], 'keep')

    def test_deleted_employee_session_returns_to_login(self):
        self.login()
        Employee.objects.filter(employee_no='T00001').delete()
        response = self.client.get(self.login_url)
        self.assertNotContains(response, 'ログインしました。')
        self.assertNotIn('book_store_employee_no', self.client.session)

    def test_login_and_logout_require_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        client.get(self.login_url)
        self.assertEqual(self.login(client).status_code, 403)
        token = client.cookies['csrftoken'].value
        response = client.post(self.login_url, {
            'employee_no': 'T00001', 'password': 'test1234',
            'csrfmiddlewaretoken': token,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(client.post(self.logout_url).status_code, 403)
