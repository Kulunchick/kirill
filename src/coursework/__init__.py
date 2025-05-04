from jinja2 import Template

from src.coursework.utils.generator import ChainGenerator

# Створення генератора з параметрами
generator = ChainGenerator(
    n=3,  # 3 ланцюги
    min_size=2,  # мінімум 2 таски в ланцюгу
    max_size=3,  # максимум 3 таски в ланцюгу
    min_t=1,     # мінімальний час виконання
    max_t=9,     # максимальний час виконання
    min_u=1,     # мінімальна вага
    max_u=5      # максимальна вага
)

# Генерація ланцюгів
# chains = generator.generate()
#
# # Створення шаблону
# with open('templates/task.html', 'r', encoding='utf-8') as file:
#     template = Template(file.read())
#
# # Рендеринг шаблону
# html = template.render(chains=chains)
#
# # Збереження результату
# with open('generated_task.html', 'w', encoding='utf-8') as file:
#     file.write(html)