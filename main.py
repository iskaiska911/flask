from flask import Flask, request
import os
import openai
import sys

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')  # this is the home page route
def hello_world(
):  # this is the home page function that generates the page code
    return "Hello world!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        req = request.get_json(silent=True, force=True)
        fulfillmentText = 'you said'
        query_result = req.get('queryResult')
        query = query_result.get('queryText')

        start_sequence = "\nJOY->"
        restart_sequence = "\nUser->"

        if query_result.get('action') == 'input.unknown':

            response =  openai.Completion.create(
                model="ft:davinci-002:personal::8CvHxb48",
                prompt="The following is a conversation with a therapist and a user. The therapist is JOY, who uses compassionate listening to have helpful and meaningful conversations with users. JOY is empathic and friendly. JOY's objective is to make the user feel better by feeling heard. With each response, JOY offers follow-up questions to encourage openness and tries to continue the conversation in a natural way. \n\nJOY-> Hello, I am your personal mental health assistant. What's on your mind today?\nUser->"+query+"JOY->",
                temperature=0.89,
                max_tokens=162,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.6,
                stop=["User"]
            )

        result = response.get('choices')[0].get('text')

        return {
            "fulfillmentText":
            result,
            "source":
            "webhookdata"
        }
        return '200'
    except Exception as e:
        print('error',e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('oops',exc_type, fname, exc_tb.tb_lineno)
        return {'error': 'Bad Request', 'message': str(e)}, 400


if __name__ == '__main__':
     app.run(debug=True, port=os.getenv("PORT", default=5000))
