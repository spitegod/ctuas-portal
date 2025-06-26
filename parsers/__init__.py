from .firstsem import parse_sheet as parse_first_sem
from .secondsem import parse_sheet as parse_second_sem

sheet_parsers = {
    "1. У.Р. Первый семестр": parse_first_sem,
    "1. У.Р. Второй семестр ": parse_second_sem,
}