# generator for local test_files
# run on Turris router, copy result to ``test_data``

from svupdater.lists import pkglists
from svupdater.packages import Status

from compress_pickle import dump

dump(pkglists(), "pkglist.gz")
status = [name for name, pkg in Status().items() if pkg.is_installed()]
dump(status, "status.gz")
