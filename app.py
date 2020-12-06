from flask import Flask, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextField, SubmitField
from wtforms.validators import InputRequired, NumberRange
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'


class CalcForm(FlaskForm):
    homeprice = IntegerField('Home Price', [InputRequired()])
    downpayment = IntegerField('Down Payment')
    interestrate = IntegerField('Interest Rate', [InputRequired()])
    taxes = IntegerField('Property Taxes (Yearly)')
    submit = SubmitField('Calculate')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = CalcForm()
    if form.validate_on_submit():
        print(form.data)
    interest = (0 if form.interestrate.data is None else (
        form.interestrate.data * .01))
    years = 30
    payments_year = 12
    mortgage = int(0 if form.homeprice.data is None else (
        form.homeprice.data))
    downpayment = form.downpayment.data or 0
    taxes = form.taxes.data or 0
    tax = (taxes/12)
    pmt = -1 * np.pmt(interest/12, years * payments_year,
                      mortgage - downpayment) + tax
    ipmt = -1 * np.ipmt(interest / payments_year, 1, years *
                        payments_year, mortgage - downpayment)
    ppmt = -1 * np.ppmt(interest/payments_year, 1,
                        years * payments_year, mortgage - downpayment)
    prin_int = ipmt + ppmt

    return render_template('index.html', form=form, prin_int=prin_int, pmt=pmt, tax=tax)


if __name__ == '__main__':
    app.run(debug=True)
