from oioioi.base.utils import RegisteredSubclassesBase, ObjectWithMixins

class ProgrammingLanguageBase(RegisteredSubclassesBase, ObjectWithMixins):
    modules_with_subclasses = ['languages']
    abstract = True
    extensions = []

class CppProgrammingLanguage(ProgrammingLanguageBase):
    description = 'C++'
    extensions = ['cpp', 'cc']

class CProgrammingLanguage(ProgrammingLanguageBase):
    description = 'C'
    extensions = ['c']

class PascalProgrammingLanguage(ProgrammingLanguageBase):
    description = 'Pascal'
    extensions = ['pas', 'p']

class PythonProgrammingLanguage(ProgrammingLanguageBase):
    description = 'Python'
    extensions = ['py']

class HaskellProgrammingLanguage(ProgrammingLanguageBase):
    description = 'Haskell'
    extensions = ['hs']
