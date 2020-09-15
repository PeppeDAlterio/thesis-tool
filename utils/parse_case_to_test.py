import utils.tests as tests

def parse(caseRow=None):

    if caseRow is None:
        raise ValueError('caseRow cannot be None')

    current = caseRow['Vulnerability'].lower()
    current_hash = caseRow['Id']
    if 'sql injection' in current:
        print('SQL INJECTION CASE: ' + current_hash)
        result = tests.sqlInjectionTest(caseRow['Instance'])
        print('Test result: ' + str(result) )
        return result

    elif 'file disclosure' in current or 'hidden file' in current:
        print('FILE DISCLOSURE CASE: ' + current_hash)
        result = tests.fileDisclosureTest(caseRow['Instance'])
        print('Test result: ' + str(result) )
        return result

    elif 'ip disclosure' in current:
        print('IP DISCLOSURE CASE: ' + current_hash)
        result = tests.ipAddressDisclosureTest(caseRow['Instance'])
        print('Test result: ' + str(result) )
        return result

    else:
        return None