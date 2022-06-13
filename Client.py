import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = '127.0.0.1'
PORT = 9090


class Client:
    # maintenant on va défénir le constructeur de la class client pour initialiser le HOST et le Port

    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('127.0.0.1', 9090))

        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = simpledialog.askstring("Alias", "Choisissez votre Alias", parent=msg)

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)  # cette fonction n'est pas la même que celle dans le serveur

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):  # Front end, c'est just pour avoir une interface UI (GUI)
        self.win = tkinter.Tk()
        self.win.configure(bg="cyan")

        self.chat_label = tkinter.Label(self.win, text="Chat: ", bg="cyan")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')

        self.msg_label = tkinter.Label(self.win, text="Message: ", bg="cyan")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Envoyer", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True
        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()

    # envoie le text dans le input au serveur
    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    # recevoir le text
    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024)
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break

    # c'est pour tout arrêter
    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)


client = Client(HOST,PORT)
