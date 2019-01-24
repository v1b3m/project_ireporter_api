import json


def register_user(self):
    return self.client.post(
        '/auth/register',
        data=json.dumps(dict(
            firstname="Benjamin",
            lastname="Mayanja",
            othernames="",
            phone_number="070-755-9192",
            username='v1b3m',
            email="test@test.com",
            password='123456'
        )),
        content_type='application/json'
    )


def login_user(self):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            email="test@test.com",
            password="123456"
        )),
        content_type='application/json'
    )


def logout_user(self, login_response):
    return self.client.post(
        '/auth/logout',
        headers=dict(
            Authorization='Bearer '+json.loads(
                login_response.data
            )['data'][0]['token']
        )
    )


def add_redflag(self, headers, input_data):
    return self.client.post(
        '/api/v1/red-flags',
        content_type='application/json',
        data=json.dumps(input_data),
        headers=headers
    )


def add_intervention(self, headers, input_data):
    return self.client.post(
        '/api/v1/interventions',
        content_type='application/json',
        data=json.dumps(input_data),
        headers=headers
    )


def create_user(self):
    pass
