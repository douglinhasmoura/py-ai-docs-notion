from typing import List, Tuple

def format_response(response: str, elapsed: float) -> str:
    """Formata a resposta do bot com metadata"""
    return f"{response}\n\n⏱️ {elapsed:.2f}s"

def handle_error(chat_history: List[Tuple], message: str, error: Exception) -> List[Tuple]:
    """Trata erros de forma consistente"""
    error_msg = f"⚠️ Erro: {str(error)}"
    if not chat_history:
        return [(message, error_msg)]
    return chat_history[:-1] + [(message, error_msg)]