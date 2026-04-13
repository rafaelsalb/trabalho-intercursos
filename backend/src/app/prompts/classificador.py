class ClassificadorPrompts:
    @staticmethod
    def classificar(data: dict) -> str:
        activity = data.get("activity")
        business_type = data.get("businessType", "")
        work_location = data.get("workLocation", "")
        works_alone = data.get("worksAlone")
        number_of_people = data.get("numberOfPeople") or data.get(
            "numero_funcionarios", ""
        )
        fixed_expenses = data.get("fixedExpenses", "")
        issues_invoices = data.get("issuesInvoices", "")
        invoice_doubts = data.get("invoiceDoubts", "")
        has_other_company = data.get("hasOtherCompany", "")
        has_benefits_or_clt = data.get("hasBenefitsOrCLT", "")
        income = data.get("income", "")

        prompt = (
            f"Classifique a empresa com base nas seguintes informações:\n"
            f"- Atividade Principal: {activity}\n"
            f"- Tipo de Negócio: {business_type}\n"
            f"- Local de Trabalho: {work_location}\n"
            f"- Trabalha Sozinho: {works_alone}\n"
            f"- Número de Pessoas: {number_of_people}\n"
            f"- Possui Despesas Fixas: {fixed_expenses}\n"
            f"- Emite Nota Fiscal: {issues_invoices}\n"
            f"- Dúvidas sobre Nota Fiscal: {invoice_doubts}\n"
            f"- Já Possui Outra Empresa: {has_other_company}\n"
            f"- Possui Benefícios ou CLT: {has_benefits_or_clt}\n"
            f"- Renda Mensal: {income}\n\n"
            "Classifique a empresa como 'Microempresa', "
            "'Pequena Empresa', 'Média Empresa' ou 'Grande Empresa'."
        )
        return prompt
