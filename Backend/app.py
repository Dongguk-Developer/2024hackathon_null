import datetime
from flask import Flask, request, jsonify
from flasgger import Swagger
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import uuid
import re
import random

app = Flask(__name__)
swagger = Swagger(app)  # Swagger 초기화

DB_FILE_PATH = "reservations.db"

def generate_simple_code():
    with sqlite3.connect(DB_FILE_PATH) as conn:
        c = conn.cursor()
        while True:
            # 간단한 6자리 숫자 코드 생성
            code = f"RSV-{random.randint(100000, 999999)}"
            c.execute("SELECT COUNT(*) FROM reservations WHERE reservation_code = ?", (code,))
            if c.fetchone()[0] == 0:
                break
        return code

# 데이터베이스 초기화
def init_db():
    conn = sqlite3.connect(DB_FILE_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            gender TEXT NOT NULL,
            birth_of_date TEXT NOT NULL,
            reservation_code TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

def is_valid_date(date_str):
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def is_valid_email(email):
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email) is not None

def is_valid_phone(phone):
    regex = r'^\d{3}-\d{3,4}-\d{4}$'
    return re.match(regex, phone) is not None

def generate_unique_code():
    with sqlite3.connect(DB_FILE_PATH) as conn:
        c = conn.cursor()
        while True:
            code = f"RSV-{uuid.uuid4().hex[:8].upper()}"
            c.execute("SELECT COUNT(*) FROM reservations WHERE reservation_code = ?", (code,))
            if c.fetchone()[0] == 0:
                break
        return code

# 이메일 전송 함수
def send_mail(youremail, yourpw, reemail, uname, reservation_code, date, time):
    smtp_server = "smtp.naver.com"
    smtp_port = 587

    sender_email = youremail
    sender_password = yourpw
    receiver_email = reemail

    subject = "체험형 공방 예약 확인 안내"
    body = (
        f"안녕하세요, {uname}님.\n\n"
        f"체험형 공방 예약 확인을 위해 아래 정보를 참고해 주세요:\n"
        f"예약 코드: {reservation_code}\n"
        f"예약 날짜: {date}\n"
        f"예약 시간: {time}\n"
        f"예약자 이름: {uname}\n\n"
        f"해당 정보를 통해 예약 확인이 가능합니다. 감사합니다!"
    )

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("이메일이 성공적으로 전송되었습니다.")
    except Exception as e:
        print(f"이메일 전송 중 오류가 발생했습니다: {e}")


@app.route('/')
def home():
    """
    기본 라우트
    ---
    tags:
      - General
    operationId: getHome
    responses:
        200:
            description: 서버가 정상적으로 작동 중임을 확인
    """
    return "Flask 서버가 정상적으로 작동 중입니다!"

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()
        name = data.get('name')
        phone = data.get('phone')
        email = data.get('email')
        date = data.get('date')
        time = data.get('time')
        gender = data.get('gender')
        birth_of_date = data.get('birth_of_date')

        # 간단한 예약 코드 생성
        reservation_code = generate_simple_code()

        if not all([name, phone, email, date, time, gender, birth_of_date]):
            return jsonify({'message': '모든 필드를 입력해주세요.'}), 400

        if not is_valid_email(email):
            return jsonify({'message': '올바른 이메일 형식이 아닙니다.'}), 400

        if not is_valid_phone(phone):
            return jsonify({'message': '올바른 전화번호 형식이 아닙니다. (예: 010-1234-5678)'}), 400

        if not is_valid_date(date) or not is_valid_date(birth_of_date):
            return jsonify({'message': '올바른 날짜 형식이 아닙니다. (예: YYYY-MM-DD)'}), 400

        conn = sqlite3.connect(DB_FILE_PATH)
        c = conn.cursor()
        c.execute('''
            INSERT INTO reservations (name, phone, email, date, time, gender, birth_of_date, reservation_code)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, phone, email, date, time, gender, birth_of_date, reservation_code))
        conn.commit()
        conn.close()

        # 이메일 전송
        send_mail(
            youremail="doraemon927@naver.com",
            yourpw="Q8K6CGPSQY15",
            reemail=email,
            uname=name,
            reservation_code=reservation_code,
            date=date,
            time=time
        )

        return jsonify({
            'message': '예약이 성공적으로 저장되었습니다.',
            'reservation_code': reservation_code
        }), 201
    except sqlite3.IntegrityError:
        return jsonify({'message': '예약 코드가 중복되었습니다. 다시 시도해주세요.'}), 400
    except Exception as e:
        print(f"예외 발생: {e}")
        return jsonify({'message': f'오류 발생: {str(e)}'}), 500


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
