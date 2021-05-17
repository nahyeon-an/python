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