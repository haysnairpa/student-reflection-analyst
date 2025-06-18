import tkinter as tk
from tkinter import ttk, scrolledtext
import speech_recognition as sr
import requests
import numpy as np
import re
import string

API_KEY = "your_api_key"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

question = []
student_answers = []
current_question_index = -1
current_student_index = 0

reflections = np.load('./reflections.npy')
questions = np.load('./questions.npy')
summary = np.load('./summary.npy')

examples = ""
for i in range(len(questions)):
   examples += f"""{i}. Questions: {questions[i]}
   Reflections: {reflections[i]}
   Summary: {summary[i]}\n\n"""

def preprocess_text(text):
    if not isinstance(text, str):
        text = ''
    processed_text = text.lower()
    processed_text = processed_text.translate(str.maketrans('', '', string.punctuation))
    processed_text = re.sub(r'\s+', ' ', processed_text).strip()
    return processed_text
''
def generate_summary(questions, reflections):
    payload = {
        "contents": [{
            "parts": [
                {
                    "text": f'''
                      You are the world's finest student reflection summarizer assistance.
                      Your goal is to summarize the reflections given to you in a particular context questions that given to the students.

                      You can use these examples for summarizing the reflections:
                      {examples}

                      Your task now is create the summary for the following context questions and reflections.

                      Questions: {questions}
                      Reflections: {reflections}

                      Your output must:
                      - Not consist "Summary: "
                      - Do not paraphrase
                    '''
                }
            ]
        }],
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        res = response.json()
        return res['candidates'][0]['content']['parts'][0]['text']
    else:
        return "Error generating summary."

class gui:
    def __init__(self, master):
        self.master = master
        master.title("QnA Session")
        master.geometry("600x500")
        master.configure(bg="#f0f0f0")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Arial', 10), borderwidth=1)
        style.configure('TLabel', font=('Arial', 12), background="#f0f0f0")
        style.configure('TEntry', font=('Arial', 12))

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="20 20 20 20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        question_frame = ttk.Frame(main_frame)
        question_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=10)
        question_frame.columnconfigure(1, weight=1)

        ttk.Label(question_frame, text="Input Question:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.question_entry = ttk.Entry(question_frame, width=50)
        self.question_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        ttk.Button(question_frame, text="Next", command=self.start_question).grid(row=0, column=2, padx=(10, 0))

        self.question_label = ttk.Label(main_frame, text="", wraplength=700)
        self.question_label.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)

        self.answer_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=60, height=5)
        self.answer_text.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=10)
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)

        self.mic_button = ttk.Button(button_frame, text="🎤 Record Answer", command=self.record_audio)
        self.mic_button.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5)

        ttk.Button(button_frame, text="Next Student", command=self.next_student).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(button_frame, text="Repeat", command=self.repeat_recording).grid(row=0, column=2, sticky=(tk.W, tk.E), padx=5)

        ttk.Button(main_frame, text="Finish Q&A", command=self.finish_qna).grid(row=4, column=0, sticky=(tk.W, tk.E), pady=10)

        self.summary_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=60, height=5, state='disabled')
        self.summary_text.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=10)

    def start_question(self):
        global current_question_index, student_answers
        q = self.question_entry.get().strip()
        if q:
            clean_question = preprocess_text(q)
            question.append(clean_question)
            student_answers.append([])
            current_question_index += 1
            self.question_label.config(text=f"Question: {clean_question}")
            self.question_entry.delete(0, tk.END)

    def record_audio(self):
        recognizer = sr.Recognizer()
        self.mic_button.config(text="Recording...", state=tk.DISABLED)
        self.master.update_idletasks()
        recognizer.dynamic_energy_threshold = True
        recognizer.energy_threshold = 300
        recognizer.pause_threshold = 0.8
        with sr.Microphone() as source:
            self.answer_text.delete('1.0', tk.END)
            self.answer_text.insert(tk.END, "Speak now...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=15, snowboy_configuration=None)
                text = recognizer.recognize_google(audio, language="en-US")
                clean_text = preprocess_text(text)
                student_answers[current_question_index].append(clean_text)
                self.answer_text.delete('1.0', tk.END)
                self.answer_text.insert(tk.END, f"Student Answer: {clean_text}")
            except sr.UnknownValueError:
                self.answer_text.delete('1.0', tk.END)
                self.answer_text.insert(tk.END, "Could not understand, please try again.")
            except sr.RequestError:
                self.answer_text.delete('1.0', tk.END)
                self.answer_text.insert(tk.END, "Network error, check your connection.")
            except sr.WaitTimeoutError:
                self.answer_text.delete('1.0', tk.END)
                self.answer_text.insert(tk.END, "No speech detected, please try again.")
        self.mic_button.config(text="🎤 Record Answer", state=tk.NORMAL)

    def next_student(self):
        global current_student_index
        current_student_index += 1
        self.answer_text.delete('1.0', tk.END)

    def finish_qna(self):
        if current_question_index >= 0:
            question_text = question[current_question_index]
            reflections_text = student_answers[current_question_index]
            summary = generate_summary(question_text, reflections_text)
            self.summary_text.config(state='normal')
            self.summary_text.delete('1.0', tk.END)
            self.summary_text.insert(tk.END, f"Summary: {summary}")
            self.summary_text.config(state='disabled')
        else:
            self.summary_text.config(state='normal')
            self.summary_text.delete('1.0', tk.END)
            self.summary_text.insert(tk.END, "No question to summarize.")
            self.summary_text.config(state='disabled')

    def repeat_recording(self):
        global current_student_index
        if student_answers[current_question_index]:
            student_answers[current_question_index].pop()
            self.answer_text.delete('1.0', tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = gui(root)
    root.mainloop()