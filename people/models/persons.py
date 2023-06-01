from odoo import models, fields, api


class Persons(models.Model):
    _name = "persons.person"
    _description = "Persons"
    _inherit = ["website.published.mixin"]

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    full_name = fields.Char(string="Full Name", compute="_compute_full_name")
    birthday = fields.Date(string="Birthday")
    age = fields.Integer(string="Age", compute="_compute_age")
    sex = fields.Selection(
        selection=[
            ("male", "Male"),
            ("female", "Female"),
            ("non-binary", "Non-Binary"),
        ],
        string="Sex",
    )
    company_id = fields.Many2one("res.company", string="Company")

    @api.depends("first_name", "last_name")
    def _compute_full_name(self):
        for person in self:
            full_name = ""
            if person.first_name:
                full_name += person.first_name
            if person.last_name:
                full_name += " " + person.last_name
            person.full_name = full_name

    @api.depends("birthday")
    def _compute_age(self):
        today = fields.Date.today()
        for person in self:
            if person.birthday:
                birthday = fields.Date.from_string(person.birthday)
                age = today.year - birthday.year
                if (today.month, today.day) < (birthday.month, birthday.day):
                    age -= 1
                person.age = age
            else:
                person.age = 0
