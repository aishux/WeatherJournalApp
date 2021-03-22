import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        new_city = request.form.get('city')
    
        if new_city:
            new_city_obj = City(name=new_city)

            db.session.add(new_city_obj)
            db.session.commit()

    cities = City.query.all()

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=500921a423e627bd78929d5d630028ce'

    weather_data = []
    try:

        for city in cities[::-1]:
            r = requests.get(url.format(city.name)).json()
            weather = {
                'city' : city.name,
                'id' : city.id,
                'temperature' : r['main']['temp'],
                'description' : r['weather'][0]['description'],
                'icon' : r['weather'][0]['icon'],
            }
            weather_data.append(weather)
    except KeyError:
        pass
    except EXCEPTION as e:
        pass


    return render_template('weather.html', weather_data=weather_data)

@app.route('/deleteAll')
def deleteAll():
    city = City.query.all()
    for i in city:
        db.session.delete(i)
    db.session.commit()
    
    return redirect(url_for('index'))


@app.route("/delete/<id>", methods = ['GET', 'POST'])
def delete(id):
    city = City.query.filter_by(id=id).first()
    db.session.delete(city)
    db.session.commit()
    return redirect(url_for('index'))

app.run(debug=True)