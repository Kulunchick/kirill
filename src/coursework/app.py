"""Основний файл - запускає веб-сервер"""
import json
from string import ascii_uppercase

from flask import Flask, render_template, request, make_response

from src.coursework.models.chain import Chain
from src.coursework.models.solution import Solution
from src.coursework.models.task import Task
from src.coursework.utils.generator import ChainGenerator
from src.coursework.utils.solver import Solver, MetricType, NonUniqueRatioError

app = Flask(__name__)


@app.route("/handle_post", methods=["POST"])
def handle_delayed_post_request():
    # Отримуємо дані з форми
    form_data = request.form

    # Конвертуємо параметри в правильні типи
    params = {
        'n': int(form_data['n']),
        'size_min': int(form_data['size_min']),
        'size_max': int(form_data['size_max']),
        't_min': int(form_data['t_min']),
        't_max': int(form_data['t_max']),
        'u_min': int(form_data['u_min']),
        'u_max': int(form_data['u_max']),
        'tests_amount': int(form_data['tests_amount']),
        'test_name': form_data['test_name']
    }

    # Параметри розв'язку
    reverse = False
    average = form_data['calculation_type'] == 'average'
    metric_type = MetricType.COMPLETION_TIME

    # Генеруємо ланцюги
    generator = ChainGenerator(
        params['n'],
        params['size_min'],
        params['size_max'],
        params['t_min'],
        params['t_max'],
        params['u_min'],
        params['u_max']
    )
    all_solutions = []

    for _ in range(params['tests_amount']):
        while True:
            try:
                chains = generator.generate()
                distribution1, criterion1 = Solver.solve_with_chains(
                    chains=chains,
                    reverse=reverse,
                    metric_type=metric_type,
                    average=average
                )

                distribution2, criterion2 = Solver.solve_with_tasks(
                    chains=chains,
                    reverse=reverse,
                    metric_type=metric_type,
                    average=average
                )

                solution = Solution(
                    distribution1=distribution1,
                    distribution2=distribution2,
                    criterion1=criterion1,
                    criterion2=criterion2
                )

                all_solutions.append({
                    'chains': chains,
                    'solution': solution
                })
                break
            except NonUniqueRatioError:
                continue

    combined_html = ""

    for i, task_data in enumerate(all_solutions, 1):
        task_html = render_template(
            'task.html',
            chains=task_data['chains'],
            solution=task_data['solution'],
            is_maximum=reverse,
            is_average=average
        )
        combined_html += f'<div class="task"><h2>Задача {i}</h2>{task_html}</div>'

    response = make_response(combined_html)
    response.headers['Content-Type'] = 'text/html'
    response.headers['Content-Disposition'] = 'attachment; filename=generated_tasks.html'

    return response


@app.route("/solve-single")
def solve_single():
    return render_template("single_task.html", title="Розв'язати задачу")


@app.route("/handle-single-task", methods=["POST"])
def handle_single_task():
    form_data = request.form
    chains_str = form_data['chains']

    chains_data = json.loads(chains_str.replace("'", '"'))

    chains = []
    for i, chain_data in enumerate(chains_data):
        tasks = []
        for j, (t, u) in enumerate(zip(chain_data['t'], chain_data['u'])):
            tasks.append(Task(i=j+1, t=t, u=u))
        chains.append(Chain(letter=ascii_uppercase[i], tasks=tasks))

    reverse = False
    average = form_data['calculation_type'] == 'average'
    metric_type = MetricType.COMPLETION_TIME

    try:
        distribution1, criterion1 = Solver.solve_with_chains(
            chains=chains,
            reverse=reverse,
            metric_type=metric_type,
            average=average
        )

        distribution2, criterion2 = Solver.solve_with_tasks(
            chains=chains,
            reverse=reverse,
            metric_type=metric_type,
            average=average
        )

        solution = Solution(
            distribution1=distribution1,
            distribution2=distribution2,
            criterion1=criterion1,
            criterion2=criterion2
        )

        task_html = render_template(
            'single_task_solution.html',
            chains=chains,
            solution=solution,
            is_maximum=reverse,
            is_average=average
        )
        return render_template('solution_page.html', task_html=task_html, title="Розв'язок задачі")

    except NonUniqueRatioError:
        return "Помилка: Неунікальні співвідношення. Спробуйте інші дані."


@app.route("/")
def index():
    return render_template("generator.html", title="Головна сторінка")


@app.errorhandler(500)
def app_internal_server_error(error):
    return (render_template("app_error.html", error_message=error.original_exception, title="Помилка"), 500)


@app.errorhandler(404)
def app_page_not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
