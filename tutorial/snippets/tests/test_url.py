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

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(data['id'], 1)
        self.assertEqual(data['code'], 'test')
        
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)
        self.assertEqual(len(data), 1)
        
    def test_snippet_detail(self):
        snippet = Snippet.objects.create(code = "test")
        snippet.save()

        url = reverse('snippet_detail', kwargs={'pk': snippet.id})
        response = self.client.get(url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        
        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(data['id'], snippet.id)
        self.assertEqual(data['title'], snippet.title)
        self.assertEqual(data['code'], snippet.code)
        self.assertEqual(data['linenos'], snippet.linenos)
        self.assertEqual(data['language'], snippet.language)
        self.assertEqual(data['style'], snippet.style)
        
        data['title'] = "title1"

        response = self.client.put(url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        stream = io.BytesIO(response.content)
        data = JSONParser().parse(stream)

        self.assertEqual(data['id'], snippet.id)
        self.assertNotEqual(data['title'], snippet.title)

        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Snippet.objects.count(), 0)