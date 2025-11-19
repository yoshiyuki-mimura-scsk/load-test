import random
from locust import HttpUser, task, between, events

target_users = []

# test_startイベントフック: テスト開始時に一度だけ実行される
@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """
    テスト開始前に一度だけ実行され、ユーザー一覧を取得します。
    """
    global target_users
    print("テスト開始: ユーザー一覧を取得します...")
    try:
        target_users = [
            {"username": "user1", "password": "password1"},
            {"username": "user2", "password": "password2"},
            {"username": "user3", "password": "password3"},
            {"username": "user4", "password": "password4"},
            {"username": "user5", "password": "password5"},
            {"username": "user6", "password": "password6"},
            {"username": "user7", "password": "password7"},
            {"username": "user8", "password": "password8"},
            {"username": "user9", "password": "password9"},
            {"username": "user10", "password": "password10"}
        ]

        if not target_users:
            print("ユーザー一覧が空です。テストを停止します。")
            # ユーザーが一人もいない場合はテストを中止する
            environment.runner.quit()
        else:
            random.shuffle(target_users)
            print(f"成功: {len(target_users)} 人のユーザー情報を準備しました。")

    except Exception as e:
        print(f"ユーザー一覧の取得に失敗しました: {e}")
        # 失敗した場合もテストを中止する
        environment.runner.quit()

class DummyApiUser(HttpUser):

    # リクエスト間の待ち時間 (1秒から3秒)
    wait_time = between(0.1, 0.3)

    def on_start(self):
        """
        このメソッドはシミュレートされるユーザーが起動するたびに実行されます。
        グローバルなユーザーリストから一人分の情報を取得し、ログインしてトークンを取得します。
        """
        global target_users
        if not target_users:
            # リストにユーザーが残っていない場合、この仮想ユーザーは何もせずに停止する
            print("利用可能なユーザーがいません。このワーカーを停止します。")
            self.stop()
            return

        # ユーザーリストの末尾から一人分の認証情報を取り出す
        # .pop() を使うことで、各ワーカーにユニークなユーザーが割り当てられる
        user_credentials = target_users.pop()
        self.username = user_credentials.get("username")
        password = user_credentials.get("password")

        if not self.username or not password:
            print(f"不正なユーザー情報です: {user_credentials}。このワーカーを停止します。")
            self.stop()
            return
            
        self.get_jwt_token(password)

    def get_jwt_token(self, password):
        """
        割り当てられたユーザー情報でJWTトークンを取得します。
        """
        try:
            response = self.client.post("/auth/login", json={
                "username": self.username,
                "password": password
            })
            response.raise_for_status()  # ステータスコードが2xxでない場合に例外を発生させる
            self.user_id = response.json()['user_id']
            self.token = response.json()['access_token']
            print(f"ユーザー '{self.user_id}' '{self.username}' が正常にログインしました。")
        except Exception as e:
            # ログインに失敗した場合、このユーザーはタスクを実行しないようにする
            self.token = None
            print(f"ユーザー '{self.username}' のログインに失敗しました: {e}")
            self.stop() # ログイン失敗したユーザーは停止させる
 
    @task
    def get_tasks(self):
        """
        取得したトークンを使って保護されたエンドポイントにアクセスするタスク。
        """
        # ログインに失敗した場合 (tokenがない場合) はタスクを実行しない
        if not hasattr(self, 'token') or not self.token:
            return

        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        self.client.get("/tasks", headers=headers, name="/tasks (タスク一覧取得)")

    @task
    def get_user_info(self):
        """
        取得したトークンを使って保護されたエンドポイントにアクセスするタスク。
        """
        # ログインに失敗した場合 (tokenがない場合) はタスクを実行しない
        if not hasattr(self, 'token') or not self.token:
            return

        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        url = "/users/{}".format(self.user_id)
        self.client.get(url=url, headers=headers, name="/users/id (ユーザ情報取得)")

    @task(0)
    def get_dummy(self):
        self.client.get("/dummy")
