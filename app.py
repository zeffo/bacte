from pathlib import Path
import litestar
from litestar.template import TemplateConfig
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.logging import LoggingConfig
from bacte import api

log_config = LoggingConfig(
    root={"level": "DEBUG"},
    log_exceptions="always"
)
app = litestar.Litestar(
    route_handlers=[
        api.home,
        api.plot
    ],
    template_config=TemplateConfig(
        directory=Path("templates"),
        engine=JinjaTemplateEngine
    ),
) 
