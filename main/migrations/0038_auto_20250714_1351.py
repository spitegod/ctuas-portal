from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    

    dependencies = [
    ("main", "0037_auto_20250714_1345"),
]

    operations = [
        migrations.AddField(
            model_name='publicwork',
            name='teacher',
            field=models.ForeignKey(
                to='main.teacher',
                on_delete=django.db.models.deletion.CASCADE,
                related_name='public_works',
                default=1,
            ),
            preserve_default=False,
        ),
    ]