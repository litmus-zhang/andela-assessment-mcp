import gradio as gr
from dotenv import load_dotenv
from meridian_mcp import get_meridian_tools
from agent import create_meridian_agent
from opik.integrations.langchain import OpikTracer
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.callbacks import StdOutCallbackHandler

# Load environment variables
load_dotenv()

class MeridianChatbotUI:
    def __init__(self):
        self.agent_executor = None
        self.tools = None
        self.tracer = OpikTracer(project_name="meridian-support-chatbot")
        self.stdout_handler = StdOutCallbackHandler()

    async def initialize(self):
        """Initialize tools and agent executor."""
        if not self.agent_executor:
            self.tools = await get_meridian_tools()
            self.agent_executor = await create_meridian_agent(self.tools)

    async def chat(self, message, history):
        """Handle chat interactions."""
        await self.initialize()
        
        # Convert history to message list
        messages = []
        for msg in history:
            if isinstance(msg, dict):
                role = msg.get("role")
                content = msg.get("content")
                if role == "user":
                    messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    messages.append(AIMessage(content=content))
            else:
                # Handle tuple format for older Gradio versions just in case
                human, ai = msg
                messages.append(HumanMessage(content=human))
                messages.append(AIMessage(content=ai))
        
        messages.append(HumanMessage(content=message))

        try:
            # Execute agent with Opik and StdOut tracing
            # print(f"messages: {messages}")
            result = await self.agent_executor.ainvoke(
                {"messages": messages},
                config={"callbacks": [self.tracer, self.stdout_handler]}
            )
            
            # The result is usually the final state of the graph
            final_message = result["messages"][-1]
            if hasattr(final_message, "content"):
                return final_message.content
            return str(final_message)
        except Exception as e:
        
            return f"Error: {str(e)}"

def create_ui():
    chatbot_ui = MeridianChatbotUI()

    # Custom Theme/CSS for "Premium" look
    theme = gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate",
        neutral_hue="slate",
        font=[gr.themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
    )

    with gr.Blocks(theme=theme, title="Meridian Electronics Support") as demo:
        gr.Markdown(
            """
            # 📱 Meridian Electronics Support
            ### Your AI-powered assistant for orders, availability, and more.
            """
        )
        
        chat_interface = gr.ChatInterface(
            fn=chatbot_ui.chat,
            examples=["Check availability for 'Keyboard'", "What's my order history?", "Help me place an order"],
            cache_examples=False,
        )

    return demo

if __name__ == "__main__":
    demo = create_ui()
    demo.launch()
