from openpyxl.cell import Cell, MergedCell

type AnyCell = Cell | MergedCell
type Row = tuple[AnyCell, ...]
