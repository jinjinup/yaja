from flask import Flask, render_template, request
import csv
from datetime import datetime

app = Flask(__name__)

# 허용된 와이파이 IP 주소들
allowed_ips = [
    '192.168.1.14',
    '192.168.1.31',
    '192.168.1.128',
    '192.168.1.130',
    '192.168.1.136',
    '192.168.45.49'  # 사용자의 IP 추가
]

@app.route('/')
def show_attendance_page():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def check_attendance():
    student_number = request.form['student_id']
    my_ip = request.remote_addr
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    is_allowed = my_ip in allowed_ips

    with open('attendance.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([student_number, my_ip, now_time, "출석 인정" if is_allowed else "실패"])

    if is_allowed:
        return f'✅ 출석 완료!<br>학번: {student_number}<br>IP: {my_ip}'
    else:
        return f'❌ 출석 실패: 등록되지 않은 IP<br>당신의 IP: {my_ip}'

@app.route('/logs')
def show_logs():
    records = []
    try:
        with open('attendance.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                student_number, ip, time, result = row
                records.append((student_number, time, ip, result))
    except FileNotFoundError:
        pass
    return render_template('logs.html', records=records)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
