import json


def register_user(self):
    return self.client.post(
        '/auth/register',
        data=json.dumps(dict(
            firstname="Benjamin",
            lastname="Mayanja",
            othernames=None,
            phone_number="0703-755-919",
            username='v1b3m',
            email="test@test.com",
            password='123456'
        )),
        content_type='application/json'
    )


def login_user(self, email, password):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            email=email,
            password=password
        )),
        content_type='application/json'
    )


def create_user(self):
    pass
