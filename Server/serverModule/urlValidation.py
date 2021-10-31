import re

#   URL 유효성을 정규표현식과 비교해 T,F를 판별
#   정규표현식은 http, https가 들어갔는지, 도메인.최상위도메인 형식인지 판별한다.


def urlValidation(input_url):
    p = re.compile(
        '^(https?://)[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+/?[a-zA-Z0-9-_/.?=]*')
    return p.match(input_url) != None
