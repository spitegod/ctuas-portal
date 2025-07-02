from .firstsem import parse_sheet as parse_first_sem
from .secondsem import parse_sheet as parse_second_sem
from .edu_methodwork import parse_methodical_work as parse_methodical_w
from .org_methodwork import parse_methodical_work as parse_org
from .sci_researchwork import parse_methodical_work as parse_org

sheet_parsers = {
    #"1. У.Р. Первый семестр": parse_first_sem,
    #"1. У.Р. Второй семестр ": parse_second_sem,
    #"2. Учебно-методическая работа": parse_methodical_w,
    #"3. Организационно-методическая ": parse_org,
    "4. Научно-исследовательская раб": parse_org

}