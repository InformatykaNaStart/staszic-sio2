from oioioi.programs.controllers import ProgrammingProblemController

class PolygonProblemController(ProgrammingProblemController):
    description = 'Zadanie zaimportowane z systemu Polygon'

    def fill_evaluation_environ(self, environ, submission, **kwargs):
        super(PolygonProblemController, self).fill_evaluation_environ(environ, submission, **kwargs)
        environ['checker_mode'] = 'testlib'

