from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField, SelectMultipleField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
from app.models import Usuario, Mutacao

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    lembrar = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')

class RegistroForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirmar_senha = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    submit = SubmitField('Registrar')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Este email já está em uso. Por favor, use outro email.')

class PerfilForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Salvar')

    def __init__(self, original_email, *args, **kwargs):
        super(PerfilForm, self).__init__(*args, **kwargs)
        self.original_email = original_email

    def validate_email(self, email):
        if email.data != self.original_email:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Este email já está em uso. Por favor, use outro email.')

class AlterarSenhaForm(FlaskForm):
    senha_atual = PasswordField('Senha Atual', validators=[DataRequired()])
    nova_senha = PasswordField('Nova Senha', validators=[DataRequired(), Length(min=6)])
    confirmar_senha = PasswordField('Confirmar Nova Senha', validators=[DataRequired(), EqualTo('nova_senha')])
    submit = SubmitField('Alterar Senha')

class AveForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    sexo = SelectField('Sexo', choices=[('M', 'Macho'), ('F', 'Fêmea')], validators=[DataRequired()])
    data_nascimento = DateField('Data de Nascimento', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('ativo', 'Ativo'),
        ('vendido', 'Vendido'),
        ('reservado', 'Reservado'),
        ('para_reproducao', 'Para Reprodução')
    ], validators=[DataRequired()])
    mutacoes = SelectMultipleField('Mutações', coerce=int)
    submit = SubmitField('Salvar')

    def __init__(self, *args, **kwargs):
        super(AveForm, self).__init__(*args, **kwargs)
        self.mutacoes.choices = [(m.id, m.nome) for m in Mutacao.query.all()]

class CasalForm(FlaskForm):
    nome = StringField('Nome do Casal', validators=[DataRequired(), Length(min=3, max=100)])
    macho_id = SelectField('Macho', coerce=int, validators=[DataRequired()])
    femea_id = SelectField('Fêmea', coerce=int, validators=[DataRequired()])
    observacoes = TextAreaField('Observações', validators=[Optional()])
    submit = SubmitField('Salvar')

class NinhadaForm(FlaskForm):
    data_postura = DateField('Data da Postura', validators=[DataRequired()])
    quantidade_ovos = IntegerField('Quantidade de Ovos', validators=[DataRequired()])
    observacoes = TextAreaField('Observações', validators=[Optional()])
    submit = SubmitField('Registrar Ninhada') 