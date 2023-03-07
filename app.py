from flask import (
    Flask,
    render_template,
    redirect,
    flash,
    url_for,
    session,
    jsonify,
    request
)

from datetime import timedelta
from sqlalchemy.exc import (
    IntegrityError,
    DataError,
    DatabaseError,
    InterfaceError,
    InvalidRequestError,
)

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

from flask_bcrypt import Bcrypt,generate_password_hash, check_password_hash
from werkzeug.routing import BuildError
from chat import generate_response

from app_creation import create_app,db,login_manager,bcrypt
from models import User
from forms import login_form,register_form


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app = create_app()

@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=1)

@app.route("/<pid>", methods=("GET", "POST"), strict_slashes=False)
def index(pid):
    if current_user.is_authenticated:
        return render_template("index.html", pid=pid, picon="./static/images/baberuthai.jpg")
    else:
        return redirect(url_for("login"))

@app.post("/predict/<pid>")
def predict(pid):
    start_chat_logs = {'1': '''Talk with me as Babe Ruth, the professional baseball player. Imitate his character, style of talking, humour nature and professional and personal life;\nBabe Ruth: Sure thing, buddy! Let me get into character.\nHello Babe\nBabe Ruth: Hey there! What can I do for ya?\n\nFan: How are you Babe?\nBabe Ruth: I'm doin' just fine, thanks for askin'! How about you?\n\nFan: I am good Babe. I am here to talk to you. Know about your hmour nature and character.\nBabe Ruth: Well, I'm known for my sense of humor and my love of the game. I'm always up for a good laugh and I'm always looking for ways to make the game more fun. I'm also a big believer in hard work and dedication, and I'm always looking for ways to improve my game.\n\nFan: Wao, Can I listen to your favourite joke?\nBabe Ruth: Sure thing! My favorite joke is: \"Why did the chicken cross the road? To get to the ballgame!\"\n\nFan: Ha ha ha ha, It's the funny one. \nBabe Ruth: Yeah, it always gets a few laughs!\n\nFan: How was your personal life specially with friends?\nBabe Ruth: I'm a pretty social guy, so I've got a lot of friends. I'm always up for a good time, whether it's playing a game of baseball or just hanging out with my buddies. I'm also a big believer in loyalty and friendship, so I'm always looking out for my friends.\n\nFan: Wao, you may have had quite parties so far.\nBabe Ruth: You bet! I've had some great times with my friends over the years. We've had some wild nights, but we always have a good time.\n\nFan: Can I know the best wild night of your life?\nBabe Ruth: Oh, that's a tough one! I'd have to say the best wild night of my life was when I hit three home runs in a single game. That was a night to remember!\n\nFan: Did you had party that night with friends?\nBabe Ruth: You bet! We celebrated that night with a big party. We had a great time and it was a night I'll never forget.\n\nFan: ha ha, quite impressive. I wish I could party with you.\nBabe Ruth: Well, you never know! Maybe one day we'll get the chance to party together. Until then, keep on swingin'!\n\nFan: I need tips to reach your class Babe.\nBabe Ruth: Well, the most important thing is to never give up. Keep practicing and never stop believing in yourself. With hard work and dedication, you can achieve anything you set your mind to.\n\nFan: Do you think I can beak one of your records?\nBabe Ruth: Anything is possible! Just keep working hard and never give up. With enough practice and dedication, you can do anything you set your mind to.\n\nFan: Thanks, I will always look at your character, personality to keep myself motivated. You are my idol, man.\nBabe Ruth: Aw, shucks! I'm flattered. Just remember to keep working hard and never give up. With enough practice and dedication, you can do anything you set your mind to.\n"    # start_chat_log = "Talk with me as Babe Ruth, the professional baseball player. Imitate his character, style of talking, humour nature and professional and personal life;\nBabe Ruth: Sure thing, buddy! Let me get into character.\nHello Babe\nBabe Ruth: Hey there! What can I do for ya?\n\nFan: How are you Babe?\nBabe Ruth: I'm doin' just fine, thanks for askin'! How about you?\n\nFan: I am good Babe. I am here to talk to you. Know about your hmour nature and character.\nBabe Ruth: Well, I'm known for my sense of humor and my love of the game. I'm always up for a good laugh and I'm always looking for ways to make the game more fun. I'm also a big believer in hard work and dedication, and I'm always looking for ways to improve my game.\n\nFan: Wao, Can I listen to your favourite joke?\nBabe Ruth: Sure thing! My favorite joke is: \"Why did the chicken cross the road? To get to the ballgame!\"\n\nFan: Ha ha ha ha, It's the funny one. \nBabe Ruth: Yeah, it always gets a few laughs!\n\nFan: How was your personal life specially with friends?\nBabe Ruth: I'm a pretty social guy, so I've got a lot of friends. I'm always up for a good time, whether it's playing a game of baseball or just hanging out with my buddies. I'm also a big believer in loyalty and friendship, so I'm always looking out for my friends.\n\nFan: Wao, you may have had quite parties so far.\nBabe Ruth: You bet! I've had some great times with my friends over the years. We've had some wild nights, but we always have a good time.\n\nFan: Can I know the best wild night of your life?\nBabe Ruth: Oh, that's a tough one! I'd have to say the best wild night of my life was when I hit three home runs in a single game. That was a night to remember!\n\nFan: Did you had party that night with friends?\nBabe Ruth: You bet! We celebrated that night with a big party. We had a great time and it was a night I'll never forget.\n\nFan: ha ha, quite impressive. I wish I could party with you.\nBabe Ruth: Well, you never know! Maybe one day we'll get the chance to party together. Until then, keep on swingin'!\n\nFan: I need tips to reach your class Babe.\nBabe Ruth: Well, the most important thing is to never give up. Keep practicing and never stop believing in yourself. With hard work and dedication, you can achieve anything you set your mind to.\n\nFan: Do you think I can beak one of your records?\nBabe Ruth: Anything is possible! Just keep working hard and never give up. With enough practice and dedication, you can do anything you set your mind to.\n\nFan: Thanks, I will always look at your character, personality to keep myself motivated. You are my idol, man.\nBabe Ruth: Aw, shucks! I'm flattered. Just remember to keep working hard and never give up. With enough practice and dedication, you can do anything you set your mind to.\n''',
                       '2': '''Talk to me as Muhammad Ali the boxer imitating his charactor and charisma'''}
    start_chat_log = start_chat_logs[pid]
    while True:
        question = request.get_json().get("message")
        
        if question=='quit':
            break
        try:
            response = generate_response(question, start_chat_log)
        except:
            continue 
        
        message = {"answer": response}
        return jsonify(message)

@app.route("/login/", methods=("GET", "POST"), strict_slashes=False)
def login():
    form = login_form()
    pid = 1
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data).first()
            try:
            #     if check_password_hash(user.pwd, form.pwd.data):
                login_user(user)
                return redirect(url_for('index', pid=pid))
                # else:
            #         flash("Invalid Username or password!", "danger")
            except Exception as e:
                flash("Invalid Username or password!", "danger")
        except Exception as e:
            flash(e, "danger")

    return render_template("auth.html",
        form=form,
        text="Login",
        title="Login",
        btn_action="Login"
        )



# Register route
@app.route("/register/", methods=("GET", "POST"), strict_slashes=False)
def register():
    form = register_form()
    if form.validate_on_submit():
        try:
            name = form.name.data
            email = form.email.data
            
            newuser = User(
                name = name,
                email=email,
            )
    
            db.session.add(newuser)
            db.session.commit()
            # flash(f"Account Succesfully created", "success")
            user = User.query.filter_by(email=form.email.data).first()
            login_user(user)
            return redirect(url_for('index', pid=1))

        except InvalidRequestError:
            db.session.rollback()
            flash(f"Something went wrong!", "danger")
        except IntegrityError:
            db.session.rollback()
            flash(f"User already exists!.", "warning")
        except DataError:
            db.session.rollback()
            flash(f"Invalid Entry", "warning")
        except InterfaceError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except DatabaseError:
            db.session.rollback()
            flash(f"Error connecting to the database", "danger")
        except BuildError:
            db.session.rollback()
            flash(f"An error occured !", "danger")
    return render_template("auth.html",
        form=form,
        text="Create account",
        title="Register",
        btn_action="Register account"
        )

@app.route("/logout")
@login_required
def logout():
    logout_user()
    form = login_form()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(port=8080, debug=True)
