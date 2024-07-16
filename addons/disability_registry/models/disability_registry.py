from odoo import models, fields,api
from odoo.exceptions import ValidationError
import re

class DisabilityRegistry(models.Model):
    _name = 'disability.registry'
    _description = 'Disability Registry'

    #Datos Personales
    name = fields.Char(string='Nombre y Apellido', required=True)
    domicilio = fields.Char(string='Domicilio', required=True)
    fecha_nacimiento = fields.Date(string='Fecha de Nacimiento', required=True)
    telefono = fields.Char(string='Teléfono',required=True)

    """"@api.constrains('telefono')
    def _check_phone(self):
        patron_telefono = re.compile(r'^\+?\d{1,4}?[-.\s]?(\(?\d{1,3}?\)?[-.\s]?)?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{10}$')
        for record in self:
            if not patron_telefono.match(record.telefono):
                raise ValidationError("Colocar un numero de telefono validor.")
            if not record.telefono.isdigit():
                raise ValidationError("Debe colocar solo numero.")"""

    correo_electronico = fields.Char(string='Correo Electrónico')

    @api.constrains('correo_electronico')
    def _check_email(self):
        for record in self:
            if not record.correo_electronico or '@' not in record.correo_electronico:
                raise ValidationError("Correo electronico no valido")

    dni = fields.Char(string='DNI', required=True)

    @api.constrains('DNI')
    def _check_dni(self):
        dni_patron = re.compile(r'^\d{8}$')
        for record in self:
            if not dni_patron.match(record.dni):
                raise ValidationError("Coloque un numero de DNI valido o agregar 0 al principo si no llega a 8 digitos.")

    #Responsable datos
    resp_name = fields.Char(string='Nombre y Apellido', required=True)
    resp_domicilio = fields.Char(string='Domicilio', required=True)
    resp_fecha_nacimiento = fields.Date(string='Fecha de Nacimiento', required=True)
    resp_telefono = fields.Char(string='Teléfono', required=True)
    resp_correo_electronico = fields.Char(string='Correo Electrónico')


    #Situacion de discapacidad
    cud = fields.Boolean(string='Tiene CUD')
    cud_fecha_emicion = fields.Date(string='Fecha de Emicion')
    cud_fecha_vencimiento = fields.Date(string='Fecha de Vencimiento')
    pension = fields.Boolean(string='Tiene Pensión por Discapacidad', required=True)
    obra_social = fields.Boolean(string='Tiene Obra Social', required=True)
    obra_social_cual = fields.Char(string='¿Cuál?')
    #Elemento de apoyo
    support_element_ids = fields.Many2many('disability.support.elements', string='Elementos de Apoyo')
    transport_ids = fields.Many2many('disability.transport', 'disability_registry_transport_rel', 'registry_id', 'transport_id', string='Medios de Movilidad')
    #Diagnostico
    diagnosis = fields.Text(string='Diagnóstico', required=True)

    #Acompañante
    acompanante = fields.Boolean(string='Tiene Acompañante', required=True)
    acompanante_nombre = fields.Char(string='Nombre y Apellido del Acompañante')
    acom_telefono = fields.Char(string='Acompañante Teléfono')
    acom_correo_electronico = fields.Char(string='Acompañante Correo Electrónico')

    @api.constrains('acom_correo_electronico', 'acompanante')
    def _check_email(self):
        for record in self:
            if record.acompanante:
                if not record.acom_correo_electronico or '@' not in record.acom_correo_electronico:
                    raise ValidationError("Correo electronico no valido")

    #Control
    controla_esfinter = fields.Boolean(string='Controla Esfínteres', required=True)
    alergias = fields.Boolean(string='Tiene Alergias', required=True)
    alergias_detalle = fields.Char(string='¿De qué?')
    #Terapia
    terapia_ids = fields.Many2many('disability.therapies', string='Terapias que realiza', required=True)
    #Movilidad
    movilidad_ids = fields.Many2many('disability.transport', string='¿En qué se moviliza?')
    usa_transporte_municipal = fields.Boolean(string='¿Es usuario del servicio de transporte municipal?', required=True)
    #Educacion
    nivel_educativo = fields.Selection([
        ('educacion especial', 'Educacion Especial'),
        ('primario_incompleto', 'Primario Incompleto'),
        ('primario_completo', 'Primario Completo'),
        ('secundario_incompleto', 'Secundario Incompleto'),
        ('secundario_completo', 'Secundario Completo'),
        ('terciario_incompleto', 'Terciario/Universitario Incompleto'),
        ('terciario_completo', 'Terciario/Universitario Completo')
    ], string='Máximo Nivel Educativo Alcanzado')

    concurre_institucion = fields.Boolean(string='¿Concurre a alguna institución?')
    institucion_cual = fields.Char(string='¿A cuál?')

    trabaja = fields.Boolean(string='¿Trabaja?', required=True)
    trabajo_donde = fields.Char(string='¿Dónde?')
    #Intervenciones
    intervencion_ids = fields.One2many('disability.intervention', 'registry_id', string='Historial de Intervenciones')


class DisabilitySupportElements(models.Model):
    _name = 'disability.support.elements'
    _description = 'Elementos de Apoyo'
    name = fields.Char(string='Elemento de Apoyo', required=True)

class DisabilityTherapies(models.Model):
    _name = 'disability.therapies'
    _description = 'Terapias que Realiza'
    name = fields.Char(string='Terapia', required=True)

class DisabilityTransport(models.Model):
    _name = 'disability.transport'
    _description = 'Medios de Movilidad'
    name = fields.Char(string='Medio de Movilidad', required=True)

class DisabilityIntervention(models.Model):
    _name = 'disability.intervention'
    _description = 'Intervenciones'
    registry_id = fields.Many2one('disability.registry', string='Registro de Discapacidad')
    fecha = fields.Date(string='Fecha')
    profesional = fields.Char(string='Profesional')
    observaciones = fields.Text(string='Observaciones')
