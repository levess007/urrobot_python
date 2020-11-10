FROM robot_base

WORKDIR /app
ADD control.py /app

CMD ["python3", "control.py"]
