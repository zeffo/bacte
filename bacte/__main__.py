from pathlib import Path
import litestar
import uvicorn
from litestar.template import TemplateConfig
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.logging import LoggingConfig
from bacte import api

if __name__ == "__main__":
    # workbook = openpyxl.load_workbook("./data/growth_curve_0.xlsx")
    # sheet = workbook.worksheets[0]
    # parser = Parser(sheet=sheet)
    # parser.parse()
    #
    # reading = None
    # for r in parser.readings:
    #     if r.wavelength == 600:
    #         reading = r
    # if reading:
    #     reading.plot()
    # else:
    #     print("No reading with 600nm wavelength found")
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
        logging_config=log_config
    )
    uvicorn.run("__main__:app", host="0.0.0.0", port=8000, log_level="debug")
    

