# python
I study PYTHON !

<br>

## 1. python 문법
- Class
- Module
- Exception
- Input/Output
- Function Arguments : *args, **kwargs

<br>

## 2. 표준 라이브러리
- str  
- os-module  
- urllib  
- datetime  
- daemon sleep : time.sleep(), threading

<br>

## 3. 모듈
- pandas
- re (regular expression)
- bs4
- numpy
- pycryptodomex (AES encrypt/decrypt)

<br>

## 4. Scrapy
1. Scarpy **프로젝트 만들기**  
```
scrapy startproject {project name}
```
2. 웹에서 **데이터를 추출**하는 Spider 구현  
```
scrapy genspider {spider name} {url}
```
3. 명령행 도구를 사용해 추출된 데이터를 **저장**  
- O : Over-write  
- o : 기존 파일 뒤에 이어서 저장(.jl 파일로 저장하는 것이 편리함)  
```
scrapy crawl {spider name} -O {filename}.jl
```
4. **여러 개의 링크**를 이어서 크롤링하는 Spider 구현  
5. Spider **전달인자** 사용  
- a 속성, name=value 형태로 전달  
```
scrapy crawl {spider name} -a {attr.name}={attr.val}
```

<br>

## 5. Django
- django-programming : 책 '파이썬 웹 프로그래밍'을 따라 만든 웹  
- resful-api : rest-framework를 이용한 rest api 구축 연습  
- social_login : allauth를 이용한 social login 개발 연습 

<br>

## 6. Machine Learning
*(sklearn 패키지 학습)*  
1. Preprocessing, Visualization  
2. Split dataset into train and test  
3. Model training/learning  
4. Score, Evaluate model  
5. Predict  

<br>

## 6-1. Keras

<br>

## 7. PySpark
- rdd-operations : 기본 tranformation/action rdd 연산 

<br>

## 8. python project
- **collector**
    - 하루에 한 번 특정 시간에 수집을 시도하는 배치형 데몬 프로그램  
    - Threading, bs4, Selenium  
    ```
    # nohup 없이 실행하면 터미널 종료 시 프로그램도 종료됨  
    nohup python jkcrawlerd.py &
    ```
