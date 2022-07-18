from django.test import TestCase
from django.contrib.auth.models import User
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from snippets.serializers import UserSerializer

from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io

class SnippetSerializerTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.request = self.factory.get('/')

    def test_user_serializer(self):
        serializer = UserSerializer(data={'username': 'ldy'}, context={'request': Request(self.request)})
        
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['username'], 'ldy')      

        user = serializer.save()
        
        self.assertEqual(user.id, 1)
        self.assertEqual(user.username, 'ldy')

        # 직렬화
        serializer = UserSerializer(user, context={'request': Request(self.request)})
        content = JSONRenderer().render(serializer.data)
        self.assertJSONEqual(content, {'url':'http://testserver/users/1/', 'id': 1, 'username': 'ldy', 'snippets': []})
        
        # 역직렬화 
        stream = io.BytesIO(content)
        data = JSONParser().parse(stream)

        self.assertEqual(data['id'], 1)
        self.assertEqual(data['username'], 'ldy')
        self.assertEqual(data['snippets'], []) 

    def test_snippet_serializer(self):
        user = User.objects.create(username="ldy")
        
        self.assertEqual(user.id, 1)
        self.assertEqual(user.username, 'ldy')

        serializer = SnippetSerializer(data={'code':'foo = "bar"\n'}, context={'request': Request(self.request)})

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['code'], 'foo = "bar"')

        snippet = serializer.save(owner=user)
        
        self.assertEqual(snippet.id, 1)
        self.assertEqual(snippet.code, 'foo = "bar"')
        self.assertEqual(snippet.owner, user)
        
        # 직렬화
        serializer = SnippetSerializer(snippet, context={'request': Request(self.request)})
        content = JSONRenderer().render(serializer.data)
        self.assertJSONEqual(content, {
            'url': 'http://testserver/snippets/1/',
            'id': 1, 
            'highlight': 'http://testserver/snippets/1/highlight/',
            'owner': 'ldy',
            'title': '',
            'code': 'foo = "bar"',
            'linenos': False,
            'language': 'python',
            'style': 'friendly'
        })

        # 역직렬화 
        stream = io.BytesIO(content)
        data = JSONParser().parse(stream)
    
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['title'], '')
        self.assertEqual(data['code'], 'foo = "bar"')
        self.assertEqual(data['linenos'], False)
        self.assertEqual(data['language'], 'python')
        self.assertEqual(data['style'], 'friendly')
        self.assertEqual(data['owner'], 'ldy')