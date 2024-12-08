from peewee import TextField, SQL, BooleanField

from calibre_db import BaseModel


class CustomColumns(BaseModel):
    datatype = TextField()
    display = TextField(constraints=[SQL("DEFAULT '{}'")])
    editable = BooleanField(constraints=[SQL("DEFAULT 1")])
    is_multiple = BooleanField(constraints=[SQL("DEFAULT 0")])
    label = TextField(unique=True)
    mark_for_delete = BooleanField(constraints=[SQL("DEFAULT 0")])
    name = TextField()
    normalized = BooleanField()

    class Meta:
        table_name = 'custom_columns'

    def __str__(self):
        return " ,".join(map(str, self.to_list()))

    def to_list(self):
        return [self.label, self.name, self.datatype, self.mark_for_delete, self.editable, self.display,
                self.is_multiple, self.normalized]

    def to_dict(self):
        escaped = str(self.display).translate(str.maketrans({"-": r"\-",
                                                    "]": r"\]",
                                                    "\\": r"\\",
                                                    "^": r"\^",
                                                    "$": r"\$",
                                                    "*": r"\*",
                                                    ".": r"\."}))
        return {'label': self.label, 'name': self.name, 'datatype': self.datatype,
                'mark_for_delete': self.mark_for_delete, 'editable': self.editable,
                'display': "escaped",
                'is_multiple': self.is_multiple,
                'normalized': self.normalized}

    @staticmethod
    def header():
        return ["Label", "Name", "Datatype", "del", "edit", "display", "mult", "norm"]

    @staticmethod
    def columns():
        tick_formatter = {'formatter': "tickCross",
                          'hozAlign': "center",
                          'formatterParams': {
                              'allowEmpty': True,
                              'allowTruthy': True,
                              'tickElement': "<i class='fa fa-check'></i>",
                              'crossElement': "<i class='fa fa-times'></i>",
                          }}
        return [
            {'title': 'Label', 'field': 'label', 'width': 200, 'responsive': 0},
            {'title': 'Name', 'field': 'name', 'width': 200, 'responsive': 0},
            {'title': 'Data Type', 'field': 'datatype', 'width': 200, 'responsive': 0},
            {'title': 'Mark for delete', 'field': 'mark_for_delete', 'responsive': 0, **tick_formatter},
            {'title': 'display', 'field': 'display', 'width': 200, 'responsive': 0},
            {'title': 'is multiple', 'field': 'is_multiple', 'responsive': 0, **tick_formatter},
            {'title': 'normalized', 'field': 'normalized', 'responsive': 0, **tick_formatter}
        ]

    @staticmethod
    def cols_width():
        return [20, 20, 10, 5, 5, 40, 5, 5]

