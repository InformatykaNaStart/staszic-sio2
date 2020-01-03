from utils import make_polygon_request, make_polygon_plain_request
from oioioi.problems.models import Problem, ProblemSite
from django.core.files import File
from django.core.files.base import ContentFile
from oioioi.base.utils import generate_key
from oioioi.programs.models import Test, ModelSolution
import tempfile
import os
import shutil
import subprocess

STANDARD_CHECKERS = ('fcmp.cpp', 'hcmp.cpp', 'ncmp.cpp', 'rcmp4.cpp', 'rcmp6.cpp', 'rcmp9.cpp', 'wcmp.cpp', 'yesno.cpp', ) 

def get_file_path(name):
    return os.path.join(os.path.dirname(__file__), 'files', name)

def generate_output(problem_id, testset, test_index):
    return make_polygon_plain_request('problem.testAnswer', problemId=problem_id, testset=testset, testIndex=test_index)

def generate_input(problem_id, testset, test_index):
    return make_polygon_plain_request('problem.testInput', problemId=problem_id, testset=testset, testIndex=test_index)

def build_statement(statement, memory, contest_name, statement_date, samples):
    directory = tempfile.mkdtemp()
    shutil.copy(get_file_path('text/sinol.cls'), directory)
    shutil.copy(get_file_path('text/logo.pdf'), directory)

    example_str = ''
    for id, sample in enumerate(samples):
        with open(os.path.join(directory, '{}.in'.format(id)), 'w') as f:
            f.write(sample['input'].replace('\r\n', '\n'))
        with open(os.path.join(directory, '{}.out'.format(id)), 'w') as f:
            f.write(sample['output'].replace('\r\n', '\n'))
        example_str += '\\makeexample{%d}\n' % (id, )

    with open(os.path.join(directory, 'text.tex'), 'w') as tex_out, open(get_file_path('text/text.tex')) as tex_in:
        template = tex_in.read().decode('utf-8')
        tex_out.write((template % dict(
                TITLE = statement['name'],
                DATE = statement_date,
                CONTEST = contest_name,
                MEMORY = memory,
                LEGEND = statement['legend'],
                INPUT = statement['input'],
                OUTPUT = statement['output'],
                EXAMPLE = example_str
            )).encode('utf-8'))

    try:
        subprocess.check_output(['pdflatex', '-interaction=batchmode', 'text.tex'], shell=False, cwd = directory)
        subprocess.check_output(['pdflatex', '-interaction=batchmode', 'text.tex'], shell=False, cwd = directory)
    except subprocess.CalledProcessError as e:
        raise RuntimeError('Something got wrong while creating pdf statement:\n{}'.format(e.output))

    return os.path.join(directory, 'text.pdf')

def build_checker(checker_info, checker_text, extra_files):
    if not checker_info['sourceType'].startswith('cpp'):
        raise RuntimeError("Don't know how to compile checker type %s" % checker_info['sourceType'])

    directory = tempfile.mkdtemp()
    for name, content in [('checker.cpp', checker_text)] + extra_files:
        with open(os.path.join(directory, name), 'w') as f:
            f.write(content.encode('utf-8'))

    try:
        subprocess.check_output(['g++', '-static', '-O2', 'checker.cpp', '-o', 'checker.exe'], shell=False, cwd=directory, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        raise RuntimeError('Something got wrong while compiling checker:\n{}'.format(e.output))

    return os.path.join(directory, 'checker.exe')

def import_problem(problem_id, contest_name, statement_date, state_reporter):
    problem_info = get_problem_info(problem_id)

    if problem_info is None:
        raise RuntimeError('Problem with id {} does not exist or "staszic-sio2" user has no permissions to WRITE to it')

    if problem_info['accessType'] not in ('WRITE', 'OWNER'):
        raise RuntimeError('"staszic-sio2" user has no permissions to WRITE to problem {}'.format(problem_id))

    problem_conf = make_polygon_request('problem.info', problemId=problem_id)
    statements = make_polygon_request('problem.statements', problemId=problem_id)

    if len(statements.keys()) != 1:
        raise RuntimeError("The problem has no statements or has more than one. I don't know what to do. I give up.")

    statement, = statements.values()
    print('statement', statement)

    state_reporter('ST')
    tests = make_polygon_request('problem.tests', problemId=problem_id, testset='tests')
    statement_tests = []

    for test in tests:
        if test['useInStatements']:
            test_desc = dict()
            if 'inputForStatements' in test:
                test_desc['input'] = test['inputForStatements']
            elif test['manual']:
                test_desc['input'] = test['input']
            else:
                test_desc['input'] = generate_input(problem_id, 'tests', test['index'])
            if 'outputForStatements' in test:
                test_desc['output'] = test['outputForStatements']
            else:
                test_desc['output'] = generate_output(problem_id, 'tests', test['index'])
            statement_tests.append(test_desc)

    statement_pdf = build_statement(statement, problem_conf['memoryLimit'], contest_name, statement_date, statement_tests)

    state_reporter('CH')
    files = make_polygon_request('problem.files', problemId=problem_id)
    sources = files['sourceFiles']
    resources = files['resourceFiles']
    
    checker_name = make_polygon_request('problem.checker', problemId=problem_id)
    
    extra_files = []
    for res in resources:
        if res['name'].endswith('.h'):
            extra_files.append((res['name'], make_polygon_plain_request('problem.viewFile', problemId=problem_id, type='resource', name=res['name'])))

    checker_info = None
    if checker_name.startswith('std::'):
        checker_name = checker_name[5:]
        if checker_name not in STANDARD_CHECKERS: raise RuntimeError('%s is not a standard checker' % (checker_name, ))
        with open(get_file_path('checkers/{}'.format(checker_name))) as f:
            checker_text = f.read()
        checker_info = dict(sourceType = 'cpp')
    else:
        for file in sources:
            if file['name'] == checker_name:
                checker_info = file
                break
        if checker_info is None: raise RuntimeError('Did not found checker info')
        checker_text = make_polygon_plain_request('problem.viewFile', problemId=problem_id, type='source', name=checker_name)

    checker_exe = build_checker(checker_info, checker_text, extra_files)

    problem = Problem.create(
            name = statement['name'],
            short_name = problem_info['name'],
            controller_name = 'staszic.polygon.controllers.PolygonProblemController',
            contest = None,
            is_public = False,
            author = None
        )
 
    ProblemSite.objects.create(problem=problem, url_key=generate_key())
    checker_obj = problem.outputchecker
    with open(checker_exe, 'rb') as f:
        checker_obj.exe_file = File(f)
    checker_obj.save()

    with open(statement_pdf, 'rb') as pdf_file:
        problem.statements.create(content=File(pdf_file))

    state_reporter('TE')
    for test in tests:
        if test['manual']:
            input = test['input']
        else:
            input = generate_input(problem_id, 'tests', test['index'])
        test_obj = Test.objects.create(
            problem_instance = problem.main_problem_instance,
            name = test['index'],
            kind = 'EXAMPLE' if test['useInStatements'] else 'NORMAL',
            time_limit = 2 * problem_conf['timeLimit'],
            memory_limit = 1024 * problem_conf['memoryLimit'],
            max_score = 1,
            order = test['index'],
            is_active = True)
        test_obj.input_file.save('%d.in' % (test['index'], ), ContentFile(input))
        test_obj.output_file.save('%d.out' % (test['index'], ), ContentFile(generate_output(problem_id, 'tests', test['index'])))

    state_reporter('SO')
    solutions = make_polygon_request('problem.solutions', problemId = problem_id)
    model_solutions = []

    for solution in solutions:
        obj = dict(
            name = solution['name'],
            order = 0 if solution['tag'] == 'MA' else 1,
            text = make_polygon_plain_request('problem.viewSolution', problemId = problem_id, name = solution['name']),
            kind = 'NORMAL' if solution['tag'] == 'MA' else 'WRONG'
            )

        model_solutions.append(obj)

    model_solutions.sort(key=lambda x: x['order'])

    for i, solution in enumerate(model_solutions):
        solution_obj = ModelSolution(problem=problem, name=solution['name'], order_key=i, kind=solution['kind'])
        solution_obj.source_file.save(solution['name'], ContentFile(solution['text']))

    return problem

def get_problem_info(problem_id):
    problems = make_polygon_request('problems.list')

    problem_info = None

    for problem in problems:
        if problem['id'] == problem_id:
            problem_info = problem
            break
    return problem_info

def check_import_problem(problem_info):
    if problem_info is None: return False
    return problem_info['accessType'] in ('WRITE', 'OWNER')
