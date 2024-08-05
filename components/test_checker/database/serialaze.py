from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from components.test_checker.database.models import KaAnswer, KaAnswerLog

class KaAnswerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = KaAnswer
        include_fk = True

class KaAnswerLogSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = KaAnswerLog
        include_fk = True
    answer = Nested(KaAnswerSchema)