from serverModule import app, db
from serverModule.models import Url
from serverModule.changeIndex import trans
from flask import redirect


@app.route('/encode/<number>')
def encode(number):
    url = Url(origin_url=number)
    db.session.add(url)
    db.session.commit()
    return f'{number}'


@app.route('/redirection')
def redirection():
    return redirect("https://www.naver.com", code=302)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
