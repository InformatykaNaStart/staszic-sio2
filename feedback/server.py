from django.conf import settings
from models import Judging
from django.utils import timezone
import SimpleXMLRPCServer

class ServerMethods(object):
    def get_judging(self, pk):
        return Judging.objects.get(pk=pk)

    def CompilationStarted(self, jid):
        judging = self.get_judging(jid)

        judging.config['compilation_status'] = 'CO'       
        judging.save()

        print 'C.ST', judging

    def CompilationFinished(self, jid, code, output):
        judging = self.get_judging(jid)
        
        judging.config['compilation_status'] = code
        judging.save()

        print 'C.FI', judging

    def JudgePrepare(self, jid, name):
        judging = self.get_judging(jid)
        pi = judging.submission.problem_instance
        test = pi.test_set.get(name=name)

        result = pi.controller.judge_prepare(judging, test, judging.config['smartjudge'])
        if result:
            judging.config['stats']['QU'] -= 1
            judging.config['stats']['DO'] += 1
            if 'NJ' not in judging.config['results']: judging.config['results']['NJ'] = 0
            judging.config['results']['NJ'] += 1
        judging.save()
        print 'J.PR', judging, name, result
        return result

    def JudgeStarted(self, jid, name):
        judging = self.get_judging(jid)
 #       print 'J.ST', judging, name
        judging.config['stats']['QU'] -= 1
        judging.config['stats']['JU'] += 1
        judging.save()

    def JudgeFinished(self, jid, name, code):
        judging = self.get_judging(jid)

        pi = judging.submission.problem_instance
        test = pi.test_set.get(name=name)
        pi.controller.judge_finished(judging, test, code, judging.config['smartjudge'])
        
        judging.config['stats']['JU'] -= 1
        judging.config['stats']['DO'] += 1
        if code not in judging.config['results']: judging.config['results'][code] = 0
        judging.config['results'][code] += 1
        judging.finish_date = timezone.now()
        judging.save()

#        print 'J.FI', judging, name, code

class Handler(SimpleXMLRPCServer.SimpleXMLRPCRequestHandler):
    def log_message(self, fmt, *args):
        pass

def serve():
    server = SimpleXMLRPCServer.SimpleXMLRPCServer(('0.0.0.0', settings.FEEDBACK_SERVER_PORT), requestHandler=Handler, allow_none=True)
    server.register_instance(ServerMethods())
    server.serve_forever()

if __name__ == '__main__':
    serve()
