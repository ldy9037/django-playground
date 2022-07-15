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
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['code'], 'test')
        
        format_suffix_url = url[:-1]+'.json'
        response = self.client.get(format_suffix_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_snippet_detail(self):
        snippet = Snippet.objects.create(code = "test")
        snippet.save()

        url = reverse('snippet_detail', kwargs={'pk': snippet.id})
        format_suffix_url = url[:-1]+'.json'

        response = self.client.get(format_suffix_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(response.data['id'], snippet.id)
        self.assertEqual(response.data['title'], snippet.title)
        self.assertEqual(response.data['code'], snippet.code)
        self.assertEqual(response.data['linenos'], snippet.linenos)
        self.assertEqual(response.data['language'], snippet.language)
        self.assertEqual(response.data['style'], snippet.style)
        
        data = response.data.copy()
        data['title'] = "title1"

        response = self.client.put(url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['id'], snippet.id)
        self.assertNotEqual(response.data['title'], snippet.title)

        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Snippet.objects.count(), 0)