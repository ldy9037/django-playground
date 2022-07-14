from django.test import TestCase
from django.urls import reverse
from snippets.models import Snippet
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.parsers import JSONParser
import io

class SnippetURLTests(APITestCase):
    
    def test_snippet_list(self):
        url = reverse('snippet_list')

        data = {
            'code': 'test'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.content, b'{"id": 1, "title": "", "code": "test", "linenos": false, "language": "python", "style": "friendly"}')
        
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual(len(data), 1)
        
