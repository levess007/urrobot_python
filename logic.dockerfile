FROM robot_base

EXPOSE 4321/tcp

WORKDIR /app
ADD logic.py /app

CMD ["python3", "logic.py"]
