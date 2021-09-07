# Flask

Flask Document : https://flask.palletsprojects.com/en/2.0.x/  

## Tutorial  
### Application Setup  
Flask application 은 Flask 클래스의 객체 생성으로 실행된다.  
{project dir}/\_\_init__.py  
- <ins>프로젝트의 init 파일에서 application factory 함수를 통해 flask 인스턴스를 생성</ins>  
- 앱에 필요한 모든 설정, 등록 이후 앱을 리턴  
- 왜? flask 인스턴스를 전역적으로 생성하는 것은 프로젝트가 커지면 여러 문제 발생 가능 !  
```
from flask import Flask

# program factory function
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)  # instance_relative_config : config 파일이 instance 폴더에 상대적임
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # Define Database
    from . import db
    db.init_app(app)

    # Register Blueprint/Views
    from . import auth
    app.register_blueprint(auth.bp)

    return app
```

<br>

### Define Database
app.teardown_appcontext() 에 함수를 등록  
- Flask 는 요청이 종료되거나 앱이 종료될 때 DB 세션을 자동으로 제거함

<br>

### Bluprints, Views  
url_for() : 이름(=endpoint, view 함수의 이름)을 통해 view 에 매핑되는 url 생성  

<br>

### Templates
Jinja 템플릿 라이브러리를 이용하여 템플릿 렌더링  
- html 에서 렌더링되는 어떤 데이터든 autoescape  
    - 예를 들어, 사용자가 < > 기호를 입력했다고 해보자
    - 이 기호들은 Html 문서를 방해할 수 있지만  
    - Jinja 를 이용하면 safe escape 가능  
    - <u>즉, 사용자가 의도한대로 브라우저에 표시되게 한다 !</u>  
- {{ }} : 표현식
- {% %} : 제어흐름문
base layout : body 를 감싸는 공통적인 html 요소  
- 다른 템플릿들은 베이스를 extend 하여 공통 section을 override  
html 템플릿에서 자동으로 사용가능하도록 되어있는 함수/인스턴스들 존재  
- ex. url_for(), g  

<br>

### SQLAlchemy
Document : https://flask-sqlalchemy.palletsprojects.com/en/2.x/  
```
pip install -U Flask-SQLAlchemy
``` 
flask app을 전달하여 사용

<br>

### WTForms
브라우저에서 제출하는 form 데이터 처리 시 유효성 검사를 쉽게 만드는 라이브러리  
- 왜 사용할까? 코드의 **가독성**이 좋아짐 !  
```
pip install -U Flask-WTF
```
First of All, form 요소를 클래스로 정의  
view 함수에서 request.form 을 이용하여 정의한 form 객체 생성하기  
값의 유효성을 검사하려면? form.validate() 호출로 가능 

<br>

### Flask Login
Document : https://flask-login.readthedocs.io/en/latest/
```
pip install flask-login
```
Flask-Login은 Flask 앱에 <ins>**사용자 세션 관리**</ins>를 제공한다.  
- active user 의 아이디를 세션에 저장  
- 자동저장 기능  
- 쿠키에서 사용자 세션 정보를 훔치지 못하도록 보호함  

<br>