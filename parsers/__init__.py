from .firstsem import parse_sheet as parse_first_sem
from .secondsem import parse_sheet as parse_second_sem
from .edu_methodwork import parse_methodical_work as parse_methodical_w
from .org_methodwork import parse_methodical_work as parse_org
from .sci_researchwork import parse_methodical_work as parse_org
from .contractwork import parse_methodical_work as parse_orgs
from .sci_methodwork import parse_methodical_work as parse_orgz
from .published_sciworks import parse_methodical_work as parse_p
from .public_work import parse_methodical_work as parse_pub
from .remarks import parse_methodical_work as parse_r

sheet_parsers = {
    #"1. У.Р. Первый семестр": parse_first_sem,
    #"1. У.Р. Второй семестр ": parse_second_sem,
    #"2. Учебно-методическая работа": parse_methodical_w,
    #"3. Организационно-методическая ": parse_org,
    #"4. Научно-исследовательская раб": parse_org,
    #"5. Участие в хоздоговорной НИР": parse_orgs,
    #"6. Научно-методическая работа": parse_orgz,
    #"7. Перечень публикаций и трудов": parse_p,
    #"8. Общественная и воспитательна": parse_pub,
    "9. Замечания": parse_r

}