from flask import render_template, redirect, request
from flask_login import login_required, current_user
from flask.views import MethodView
from web.api.models.task import Task
from web import db, app, ALLOWED_EXTENSIONS
from web.api.forms.EditTaskInfoForms import EditTaskContentForm, EditTaskTagForm
from web.api.forms.PhotoForm import PhotoForm
import os
import random
from werkzeug.utils import secure_filename
from web.api.models.answer import Answer


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class EditTaskContentController(MethodView):
    @login_required
    def get(self, id):
        if current_user.role != 'admin':
            return redirect('/error/rights')

        task = db.session.query(Task).filter(Task.id == id).first()
        form = EditTaskContentForm()
        return render_template('editing/editTaskContent.html', task=task, form=form)

    @login_required
    def post(self, id):
        if current_user.role != 'admin':
            return redirect('/error/rights')

        task = db.session.query(Task).filter(Task.id == id).first()
        form = EditTaskContentForm()
        if form.validate_on_submit():
            Task.update_by_id(task.id, 'content', form.content.data)
            return render_template('editing/editTaskContent.html', task=task, form=form,
                                   success_text='Условие успешно изменено!')
        return render_template('editind/editTaskContent.html', task=task, form=form)


class EditTaskPictureController(MethodView):
    @login_required
    def get(self, id):
        if current_user.role != 'admin':
            return redirect('/error/rights')

        task = db.session.query(Task).filter(Task.id == id).first()
        form = PhotoForm()
        return render_template('editing/editTaskPicture.html', task=task, form=form)

    @login_required
    def post(self, id):
        if current_user.role != 'admin':
            return redirect('/error/rights')

        task = db.session.query(Task).filter(Task.id == id).first()
        form = PhotoForm()
        if form.submit_photo.data and form.validate_on_submit():
            file = request.files['file']
            if file and allowed_file(file.filename):
                code = ''.join([random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')) for x in range(8)])
                filename = code + current_user.code + secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                path_to_deleting_file = 'web/static/photos/uploads/' + str(task.picture)
                os.remove(path_to_deleting_file)
                Task.update_by_id(task.id, 'picture', filename)
                return render_template('editing/editTaskPicture.html', task=task, form=form,
                                       success_text='Картинка успешно изменена!')
            return render_template('editing/editTaskPicture.html', form=form,
                                   error_text='Что-то пошло не так. Попробуйте еще раз.')
        return render_template('editing/editTaskPicture.html', task=task, form=form)


class EditTaskAnswerController(MethodView):
    @login_required
    def get(self, id):
        if current_user.role != 'admin':
            return redirect('/error/rights')

        task = db.session.query(Task).filter(Task.id == id).first()
        answers = Answer.get_all_answers_from_task(id)

        oneAnswer = False
        fourAnswer = False

        if len(answers) == 1:
            oneAnswer = True
        elif len(answers) == 4:
            fourAnswer = True

        return render_template('editing/editTaskAnswer.html', task=task, oneAnswer=oneAnswer, fourAnswer=fourAnswer,
                               answers=answers)

    @login_required
    def post(self, id):
        if current_user.role != 'admin':
            return redirect('/error/rights')

        task = db.session.query(Task).filter(Task.id == id).first()
        answers = Answer.get_all_answers_from_task(id)

        fourAnswer = False

        if len(answers) == 4:
            fourAnswer = True

        if 'submit-itog-answer' in request.form:
            newanswer = request.form['new-itog-answer']
            if newanswer == '':
                return render_template('editing/editTaskAnswer.html', task=task, answers=answers, fourAnswer=fourAnswer,
                                       error_text='Ответ не может быть пустым!')
            if fourAnswer:
                for i in range(4):
                    if answers[i].content == newanswer:
                        return render_template('editing/editTaskAnswer.html', task=task, answers=answers,
                                               fourAnswer=fourAnswer, error_text=
                                               'Новый правильный ответ не может совпадать с вариантом ответа!')
                Answer.update_by_id(answers[0].id, 'content', newanswer)
            Task.update_by_id(task.id, 'answer', newanswer)
            return render_template('editing/editTaskAnswer.html', task=task, answers=answers, fourAnswer=fourAnswer,
                                   success_text='Ответ успешно изменен!')
        return render_template('editing/editTaskAnswer.html', task=task, answers=answers, fourAnswer=fourAnswer)


class EditTaskTagController(MethodView):
    @login_required
    def get(self, id):
        if current_user.role != 'admin':
            return redirect('/error/rights')

        form = EditTaskTagForm()
        task = db.session.query(Task).filter(Task.id == id).first()
        return render_template('editing/editTaskTag.html', task=task, form=form)

    @login_required
    def post(self, id):
        if current_user.role != 'admin':
            return redirect('/error/rights')

        task = db.session.query(Task).filter(Task.id == id).first()
        form = EditTaskTagForm()
        if form.validate_on_submit():
            Task.update_by_id(task.id, 'tag', form.tag.data)
            return render_template('editing/editTaskTag.html', task=task, form=form,
                                   success_text='Тег успешно изменен!')
        return render_template('editing/editTaskTag.html', task=task, form=form)


class EditTaskRatingController(MethodView):
    @login_required
    def get(self, id):
        if current_user.role != 'admin':
            return redirect('/error/rights')

        task = db.session.query(Task).filter(Task.id == id).first()
        return render_template('editing/editTaskRating.html', task=task)

    @login_required
    def post(self, id):
        if current_user.role != 'admin':
            return redirect('/error/rights')

        task = db.session.query(Task).filter(Task.id == id).first()
        if 'submit-new-rating' in request.form:
            newrating = request.form['select-rating']
            Task.update_by_id(task.id, 'rating', newrating)
            return render_template('editing/editTaskRating.html', task=task, success_text='Сложность успешно изменена!')
        return render_template('editing/editTaskRating.html', task=task)
