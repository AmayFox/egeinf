from flask import redirect
from flask_login import login_required, current_user
from flask.views import MethodView
from web.api.models.user import User


class SetSmallGrade(MethodView):
    @login_required
    def get(self):
        User.update_by_login(current_user.login, 'grade', 9)
        return redirect('/account')


class SetBigGrade(MethodView):
    @login_required
    def get(self):
        User.update_by_login(current_user.login, 'grade', 11)
        return redirect('/account')
