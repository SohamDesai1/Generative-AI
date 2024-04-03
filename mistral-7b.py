from ctransformers import AutoModelForCausalLM
import gradio as gr

def load_llm():
    llm = AutoModelForCausalLM.from_pretrained("./models/mistral-7b-instruct-v0.2.Q5_K_M.gguf")
    return llm

def chat(msg,hist):
    llm = load_llm()
    res = llm(msg)
    return res

gr.ChatInterface(fn=chat,title="Mistral").launch()
