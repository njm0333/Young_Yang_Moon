# -*-coding:utf-8-*-
import random
import socket
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login_process', methods=['POST'])
def login_process():
    user_name = request.form.get('username')
    random_code = random.randint(100000, 999999)
    full_stock_name = f"{user_name}({random_code})"

    # 🎯 [추가] 로그인 시 랜덤 계좌 정보 생성
    acc_part1 = random.randint(1000, 9999) # 앞 4자리
    acc_part2 = random.randint(1000, 9999) # 뒤 4자리

    account_types = ["위탁종합", "증권종합", "종합계좌", "MTS종합", "해외종합"]
    chosen_type = random.choice(account_types)

    full_account_name = f"{acc_part1}-{acc_part2} [{chosen_type}]"

    # 생성된 종목명과 계좌명을 가지고 라우터로 이동
    return redirect(url_for('universal_router', stock_name=full_stock_name, account_name=full_account_name, page='main'))

@app.route('/main')
def universal_router():
    stock_name = request.args.get('stock_name', '무명주주(000000)')
    # 🎯 [추가] 넘어온 랜덤 계좌명을 받아줌 (없으면 기본값 가이드)
    account_name = request.args.get('account_name', '0000-0000 [위탁종합]')
    target_page = request.args.get('page', 'main')

    # 중요: 페이지 이동 시 stock_name과 account_name을 함께 넘겨줌
    return render_template(f'{target_page}.html', stock_name=stock_name, account_name=account_name, session="정규장 (점심)")

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()

    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        print("\n" + "="*60)
        print(f"🚀 영양문 터미널 서버가 가동되었습니다!")
        print(f"💻 PC 접속 주소: http://localhost:5000")
        print(f"📱 동일 와이파이 핸드폰 접속 주소: http://{local_ip}:5000")
        print("="*60 + "\n")

    app.run(host='0.0.0.0', port=5000, debug=True)