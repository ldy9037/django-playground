from django.test import TestCase

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

class SnippetSerializerTests(TestCase):
    def setUp(self):
        self.snippet = Snippet(code='foo = "bar"\n')
        self.snippet.save()
        
        self.snippet = Snippet(code='print("hello, world")\n')
        self.snippet.save()

    def test_serializer(self):
        serializer = SnippetSerializer(self.snippet)
        self.assertEqual(serializer.data, {'id': 2, 'title': '', 'code': 'print(\"hello, world\")\n', 'linenos': False, 'language': 'python', 'style': 'friendly'})

        content = JSONRenderer().render(serializer.data)
        self.assertEqual(content, b'{"id":2,"title":"","code":"print(\\"hello, world\\")\\n","linenos":false,"language":"python","style":"friendly"}')
