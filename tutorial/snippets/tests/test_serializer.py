import email
from django.test import TestCase
from django.contrib.auth.models import User
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from snippets.serializers import UserSerializer

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from collections import OrderedDict
import io

class SnippetSerializerTests(TestCase):
    def setUp(self):
        self.user = User(username="ldy", email="ldy9037@naver.com", password="12345678")
        self.user.save()

        self.snippet = Snippet(code='foo = "bar"\n', owner=self.user)
        self.snippet.save()
        
        self.snippet = Snippet(code='print("hello, world")\n', owner=self.user)
        self.snippet.save()

    def test_user_serializer(self):
        serializer = UserSerializer(self.user)
        self.assertEqual(serializer.data, {'id': 1, 'username': 'ldy', 'snippets': [1, 2]})
        
    def test_snippet_serializer(self):
        serializer = SnippetSerializer(self.snippet)
        self.assertEqual(serializer.data, {'id': 2, 'title': '', 'code': 'print("hello, world")\n', 'linenos': False, 'language': 'python', 'style': 'friendly', 'owner': 1})

        content = JSONRenderer().render(serializer.data)
        self.assertEqual(content, b'{"id":2,"title":"","code":"print(\\"hello, world\\")\\n","linenos":false,"language":"python","style":"friendly","owner":1}')

        stream = io.BytesIO(content)
        data = JSONParser().parse(stream)
        serializer = SnippetSerializer(data=data)
        
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, OrderedDict([('title', ''), ('code', 'print("hello, world")'), ('linenos', False), ('language', 'python'), ('style', 'friendly'), ('owner', self.user)]))
        serializer.save()

        serializer = SnippetSerializer(Snippet.objects.all(), many=True)
        self.assertEqual(serializer.data, [OrderedDict([('id', 1), ('title', ''), ('code', 'foo = "bar"\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly'), ('owner', 1)]), OrderedDict([('id', 2), ('title', ''), ('code', 'print("hello, world")\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly'), ('owner', 1)]), OrderedDict([('id', 3), ('title', ''), ('code', 'print("hello, world")'), ('linenos', False), ('language', 'python'), ('style', 'friendly'), ('owner', 1)])])
