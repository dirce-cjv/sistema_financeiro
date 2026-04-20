from __future__ import annotations 

def build_categorize_prompt(description: str) -> str:
    return f"""
Você é um classificador de despesas financeiras.

Classifique a despesa em apenas UMA das categorias abaixo:

Alimentação
Transporte
Moradia
Saúde
Lazer
Assinaturas
Outros

Use estas associações:
Alimentação: supermercado, restaurante, lanche, almoço, jantar, pastel, pizzaria, kalzone, comida
Transporte: combustível, gasolina, uber, ônibus, transporte, pedágio, estacionamento, carro, manutenção
Moradia: aluguel, energia, água, internet, telefone, condomínio
Saúde: plano de saúde, consulta, médico, exame, remédio, farmácia, academia
Lazer: cinema, viagens, passeios, festas
Assinaturas: netflix, spotify, amazon, aplicativos

Regras importantes:
- Escolha sempre a categoria mais provável.
- Nunca responda "não identificado".
- Se não tiver certeza, responda "Outros".
- Responda apenas com o nome da categoria.
- Não escreva frases ou explicações.

Despesa:
{description}
"""