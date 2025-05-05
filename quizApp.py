import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style
import csv

# Load quiz data
def load_quiz(csv_file):
    quiz_data = []
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            question = {"questions": row["question"], "answer": row["answer"]}
            if "choices" in row and row["choices"]:
                question["choices"] = row["choices"].split(',')
            quiz_data.append(question)
    return quiz_data

quiz_data = load_quiz("quiz_data.csv")

# Timer
time_per_question = 20
time_remaining = time_per_question
timer_id = None

def update_timer():
    global time_remaining, timer_id
    timer_label.config(text=f"Time: {time_remaining}s")
    if time_remaining > 0:
        time_remaining -= 1
        timer_id = root.after(1000, update_timer)
    else:
        feedback_label.config(text="Time's up! +0", foreground='red')
        root.after(1000, next_question)

# Display questions
def show_qs():
    global time_remaining, timer_id
    if timer_id is not None:
        root.after_cancel(timer_id)
    time_remaining = time_per_question
    update_timer()

    question = quiz_data[current_qs]
    qs_label.config(text=question["questions"])
    feedback_label.config(text='')

    if "choices" in question:
        for i in range(4):
            if i < len(question["choices"]):
                choice_btns[i].config(text=question["choices"][i], state='normal')
                choice_btns[i].pack(pady=10, fill='x', padx=100)
            else:
                choice_btns[i].pack_forget()
        identification_entry.pack_forget()
        identification_btn.pack_forget()
    else:
        for button in choice_btns:
            button.pack_forget()
        identification_entry.pack(pady=10)
        identification_btn.pack(pady=10)

# Check answer
def check_answer(choice=None):
    global timer_id
    if timer_id is not None:
        root.after_cancel(timer_id)

    question = quiz_data[current_qs]

    if "choices" in question:
        selected_choice = choice_btns[choice].cget('text')
        if selected_choice == question['answer']:
            update_score(True)
        else:
            update_score(False)
    else:
        entered_answer = identification_entry.get().strip()
        if entered_answer.lower() == question['answer'].lower():
            update_score(True)
        else:
            update_score(False)
        identification_entry.delete(0, tk.END)

    feedback_label.after(1000, next_question)

# Update score
def update_score(correct):
    global score
    if correct:
        score += 1
        feedback_label.config(text='Correct! +1', foreground='green')
    else:
        feedback_label.config(text='Incorrect! +0', foreground='red')

    score_label.config(text='Score: {}/{}'.format(score, len(quiz_data)))

    for button in choice_btns:
        button.config(state='disabled')

# Move to next question
def next_question():
    global current_qs, timer_id
    if timer_id is not None:
        root.after_cancel(timer_id)
    current_qs += 1

    # Update progress bar and label
    progress_percent = min(100, int((current_qs / len(quiz_data)) * 100))
    progress['value'] = progress_percent
    progress_label.config(text=f"Progress: {progress_percent}%")

    if current_qs < len(quiz_data):
        show_qs()
    elif score > 6:
        messagebox.showinfo('Quiz Completed',
                            'Congratulations! Final score: {}/{}'.format(score, len(quiz_data)))
        root.quit()
    else:
        messagebox.showinfo('Quiz Completed',
                            'Its okay! Final score: {}/{}'.format(score, len(quiz_data)))
        root.quit()

# Window
root = tk.Tk()
root.title('Quiz App - CONDE IK2')
root.geometry('600x550')
style = Style(theme='litera')

# Button & label styles
style.configure('TLabel', font=('Courier', 20, 'bold'))
style.configure('TButton', font=('Courier', 15))

# Background color
root.configure(bg='#f7f7f7')

# Score & timer frame
top_frame = ttk.Frame(root)
top_frame.pack(side='top', fill='x', padx=20, pady=10)

# Timer label (top left)
timer_label = ttk.Label(
    top_frame,
    text=f"Time: {time_per_question}s",
    font=('Courier', 15)
)
timer_label.pack(side='left')

# Score label (top right)
score = 0
score_label = ttk.Label(
    top_frame,
    text='Score: 0/{}'.format(len(quiz_data)),
    font=('Courier', 15)
)
score_label.pack(side='right')

# Progress bar (center top)
progress = ttk.Progressbar(top_frame, orient='horizontal', length=200, mode='determinate', maximum=100)
progress.pack(side='top', pady=5)

# Progress percentage label
progress_label = ttk.Label(top_frame, text="Progress: 0%", font=('Courier', 12))
progress_label.pack(side='top')

# Question label
qs_label = ttk.Label(
    root,
    anchor='center',
    wraplength=500,
    padding=10,
    style='TLabel'
)
qs_label.pack(pady=20)

# Choice buttons
choice_btns = []
for i in range(4):
    button = ttk.Button(
        root,
        command=lambda i=i: check_answer(i),
        style='TButton'
    )
    button.pack(pady=10, fill='x', padx=100)
    choice_btns.append(button)

# Feedback label
feedback_label = ttk.Label(
    root,
    anchor='center',
    padding=10,
    style='TLabel'
)
feedback_label.pack(pady=10)

# Identification questions
identification_entry = ttk.Entry(root, font=('Courier', 15), width=40)
identification_btn = ttk.Button(
    root,
    text='Submit',
    command=lambda: check_answer(),
    style='TButton'
)

# Question index
current_qs = 0

# Show first question
show_qs()

root.mainloop()
