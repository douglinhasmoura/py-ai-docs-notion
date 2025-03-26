import os
from dotenv import load_dotenv
import gradio as gr
from gradio.themes import Soft
from src.notion import NotionAgent
import time

load_dotenv()

class NotionAgentUI:
    def __init__(self):
        self.agent = NotionAgent()
        self.chat_history = []

    def _respond(self, message: str, temp: float, max_len: int):
        try:
            self.agent.llm.temperature = temp
            
            # Mensagem de processamento
            self.chat_history.append((message, "⌛ Processando..."))
            yield "", self.chat_history, gr.update(interactive=False)
            
            start_time = time.time()
            response = self.agent.respond(message, self.chat_history)
            elapsed = time.time() - start_time
            
            # Garante que a resposta não é None
            if response is None:
                response = "Não foi possível gerar uma resposta."
                
            formatted_response = f"{response}\n\n⏱️ {elapsed:.2f}s"
            self.chat_history[-1] = (message, formatted_response)
            
            yield "", self.chat_history, gr.update(interactive=True)
            
        except Exception as e:
            error_msg = f"⚠️ Erro: {str(e)}"
            if not self.chat_history:
                self.chat_history.append((message, error_msg))
            else:
                self.chat_history[-1] = (message, error_msg)
            yield "", self.chat_history, gr.update(interactive=True)

    def _clear_chat(self):
        self.chat_history = []
        return None, self.chat_history, gr.update(value="", placeholder="Digite sua pergunta...")

    def launch(self):
        custom_theme = Soft(
            primary_hue="indigo",
            secondary_hue="amber",
            font=[gr.themes.GoogleFont("Open Sans")]
        )

        with gr.Blocks(theme=custom_theme, title="Assistente Imobiliário", css="""
            .message { max-width: 80%; }
            .gradio-container { max-width: 900px !important; margin: 0 auto; }
            .loading-dots::after {
                content: '.';
                animation: dots 1.5s steps(5, end) infinite;
            }
            @keyframes dots {
                0%, 20% { color: rgba(0,0,0,0); text-shadow: .25em 0 0 rgba(0,0,0,0), .5em 0 0 rgba(0,0,0,0); }
                40% { color: #4f46e5; text-shadow: .25em 0 0 rgba(0,0,0,0), .5em 0 0 rgba(0,0,0,0); }
                60% { text-shadow: .25em 0 0 #4f46e5, .5em 0 0 rgba(0,0,0,0); }
                80%, 100% { text-shadow: .25em 0 0 #4f46e5, .5em 0 0 #4f46e5; }
            }
            """) as demo:
            
            # Header
            gr.HTML("""
            <div style="text-align: center; margin-bottom: 20px;">
                <h1 style="margin-bottom: 5px;">🏠 Assistente Imobiliário</h1>
                <p>Converse com nossos documentos especializados</p>
            </div>
            """)
            
            # Área de Chat
            with gr.Row():
                chatbot = gr.Chatbot(
                    label="Conversa",
                    avatar_images=(
                        "https://i.imgur.com/hJNlQdW.png",  # User
                        "https://i.imgur.com/4C43g7F.png"    # Bot
                    ),
                    height=500,
                    show_copy_button=True,
                    bubble_full_width=False
                )
                
            # Controles
            with gr.Row():
                with gr.Column(scale=8):
                    msg = gr.Textbox(
                        placeholder="Digite sua pergunta sobre documentos imobiliários...",
                        show_label=False,
                        container=False,
                        autofocus=True
                    )
                with gr.Column(scale=2):
                    submit_btn = gr.Button("Enviar", variant="primary")
                    clear_btn = gr.Button("Limpar", variant="secondary")
            
            # Painel Lateral
            with gr.Accordion("⚙️ Configurações", open=False):
                gr.Markdown("### Opções de Resposta")
                temperature = gr.Slider(0, 1, value=0.3, label="Criatividade")
                max_length = gr.Slider(100, 2000, value=800, step=100, label="Comprimento Máximo")
                
                gr.Markdown("### Documentos Carregados")
                gr.HTML("""
                <div style='border: 1px solid #e0e0e0; padding: 15px; border-radius: 8px;'>
                    <p>📄 <strong>Documentos carregados:</strong> 1</p>
                    <p>🔄 <strong>Última atualização:</strong> Hoje</p>
                </div>
                """)
            
            # Exemplos
            gr.Examples(
                examples=[
                    "Quais documentos são necessários para alugar um imóvel?",
                    "Qual é o prazo padrão de um contrato de locação?",
                    "Como funciona o processo de vistoria?"
                ],
                inputs=msg,
                label="Perguntas Exemplo",
                examples_per_page=3
            )
            
            # Eventos
            msg.submit(
                self._respond,
                [msg, temperature, max_length],
                [msg, chatbot, msg]
            )
            submit_btn.click(
                self._respond,
                [msg, temperature, max_length],
                [msg, chatbot, msg]
            )
            clear_btn.click(
                self._clear_chat,
                outputs=[msg, chatbot, msg]
            )
        
        demo.launch(share=False, server_name=os.getenv("SERVER_NAME_IP"), server_port=os.getenv("SERVER_PORT"))

if __name__ == "__main__":
    ui = NotionAgentUI()
    ui.launch()