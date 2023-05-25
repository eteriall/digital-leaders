# -*- coding: utf-8 -*-
import re

from cert_generator import *
from flask import Flask, render_template, Response
import flask
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session, send_file, \
    send_from_directory, Response
import sqlite3
import random
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from os import path

videolist = ['vid1.mp4', 'vid2.mp4', 'vid3.mp4', 'vid4.mp4']
imglist = ['photo1682956309.jpeg', 'photo1682956437.jpeg', 'photo16829566311.jpeg', 'photo1682957136.jpeg']
textlist = ["1 eee", """<h2><strong>Конспект урока</strong></h2>
<h3><br />Часть 1. Зачем это необходимо?</h3>
<p>В данном блоке мы разберёмся, зачем необходимо писать резюме и что это вообще такое.</p>
<p><span style="color: #0000ff;"><br />✍️ Резюме (от фр. r&eacute;sum&eacute; &laquo;сводка&raquo;) &mdash; документ, содержащий информацию о навыках, опыте работы, образовании, и другую относящуюся к делу информацию, обычно требуемую для рассмотрения кандидатуры человека для найма на работу.</span></p>
<p><span style="color: #0000ff;"><br />✍️ HR-специалист &ndash; это менеджер по управлению персоналом, который ищет кандидатов на имеющиеся вакансии, формирует кадровую политику компании, разрабатывает модели мотивации персоналом и обеспечивает наиболее эффективную рабочую атмосферу, ведет документацию по персоналу.</span></p>
<p><br />То есть это основной документ, который необходим, чтобы HR-специалисты (отдел кадров) имели представление о вас - резюме.</p>
<blockquote>
<p><br />❗ Резюме &ndash; Ваша визитная карточка, которая наиболее точно должна описывать Вас как будущего работника в выбранной компании.</p>
</blockquote>
<p><br />HR-специалисту достаточно 15-20 секунд, чтобы понять, подходит ли человек на должность, или нет.</p>""", """
<h2>Конспект урока</h2>
<h3><br /><strong>Часть 2. Составление резюме.</strong></h3>
<p>Идеальный объем резюме &ndash; 1-2 страницы формата А4. <br />Для первого знакомства с кандидатом достаточно, а дополнительные сведения можно получить в ходе личной беседы. Многостраничные резюме раздражают HR-специалистов. Чаще всего их даже не читают, а сразу отправляют в корзину.</p>
<hr />
<h3><strong>Шрифт и оформление</strong></h3>
<p>При создании CV вы можете использовать любые шрифты, входящие в стандартный пакет офисного программного обеспечения.<br />(<strong>Например</strong>: Helvetica; Calibri; Arial; Raleway; Roboto)<br /><strong>Шрифт</strong> &mdash; 12-14 пунктов (12-14 пт).<br />Для выделения важных моментов стоит использовать <strong>полужирный шрифт</strong>.</p>
<hr />
<h3><strong>Личные сведения</strong></h3>
<p>В этом блоке следует указать <strong>фамилию и имя</strong>.<br />Заполните <strong>дату рождения и место проживания</strong> (страна, город, станция метро (при наличии)). Полный домашний адрес вписывать не нужно.</p>
<hr />
<h3><strong>Контактные данные</strong></h3>
<p>В качестве контактов следует включить номер мобильного телефона, адрес электронной почты, аккаунты в соцсетях и мессенджерах.<br />! Все указанные <strong>ссылки должны быть актуальными</strong>, чтобы в случае одобрения заявки была возможность с вами связаться. Название почты должно быть оформлено в <strong>деловом стиле</strong> (фамилия и инициалы, имя и фамилия).</p>
<hr />
<h3><strong>Опыт работы</strong></h3>
<p>Во время заполнения поля следует использовать <strong>обратный хронологический порядок</strong>. Сначала последнее место работы, после предыдущие.<br />Желательно перечислять должности, соответствующие выбранной вакансии. При наличии успехов на предыдущей работе, их также следует указать в резюме.</p>
<hr />
<h3><strong>Образование</strong></h3>
<p>Лучше указывать только последнее пройденное обучение, т.е. самое значимое. Но можно указать и другие, если они более подходящие под выбранную должность.</p>
<hr />
<h3><strong>Профессиональные навыки</strong></h3>
<h4><strong>! На этот блок обращают особое внимание</strong></h4>
<p>Перечисляйте только те компетенции, которые имеют отношение к вакантной должности. Лучше оформить в виде маркированного списка (к главным умениям можно добавить уровень овладения).</p>
<hr />
<h3><strong>Личные качества</strong></h3>
<p>Заполнение раздела с Soft-skills. Не стоит расхваливать себя. Укажите <strong>3-5 качества</strong>, которые наиболее значимы для выбранной должности.</p>
<p>&nbsp;</p>""", "4 sfasfga"]
bonuslist = {
    1: [],
    2: ['lesson2File.docx', 'Konspect2.pdf'],
    3: ['lesson3Bonus.png', 'lesson3File.pdf'],
    4: ['lesson2File.docx', 'lesson2File.docx', 'lesson2File.docx'],
}

tests = {
    1: {
        'Кто такие HR?': [[1, 0, 0, 0], ['Кадровые специалисты компаний',
                                            'Программисты в компании',
                                            'Рекламодатели',
                                            'Менеджеры в компаниях']],
        'Что такое hard & soft skills?': [[0, 1, 0, 0, 0], ['Нейросети',
                                                            'Проффесиональные и над проффесиональные навыки',
                                                            'Платформы для поиска работы',
                                                            'Навыки программирования',
                                                            'Виды HR']],
    },
    2: {
        'Сколько тратит в среднем времени HR на просмотр вашего резюме?': [[0, 0, 1, 0, 0], ['30 секунд',
                                                                                             '4 минуты',
                                                                                             '15-20 секунд',
                                                                                             '10 минут',
                                                                                             '10 секунд']],
    },
    3: {
        'Какое количество страниц в вашем резюме будет оптимально для HR?': [[0, 0, 0, 1, 0], [
            'Пол страницы A4',
            'Страница A4',
            '5 страниц A4',
            '1-2 страницы A4',
            'Нисколько, на собеседовании всё равно всё обсудим']],
        'В каком формате оптимально отправлять свое резюме HR-ру?': [[1, 0, 0, 0, 0], [
            'PDF',
            'PPTX/PTX',
            'KEY',
            'ODP',
            'TXT']],
        'Что лучше всего указывать в блоке '
        'проффесиональных навыков при поступлении '
        'в it - компанию?': [[0, 0, 0, 0, 1],
                             [
                                 'Я учился в музыкальной школе',
                                 'Умею хорошо общаться с людьми',
                                 'Учился в школе',
                                 'Часто читаю книги',
                                 'Владею языком программирования Python на уровне Middle',
                             ]],
    },
    4: {
        'Оцените курс': [[1, 1, 1], ['Курс понравился', 'Курс хороший, но есть, что доработать', 'Курс не понравился']],
    },
}

app = Flask(__name__)
alf = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

quotes_success = (
    'А в начале пути мало кто в нас верил, не правда ли?',
    'Три слагаемых успеха на «Н»: Напор, Наглость и Независимость',
    'Через тернии к звездам.'
)
quotes_sad = (
    'Каждая неудавшаяся попытка — это еще один шаг вперед',
    'Тот, кто не рискует - не пьёт шампанское',
    "Драгоценный камень нельзя отполировать без трения",
    "Попытка — первый шаг к успеху"
)

ROOT = path.dirname(path.realpath(__file__))

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

socketio = SocketIO(app, cors_allowed_origins="*")
# socketio = SocketIO(app, cors_allowed_origins="*")

_users_in_room = {}  # stores room wise user list
_room_of_sid = {}  # stores room joined by an used
_name_of_sid = {}  # stores display name of users


@app.route("/stream", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        room_id = request.form['room_id']
        return redirect(url_for("entry_checkpoint", room_id=room_id))

    return render_template("home.html")


@app.route("/room/<string:room_id>/")
def enter_room(room_id):
    if room_id not in session:
        return redirect(url_for("entry_checkpoint", room_id=room_id))
    return render_template("chatroom.html", room_id=room_id, display_name=session[room_id]["name"],
                           mute_audio=session[room_id]["mute_audio"], mute_video=session[room_id]["mute_video"])


@app.route("/room/<string:room_id>/checkpoint/", methods=["GET", "POST"])
def entry_checkpoint(room_id):
    if request.method == "POST":
        try:
            con = sqlite3.connect(path.join(ROOT, "web_db.db"))
            cur = con.cursor()
            display_name = cur.execute(f'select name from user_info where id = {session["acc"]}').fetchall()[0][0]
        except Exception:
            display_name = 'Аноним'
        mute_audio = request.form['mute_audio']
        mute_video = request.form['mute_video']
        session[room_id] = {"name": display_name, "mute_audio": mute_audio, "mute_video": mute_video}
        return redirect(url_for("enter_room", room_id=room_id))
    return render_template("chatroom_checkpoint.html", room_id=room_id)


@socketio.on("connect")
def on_connect():
    sid = request.sid
    print("New socket connected ", sid)


@socketio.on("join-room")
def on_join_room(data):
    sid = request.sid
    room_id = data["room_id"]
    display_name = session[room_id]["name"]

    # register sid to the room
    join_room(room_id)
    _room_of_sid[sid] = room_id
    _name_of_sid[sid] = display_name

    # broadcast to others in the room
    print("[{}] New member joined: {}<{}>".format(room_id, display_name, sid))
    emit("user-connect", {"sid": sid, "name": display_name}, broadcast=True, include_self=False, room=room_id)

    # add to user list maintained on server
    if room_id not in _users_in_room:
        _users_in_room[room_id] = [sid]
        emit("user-list", {"my_id": sid})  # send own id only
    else:
        usrlist = {u_id: _name_of_sid[u_id] for u_id in _users_in_room[room_id]}
        emit("user-list", {"list": usrlist, "my_id": sid})  # send list of existing users to the new member
        _users_in_room[room_id].append(sid)  # add new member to user list maintained on server

    print("\nusers: ", _users_in_room, "\n")


@socketio.on("disconnect")
def on_disconnect():
    sid = request.sid
    room_id = _room_of_sid[sid]
    display_name = _name_of_sid[sid]

    print("[{}] Member left: {}<{}>".format(room_id, display_name, sid))
    emit("user-disconnect", {"sid": sid}, broadcast=True, include_self=False, room=room_id)

    _users_in_room[room_id].remove(sid)
    if len(_users_in_room[room_id]) == 0:
        _users_in_room.pop(room_id)

    _room_of_sid.pop(sid)
    _name_of_sid.pop(sid)

    print("\nusers: ", _users_in_room, "\n")


@socketio.on("data")
def on_data(data):
    sender_sid = data['sender_id']
    target_sid = data['target_id']
    if sender_sid != request.sid:
        print("[Not supposed to happen!] request.sid and sender_id don't match!!!")

    if data["type"] != "new-ice-candidate":
        print('{} message from {} to {}'.format(data["type"], sender_sid, target_sid))
    socketio.emit('data', data, room=target_sid)


@app.template_filter(name='linebreaksbr')
def linebreaksbr_filter(text):
    return text.replace('\n', '<br>')


@app.route('/')
@app.route('/main')
def main():
    if "acc" in session and session['acc'] != "-1":
        con = sqlite3.connect(path.join(ROOT, "web_db.db"))
        cur = con.cursor()
        a = cur.execute(f'select progress from user_info where id = {session["acc"]}').fetchall()[0][0]
        imglist = ['photo1682956309.jpeg', 'photo1682956437.jpeg', 'photo16829566311.jpeg', 'photo1682957136.jpeg']
        if a == 1:
            imglist[0] = 'galkf.jpg'
            imglist[2] = 'krest.jpg'
            imglist[3] = 'krest.jpg'
        elif a == 2:
            imglist[0] = 'galkf.jpg'
            imglist[1] = 'galkf.jpg'
            imglist[3] = 'krest.jpg'
        elif a == 3:
            imglist[0] = 'galkf.jpg'
            imglist[1] = 'galkf.jpg'
            imglist[2] = 'galkf.jpg'
        elif a == 4:
            imglist[0] = 'galkf.jpg'
            imglist[1] = 'galkf.jpg'
            imglist[2] = 'galkf.jpg'
            imglist[3] = 'galkf.jpg'
        else:
            imglist[1] = 'krest.jpg'
            imglist[2] = 'krest.jpg'
            imglist[3] = 'krest.jpg'

        name = session["name"]
        link = session["link"]
        return render_template("main.html", name=name, im=imglist)
    return render_template("index.html")


@app.route('/lesson/<num>')
def lesson(num):
    if num == '4':
        return redirect('/test/4')
    if "acc" in session and session['acc'] != "-1":
        con = sqlite3.connect(path.join(ROOT, "web_db.db"))
        cur = con.cursor()
        a = cur.execute(f'select progress from user_info where id = {session["acc"]}').fetchall()[0][0]
        if int(num) > a + 1:
            return render_template('nope.html')
        bonushtml = '<p>К этому уроку нет бонусов</p>'
        if bonuslist[int(num)] != []:
            bonushtml = '<ul class="u-custom-list u-file-icon u-spacing-90 u-text u-text-default u-text-2">'
            for i in bonuslist[int(num)]:
                bonushtml += f"""
                <li style="padding-left: 49px;">
                    <div class="u-list-icon">
                      <img src="/static/file.png" alt="" style="font-size: 5.8em; margin: -5.8em;">
                    </div><a href = "/static/{i}" download>{i}</a>
                  </li>"""
            bonushtml += '</ul>'
        return render_template('lesson.html', num=num, vid=videolist[int(num) - 1], text=textlist[int(num) - 1],
                               bonus=bonushtml, lesson=num)
    else:
        return redirect(url_for('start'))


@app.route('/logout')
def logout():
    session['acc'] = '-1'
    return redirect(url_for('main'))


@app.route('/data-policy')
def data_policy():
    return render_template('data-policy.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory('/static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/test/<lesson>', methods=['POST', 'GET'])
def test(lesson):
    if "acc" in session and session['acc'] != "-1":
        if flask.request.method == 'POST':
            values = list(map(int, flask.request.form.values()))
            proc = int(sum(values * 100) / len(values))
            if proc >= 80:
                con = sqlite3.connect(path.join(ROOT, "web_db.db"))
                cur = con.cursor()
                cur.execute(
                    f'update user_info set progress=max(progress, {int(lesson)}) where id = {session["acc"]}').fetchall()
                con.commit()
                return render_template('result.html', proc=proc, text=random.choice(quotes_success), lesson=int(lesson))
            else:
                return render_template('result.html', proc=proc, text=random.choice(quotes_sad), lesson=int(lesson))
        return render_template('test.html', lesson=int(lesson), q=tests[int(lesson)])
    else:
        return redirect(url_for('start'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    con = sqlite3.connect(path.join(ROOT, "web_db.db"))
    print(flask.request.method)
    if flask.request.method == 'POST':
        cur = con.cursor()
        login = flask.request.form['log']
        pas = flask.request.form['pass']

        acc = cur.execute(f'''SELECT * FROM user_info WHERE login = "{login}" AND pass = "{pas}"''').fetchall()
        if acc:
            session['acc'] = str(acc[0][0])
            session['name'] = str(acc[0][4])
            session['link'] = str(acc[0][3])

            return redirect(url_for('main'))
        else:
            return redirect('/login?error=wrongcred')
    else:
        return render_template('login.html',
                               error={'wrongcred': 'Неправильный логин или пароль'}.get(request.args.get('error')))


@app.route('/start')
def start():
    return render_template('start.html')


@app.route('/registration', methods=['POST', 'GET'])
def reg():
    con = sqlite3.connect(path.join(ROOT, "web_db.db"))
    if flask.request.method == 'POST':

        cur = con.cursor()
        name = flask.request.form['name']
        login = flask.request.form['log']
        pas = flask.request.form['pass']

        acc = cur.execute(f'''SELECT * FROM user_info WHERE login = "{login}"''').fetchall()

        if acc and acc[0][1] == login:
            return redirect('/registration?error=alreadyexists')
            # return '''<a href = /reg> Логин занят </a>'''

        # На платформе может быть несколько людей с одним и тем же именем
        # elif acc and acc[0][4] == name:
        #     return redirect()
        else:
            if len(pas) >= 8:
                while True:
                    link = ''.join(random.sample(alf, len(alf)))
                    flag = cur.execute(f'select * from user_info where link_to_user = "{link}"').fetchall()
                    if not flag:
                        break
                cur.execute(
                    f"INSERT INTO user_info (login, pass, link_to_user, name, progress) values ('{login}', '{pas}', '{link}', '{name}', 0)").fetchall()
                con.commit()
                return redirect('/start')
            else:
                return redirect('/registration?error=passlen')
                # return '''<a href = /reg> В пароле должно быть не менее 8 символов </a>'''

    else:
        error = request.args.get('error')
        if error is not None:
            error = {'alreadyexists': 'Данная почта уже зарегистрирована',
                     'passlen': 'Длина пароля должна быть больше 8 символов',
                     '': ''}.get(error, 'Непредвиденная ошибка')
        print(error)
        return render_template('reg.html', error=error)


@app.route('/download-cert', methods=['GET'])
def download_cert():
    con = sqlite3.connect(path.join(ROOT, "web_db.db"))
    cur = con.cursor()
    name = cur.execute(f'select name from user_info where id = {session["acc"]}').fetchall()[0][0]
    regex = re.compile(r"username")
    filename = "template.docx"
    doc = Document(filename)
    docx_replace_regex(doc, regex, name)
    doc.save('cert.docx')
    return send_file('cert.docx')


if __name__ == "__main__":
    import eventlet
    import eventlet.wsgi
    from eventlet.green import socket
    from eventlet.green.OpenSSL import SSL

    eventlet.wsgi.server(
        eventlet.wrap_ssl(eventlet.listen(('', 82)),
                          certfile='/etc/letsencrypt/live/rasskazchikov.ru/fullchain.pem',
                          keyfile='/etc/letsencrypt/live/rasskazchikov.ru/privkey.pem',
                          server_side=True), app)

    # app.run(debug=True, host='0.0.0.0', port=81)