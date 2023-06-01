from odoo import http
from odoo.http import request


from odoo import http
from odoo.http import request


class PersonsController(http.Controller):
    @http.route("/persons", auth="public", type="http", website=True)
    def render_persons_template(self, **kwargs):
        persons = (
            request.env["persons.person"]
            .sudo()
            .search([], limit=5, order="id desc")
        )
        return request.render(
            "people.person_card_template",
            {
                "persons": persons,
            },
        )


class PersonForm(http.Controller):
    @http.route("/persons/create", type="http", auth="public", website=True)
    def person_form(self, **post):
        return request.render("people.person_form", {})

    @http.route(
        ["/persons/create/submit"], type="http", auth="public", website=True
    )
    def customer_form_submit(self, **post):
        person = {
            "first_name": post.get("first_name"),
            "last_name": post.get("last_name"),
            "birthday": post.get("birthday"),
            "sex": post.get("sex"),
        }
        request.env["persons.person"].sudo().create(person)
        vals = {
            "person": person,
        }
        return request.render("people.person_form_success", vals)
