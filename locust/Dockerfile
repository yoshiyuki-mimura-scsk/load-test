FROM locustio/locust:latest

COPY locustfile.py /locust/

EXPOSE 8089

CMD ["-f", "/locust/locustfile.py", "--host", "http://api.load-test.svc.cluster.local:8080"]
