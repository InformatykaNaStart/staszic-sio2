from oioioi.contests.scores import IntegerScore

def test_key(name):
    if name.endswith('ocen'):
        name = name[:-4]
    if name[-1] not in '0123456789':
        return (int(name[:-1]), name[-1])
    return (int(name), '')

def binary_score_aggregator(group_results):
    if not group_results:
        return (None, None, 'OK')
    else:
        submission_result = 'OK'
        for group_name, result in sorted(group_results.items(), key=lambda x: test_key(x[0])):
            if result['status'] != 'OK' and submission_result == 'OK':
                submission_result = result['status']

        return (IntegerScore(1 if submission_result == 'OK' else 0), IntegerScore(1), submission_result)

def binary_group_scorer(test_results):
    if not test_results:
        return (None, None, 'OK')
    else:
        group_result = 'OK'
        for test_name, result in sorted(test_results.items(), key=lambda x: int(x[1]['order'])):
            if result['status'] != 'OK' and group_result == 'OK':
                group_result = '{}@{}'.format(result['status'], test_name)

        return (IntegerScore(1 if group_result == 'OK' else 0), IntegerScore(1), group_result)
