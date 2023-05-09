from flask import Flask , render_template , request , jsonify
import text_sentiment_prediction
from predict_bot_response import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# api ouvindo solicitações POST e prevendo sentimentos
@app.route('/predict' , methods = ['POST'])
def predict():

    response = ""
    review = request.json.get('customer_review')
    if not review:
        response = {'status' : 'error',
                    'message' : 'Avaliação em Branco'}
    
    else:

        # chamando o método predict do módulo de previsão.py
        sentiment , path = text_sentiment_prediction.predict(review)
        response = {'status' : 'success',
                    'message' : 'Entendi',
                    'sentiment' : sentiment,
                    'path' : path}

    return jsonify(response)


# Criando uma API para salvar a avaliação. O usuário clica no botão Salvar
@app.route('/save' , methods = ['POST'])
def save():

    # extraindo data, nome do produto, avaliação e sentimento associados aos dados JSON
    date = request.json.get('date')
    product = request.json.get('product')
    review = request.json.get('review')
    sentiment = request.json.get('sentiment')

    # criando uma variável final separada por vírgulas
    data_entry = date + "," + product + "," + review + "," + sentiment

    # abra o arquivo no modo 'append'
    f = open('./static/assets/datafiles/data_entry.csv' , 'a')

    # Registre os dados no arquivo
    f.write(data_entry + '\n')

    # feche o arquivo
    f.close()

    # retorne uma mensagem de sucesso
    return jsonify({'status' : 'success' , 
                    'message' : 'Dados Registrados'})


# escrevendo a api do  chatbot
@app.route("/", methods=[""])
def bot():
    # Obtenha a entrada do usuário
    input_text = request.json.get("user_bot_input_text")
   
    # Chame o método para obter a resposta do robô
    bot_res = bot_response(input_text)

    response = {
            "bot_response": bot_res
        }

    return jsonify(response)
     
if __name__ == '__main__':
    app.run(debug=True)