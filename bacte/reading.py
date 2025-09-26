import polars as pl

from bacte.types import AnyCell, Row


def get_row_values(row: Row):
    return [c.value for c in row]


class Reading:
    def __init__(self, meta: list[AnyCell], data: list[Row]):
        self.meta = meta
        self._data = data

        schema = list(map(str, get_row_values(data[0])))
        values = [get_row_values(row) for row in data[1:]]
        self.data = pl.DataFrame(data=values, schema=schema, orient="row")

        self.wavelength = self.plate = self.absorbance = self.sample_group = None
        for item in self.meta:
            value = str(item.value).lower().strip().replace(":", "").split()
            match value:
                case ["absorbance", absorbance]:
                    self.absorbance = int(absorbance)
                case ["wavelength", wavelength, "nm"]:
                    self.wavelength = int(wavelength)
                case ["sample", "group", "group", sample_group]:
                    self.sample_group = int(sample_group)
                case ["plate", plate]:
                    self.plate = int(plate)
                case _:
                    continue

    def __str__(self):
        return (
            f"{self.absorbance},  {self.wavelength}, {self.plate}, {self.sample_group}"
        )

    def to_dict(self):
        return {
            "metadata": {
                "wavelength": self.wavelength,
                "absorbance": self.absorbance,
                "plate": self.plate,
                "sample_group": self.sample_group
            },
            "data": self.data.to_dicts()
        }
