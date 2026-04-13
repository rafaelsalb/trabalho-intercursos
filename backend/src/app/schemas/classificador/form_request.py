from marshmallow import Schema, fields


class ClassificadorFormRequestSchema(Schema):
    activity = fields.Str(required=True)
    businessType = fields.Str(required=True)
    workLocation = fields.Str(required=True)
    worksAlone = fields.Str(required=True)
    numberOfPeople = fields.Str(required=False)
    fixedExpenses = fields.Str(required=True)
    issuesInvoices = fields.Str(required=True)
    invoiceDoubts = fields.Str(required=False)
    hasOtherCompany = fields.Str(required=True)
    hasBenefitsOrCLT = fields.Str(required=True)
    income = fields.Str(required=True)
