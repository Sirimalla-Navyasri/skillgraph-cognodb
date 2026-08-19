from app import app

c = app.test_client()
resp = c.get('/graph')
print('STATUS:', resp.status_code)
print(resp.data.decode())
