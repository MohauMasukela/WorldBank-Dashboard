from flask import Flask, render_template, request, redirect, url_for,flash
import json

import plotly
from worldbankapi import gdp_data,gdp_pp
import plotly.express as px

from flask_wtf import FlaskForm
from wtforms.fields import SelectMultipleField
from wtforms import SelectMultipleField, SubmitField,SelectField
from wtforms.validators import DataRequired,Email,ValidationError
from flask_bootstrap import Bootstrap5



# class MultiCheckboxField(SelectMultipleField):
#     widget = widgets.ListWidget(prefix_label=False)
#     option_widget = widgets.CheckboxInput()

class CountryFilter(FlaskForm):

    choices=['China','Ghana','Kenya','Nigeria','South Africa','Russia','United States']

    input_country=SelectMultipleField("Select Country",choices=choices)

    submit = SubmitField('Submit')






app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

@app.route('/',methods=("GET","POST"))
def index():


    form=CountryFilter()
    if request.method=="POST":

        
        filter_v=request.form.getlist("input_country")
        data=gdp_data[gdp_data["Country"].isin(filter_v)]

        df=gdp_pp[gdp_pp["Country"].isin(filter_v)]
        # print(filter_v)
        # print(data)
        # print(request.form.getlist("input_country"))
  
        fig = px.line(data, x="Date", y="GDP",color="Country", title="Compare Countries GDP Growth Anually") 
        fig2 = px.bar(df, x="Country", y="GDP pp Employed",color="Country", title="Compare Countries current GDP pp Employed") 
        graph = json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)  
        graph2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)  

        return render_template('graph.html',plot=graph,plot2=graph2,form=form)
    



  
    fig = px.line(gdp_data, x="Date", y="GDP",color="Country", title="Compare Countries GDP Growth Anually") 
    fig2 = px.bar(gdp_pp, x="Country", y="GDP pp Employed",color="Country", title="Compare Countries current GDP pp Employed") 
    graph = json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)  
    graph2 = json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)  

        


   
    return render_template('index.html',plot=graph,plot2=graph2,form=form)




if __name__ == "__main__":

    app.run(debug=True)