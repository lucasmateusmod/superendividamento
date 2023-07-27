from flask import Flask, render_template, request
import calendar

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    devedor = request.form['devedor']
    salario_devedor = float(request.form['salario_devedor'])
    plano_pagamento = request.form['plano_pagamento']
    data_inicio = request.form['data_inicio']

    credores = []
    for i in range(1, 101):  # Considera até 100 credores no máximo
        credor_key = f'credor_{i}'
        divida_key = f'divida_{i}'
        if credor_key in request.form:
            credor = request.form[credor_key]
            divida = request.form.get(divida_key, '')
            try:
                divida = float(divida)
            except ValueError:
                divida = 0.0
            credores.append((credor, divida))
        else:
            break

    total_dividas = sum(divida for _, divida in credores)
    parcela_total = salario_devedor * 0.3
    meses_pagamento = min(60, int(total_dividas / (parcela_total * 0.3)))  # Limita o pagamento a 60 meses

    parcelas_proporcionais = []
    for _, divida in credores:
        parcela_proporcional = divida / meses_pagamento
        parcelas_proporcionais.append([parcela_proporcional for _ in range(meses_pagamento)])

    # Calcular os meses e anos com base na data de início
    data_inicio_mes = int(data_inicio[5:7])
    data_inicio_ano = int(data_inicio[:4])
    data_mes_ano = []
    for i in range(meses_pagamento):
        mes = (data_inicio_mes + i - 1) % 12 + 1
        ano = data_inicio_ano + (data_inicio_mes + i - 1) // 12
        data_mes_ano.append(f"{calendar.month_name[mes]} {ano}")

    return render_template('result.html', devedor=devedor, credores=credores, parcelas_proporcionais=parcelas_proporcionais,
                           total_parcelas=meses_pagamento, plano_pagamento=plano_pagamento, data_inicio=data_inicio, data_mes_ano=data_mes_ano)

if __name__ == '__main__':
    app.run()


