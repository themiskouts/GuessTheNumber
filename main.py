import random
import customtkinter as ctk

# 1. Ρυθμίσεις Εμφάνισης (Dark Mode & Θέμα)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# 2. Αρχικές Μεταβλητές Παιχνιδιού (Global Variables)
secret_number = 0
lives = 0
max_lives = 7
difficulty = "Medium"
low_range = 1
high_range = 100

# Λίστα για τα High Scores (Κρατάει τις λιγότερες προσπάθειες ανά επίπεδο)
high_scores = {"Easy": "-", "Medium": "-", "Hard": "-"}


# 3. Συναρτήσεις Λογικής (Functions)


def start_new_game():
    """Μηδενίζει το παιχνίδι και διαλέγει νέο αριθμό χωρίς να κλείσει το παράθυρο"""
    global secret_number, lives, max_lives, low_range, high_range
    secret_number = random.randint(low_range, high_range)
    lives = max_lives

    # Επαναφορά των Γραφικών
    entry_guess.delete(0, ctk.END)
    btn_submit.configure(state="normal")
    label_feedback.configure(
        text=f"Διάλεξα αριθμό από {low_range} έως {high_range}!\nΈχεις {lives} ζωές. Μάντεψε!",
        text_color="white",
    )
    update_score_label()


def set_difficulty(level):
    """Αλλάζει το επίπεδο δυσκολίας και τις ζωές"""
    global difficulty, max_lives, low_range, high_range
    difficulty = level

    if level == "Easy":
        low_range, high_range = 1, 50
        max_lives = 10
    elif level == "Medium":
        low_range, high_range = 1, 100
        max_lives = 7
    elif level == "Hard":
        low_range, high_range = 1, 500
        max_lives = 5

    # Αλλαγή χρωμάτων στα κουμπιά για να φαίνεται ποιο είναι επιλεγμένο
    btn_easy.configure(fg_color="#1f538d" if level == "Easy" else "gray")
    btn_medium.configure(fg_color="#1f538d" if level == "Medium" else "gray")
    btn_hard.configure(fg_color="#1f538d" if level == "Hard" else "gray")

    # Ξεκινάει αυτόματα νέο παιχνίδι με τη νέα δυσκολία
    start_new_game()


def update_score_label():
    """Ανανεώνει το κείμενο των High Scores στην οθόνη"""
    label_highscore.configure(
        text=f"🏆 High Scores ➡️ Easy: {high_scores['Easy']} | Medium: {high_scores['Medium']} | Hard: {high_scores['Hard']}"
    )


def check_guess(event=None):
    """Ελέγχει την πρόβλεψη του χρήστη (Λειτουργεί με κλικ ή με το Enter)"""
    global lives, secret_number, difficulty, max_lives

    # Αν το παιχνίδι έχει τελειώσει (κουμπί κλειδωμένο), μην κάνεις τίποτα
    if btn_submit.cget("state") == "disabled":
        return

    user_input = entry_guess.get()

    # Έλεγχος εγκυρότητας
    if not user_input.isdigit():
        label_feedback.configure(
            text="❌ Βάλε έναν σωστό αριθμό!", text_color="red"
        )
        return

    guess = int(user_input)
    lives -= 1
    tries_used = max_lives - lives  # Πόσες προσπάθειες ξόδεψε

    if guess < secret_number:
        if lives > 0:
            label_feedback.configure(
                text=f"⬆️ Πιο ψηλά! (Απομένουν {lives} ζωές)", text_color="cyan"
            )
        else:
            label_feedback.configure(
                text=f"💀 Game Over! Ο αριθμός ήταν το {secret_number}",
                text_color="red",
            )
            btn_submit.configure(state="disabled")
    elif guess > secret_number:
        if lives > 0:
            label_feedback.configure(
                text=f"⬇️ Πιο χαμηλά! (Απομένουν {lives} ζωές)",
                text_color="orange",
            )
        else:
            label_feedback.configure(
                text=f"💀 Game Over! Ο αριθμός ήταν το {secret_number}",
                text_color="red",
            )
            btn_submit.configure(state="disabled")
    else:
        # Παίκτης Κέρδισε
        btn_submit.configure(state="disabled")

        # Έλεγχος και καταγραφή High Score (λιγότερες προσπάθειες = καλύτερα)
        current_hs = high_scores[difficulty]
        if current_hs == "-" or tries_used < current_hs:
            high_scores[difficulty] = tries_used
            update_score_label()
            label_feedback.configure(
                text=f"🔥 ΝΕΟ ΡΕΚΟΡ! Το βρήκες σε μόλις {tries_used} προσπάθειες!",
                text_color="green",
            )
        else:
            label_feedback.configure(
                text=f"🎉 Το βρήκες! Χρειάστηκες {tries_used} προσπάθειες.",
                text_color="green",
            )


# 4. Δημιουργία και Ρύθμιση Παραθύρου
window = ctk.CTk()
window.title("Guess The Number - Ultimate Edition")
window.geometry("500x450")

# ΕΔΩ ΕΓΙΝΕ TRUE: Ο χρήστης μπορεί να το μεγαλώσει/μικρύνει όσο θέλει!
window.resizable(True, True)

try:
    window.after(200, lambda: window.iconbitmap("game_icon.ico"))
except:
    pass

# ΕΔΩ ΣΥΝΔΕΟΥΜΕ ΤΟ ΠΛΗΚΤΡΟ ENTER (<Return>) ΜΕ ΤΗ ΣΥΝΑΡΤΗΣΗ CHECK_GUESS
window.bind("<Return>", check_guess)

# 5. Στοιχεία Οθόνης (GUI Widgets)
label_title = ctk.CTkLabel(
    window, text="Μάντεψε τον Αριθμό", font=("Arial", 24, "bold")
)
label_title.pack(pady=15)

# Frame (κουτί) για τα κουμπιά δυσκολίας
frame_diff = ctk.CTkFrame(window)
frame_diff.pack(pady=5)

label_diff = ctk.CTkLabel(frame_diff, text="Δυσκολία:", font=("Arial", 12))
label_diff.grid(row=0, column=0, padx=10, pady=5)

btn_easy = ctk.CTkButton(
    frame_diff, text="Easy", width=70, command=lambda: set_difficulty("Easy")
)
btn_easy.grid(row=0, column=1, padx=5, pady=5)

btn_medium = ctk.CTkButton(
    frame_diff, text="Medium", width=70, command=lambda: set_difficulty("Medium")
)
btn_medium.grid(row=0, column=2, padx=5, pady=5)

btn_hard = ctk.CTkButton(
    frame_diff, text="Hard", width=70, command=lambda: set_difficulty("Hard")
)
btn_hard.grid(row=0, column=3, padx=5, pady=5)

# Label για τα High Scores
label_highscore = ctk.CTkLabel(
    window, text="", font=("Arial", 13, "italic"), text_color="#FFD700"
)
label_highscore.pack(pady=5)

# Κουτί Εισαγωγής
entry_guess = ctk.CTkEntry(
    window, width=180, placeholder_text="Γράψε αριθμό..."
)
entry_guess.pack(pady=15)

# Κουμπί Υποβολής
btn_submit = ctk.CTkButton(
    window, text="Υποβολή", font=("Arial", 14, "bold"), command=check_guess
)
btn_submit.pack(pady=5)

# ΚΟΥΜΠΙ RESTART (Επανεκκίνηση)
btn_restart = ctk.CTkButton(
    window,
    text="🔄 Παίξε Ξανά (Restart)",
    font=("Arial", 13, "bold"),
    fg_color="#27ae60",
    hover_color="#218c53",
    command=start_new_game,
)
btn_restart.pack(pady=10)

# Label Μηνυμάτων
label_feedback = ctk.CTkLabel(window, text="", font=("Arial", 14))
label_feedback.pack(pady=15)

# Εκκίνηση του παιχνιδιού με προεπιλογή το Medium
set_difficulty("Medium")

window.mainloop()