from flask import render_template
from flask.views import MethodView


class ErrorRightsController(MethodView):
    def get(self):
        return render_template('errors/right.html')
