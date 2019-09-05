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
        hooks = self.config.get('hooks', None)
        if hooks is not None:
            for hook_name, hook_file in hooks.items():
                hook_path = os.path.join(self.rootdir, hook_file)
                if os.path.isfile(hook_path):
                    hook_obj = ProblemHooks(problem=self.problem, type=hook_name)
                    hook_obj.content.save('{problem}.{hook}.hook'.format(problem=self.short_name, hook=hook_name),
                            File(open(hook_path, 'rb')))


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
        
        print('sinol2', config.get('type', None) == 'sinol2')
        return config.get('type', None) == 'sinol2'

