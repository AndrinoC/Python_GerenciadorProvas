import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import os

def load_questions():
    if os.path.exists('Teste.json'):
        with open('Teste.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

def save_questions(questions):
    with open('Teste.json', 'w', encoding='utf-8') as file:
        json.dump(questions, file, ensure_ascii=False, indent=4)

class QuestionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Testes")
        self.root.geometry("800x400")  # Define o tamanho fixo da janela
        self.root.resizable(False, False)  # Desabilita a redimensão da janela
        self.questions = load_questions()
        self.current_category = None
        self.question_var = tk.StringVar()
        self.answer_var = tk.StringVar()
        self.weight_var = tk.StringVar()
        self.create_widgets()
        self.load_existing_categories()
        self.apply_dark_theme()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky="nsew")
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

        self.question_frame = tk.Frame(self.root, bg='#2E2E2E')
        self.question_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        tk.Label(self.question_frame, text="Pergunta", bg='#2E2E2E', fg='#FFFFFF').grid(row=0, column=0, sticky="w")
        tk.Entry(self.question_frame, textvariable=self.question_var, bg='#1E1E1E', fg='#FFFFFF', insertbackground='white').grid(row=0, column=1, sticky="ew", padx=5)

        tk.Label(self.question_frame, text="Alternativa", bg='#2E2E2E', fg='#FFFFFF').grid(row=1, column=0, sticky="w")
        tk.Entry(self.question_frame, textvariable=self.answer_var, bg='#1E1E1E', fg='#FFFFFF', insertbackground='white').grid(row=1, column=1, sticky="ew", padx=5)

        tk.Label(self.question_frame, text="Peso", bg='#2E2E2E', fg='#FFFFFF').grid(row=2, column=0, sticky="w")
        tk.Entry(self.question_frame, textvariable=self.weight_var, bg='#1E1E1E', fg='#FFFFFF', insertbackground='white').grid(row=2, column=1, sticky="ew", padx=5)

        tk.Button(self.question_frame, text="Adicionar", command=lambda: self.add_question(self.current_category), bg='#4A4A4A', fg='#FFFFFF').grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")

        listbox_frame = tk.Frame(self.question_frame, bg='#2E2E2E')
        listbox_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=5, pady=(5, 0))

        self.question_listbox = tk.Listbox(listbox_frame, bg='#1E1E1E', fg='#FFFFFF', selectbackground='#4A4A4A', selectforeground='#FFFFFF')
        self.question_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.question_listbox.bind("<<ListboxSelect>>", self.on_listbox_click)
        self.question_listbox.bind("<Double-1>", self.show_selected_question)

        scrollbar = tk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.question_listbox.yview, bg='#2E2E2E', troughcolor='#1E1E1E')
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.question_listbox.config(yscrollcommand=scrollbar.set)

        self.button_frame = tk.Frame(self.root, bg='#2E2E2E')
        self.button_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        self.button_frame.grid_columnconfigure([0, 1, 2], weight=1)

        tk.Button(self.button_frame, text="Adicionar Categoria", command=self.add_category, bg='#4A4A4A', fg='#FFFFFF').grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(self.button_frame, text="Renomear Categoria", command=self.rename_category, bg='#4A4A4A', fg='#FFFFFF').grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        tk.Button(self.button_frame, text="Excluir Categoria", command=self.delete_category, bg='#4A4A4A', fg='#FFFFFF').grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        tk.Button(self.button_frame, text="Limpar Alternativas", command=self.clear_alternatives, bg='#4A4A4A', fg='#FFFFFF').grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        tk.Button(self.button_frame, text="Limpar Todas as Perguntas", command=self.clear_all_questions, bg='#4A4A4A', fg='#FFFFFF').grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        tk.Button(self.button_frame, text="Excluir Pergunta", command=self.delete_question, bg='#4A4A4A', fg='#FFFFFF').grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        self.root.grid_rowconfigure(0, weight=1)  # Expande notebook
        self.root.grid_rowconfigure(1, weight=1)  # Expande question_frame
        self.root.grid_columnconfigure(0, weight=1)  # Expande notebook e question_frame
        self.question_frame.grid_rowconfigure(4, weight=1)  # Expande listbox_frame
        self.question_frame.grid_columnconfigure(1, weight=1)  # Expande entradas e botões
        self.update_question_list()

    def apply_dark_theme(self):
        self.root.configure(bg='#2E2E2E')  # Cor de fundo da janela principal
        self.notebook.configure(style='TNotebook')
        style = ttk.Style()

        # Notebook and Tab style
        style.configure('TNotebook', background='#2E2E2E', foreground='#FFFFFF')
        style.configure('TNotebook.Tab', background='#4A4A4A', foreground='#000000', padding=[10, 5])
        style.map('TNotebook.Tab',
                background=[('selected', '#3C3C3C')],
                foreground=[('selected', '#000000')])  # Texto preto para a aba selecionada

    def add_category_tab(self, category):
        frame = tk.Frame(self.notebook, bg='#FFFFFF')
        self.notebook.add(frame, text=category)
        self.current_category = category.upper()
        self.update_question_list(category)

    def load_existing_categories(self):
        for category in self.questions:
            self.add_category_tab(category)

    def add_category(self):
        category_name = simpledialog.askstring("Nova Categoria", "Digite o nome da nova categoria:")
        if category_name:
            category_name = category_name.upper()
            if category_name not in self.questions:
                self.questions[category_name] = []
                self.add_category_tab(category_name)
                save_questions(self.questions)
            else:
                messagebox.showerror("Erro", "Categoria já existe.")

    def rename_category(self):
        selected_tab = self.notebook.select()
        current_name = self.notebook.tab(selected_tab, "text")
        new_name = simpledialog.askstring("Renomear Categoria", f"Renomear '{current_name}' para:")
        if new_name:
            new_name = new_name.upper()
            if new_name not in self.questions:
                self.questions[new_name] = self.questions.pop(current_name)
                self.notebook.tab(selected_tab, text=new_name)
                save_questions(self.questions)
            else:
                messagebox.showerror("Erro", "Categoria já existe.")

    def delete_category(self):
        selected_tab = self.notebook.select()
        category_name = self.notebook.tab(selected_tab, "text")
        if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir a categoria '{category_name}'?"):
            del self.questions[category_name]
            self.notebook.forget(self.notebook.index(selected_tab))
            save_questions(self.questions)

    def on_tab_change(self, event):
        selected_tab = event.widget.tab('current')['text']
        self.current_category = selected_tab.upper()
        self.update_question_list(self.current_category)

    def update_question_list(self, category=None):
        if not category:
            category = self.current_category
        if category and category in self.questions:
            self.question_listbox.delete(0, tk.END)
            for question in self.questions[category]:
                self.question_listbox.insert(tk.END, question['question'])
        else:
            self.question_listbox.delete(0, tk.END)

    def add_question(self, category):
        question_text = self.question_var.get().strip()
        answer_text = self.answer_var.get().strip()
        weight_text = self.weight_var.get().strip()
        if not question_text or not answer_text or not weight_text:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return
        try:
            weight = float(weight_text)
        except ValueError:
            messagebox.showerror("Erro", "Peso deve ser um número.")
            return
        question = next((q for q in self.questions[category] if q['question'] == question_text), None)
        if question:
            question['alternatives'].append({'answer': answer_text, 'weight': weight})
        else:
            self.questions[category].append({
                'question': question_text,
                'alternatives': [{'answer': answer_text, 'weight': weight}]
            })
        self.answer_var.set("")
        self.weight_var.set("")
        self.update_question_list(category)
        save_questions(self.questions)

    def on_listbox_click(self, event):
        category = self.current_category
        if not category or category not in self.questions:
            messagebox.showerror("Erro", "Nenhuma categoria ou perguntas disponíveis.")
            return
        selection = self.question_listbox.curselection()
        if selection:
            index = selection[0]
            selected_question = self.questions[category][index]
            self.question_var.set(selected_question['question'])

    def show_selected_question(self, event):
        category = self.current_category
        if not category or category not in self.questions:
            messagebox.showerror("Erro", "Nenhuma categoria ou perguntas disponíveis.")
            return
        selection = self.question_listbox.curselection()
        if selection:
            index = selection[0]
            selected_question = self.questions[category][index]
            alternatives = "\n".join([f"{a['answer']} (Peso: {a['weight']})" for a in selected_question['alternatives']])
            messagebox.showinfo("Alternativas", alternatives)

    def delete_question(self):
        category = self.current_category
        if not category:
            messagebox.showerror("Erro", "Nenhuma categoria selecionada.")
            return
        selection = self.question_listbox.curselection()
        if selection:
            index = selection[0]
            if messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir a pergunta '{self.questions[category][index]['question']}'?"):
                del self.questions[category][index]
                self.update_question_list(category)
                save_questions(self.questions)
                messagebox.showinfo("Sucesso", "Pergunta excluída com sucesso.")
        else:
            messagebox.showerror("Erro", "Nenhuma pergunta selecionada.")

    def clear_alternatives(self):
        category = self.current_category
        if not category:
            messagebox.showerror("Erro", "Nenhuma categoria selecionada.")
            return
        selection = self.question_listbox.curselection()
        if selection:
            index = selection[0]
            self.questions[category][index]['alternatives'] = []
            self.update_question_list(category)
            save_questions(self.questions)
            messagebox.showinfo("Sucesso", "Todas as alternativas foram removidas.")

    def clear_all_questions(self):
        category = self.current_category
        if category:
            self.questions[category] = []
            self.update_question_list(category)
            save_questions(self.questions)
            messagebox.showinfo("Sucesso", "Todas as perguntas foram removidas.")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuestionApp(root)
    root.mainloop()
