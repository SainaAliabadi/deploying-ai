import gradio as gr
from chat_system.src.chat_engine import ChatEngine

engine = ChatEngine()

def fn(message, history):
    """
    history may come in tuple format or dict format depending on version.
    We don't rely on it — we keep memory inside ChatEngine.
    """

    response = engine.chat(message)
    return response


demo = gr.ChatInterface(
    fn=fn,
    title="🧠 Atlas — Multi-Service AI Assistant",
    description=(
        "Atlas can:\n"
        "- 🌍 Provide country information\n"
        "- 📚 Answer AI knowledge questions\n"
        "- 📊 Compute statistics (mean, sum, median, stdev)\n\n"
        "🚫 Restricted Topics:\n"
        "Cats, Dogs, Horoscopes, Zodiac Signs, Taylor Swift"
    ),
)

demo.launch()
