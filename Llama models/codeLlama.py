from ctransformers import AutoModelForCausalLM
import gradio as gr 
def load_llm():
    llm = AutoModelForCausalLM.from_pretrained("./models/codellama-7b-instruct.Q5_K_M.gguf",model_type="llama", max_new_tokens = 1096,temperature=0.1)
    return llm
 
def chating(msg,hist):
    llm = load_llm()
    res = llm(msg)
    return res

gr.ChatInterface(fn=chating,title="Code Llama").launch()