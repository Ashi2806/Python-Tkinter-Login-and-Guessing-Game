import random
from tkinter import *
import sqlite3

# Database setup
conn = sqlite3.connect("game.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS details(name varchar(20), phone varchar(10) UNIQUE, password varchar(6))")
cur.execute("CREATE TABLE IF NOT EXISTS scores(name TEXT, attempts INTEGER)")
conn.commit()

a = Tk()
a.geometry('400x300')
a.title('Login page')
Label(a, text="LOGIN ", fg='black', font='Arial 14 bold').place(x=110, y=10)

phone = StringVar()
Label(a, text="Phone number :").place(x=110, y=80)
Entry(a, textvariable=phone).place(x=215, y=80)

password = StringVar()
Label(a, text="Password :").place(x=110, y=110)
Entry(a, textvariable=password, show='*').place(x=215, y=110)

Button(a, text='sign in', command=lambda: check_login()).place(x=110, y=190)
Button(a, text='sign up', command=lambda: sign_up()).place(x=180, y=190)
# Login Page
def check_login():
    conn = sqlite3.connect("game.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM details WHERE phone=? AND password=?", (phone.get(), password.get()))
    result = cur.fetchone()
    conn.close()

    if result:
        a.withdraw()  # close login window
        play(result[0])   # Pass the user's name
    else:
        Label(a, text="Invalid login details, sign up to create a new account", fg="red").place(x=120, y=230)

# Sign_up Page
def sign_up():
    global cpassword, msg_label
    b = Toplevel()
    b.geometry('400x300')
    b.title('Sign up ')
    Label(b, text="Sign up ", fg='black', font='Arial 14 bold').place(x=110, y=10)

    s_name = StringVar()
    Label(b, text='Name :').place(x=110, y=40)
    Entry(b, textvariable=s_name).place(x=215, y=40)

    s_phone = StringVar()
    Label(b, text="Phone number :").place(x=110, y=80)
    Entry(b, textvariable=s_phone).place(x=215, y=80)

    s_password = StringVar()
    Label(b, text="Password :").place(x=110, y=110)
    Entry(b, textvariable=s_password, show='*').place(x=215, y=110)

    cpassword = StringVar()
    Label(b, text="Confirm Password:").place(x=110, y=140)
    Entry(b, textvariable=cpassword, show='*').place(x=215, y=140)

    Button(b, text='sign up', command=lambda: save_data(s_name, s_phone, s_password, b)).place(x=180, y=190)

    msg_label = Label(b, text="", fg="red")
    msg_label.place(x=80, y=240)

# Login/Sign_up details check up
def save_data(s_name, s_phone, s_password, b):
    phone_val = s_phone.get()
    pwd = s_password.get()

    if not phone_val.isdigit() or len(phone_val) != 10 or phone_val[0] in ['0','1','2','3','4','5']:
        msg_label.config(text="Phone must be 10 digits and start with 6-9", fg="red")
        return

    if len(pwd) < 6 or not any(i.isalpha() for i in pwd) or not any(i.isdigit() for i in pwd):
        msg_label.config(text="Password must have letters & numbers (min 6)", fg="red")
        return

    if pwd != cpassword.get():
        msg_label.config(text="Password Mismatch", fg="red")
        return

    conn = sqlite3.connect("game.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM details WHERE phone=?", (phone_val,))
    if cur.fetchone():
        msg_label.config(text="Account already exists", fg="red")
        conn.close()
        return

    cur.execute("SELECT * FROM details WHERE name=?", (s_name.get(),))
    if cur.fetchone():
        msg_label.config(text="Username already taken", fg="red")
        conn.close()
        return

    cur.execute("INSERT INTO details VALUES (?,?,?)", (s_name.get(), phone_val, pwd))
    conn.commit()
    conn.close()
    msg_label.config(text="Signup Successful", fg="green")

    b.destroy()  # close signup window after success

def leaderboard():
    conn = sqlite3.connect("game.db")
    cur = conn.cursor()
    cur.execute("SELECT name, MIN(attempts) FROM scores GROUP BY name ORDER BY MIN(attempts)")
    results = cur.fetchall()
    conn.close()

    lb = Toplevel()
    lb.geometry('400x300')
    lb.title('Leaderboard')
    Label(lb, text="Leaderboard", font=("Arial", 14, "bold")).pack(pady=10)

    for idx, (player, score) in enumerate(results, start=1):
        Label(lb, text=f"{idx}. {player} - {score} attempts", font=("Arial", 12)).pack()

# Game page
def play(name):
    p = Toplevel()
    p.geometry('500x500')
    p.title('Number Guessing Game')

    Label(p, text=f'Welcome {name}! Ready to play?', font=("Arial", 14)).place(x=16, y=30)

    lowest_num = IntVar()
    Label(p, text='Start').place(x=16, y=70)
    Entry(p, textvariable=lowest_num).place(x=80, y=70)

    highest_num = IntVar()
    Label(p, text='End').place(x=16, y=100)
    Entry(p, textvariable=highest_num).place(x=80, y=100)

    def start_game():
        start = lowest_num.get()
        end = highest_num.get()
        if start >= end:
            Label(p, text="Invalid range! End must be greater than Start.", fg="red").place(x=16, y=130)
            return

        answer = random.randint(start, end)
        guesses = {"count": 0}
        p.destroy()
        o = Toplevel()
        o.geometry('400x300')
        o.title('Play Game')

        Label(o, text=f'Guess a number between {start} and {end}').pack(pady=10)

        guess_var = IntVar()
        Entry(o, textvariable=guess_var).pack(pady=5)

        result_label = Label(o, text="")
        result_label.pack(pady=10)

        def check_guess():
            try:
                guess = int(guess_var.get())
                guesses["count"] += 1
                if guess < start or guess > end:
                    result_label.config(text=f"Out of range! ({start}-{end})", fg="red")
                elif guess < answer:
                    result_label.config(text="Too low! Try again.", fg="orange")
                elif guess > answer:
                    result_label.config(text="Too high! Try again.", fg="blue")
                else:
                    # Save score
                    conn = sqlite3.connect("game.db")
                    cur = conn.cursor()
                    cur.execute("INSERT INTO scores VALUES (?, ?)", (name, guesses["count"]))
                    conn.commit()
                    conn.close()

                    o.destroy()
                    c = Toplevel()
                    c.geometry('400x300')
                    c.title('Result')
                    Label(c, text=f"🎉 Correct! The answer is {answer}\nAttempts: {guesses['count']}",
                          font=("Arial", 12), fg="green").pack(pady=20)
                    Button(c, text="Play Again", command=lambda: [c.destroy(), play(name)]).pack(pady=10)
                    Button(c, text="View Leaderboard", command=leaderboard).pack(pady=10)
                    Button(c, text="Exit", command=lambda: [c.destroy(), a.destroy()]).pack(pady=10)
            except ValueError:
                result_label.config(text="Please enter a valid number.", fg="red")

        Button(o, text="Check", command=check_guess).pack(pady=5)
    Button(p, text='Start Game', command=start_game).place(x=20, y=150)
a.mainloop()