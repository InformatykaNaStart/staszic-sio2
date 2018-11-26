from models import Judging, SmartJudgeConfig
from oioioi.contests.models import Submission
from oioioi.programs.handlers import _skip_on_compilation_error

def invalidate_judgings(env):
    Judging.objects.filter(pk__in = env['judgings'].values()).update(active=False)
    return env

def create_judgings(env):
    judging_spec = {}

    submission = Submission.objects.get(pk=env['submission_id'])
    contest = submission.problem_instance.contest
    smartjudge_config = SmartJudgeConfig.objects.filter(contest=contest).first() or SmartJudgeConfig()
    mode = smartjudge_config.mode

    for report_kind in env['report_kinds']:
        config = {
                'smartjudge': dict(mode=mode),
                'compilation_status': 'QU',
                'stats': dict(QU=0, DO=0, JU=0),
                'results': dict(),
                }
        judging = Judging.objects.create(submission=submission, kind=report_kind, config=config)
        judging_spec[report_kind] = judging.pk

    env['judgings'] = judging_spec
    return env

def select(judging, kind):
    order = []
    if kind == 'EXAMPLE': order = ['INITIAL', 'FULL']
    if kind == 'NORMAL': order = ['NORMAL', 'FULL']

    for o in order:
        if o in judging: return judging[o]


@_skip_on_compilation_error
def put_judgings_into_tests(env):
    judgings = env['judgings']

    test_counts = {}

    for test in env['tests'].values():
        test['judging_id'] = select(judgings, test['kind'])
        if test['judging_id'] is None:
            del test['judging_id']
        else:
            jid = test['judging_id']
            if jid not in test_counts: test_counts[jid] = 0
            test_counts[jid] += 1

    for jid, cnt in test_counts.items():
        judging = Judging.objects.get(pk=jid)
        judging.config['stats'] = dict(QU=cnt, JU=0, DO=0)
        judging.save()

    return env

def get_stats_from_judging(results):
    if results is None: return {}
    columns = ['OK', 'WA', 'RE', 'TLE']
    result = {k:0 for k in columns}
    for k, v in sorted(results.items()):
        result[k] = v
        if k not in columns: columns.append(k)

    return [(c, result[c]) for c in columns]


