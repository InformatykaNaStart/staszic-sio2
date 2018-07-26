import django
django.setup()

from polygon_import import import_problem

print import_problem(28241, 'Konkurs testowy', 'TU JE DATA')
