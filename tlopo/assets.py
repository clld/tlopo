from pathlib import Path

from clld.web.assets import environment

import tlopo


environment.append_path(
    Path(tlopo.__file__).parent.joinpath('static').as_posix(),
    url='/tlopo:static/')
environment.load_path = list(reversed(environment.load_path))
