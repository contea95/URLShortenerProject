from flask import redirect, render_template, request
from serverModule import app, db
from serverModule.model import Url
import validators


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/encode/<input_url>')
def encode(input_url):
    if str(input_url).startswith('http://') == False or str(input_url).startswith('https://') == False:
        print("malfunction")
        return render_template('404.html'), 404
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


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        # HTML 폼에서 전달받은 url
        url = request.form['url']
        input_url = str(url)

        if str(input_url).startswith('http://') or str(input_url).startswith('https://'):
            print("start http or https")
    count = Url.query.filter_by(origin_url=input_url).first()
    if count is None:
        # DB 내 단축 URL이 없을 경우
        url = Url(origin_url=input_url)
        db.session.add(url)
        db.session.commit()
        id_num = url.search_id_by_origin_url(origin_url=input_url)
        print("new url Update!")
        # return f'{id_num.id}'
        return render_template("result.html", url=id_num.id)
    else:
        # DB 내 단축 URL이 있을 경우
        url = Url.query.filter_by(origin_url=input_url).first()
        print("URL READ IN DB")
        # return f'{url.id}'
        return render_template("result.html", url=url.id)

        # return render_template("result.html", url=url)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
