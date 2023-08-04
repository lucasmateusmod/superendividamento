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
    max_parcela = salario_devedor * 0.3
    total_parcelas_possiveis = min(60, int(total_dividas / max_parcela))
    percentual_pago = (total_parcelas_possiveis * max_parcela) / total_dividas * 100

    total_parcelas = 60  # Define o número total de parcelas para o plano possível
    data_inicio_mes = int(data_inicio[5:7])
    data_inicio_ano = int(data_inicio[:4])
    data_mes_ano = []
    for i in range(total_parcelas):
        mes = (data_inicio_mes + i - 1) % 12 + 1
        ano = data_inicio_ano + (data_inicio_mes + i - 1) // 12
        data_mes_ano.append(f"{calendar.month_name[mes]} {ano}")

    parcelas_proporcionais = []
    for mes in range(total_parcelas):
        parcelas_mes = []
        valor_total_parcelas_mes = 0
        for credor, divida in credores:
            parcela_proporcional = divida / total_parcelas_possiveis
            parcela = min(parcela_proporcional, max_parcela)
            valor_total_parcelas_mes += parcela
            parcelas_mes.append(parcela)
        # Verifica se o valor total das parcelas do mês ultrapassa o limite de 30% do salário
        if valor_total_parcelas_mes > max_parcela:
            # Reduz todas as parcelas do mês proporcionalmente para respeitar o limite
            fator_reducao = max_parcela / valor_total_parcelas_mes
            parcelas_mes = [parcela * fator_reducao for parcela in parcelas_mes]
        parcelas_proporcionais.append(parcelas_mes)

    return render_template('result.html', devedor=devedor, credores=credores,
                           total_dividas=total_dividas, max_parcela=max_parcela,
                           total_parcelas=total_parcelas, data_inicio=data_inicio,
                           data_mes_ano=data_mes_ano, plano_pagamento=plano_pagamento,
                           percentual_pago=percentual_pago,
                           parcelas_proporcionais=parcelas_proporcionais)

if __name__ == '__main__':
    app.run()





