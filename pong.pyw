import tkinter as tk
import random
import math

class PongGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Pong Game")

        # Menu inicial
        self.create_menu()

    def create_menu(self):
        # Limpa qualquer widget anterior
        for widget in self.master.winfo_children():
            widget.destroy()

        # Criando o menu
        self.menu_canvas = tk.Canvas(self.master, width=600, height=400, bg="black")
        self.menu_canvas.pack()

        # Título do jogo
        self.menu_canvas.create_text(300, 100, text="PONG", font=("Arial", 40), fill="white")

        # Botão Jogar
        self.play_button = tk.Button(self.master, text="Jogar", font=("Arial", 20), command=self.start_game)
        self.play_button.place(x=260, y=200)

        # Botão Sair
        self.exit_button = tk.Button(self.master, text="Sair", font=("Arial", 20), command=self.master.quit)
        self.exit_button.place(x=270, y=250)

        # Créditos
        self.menu_canvas.create_text(300, 350, text="Criado por Kleber Klaar", font=("Arial", 12), fill="white")

    def start_game(self):
        # Limpa o menu e começa o jogo
        for widget in self.master.winfo_children():
            widget.destroy()

        self.canvas = tk.Canvas(self.master, width=600, height=400, bg="black")
        self.canvas.pack()

        # Criando as raquetes e a bolinha
        self.paddle_left = self.canvas.create_rectangle(30, 150, 40, 250, fill="white")
        self.paddle_right = self.canvas.create_rectangle(560, 150, 570, 250, fill="white")
        self.ball = self.canvas.create_oval(290, 190, 310, 210, fill="white")

        # Velocidades iniciais
        self.initial_x_speed = random.choice([-4, 4])
        self.initial_y_speed = random.choice([-3, 3])
        self.ball_x_speed = self.initial_x_speed
        self.ball_y_speed = self.initial_y_speed

        # Pontuação
        self.left_score = 0
        self.right_score = 0
        self.left_score_label = tk.Label(self.master, text=f"{self.left_score}", font=("Arial", 24), fg="white", bg="black")
        self.left_score_label.place(x=150, y=20)
        self.right_score_label = tk.Label(self.master, text=f"{self.right_score}", font=("Arial", 24), fg="white", bg="black")
        self.right_score_label.place(x=450, y=20)

        # Velocidade da bola
        self.speed_label = tk.Label(self.master, text="Velocidade da Bola: 0", font=("Arial", 12), fg="white", bg="black")
        self.speed_label.place(x=250, y=20)

        # Movimentação das raquetes
        self.paddle_speed = 20
        self.paddle_right_up = False
        self.paddle_right_down = False
        self.paddle_left_up = False
        self.paddle_left_down = False

        self.master.bind("<KeyPress>", self.key_press)
        self.master.bind("<KeyRelease>", self.key_release)

        # Loop principal
        self.game_loop()

    def game_loop(self):
        self.move_ball()
        self.check_collision()
        self.update_speed_display()
        self.move_paddles()  # Move as raquetes continuamente com base no estado das teclas

        self.master.after(30, self.game_loop)

    def move_ball(self):
        self.canvas.move(self.ball, self.ball_x_speed, self.ball_y_speed)
        ball_pos = self.canvas.coords(self.ball)

        # Verifica se a bolinha atingiu o topo ou a parte inferior
        if ball_pos[1] <= 0 or ball_pos[3] >= 400:
            self.ball_y_speed = -self.ball_y_speed

        # Verifica se a bolinha saiu do lado esquerdo ou direito (marcou ponto)
        if ball_pos[0] <= 0:
            self.right_score += 1
            self.right_score_label.config(text=f"{self.right_score}")
            self.reset_ball()

        if ball_pos[2] >= 600:
            self.left_score += 1
            self.left_score_label.config(text=f"{self.left_score}")
            self.reset_ball()

    def move_paddle_right_up(self):
        self.canvas.move(self.paddle_right, 0, -self.paddle_speed)

    def move_paddle_right_down(self):
        self.canvas.move(self.paddle_right, 0, self.paddle_speed)

    def move_paddle_left_up(self):
        self.canvas.move(self.paddle_left, 0, -self.paddle_speed)

    def move_paddle_left_down(self):
        self.canvas.move(self.paddle_left, 0, self.paddle_speed)

    def key_press(self, event):
        # Detecta quando uma tecla é pressionada
        if event.keysym == "Up":
            self.paddle_right_up = True
        elif event.keysym == "Down":
            self.paddle_right_down = True
        elif event.keysym == "w":
            self.paddle_left_up = True
        elif event.keysym == "s":
            self.paddle_left_down = True

    def key_release(self, event):
        # Detecta quando uma tecla é solta
        if event.keysym == "Up":
            self.paddle_right_up = False
        elif event.keysym == "Down":
            self.paddle_right_down = False
        elif event.keysym == "w":
            self.paddle_left_up = False
        elif event.keysym == "s":
            self.paddle_left_down = False

    def move_paddles(self):
        # Move as raquetes continuamente enquanto as teclas estiverem pressionadas
        if self.paddle_right_up:
            self.move_paddle_right_up()
        if self.paddle_right_down:
            self.move_paddle_right_down()
        if self.paddle_left_up:
            self.move_paddle_left_up()
        if self.paddle_left_down:
            self.move_paddle_left_down()

    def check_collision(self):
        ball_pos = self.canvas.coords(self.ball)
        paddle_left_pos = self.canvas.coords(self.paddle_left)
        paddle_right_pos = self.canvas.coords(self.paddle_right)

        # Verifica colisão com a raquete esquerda
        if ball_pos[0] <= paddle_left_pos[2] and ball_pos[1] < paddle_left_pos[3] and ball_pos[3] > paddle_left_pos[1]:
            self.ball_x_speed = -self.ball_x_speed
            self.increase_speed()

        # Verifica colisão com a raquete direita
        if ball_pos[2] >= paddle_right_pos[0] and ball_pos[1] < paddle_right_pos[3] and ball_pos[3] > paddle_right_pos[1]:
            self.ball_x_speed = -self.ball_x_speed
            self.increase_speed()

    def increase_speed(self):
        # Aumenta a velocidade em 0.1 após cada colisão com a raquete
        if self.ball_x_speed > 0:
            self.ball_x_speed += 0.5
        else:
            self.ball_x_speed -= 0.5

        if self.ball_y_speed > 0:
            self.ball_y_speed += 0.5
        else:
            self.ball_y_speed -= 0.5

    def reset_ball(self):
        # Reseta a posição da bolinha e sua velocidade
        self.canvas.coords(self.ball, 290, 190, 310, 210)
        self.ball_x_speed = self.initial_x_speed
        self.ball_y_speed = self.initial_y_speed

    def update_speed_display(self):
        # Calcula a velocidade total da bolinha
        current_speed = math.sqrt(self.ball_x_speed**2 + self.ball_y_speed**2)
        self.speed_label.config(text=f"Velocidade da Bola: {current_speed:.2f}")

root = tk.Tk()
game = PongGame(root)
root.mainloop()
