FROM locustio/locust:latest

COPY locustfile.py /locust/

EXPOSE 8089

CMD ["locust", "-f", "/locust/locustfile.py", "--host", "http://load-test.load-test.svc.cluster.local"]
