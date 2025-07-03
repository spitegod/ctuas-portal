from .firstsem import parse_sheet as parse_first_sem
from .secondsem import parse_sheet as parse_second_sem
from .edu_methodwork import parse_methodical_work as parse_methodical_w
from .org_methodwork import parse_methodical_work as parse_org
from .sci_researchwork import parse_methodical_work as parse_sci
from .contractwork import parse_methodical_work as parse_contract
from .sci_methodwork import parse_methodical_work as parse_sci_method
from .published_sciworks import parse_methodical_work as parse_published
from .public_work import parse_methodical_work as parse_public
from .remarks import parse_methodical_work as parse_remarks
from .raising import parse_methodical_work as parse_raising
from .recommendation import parse_methodical_work as parse_recom

sheet_parsers = {
    "1. У.Р. Первый семестр": parse_first_sem,
    "1. У.Р. Второй семестр ": parse_second_sem,
    "2. Учебно-методическая работа": parse_methodical_w,
    "3. Организационно-методическая ": parse_org,
    "4. Научно-исследовательская раб": parse_sci,
    "5. Участие в хоздоговорной НИР": parse_contract,
    "6. Научно-методическая работа": parse_sci_method,
    "7. Перечень публикаций и трудов": parse_published,
    "8. Общественная и воспитательна": parse_public,
    "9. Замечания": parse_remarks,
    "Повышение квалификации": parse_raising,
    "Рекомендация кафедры ": parse_recom,

}