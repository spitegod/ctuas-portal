from main.models import SecondSem

def float_or_zero(val):
    try:
        return float(val)
    except (TypeError, ValueError):
        return 0.0

def parse_sheet(sheet):
    for i, row in enumerate(sheet.iter_rows(min_row=3, values_only=True), start=3):
        if not row[0] or not isinstance(row[0], str) or row[0].strip() == "":
            continue

        if sum(1 for cell in row if cell not in (None, "", 0)) < 3:
            continue

        total_plan = sum(filter(None, [
            float_or_zero(row[4]), float_or_zero(row[5]), float_or_zero(row[6]),
            float_or_zero(row[7]), float_or_zero(row[8]), float_or_zero(row[9]),
            float_or_zero(row[10]), float_or_zero(row[11]), float_or_zero(row[12]),
            float_or_zero(row[13]), float_or_zero(row[14]), float_or_zero(row[15]),
            float_or_zero(row[16]), float_or_zero(row[17]), float_or_zero(row[18]),
            float_or_zero(row[19])
        ]))

        SecondSem.objects.create(
            discipline=row[0],
            course=row[1],
            group_count=row[2],
            student_count=row[3],
            lectures=float_or_zero(row[4]),
            practicals=float_or_zero(row[5]),
            labs=float_or_zero(row[6]),
            project_work=float_or_zero(row[7]),
            consultations=float_or_zero(row[8]),
            tests=float_or_zero(row[9]),
            exams=float_or_zero(row[10]),
            review_distance=float_or_zero(row[11]),
            practice_supervision=float_or_zero(row[12]),
            visit_control=float_or_zero(row[13]),
            qualification_supervision=float_or_zero(row[14]),
            committee_work=float_or_zero(row[15]),
            exam_commission=float_or_zero(row[16]),
            phd_supervision=float_or_zero(row[17]),
            org_srs=float_or_zero(row[18]),
            rating=float_or_zero(row[19]),
            total_plan=round(total_plan, 1),
            total_actual=float_or_zero(row[21])
        )

        print(f"[{i}] {row[0]} — добавлено")
