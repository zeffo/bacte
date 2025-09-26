from io import BytesIO
from typing import Annotated, Any

import litestar
import openpyxl
from litestar.datastructures import UploadFile
from litestar.enums import RequestEncodingType
from litestar.params import Body
from litestar.response import Template

from bacte.parser import Parser


@litestar.get("/")
async def home() -> Template:
    return Template(template_name="index.html")


@litestar.post("/plot")
async def plot(
    data: Annotated[UploadFile, Body(media_type=RequestEncodingType.MULTI_PART)],
) -> (
    list[dict[str, dict[str, int | None] | list[dict[str, list[Any]]]]]
    | litestar.Response[dict[str, str]]
):
    content = BytesIO(await data.read())
    try:
        workbook = openpyxl.load_workbook(content)
    except OSError:
        return litestar.Response(
            {"error": "could not parse spreadsheet"}, status_code=500
        )
    sheet = Parser.find_sheet(workbook) or workbook.worksheets[0]
    parser = Parser(sheet=sheet)
    parser.parse()
    return [r.to_dict() for r in parser.readings]
