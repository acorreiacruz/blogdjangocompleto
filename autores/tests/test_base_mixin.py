from django.urls import reverse
from django.test import TestCase

class TestBaseMixin(TestCase):

    def get_url(self, name,**kwargs):
        url = reverse(f"autores:{name}", kwargs={**kwargs})
        return url

    def get_response(self, name, method='get', data=None, follow=True, **kwargs):
        if method == 'get':
            response = self.client.get(
                self.get_url(name, **kwargs)
            )

        if method == 'post':
            response = self.client.post(
                self.get_url(name, **kwargs),
                data=data,
                follow=follow
            )

        return response