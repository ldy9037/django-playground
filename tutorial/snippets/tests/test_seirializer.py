from django.test import TestCase

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from collections import OrderedDict
import io

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

        stream = io.BytesIO(content)
        data = JSONParser().parse(stream)
        serializer = SnippetSerializer(data=data)
        
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, OrderedDict([('title', ''), ('code', 'print("hello, world")'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]))
        serializer.save()

        serializer = SnippetSerializer(Snippet.objects.all(), many=True)
        self.assertEqual(serializer.data, [OrderedDict([('id', 1), ('title', ''), ('code', 'foo = "bar"\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 2), ('title', ''), ('code', 'print("hello, world")\n'), ('linenos', False), ('language', 'python'), ('style', 'friendly')]), OrderedDict([('id', 3), ('title', ''), ('code', 'print("hello, world")'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])])
