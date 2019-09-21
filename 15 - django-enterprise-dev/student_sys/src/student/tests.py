from django.test import TestCase, Client

from .models import Student
# Create your tests here.


class StudentTestCatse(TestCase):
    def setUp(self):
        Student.objects.create(name='hippiezhou',
                               sex=1,
                               email='hippiezhou@outllok.com',
                               profession='程序员',
                               qq='12345678',
                               phone='87654321')

        def test_create_and_sex_show(self):
            student = Student.objects.create(name='huyang',
                                             sex=1,
                                             email='admin@outlook.com',
                                             profession='程序员',
                                             qq='12345',
                                             phone='54321')
            self.assertEqual(student.sex_show, '男', '性别字段内容跟展示不一致')
            # self.assertEqual(student.get_sex_display(), '男', '性别字段内容跟展示不一致')

        def test_filter(self):
            Student.objects.create(name='huyang',
                                   sex=1,
                                   email='nobody@outlook.com',
                                   profession='程序员',
                                   qq='123',
                                   phone='456')
            name = 'the5fire'
            students = Student.objects.filter(name=name)
            self.assertEqual(students.count(), 1,
                             '应该只存在一个名称为:{}的记录'.format(name))


def test_get_index(self):
    client = Client()
    response = client.get('/')
    self.assertEqual(response.status_code, 200, 'status code must be 200!')


def test_post_student(self):
    client = Client()
    data = dict(
        name='test_for_post',
        sex=1,
        email='333@dd.com',
        qq='33333333',
        phone='44444444444',
    )
    response = client.post('/', data)
    self.assertEqual(response.status_code, 302, 'status must be 302!')

    response = client.get('/')
    self.assertTrue('test_for_post' in response.content,
                    'response content must contain "test_for_post"')
