import tkinter as tk
import tkinter.ttk as ttk
from tkinter.simpledialog import Dialog


class AcknowledgementDialogue(Dialog):
    def __init__(
        self, parent: tk.Toplevel, message: str, title: str = 'Connect4Man'
    ) -> None:
        self.message = message
        super().__init__(parent, title)

    def body(self, parent: tk.Frame) -> tk.Frame:
        self.resizable(False, False)
        message_label = ttk.Label(parent, text=self.message)
        message_label.pack()
        return parent

    def buttonbox(self) -> None:
        box = ttk.Frame(self)
        w = ttk.Button(
            box,
            text='OK',
            width=10,
            command=self.cancel,
            default=tk.ACTIVE,
        )
        w.pack(side=tk.LEFT, padx=5, pady=5)
        self.bind('<Return>', self.cancel)
        self.bind('<Escape>', self.cancel)
        box.pack()


class HangmanWordEntry(Dialog):
    def __init__(
        self,
        parent: tk.Toplevel | tk.Tk,
        max_len: int,
        word_var: tk.StringVar,
        prompt: str,
    ) -> None:
        self.max_len = max_len
        self.word_var = word_var
        self.prompt = prompt
        self.word_var.trace_add(
            'write',
            lambda *_: self.word_var.set(self.word_var.get().upper()),
        )
        super().__init__(parent, 'Provide a word')

    def body(self, parent: tk.Frame) -> ttk.Entry:
        self.resizable(False, False)
        word_label = ttk.Label(
            parent,
            text=self.prompt,
        )
        self.word_entry = ttk.Entry(
            parent,
            exportselection=False,
            textvariable=self.word_var,
            font=ttk.Style().configure('TButton')['font'],
        )
        self.word_entry.bind(
            '<Control-KeyRelease-a>',
            lambda *_: self.word_entry.select_range(0, tk.END),
        )
        word_label.grid(row=0, column=0)
        self.word_entry.grid(row=1, column=0)
        return self.word_entry

    def buttonbox(self) -> None:
        box = ttk.Frame(self)
        w = ttk.Button(
            box,
            text='Submit',
            width=10,
            command=self.ok,
        )
        w.pack(side=tk.LEFT, padx=5, pady=5)
        self.bind('<Return>', self.ok)
        self.bind('<Escape>', self.cancel)
        box.pack()

    def validate(self) -> bool:
        word = self.word_var.get()
        if not word:
            AcknowledgementDialogue(
                parent=self,
                title='Bad Word Entry',
                message='Word entered cannot be blank',
            )
            return False
        if not word.isalpha():
            AcknowledgementDialogue(
                parent=self,
                title='Bad Word Entry',
                message='Word entered can only contain letters [A-Z]',
            )
            return False
        if len(word) > self.max_len:
            AcknowledgementDialogue(
                parent=self,
                title='Bad Word Entry',
                message=f'Word can have at most {self.max_len} letters',
            )
            return False

        return True
