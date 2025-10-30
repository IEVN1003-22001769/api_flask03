from wtforms import Form
from wtforms import StringField, FloatField, PasswordField, IntegerField, EmailField, RadioField
from wtforms import validators

class UserForm(Form):
    matricula=IntegerField('Matricula', [validators.DataRequired(message="La matricula es obligatoria")])
    nombre=StringField('Nombre', [validators.DataRequired(message="El campo es requerido")])
    apellido=StringField('Apellido', [validators.DataRequired(message="El campo es requerido")])
    correo=EmailField('Correo', [validators.Email(message="El campo es requerido")])


class FigurasA(Form):
    figura = RadioField('Elige una figura', 
        choices=[
            ('triangulo', 'Triángulo'),
            ('rectangulo', 'Rectángulo'),
            ('circulo', 'Círculo'),
            ('pentagono', 'Pentágono')
        ],
        validators=[validators.DataRequired(message="elige una figura")]
    )

    valor1 = FloatField('Numero 1', [validators.DataRequired(message="Este valor es obligatorio.")])

    valor2 = FloatField('Numero 2', [validators.Optional()])


