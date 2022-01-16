from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField
from wtforms.validators import DataRequired, Length



class Form(FlaskForm):
    keyword = StringField('Keyword',
                           validators=[DataRequired(), Length(min=2, max=50)]) #list of validators
    location = StringField('Location',
                        validators=[DataRequired(), Length(min=2, max=50)])
    restaurant01 = StringField('Find restaurants similar to ',
                        validators=[DataRequired(), Length(min=2, max=50)])
    restaurant02 = StringField('From restaurant',
                        validators=[DataRequired(), Length(min=2, max=50)])
    restaurant03 = StringField('To restaurant',
                        validators=[DataRequired(), Length(min=2, max=50)])
    traversal = RadioField( choices=[('BFS','BFS'),('DFS','DFS')])
    shortest_path = RadioField( choices=[('Bellman Ford','Bellman Ford'),('Dijkstra','Dijkstra')])
    
    submit = SubmitField('Search')


class AdvancedFrom(FlaskForm):
    keyword = StringField('Keyword',
                           validators=[DataRequired(), Length(min=2, max=50)]) #list of validators
    location = StringField('Location',
                        validators=[DataRequired(), Length(min=2, max=50)])
    restaurant01 = StringField('Find restaurants similar to ',
                        validators=[DataRequired(), Length(min=2, max=50)])
    restaurant02 = StringField('From restaurant',
                        validators=[DataRequired(), Length(min=2, max=50)])
    restaurant03 = StringField('To restaurant',
                        validators=[DataRequired(), Length(min=2, max=50)])
    traversal = RadioField( choices=[('BFS','BFS'),('DFS','DFS')])
    shortest_path = RadioField( choices=[('Bellman Ford','Bellman Ford'),('Dijkstra','Dijkstra')])
    
    submit = SubmitField('Search')