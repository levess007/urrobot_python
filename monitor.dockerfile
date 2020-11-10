FROM robot_base

EXPOSE 5432/tcp

WORKDIR /app
ADD monitor.py /app

CMD ["python2.7", "monitor.py"]
