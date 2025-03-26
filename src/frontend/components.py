import gradio as gr
from typing import List, Tuple

def create_chat_ui() -> Tuple[gr.Chatbot, gr.Textbox]:
    """Cria componentes reutilizáveis da interface"""
    chatbot = gr.Chatbot(
        bubble_full_width=False,
        avatar_images=(
            "https://i.imgur.com/hJNlQdW.png",  # User
            "https://i.imgur.com/4C43g7F.png"    # Bot
        )
    )
    textbox = gr.Textbox(placeholder="Digite sua pergunta...")
    return chatbot, textbox

def create_settings_panel() -> gr.Accordion:
    """Painel de configurações reutilizável"""
    with gr.Accordion("⚙️ Configurações", open=False) as panel:
        temp_slider = gr.Slider(0, 1, value=0.3, label="Criatividade")
        max_len = gr.Slider(100, 2000, value=800, label="Comprimento Máximo")
    return panel, temp_slider, max_len