FROM robot_base

EXPOSE 4321/tcp

ADD logic.py /app

CMD ["python3", "logic_oneround.py"]
