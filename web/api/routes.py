from flask import Blueprint

api = Blueprint('api', __name__, template_folder='../templates', static_folder='../static')

from web.api.controllers.MainPageController import MainPageController
from web.api.controllers.UserControllers.RegController import RegController
from web.api.controllers.UserControllers.LoginController import LoginController
from web.api.controllers.UserControllers.LogoutController import LogoutController
from web.api.controllers.UserControllers.AccountController import AccountController
from web.api.controllers.UserControllers.SetGradeControllers import SetBigGrade, SetSmallGrade
from web.api.controllers.UserControllers.EditProfileInfoControllers import EditAvatarController, EditEmailController, \
    EditNameController, EditPasswordController
from web.api.controllers.TasksController.TasksController import TasksController
from web.api.controllers.TasksController.CreateTaskOneAnswerController import CreateTaskOneAnswerController
from web.api.controllers.TasksController.CreateTaskFourAnswersController import CreateTaskFourAnswersController
from web.api.controllers.TasksController.CreateTaskProgController import CreateTaskProgController
from web.api.controllers.TasksController.SolveTaskController import SolveTaskController
from web.api.controllers.TasksController.ShowProgAnswer import ShowProgAnswerController
from web.api.controllers.TasksController.CheckingProgAnswersControllers import GoodProgramController, BadProgramController
from web.api.controllers.ScoreboardController import ScoreboardController, Scoreboard9Controller, Scoreboard11Controller
from web.api.controllers.TasksController.ShowAllTasksController import ShowAllTasksController
from web.api.controllers.UserControllers.ShowOtherUserController import ShowOtherUserController
from web.api.controllers.TasksController.EditTaskControllers import EditTaskContentController, \
    EditTaskPictureController, EditTaskAnswerController, EditTaskTagController, EditTaskRatingController
from web.api.controllers.ErrorRightsController import ErrorRightsController

'''
PAGES
'''
api.add_url_rule('/', view_func=MainPageController.as_view('MainPage'))
api.add_url_rule('scoreboard', view_func=ScoreboardController.as_view('ScoreboardController'))

api.add_url_rule('scoreboard/9', view_func=Scoreboard9Controller.as_view('Scoreboard9Page'))
api.add_url_rule('scoreboard/11', view_func=Scoreboard11Controller.as_view('Scoreboard11Page'))

api.add_url_rule('error/rights', view_func=ErrorRightsController.as_view('ErrorRightsPage'))

'''
AUTH
'''
api.add_url_rule('login', view_func=LoginController.as_view('LoginPage'))
api.add_url_rule('reg', view_func=RegController.as_view('RegPage'))
api.add_url_rule('logout', view_func=LogoutController.as_view('LogoutController'))


'''
ACCOUNT
'''
api.add_url_rule('account', view_func=AccountController.as_view('AccountPage'))
api.add_url_rule('class/nine', view_func=SetSmallGrade.as_view('SetSmallGradeController'))
api.add_url_rule('class/eleven', view_func=SetBigGrade.as_view('SetBigGradeController'))

api.add_url_rule('edit/name', view_func=EditNameController.as_view('EditNamePage'))
api.add_url_rule('edit/email', view_func=EditEmailController.as_view('EditEmailPage'))
api.add_url_rule('edit/password', view_func=EditPasswordController.as_view('EditPasswordPage'))
api.add_url_rule('edit/photo', view_func=EditAvatarController.as_view('EditAvatarPage'))

api.add_url_rule('user/<string:login>', view_func=ShowOtherUserController.as_view('ShowOtherUserPage'))


'''
TASKS PAGE
'''
api.add_url_rule('tasks', view_func=TasksController.as_view('TasksPage'))
api.add_url_rule('create/task/one/answer', view_func=CreateTaskOneAnswerController.as_view('CreateTaskOneAnswerPage'))
api.add_url_rule('create/task/four/answer', view_func=CreateTaskFourAnswersController.as_view('CreateTaskFourAnswersPage'))
api.add_url_rule('create/task/prog', view_func=CreateTaskProgController.as_view('CreateTaskProgPage'))
api.add_url_rule('task/solve/<int:id>', view_func=SolveTaskController.as_view('SolveTaskPage'))
api.add_url_rule('task/show/answer/<string:filename>', view_func=ShowProgAnswerController.as_view('ShowProgAnswerPage'))

api.add_url_rule('task/good/program/<int:id>', view_func=GoodProgramController.as_view('GoodProgramController'))
api.add_url_rule('task/bad/program/<int:id>', view_func=BadProgramController.as_view('BadProgramController'))
api.add_url_rule('show/tasks', view_func=ShowAllTasksController.as_view('ShowAllTasksPage'))

# TASK EDIT
api.add_url_rule('task/edit/content/<int:id>', view_func=EditTaskContentController.as_view('EditTaskContentPage'))
api.add_url_rule('task/edit/picture/<int:id>', view_func=EditTaskPictureController.as_view('EditTaskPicturePage'))
api.add_url_rule('task/edit/answer/<int:id>', view_func=EditTaskAnswerController.as_view('EditTaskAnswerPage'))
api.add_url_rule('task/edit/tag/<int:id>', view_func=EditTaskTagController.as_view('EditTaskTagPage'))
api.add_url_rule('task/edit/rating/<int:id>', view_func=EditTaskRatingController.as_view('EditTaskRatingPage'))

