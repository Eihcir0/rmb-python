import uuid
from django.db import models
from lcvista.models import AuditableModel
from simple_history.models import HistoricalRecords


class RobotMonkeyButler(AuditableModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    history = HistoricalRecords()

    # Other field type examples:
    # CHOICE1 = 'choice1'
    # CHOICE2 = 'choice2'
    # CHOICES = [CHOICE1, CHOICE2]
    # my_choice_field = models.CharField(
    #     max_length=40,
    #     choices=CHOICES,
    #     default='',
    # )
    # from django.contrib.postgres.fields import JSONField (goes on top level)
    # json_field = JSONField()
    # fk_field = models.ForeignKey(MyModel, null=True, on_delete=models.SET_NULL, related_name='robot_monkey_butler')
    # datetime_field = models.DateTimeField(null=True)
    # int_field = models.IntegerField(default=1, unique=True, editable=False)
    # text_field = models.TextField(blank=True)
