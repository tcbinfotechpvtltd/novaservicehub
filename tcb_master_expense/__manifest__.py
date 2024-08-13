{
    'name': 'Expense Master',
    'version': '1.0',
    'summary': 'Summery',
    'description': 'Description',
    'sequence': '-1000000',
    'category': 'Category',
    'author': 'TCB',
    'depends': ['hr_expense', 'sales_inherit'],
    'data': [
        'security/ir.model.access.csv',
        'views/expense_master_view.xml'
    ]
}
