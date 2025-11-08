from wtforms import Form, StringField, RadioField, BooleanField, IntegerField,EmailField,FloatField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, NumberRange
from wtforms import validators

class PizzaForm(Form):
    nombre = StringField('Nombre', [
        DataRequired(message="El nombre es obligatorio.")
    ])
    direccion = StringField('Dirección', [
        DataRequired(message="La dirección es obligatoria.")
    ])
    telefono = StringField('Teléfono', [
        DataRequired(message="El teléfono es obligatorio.")
    ])
    #  Datos de la Pizza
    tamano = RadioField('Tamaño de la Pizza', 
        choices=[
            ('Chica', 'Chica ($40)'),
            ('Mediana', 'Mediana ($80)'),
            ('Grande', 'Grande ($120)')
        ],
        validators=[DataRequired(message="Debe seleccionar un tamaño.")]
    )
    jamon = BooleanField('Jamón ($10)')
    pina = BooleanField('Piña ($10)')
    champinones = BooleanField('Champiñones ($10)')
    
    cantidad = IntegerField('Número de Pizzas', 
        default=1,
        validators=[
            DataRequired(message="La cantidad es obligatoria."),
            NumberRange(min=1, message="Debe ser al menos 1 pizza.")
        ]
    )

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


