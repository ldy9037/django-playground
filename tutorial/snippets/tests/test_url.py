from django.urls import reverse
from snippets.models import Snippet
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

class SnippetURLTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="ldy")

    def test_snippet_list(self):
        url = reverse('snippet_list')
        
        data = {
            'code': 'test'
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['code'], 'test')
        
        format_suffix_url = url[:-1]+'.json'
        self.client.force_authenticate(user=None)
        response = self.client.get(format_suffix_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_snippet_detail(self):
        snippet = Snippet.objects.create(code = "test", owner = self.user)
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

        new_user = User.objects.create(username="hani")
        self.client.force_authenticate(user=new_user)
        response = self.client.put(url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['id'], snippet.id)
        self.assertNotEqual(response.data['title'], snippet.title)

        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Snippet.objects.count(), 0)
    
    def test_user_list(self):
        url = reverse('user_list')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertEqual(len(response.data), 1)   

    def test_user_detail(self):
        url = reverse('user_detail', kwargs={'pk': self.user.id})
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'ldy')
    
    def test_root_url(self):
        snippet = Snippet.objects.create(code = "test", owner = self.user)
        snippet.save()

        snippet = Snippet.objects.create(code = "test2", owner = self.user)
        snippet.save()

        url = reverse('api_root')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        users_response = self.client.get(response.data['users'])
        self.assertEqual(users_response.status_code, status.HTTP_200_OK)   
        self.assertEqual(len(users_response.data), 1)
        
        snippets_response = self.client.get(response.data['snippets'])
        self.assertEqual(snippets_response.status_code, status.HTTP_200_OK)  
        self.assertEqual(len(snippets_response.data), 2) 
    
    def test_snippet_highlight(self):
        snippet = Snippet.objects.create(code = 'foo = "bar"\n', owner = self.user)
        snippet.save()

        url = reverse('snippet_highlight', kwargs={'pk': snippet.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('class="highlight"' in response.data)