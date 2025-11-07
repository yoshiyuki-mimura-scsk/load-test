# 公式 Locust イメージをベースに
FROM locustio/locust:latest

# テスト用スクリプトをコンテナ内にコピー
COPY locustfile.py /locust/

# 必要に応じてパッケージ追加インストールも可能（requirements.txtを追加する場合）
# COPY requirements.txt /locust/
# RUN pip install -r /locust/requirements.txt

# Web UI として 8089ポートが利用される
EXPOSE 8089

# Entrypoint を指定（デフォルト通りのため、通常は不要）
# CMD ["-f", "/locust/locustfile.py"]
