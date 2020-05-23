from tortoise.models import Model
from tortoise import fields


class Tournament(Model):
    id = fields.IntField(pk=True, description="id")
    name = fields.CharField(max_length=64, null=False, unique=True, description="名称")
    description = fields.TextField(null=True, description="描述")
    created_at = fields.DatetimeField(auto_now=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now_add=True, description="修改时间")

    class Meta:
        # Set this to configure a manual table name, instead of a generated one
        table = "tournament"
        # Set this to generate a comment message for the table being created for the current model
        table_description = "Tournament"
        # indexes=(("field_a", "field_b"), ("field_c", "field_d", "field_e")
        # unique_together=(("field_a", "field_b"), ("field_c", "field_d", "field_e"))
        # ordering = ["name", "-score"]

    def __str__(self):
        return self.name


class Event(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    # References to other models are defined in format
    # "{app_name}.{model_name}" - where {app_name} is defined in tortoise config
    tournament = fields.ForeignKeyField("models.Tournament", related_name='events')
    participants = fields.ManyToManyField("models.Team", related_name='events', through='event_team')
    prize = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_at = fields.DatetimeField(auto_now=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now_add=True, description="修改时间")

    class Meta:
        table = "event"
        table_description = "Event"

    def __str__(self):
        return self.name


class Team(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now=True, description="创建时间")
    updated_at = fields.DatetimeField(auto_now_add=True, description="修改时间")
    # new add raise error after you have execute Tortoise.init
    # you should use
    # description = fields.TextField(null=True, description="描述")

    class Meta:
        table = "team"
        table_description = "Team"

    def __str__(self):
        return self.name
