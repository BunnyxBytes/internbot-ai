import tkinter as tk
from tkinter import font
import random

# AI brain
responses = {
    "hello": ["Hello! How are you?", "Hi there! What's up?", "Hey! How can I help you today?"],
    "how are you": ["I'm doing great, thanks! How about you?", "I'm awesome. You tell me?", "All good on my end!"],
    "i am fine": ["That's great to hear! What would you like to talk about?", "Awesome! How can I help you today?", "Good to know! So, what's up?"],
    "who are you": ["I'm InternBot, an AI chatbot. I was made with Python + Tkinter.", "I'm a GUI based AI assistant."],
    "what is python": ["Python is a easy and simple language! It is one of the most popular language in the world. That's what I'm built with.", "Python is a high level, interpreted programming language known for its clear and readable syntax and versatility."],
    "what is an internship": ["You'll learn a lot by building projects and real-world experience in a corporate or technical environment.", "An internship is a short-term professional opportunity where you work in a real-world job to gain hands-on experience, learn new skills, and explore a career path under path under the guidance of mentors."],
    "thanks": ["You're welcome! Anything else?", "No problem. Happy to help.", "My pleasure!"],
    "bye": ["Goodbye! See you later.", "Bye bye! Closing the window.", "Take care! Catch you next time."]
}

default_replies = ["Hmm, I didn't get that.", "Sorry, I don't have an answer for that.", "Can you try asking differently?"]
message_bubbles = []

def get_bot_reply(user_msg):
    user_msg = user_msg.lower().replace("'","")
    for keyword in responses:
        if keyword in user_msg:
            return random.choice(responses[keyword])
    return random.choice(default_replies)

def current_wraplength():
    width = canvas.winfo_width()
    if width <= 1:
        width = 400
    return max(180, min(420, int(width * 0.62)))

def on_canvas_resize(event):
    canvas.itemconfig(chat_window, width=event.width)
    wrap = current_wraplength()
    for bubble in message_bubbles:
        bubble.configure(wraplength=wrap)
    canvas.configure(scrollregion=canvas.bbox("all"))

def add_message(text, sender="bot"):
    # Main bubble frame
    bubble_frame = tk.Frame(chat_frame, bg="#0d1117")
    bubble_frame.pack(fill="x",expand=True,pady=3)

    # Message bubble
    if sender == "user":
        bubble = tk.Label(bubble_frame, text=text, font=("segoe UI",11), bg="#1069f8", fg="white",
                          wraplength=current_wraplength(), justify="left", padx=12, pady=8)
        bubble.pack(side="left", anchor="w",padx=(15,0))
    else:
        bubble = tk.Label(bubble_frame, text=text, font=("Segoe UI",11), bg="#21262d", fg="#e6edf3",
                          wraplength=current_wraplength(), justify="left", padx=12, pady=8)
        bubble.pack(side="right", anchor="e",padx=(0,15))
    message_bubbles.append(bubble)

    # Auto scroll to bottom
    canvas.update_idletasks()
    canvas.yview_moveto(1.0)

def send_message(event=None):
    user_msg = user_input.get().strip()
    if user_msg == "":
        return

    add_message(user_msg, "user")
    user_input.delete(0, tk.END)

    if user_msg.lower() == "bye":
        bot_reply = random.choice(responses["bye"])
        window.after(500, lambda: add_message(bot_reply, "bot"))
        window.after(2500, window.destroy)
        return

    bot_reply = get_bot_reply(user_msg)
    # Thoda delay taaki real lage
    window.after(600, lambda: add_message(bot_reply, "bot"))

# --- WINDOW SETUP ---
window = tk.Tk()
window.title("InternBot AI")
window.geometry("400x550")
window.config(bg="#27364d") # Insta dark mode color

# Fonts
title_font = font.Font(family="Segoe UI", size=14, weight="bold")
chat_font = font.Font(family="Segoe UI", size=10)

# Top bar - Instagram style
top_bar = tk.Frame(window, bg="#1c2025", height=60)
top_bar.pack(fill="x")
top_bar.pack_propagate(False)

profile_pic = tk.Label(top_bar, text="🤖", font=("Segoe UI", 20), bg="#161b22")
profile_pic.pack(side="left", padx=15)

name_label = tk.Label(top_bar, text="InternBot AI", font=title_font, bg="#161b22", fg="#e6edf3")
name_label.pack(side="left", pady=15)

status_label = tk.Label(top_bar, text="● Online", font=("Segoe UI", 9), bg="#161b22", fg="#3fb950")
status_label.pack(side="left", padx=8, pady=18)


# Input area
input_frame = tk.Frame(window, bg="#161b22", height=60)
input_frame.pack(fill="x", side="bottom")
input_frame.pack_propagate(False)

user_input = tk.Entry(input_frame, font=chat_font, bg="#21262d", fg="#e6edf3",
                      insertbackground="#e6edf3", bd=0, relief=tk.FLAT)
user_input.pack(side="left", fill="x", expand=True, ipady=10, padx=15, pady=10)
user_input.bind("<Return>", send_message)
user_input.focus()

send_btn = tk.Button(input_frame, text="Send", command=send_message,
                     font=("Segoe UI", 10, "bold"), bg="#1f6feb", fg="white",
                     activebackground="#388bfd", activeforeground="white",
                     bd=0, padx=20, pady=8, cursor="hand2")
send_btn.pack(side="right", padx=(0,15), pady=10)

# Chat area with scrollbar
canvas = tk.Canvas(window, bg="#0d1117", highlightthickness=0)
scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
chat_frame = tk.Frame(canvas, bg="#0d1117")

chat_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
chat_window = canvas.create_window((0, 0), window=chat_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", on_canvas_resize)

canvas.pack(side="left", fill="both", expand=True, padx=(0,0))
scrollbar.pack(side="right", fill="y")

# First message
add_message("Hey! I'm InternBot AI. Ask me anything ✨", "bot")

window.mainloop()