from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from components.test_generator.database.models import KAQuestion, KAQuestionVariant, KATest, KAVariant

class KAQuestionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = KAQuestion
        include_fk = True

class KATestSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = KATest
        include_fk = True

class KAVariantSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = KAVariant
        include_fk = True
    question_variants = Nested("KAQuestionVariantSchema", many=True)

class KAQuestionVariantSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = KAQuestionVariant
        include_fk = True
    question = Nested(KAQuestionSchema)
    variant = Nested(KAVariantSchema)