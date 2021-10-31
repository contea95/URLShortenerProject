from flask import json, redirect, render_template, request, jsonify
from serverModule import app, db
from serverModule.model import Url
import json


@app.route('/')
def index():
    return render_template("index.html")

#   Redirect 담당 함수


@app.route('/<input_code>')
def redirection(input_code):
    #   DB 내에 단축된 URL이 있으면 Redirect, 없으면 404 오류페이지
    count = Url.query.filter_by(id=input_code).first()
    if count is not None:
        url = Url.query.filter_by(id=input_code).first()
        # return f'{url.origin_url}'
        return redirect(str(url.origin_url), code=302)
    else:
        return render_template('404.html'), 404

#   테스트용 페이지


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        # HTML 폼에서 전달받은 url
        url = request.form['url']
        input_url = str(url)
        print(url)

        if str(input_url).startswith('http://') == False and str(input_url).startswith('https://') == False:
            return render_template('404.html'), 404
        else:
            count = Url.query.filter_by(origin_url=input_url).first()
            if count is None:
                # DB 내 단축 URL이 없을 경우
                url = Url(origin_url=input_url)
                db.session.add(url)
                db.session.commit()
                id_num = url.search_id_by_origin_url(origin_url=input_url)
                print("new url Update!")
                return render_template("result.html", url=id_num.id)
            else:
                # DB 내 단축 URL이 있을 경우
                url = Url.query.filter_by(origin_url=input_url).first()
                print("URL READ IN DB")
                return render_template("result.html", url=url.id)

#   iOS용 접근 링크


@app.route('/result_json', methods=['POST', 'GET'])
def result_json():
    if request.method == 'POST':
        # HTML 폼에서 전달받은 url
        url = request.form['url']
        input_url = str(url)
        print(url)

        if str(input_url).startswith('http://') == False and str(input_url).startswith('https://') == False:
            return render_template('404.html'), 404
        else:
            count = Url.query.filter_by(origin_url=input_url).first()
            if count is None:
                # DB 내 단축 URL이 없을 경우
                url = Url(origin_url=input_url)
                db.session.add(url)
                db.session.commit()
                id_num = url.search_id_by_origin_url(origin_url=input_url)
                print("new url Update!")
                return jsonify([id_num.id])
            else:
                # DB 내 단축 URL이 있을 경우
                url = Url.query.filter_by(origin_url=input_url).first()
                print("URL READ IN DB")
                return jsonify({"url": str(url.id)})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
