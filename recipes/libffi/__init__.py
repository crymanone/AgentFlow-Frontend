# recipes/libffi/__init__.py

from pythonforandroid.recipe import Recipe
from pythonforandroid.util import current_directory
from pythonforandroid.logger import sh
import os

class LibFFI_64Recipe(Recipe):
    version = '3.2.1'
    url = 'https://github.com/libffi/libffi/archive/v{version}.tar.gz'
    
    def build_arch(self, arch):
        env = self.get_recipe_env(arch)
        with current_directory(self.get_build_dir(arch.arch)):
            if not os.path.exists('configure'):
                sh.autoreconf('-fvi', _env=env)
            sh.configure(
                './configure',
                '--host={}'.format(arch.command_prefix),
                '--prefix={}/install'.format(os.getcwd()),
                '--enable-shared',
                _env=env
            )
            sh.make('install', _env=env)

recipe = LibFFI_64Recipe()