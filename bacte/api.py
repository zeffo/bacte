from io import BytesIO
from typing import Annotated, Any

import litestar
from litestar.response import Template
import openpyxl
from litestar.datastructures import UploadFile
from litestar.enums import RequestEncodingType
from litestar.params import Body

from bacte.parser import Parser


@litestar.get("/")
async def home() -> Template:
    return Template(template_name="index.html")
    

@litestar.post("/plot")
async def plot(
    data: Annotated[UploadFile, Body(media_type=RequestEncodingType.MULTI_PART)],
) -> list[dict[str, dict[str, int | None] | list[dict[str, list[Any]]]]]:
    content = BytesIO(await data.read())
    workbook = openpyxl.load_workbook(content)
    sheet = workbook.worksheets[0]
    parser = Parser(sheet=sheet)
    parser.parse()
    return [
        r.to_dict() for r in parser.readings
    ]

