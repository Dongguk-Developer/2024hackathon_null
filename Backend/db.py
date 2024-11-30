import sqlite3
from flask import Flask

app = Flask(__name__)

# 데이터베이스 파일 경로
DB_FILE_PATH = "reservations.db"

# 테이블 생성
def init_db():
    """
    reservations 테이블이 없으면 새로 생성.
    """
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
            reservation_code TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()
    print("테이블이 생성되었습니다.")

# 테이블 스키마 업데이트
def update_db_schema():
    """
    reservations 테이블에 열이 없으면 추가.
    """
    conn = sqlite3.connect(DB_FILE_PATH)
    c = conn.cursor()

    # 테이블의 현재 스키마 가져오기
    c.execute("PRAGMA table_info(reservations)")
    existing_columns = [row[1] for row in c.fetchall()]  # 열 이름 가져오기

    # gender 열 추가
    if "gender" not in existing_columns:
        c.execute("ALTER TABLE reservations ADD COLUMN gender TEXT")

    # date_of_birth 열 추가
    if "date_of_birth" not in existing_columns:
        c.execute("ALTER TABLE reservations ADD COLUMN date_of_birth TEXT")

    conn.commit()
    conn.close()
    print("테이블 스키마 업데이트 완료.")

@app.route('/')
def home():
    return "Flask 서버가 정상적으로 작동 중입니다!"

if __name__ == "__main__":
    # 1. 테이블이 없으면 생성
    init_db()

    # 2. 테이블 스키마 업데이트
    update_db_schema()

    # 3. Flask 앱 실행
    app.run(host="0.0.0.0", port=5000, debug=True)
