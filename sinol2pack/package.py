import os
from oioioi.sinolpack.package import SinolPackageBackend, SinolPackage
from oioioi.base.utils.archive import Archive
import tarfile
import yaml
from django.core.files import File
from models import ProblemHooks

class Sinol2Package(SinolPackage):
    package_backend_name = 'staszic.sinol2pack.package.Sinol2PackageBackend'
    controller_name = 'staszic.sinol2pack.controllers.Sinol2ProblemController'

    def _process_package(self):
        super(Sinol2Package, self)._process_package()
        self._save_hooks()

    def _save_hooks(self):
        hooks_file = self.config.get('hooks_file', None)
        if hooks_file is not None:
            hooks_path = os.path.join(self.rootdir, hooks_file)
            if os.path.isfile(hooks_path):
                hooks_obj = ProblemHooks(problem=self.problem)
                hooks_obj.content.save(self.short_name + '.hooks.py',
                        File(open(hooks_path, 'rb')))


class Sinol2PackageBackend(SinolPackageBackend):
    description = 'Packa Sinolowa z dodatkiem sosu czosnkowego'
    package_class = Sinol2Package

    def identify(self, path, original_filename=None):
        if not tarfile.is_tarfile(path):
            return False

        tar = tarfile.open(path)
        
        files = [name for name in tar.getnames() if name.endswith('/config.yml')]

        if len(files) != 1:
            return False

        the_file, = files

        f = tar.extractfile(the_file)
        config = yaml.load(f.read())
        f.close()

        return config.get('type', None) == 'sinol2'

