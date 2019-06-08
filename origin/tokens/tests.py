from rest_framework.test import APISimpleTestCase


class HelloWorld(APISimpleTestCase):
    def test_root(self):
        resp = self.client.get("/")
        assert resp.status_code == 200
