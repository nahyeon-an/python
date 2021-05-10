import subprocess
import datetime
import time
import json

wait = datetime.timedelta(minutes=5).total_seconds()
day = datetime.timedelta(days=1).total_seconds()

# while True:

# command
subprocess.call(['python', 'gb_evaluate_model.py'])
subprocess.call(['python', 'rating_evaluate_model.py'])

time.sleep(wait)  # 파일 저장 완료될 때까지 콜백 만들 수 있으면 좋겠다.

# print("save model done")

with open("secrets.json", 'r') as f:
    info = json.load(f)
send = "ec2-user@{}:/home/ec2-user/job4/job4/letter/".format(info['host'])
subprocess.call(['scp', '-i', 'job4.pem', '-r', 'output/*',
                 send])

    # time.sleep(day)

