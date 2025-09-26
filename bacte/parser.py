from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

from bacte.reading import Reading
from bacte.types import AnyCell, Row



def is_row_empty(row: Row):
    return not (row[0].value and str(row[0].value).strip())

def clean_row(row: Row):
    return row

class Parser:
    def __init__(self, sheet: Worksheet):
        self.sheet = sheet
        self.rows = sheet.rows
        self.title, self.subtitle, self.timestamp = self.get_metadata()
        self.readings: list[Reading] = []

    def get_metadata(self):
        rows = self.rows
        return [str(next(rows)[0].value) for _ in range(3)]

    def parse(self):
        rows = self.rows
        readings: list[tuple[list[AnyCell], list[Row]]] = []
        while rows:
            meta: list[AnyCell] = []
            grid: list[Row] = []
            try:
                while not str((row := next(rows))[0].value).lower().startswith("reading"):
                    if not is_row_empty(row):
                        meta.append(row[0])
                grid.append(clean_row(row))
                while not is_row_empty(row := next(rows)):
                    grid.append(clean_row(row))
            except StopIteration:
                break
            readings.append((meta, grid))
        for reading in readings:
            r = Reading(meta=reading[0], data=reading[1])
            self.readings.append(r)


    @staticmethod
    def find_sheet(workbook: Workbook) -> Worksheet | None:
        for sheet in workbook.worksheets:
            if sheet.title.lower().strip().startswith("absorbance"):
                return sheet





