from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    transactions = None
    if request.method == 'POST':
        contributions = {}
        num_people = int(request.form['num_people'])
        for i in range(num_people):
            name = request.form[f'name_{i}']
            amount = float(request.form[f'amount_{i}'])
            contributions[name] = amount

        transactions = calculate_split(contributions)

    return render_template('index.html', transactions=transactions)

def calculate_balances(contributions):
    total_amount = sum(contributions.values())
    num_people = len(contributions)
    equal_share = total_amount / num_people

    balances = {}
    for person, amount in contributions.items():
        balances[person] = amount - equal_share

    return balances

def settle_debts(balances):
    debtors = []
    creditors = []

    for person, balance in balances.items():
        if balance < 0:
            debtors.append((person, balance))
        elif balance > 0:
            creditors.append((person, balance))

    debtors.sort(key=lambda x: x[1])
    creditors.sort(key=lambda x: x[1], reverse=True)

    transactions = []

    i, j = 0, 0

    while i < len(debtors) and j < len(creditors):
        debtor, debt_amount = debtors[i]
        creditor, credit_amount = creditors[j]

        amount = min(-debt_amount, credit_amount)
        transactions.append((debtor, creditor, amount))

        debtors[i] = (debtor, debt_amount + amount)
        creditors[j] = (creditor, credit_amount - amount)

        if debtors[i][1] == 0:
            i += 1
        if creditors[j][1] == 0:
            j += 1

    return transactions

def calculate_split(contributions):
    balances = calculate_balances(contributions)
    transactions = settle_debts(balances)
    return transactions

if __name__ == '__main__':
    app.run(debug=True)