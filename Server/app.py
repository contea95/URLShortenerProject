from flask import redirect
from serverModule import app, db
from serverModule.model import Url


@app.route('/')
def hello():
    return f'{"hello"}'


@app.route('/encode/<input_url>')
def encode(input_url):
    count = Url.query.filter_by(origin_url=input_url).first()
    if count is None:
        # DB 내 단축 URL이 없을 경우
        url = Url(origin_url=input_url)
        db.session.add(url)
        db.session.commit()
        id_num = url.search_id_by_origin_url(origin_url=input_url)
        print("new url Update!")
        return f'{id_num.id}'
    else:
        # DB 내 단축 URL이 있을 경우
        url = Url.query.filter_by(origin_url=input_url).first()
        print("URL READ IN DB")
        return f'{url.id}'


@app.route('/redirection/<input_code>')
def redirection(input_code):
    url = Url.query.filter_by(id=input_code).first()
    # return f'{url.origin_url}'
    return redirect("https://" + str(url.origin_url), code=302)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
