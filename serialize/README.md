# Serialize / Deserialize  
직렬화와 역직렬화  

- [Serialize / Deserialize](#serialize--deserialize)
  - [ORM 과 ODM](#orm-과-odm)
  - [marshmallow](#marshmallow)
    - [1. Schema 선언하기](#1-schema-선언하기)
    - [2. 객체를 직렬화 (dump, dumps)](#2-객체를-직렬화-dump-dumps)
    - [3. 객체를 역직렬화 (load)](#3-객체를-역직렬화-load)
    - [객체 컬렉션 다루기](#객체-컬렉션-다루기)
    - [유효성 검사](#유효성-검사)

<br>

## ORM 과 ODM  
ORM (Object Relational Mapping)  
- Object 모델과 Relational DB 를 매핑  
- 데이터의 관계형 표현과 객체 사이에 변환을 위해 사용  

ODM (Object Data Mapping)  
- Object 모델과 Document DB 를 매핑  
- 데이터의 도큐먼트형 표현과 객체 사이의 변환을 위해 사용  

<br>

## marshmallow  
ORM/ODM/framework-agnostic 파이썬 라이브러리  
- 복잡한 데이터 타입, 객체 등과 파이썬 데이터 타입 사이의 변환  

### 1. Schema 선언하기  
딕셔너리로부터 스키마 생성하기  

### 2. 객체를 직렬화 (dump, dumps)  
only, exclude 파라미터를 통해 스키마의 원하는 필드만을 아웃풋으로 만들 수 있음  

### 3. 객체를 역직렬화 (load)  
애플리케이션 레벨의 자료구조로 입력 딕셔너리를 유효성 검사하고, 역직렬화 한다.  

load : 역직렬화된 값에 매핑되는 필드로 구성된 딕셔너리를 리턴함  
- 유효성 검사에서 에러 발생 시, ValidationError 발생  

객체로 역직렬화 하려고 한다면?  
정의한 Schema에 post_load 데코레이터를 씌운 메서드를 추가  
- 해당 메서드는 역직렬화된 데이터의 딕셔너리를 입력으로 받음  
- 이제 load 함수를 통해 바로 객체로 역직렬화 가능  

### 객체 컬렉션 다루기  
many=True 파라미터를 통해 객체 컬렉션 리스트/iterable 을 한번에 직렬화/역직렬화 할 수 있다  

### 유효성 검사  
load -> ValidationError  
ValidationError.messages  
ValidationError.valid_data : 올바르게 역직렬화된 데이터  

컬렉션에 대한 유효성 검사에서 에러가 발생하면  
ValidationError.messages 에 컬렉션의 인덱스를 key로 하여 
