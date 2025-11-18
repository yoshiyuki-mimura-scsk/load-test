from locust import HttpUser, task, between

class DummyApiUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_dummy(self):
        self.client.get("/dummy")

    def on_start(self):
         """このメソッドはユーザーが起動するたびに実行される"""
         self.token = self.get_jwt_token()
 
    def get_jwt_token(self):
        # トークンを取得するための認証エンドポイントにリクエストを送信
        response = self.client.post("/auth/login", json={
             "username": "your_username",
             "password": "your_password"
        })
        return response.json()['access_token']  # 取得したトークンを返す
 
    @task(0) # 0は実行されない。コメントアウトと同義
    def no_test(self):
        # JWTトークンをヘッダーに追加してGETリクエストを送信
        headers = {
            "Authorization": f"Bearer {self.token}",
            "EnvValue": f"Bearer {self.env_value}"
        }
        self.client.get("/test", headers=headers)

    @task(1) # 1以上の値で順番に実行される
    def get_test(self):
        # JWTトークンをヘッダーに追加してGETリクエストを送信
        headers = {
            "Authorization": f"Bearer {self.token}",
            "EnvValue": f"Bearer {self.env_value}"
        }
        self.client.get("/test", headers=headers)
