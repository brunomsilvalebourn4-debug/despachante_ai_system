from flask import Blueprint
from flask import render_template
from flask import request

from services.ai_service import chamar_ia

# =========================================
# BLUEPRINT
# =========================================

ai_bp = Blueprint(

    'ai_bp',

    __name__

)

# =========================================
# IA
# =========================================

@ai_bp.route('/ia', methods=['GET', 'POST'])
def pagina_ia():

    resposta = None

    if request.method == 'POST':

        pergunta = request.form.get(
            'pergunta'
        )

        telefone = request.form.get(
            'telefone'
        )

        # TELEFONE PADRÃO
        if not telefone:

            telefone = 'admin'

        resposta = chamar_ia(

            pergunta,
            telefone

        )

    return render_template(

        'ai_chat.html',

        resposta=resposta

    )