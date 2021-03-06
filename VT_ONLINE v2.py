from tkinter import *
import tkinter.messagebox as tkMessageBox
import sqlite3
from tkinter import ttk

root = Tk()
root.title("Formulaire d'identification")

width = 540
height = 780
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)

# =======================================VARIABLES=====================================
LOGIN = StringVar()
PASSWORD = StringVar()
PRENOM = StringVar()
NOM = StringVar()
RUE = StringVar()
CODE = StringVar()
VILLE= StringVar()
TEL = StringVar()
EMAIL= StringVar()

# =======================================METHODS=======================================
def Database():
    global conn, cursor
    conn = sqlite3.connect("db_VTONLINE.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS user (users_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, login TEXT, password TEXT, prenom TEXT, nom TEXT, adresse TEXT, code INTEGER, ville TEXT, tel TEXT, email TEXT, type TEXT)")

def Exit():
    result = tkMessageBox.askquestion('System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()

def LoginForm():
    global LoginFrame, lbl_result1
    LoginFrame = Frame(root)
    LoginFrame.pack(side=TOP, pady=80)

    lbl_username = Label(LoginFrame, text="Login:", font=('arial', 25), bd=18)
    lbl_username.grid(row=1)
    lbl_password = Label(LoginFrame, text="Password:", font=('arial', 25), bd=18)
    lbl_password.grid(row=2)

    lbl_result1 = Label(LoginFrame, text="", font=('arial', 18))
    lbl_result1.grid(row=3, columnspan=2)

    username = Entry(LoginFrame, font=('arial', 20), textvariable=LOGIN, width=15)
    username.grid(row=1, column=1)
    password = Entry(LoginFrame, font=('arial', 20), textvariable=PASSWORD, width=15, show="*" )
    password.grid(row=2, column=1)

    btn_login = Button(LoginFrame, text="Login", font=('arial', 18), width=35, command=Login)
    btn_login.grid(row=4, columnspan=2, pady=20)

    lbl_register = Label(LoginFrame, text="S'enregistrer", fg="Blue", font=('arial', 22))
    lbl_register.grid(row=0, sticky=W)
    lbl_register.bind('<Button-1>', ToggleToRegister)


def RegisterForm():
    global RegisterFrame, lbl_result2
    RegisterFrame = Frame()
#    RegisterFrame.title("Registration")
    RegisterFrame.pack(side=TOP, pady=2)
    lbl_username = Label(RegisterFrame, text="Login:", font=('arial', 18), bd=18)
    lbl_username.grid(row=1)
    lbl_password = Label(RegisterFrame, text="Password:", font=('arial', 18), bd=18)
    lbl_password.grid(row=2)
    lbl_firstname = Label(RegisterFrame, text="Pr??nom:", font=('arial', 18), bd=18)
    lbl_firstname.grid(row=3)
    lbl_lastname = Label(RegisterFrame, text="Nom:", font=('arial', 18), bd=18)
    lbl_lastname.grid(row=4)
    lbl_adresse = Label(RegisterFrame, text="Rue + N??:", font=('arial', 18), bd=18)
    lbl_adresse.grid(row=5)
    lbl_code = Label(RegisterFrame, text="Code Postal :", font=('arial', 18), bd=18)
    lbl_code.grid(row=6)
    lbl_adresse = Label(RegisterFrame, text="Ville:", font=('arial', 18), bd=18)
    lbl_adresse.grid(row=7)
    lbl_code = Label(RegisterFrame, text="T??l??phone:", font=('arial', 18), bd=18)
    lbl_code.grid(row=8)
    lbl_email = Label(RegisterFrame, text="E-Mail or Website:", font=('arial', 18), bd=18)
    lbl_email.grid(row=9)

    lbl_result2 = Label(RegisterFrame, text="", font=('arial', 18))
    lbl_result2.grid(row=12, columnspan=2)

    username = Entry(RegisterFrame, font=('arial', 20), textvariable=LOGIN, width=15)
    username.grid(row=1, column=1)
    password = Entry(RegisterFrame, font=('arial', 20), textvariable=PASSWORD, width=15, show="*")
    password.grid(row=2, column=1)
    firstname = Entry(RegisterFrame, font=('arial', 20), textvariable=PRENOM, width=15)
    firstname.grid(row=3, column=1)
    lastname = Entry(RegisterFrame, font=('arial', 20), textvariable=NOM, width=15)
    lastname.grid(row=4, column=1)

    adresse = Entry(RegisterFrame, font=('arial', 20), textvariable=RUE, width=15)
    adresse.grid(row=5, column=1)
    code = Entry(RegisterFrame, font=('arial', 20), textvariable=CODE, width=15)
    code.grid(row=6, column=1)
    ville = Entry(RegisterFrame, font=('arial', 20), textvariable=VILLE, width=15)
    ville.grid(row=7, column=1)
    telephone = Entry(RegisterFrame, font=('arial', 20), textvariable=TEL, width=15)
    telephone.grid(row=8, column=1)
    email = Entry(RegisterFrame, font=('arial', 20), textvariable=EMAIL, width=15)
    email.grid(row=9, column=1)

    btn_login = Button(RegisterFrame, text="S'enregistrer", font=('arial', 18), width=35, command=RegisterUser)
    btn_login.grid(row=10, columnspan=2, pady=10)
    btn_login = Button(RegisterFrame, text="S'enregistrer en tant que professionel", font=('arial', 14), width=35, command=RegisterStaff)
    btn_login.grid(row=11, columnspan=2, pady=10)

    lbl_login = Label(RegisterFrame, text="Login", fg="Blue", font=('arial', 12))
    lbl_login.grid(row=0, sticky=W)
    lbl_login.bind('<Button-1>', ToggleToLogin)

def ToggleToLogin(event=None):
    RegisterFrame.destroy()
    LoginForm()

def ToggleToRegister(event=None):
    LoginFrame.destroy()
    RegisterForm()

# ============================ENREGISTREMENT DES DONNEES UTILISATEURS==========================
def RegisterUser():
    Database()
    if LOGIN.get == "" or PASSWORD.get() == "" or PRENOM.get() == "" or NOM.get == "":
        lbl_result2.config(text="Veuillez compl??ter le formulaire !", fg="orange")
    else:
        cursor.execute("SELECT * FROM user WHERE login = ?", (LOGIN.get(),))
        if cursor.fetchone() is not None:
            lbl_result2.config(text="Ce nom existe d??j??", fg="red")
        else:
            cursor.execute("INSERT INTO user (login, password, prenom, nom, adresse, code, ville, tel , email, type) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, 'user')",
                           (str(LOGIN.get()), str(PASSWORD.get()), str(PRENOM.get()), str(NOM.get()), str(RUE.get()), str(CODE.get()), str(VILLE.get()),str(TEL.get()), str(EMAIL.get())))
            conn.commit()
            LOGIN.set("")
            PASSWORD.set("")
            PRENOM.set("")
            NOM.set("")
            RUE.set("")
            CODE.set("")
            VILLE.set("")
            TEL.set("")
            EMAIL.set("")

            lbl_result2.config(text="Vous ??tes bien enregistr?? !", fg="black")
        cursor.close()
        conn.close()
# ============================ENREGISTREMENT DES DONNEES VETERINAIRES==========================
def RegisterStaff():
    Database()
    if LOGIN.get == "" or PASSWORD.get() == "" or PRENOM.get() == "" or NOM.get == "":
        lbl_result2.config(text="Veuillez compl??ter le formulaire !", fg="orange")
    else:
        cursor.execute("SELECT * FROM user WHERE login = ?", (LOGIN.get(),))
        if cursor.fetchone() is not None:
            lbl_result2.config(text="Ce nom existe d??j??", fg="red")
        else:
            cursor.execute("INSERT INTO user (login, password, prenom, nom, adresse, code, ville, tel , email, type) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, 'staff')",
                           (str(LOGIN.get()), str(PASSWORD.get()), str(PRENOM.get()), str(NOM.get()), str(RUE.get()), str(CODE.get()), str(VILLE.get()),str(TEL.get()), str(EMAIL.get())))
            conn.commit()
            lbl_result2.config(text="Vous ??tes bien enregistr?? en tant que Professionnel !", fg="black")
        cursor.close()
        conn.close()


############################################################################################
# ============================ OUVERTURE DE LA FENETRE UTILISATEUR==========================
############################################################################################
def utilisateur():
    win = Toplevel()
    win.title("Rechercher votre v??t??rinaire")
    win.geometry("800x900+350+70")
    win['bg'] = "orange"

    label_accueil1 = Label(win, text="Bienvenue sur VT_ONLINE", fg="white", bg="grey", font="Verdana 34")
    label_accueil1.grid(row=1, columnspan=4, sticky="W", padx=140, pady=10)

    label_accueil2 = Label(win, text="Choisissez votre sp??cialiste pr??s de chez vous", fg="black", font="Verdana 18")
    label_accueil2.grid(row=2, columnspan=4, sticky="W", padx=140, pady=20)

    # Les labels
    labelUn = Label(win, text="Votre animal ? ")
    labelUn.grid(row=3, column=1, sticky="E", pady=10)
    labelDeux = Label(win, text="Type de consultation:")
    labelDeux.grid(row=4, column=1, sticky="E", pady=10)
    labelTrois = Label(win, text="Votre code postal :")
    labelTrois.grid(row=5, column=1, sticky="E", pady=15)
    label4 = Label(win, text="Commentaires :")
    label4.grid(row=6, column=1, sticky="E", pady=15)

    # COMMENTAIRES
    frameC = Frame(win)
    frameC.grid(row=6, column=2, rowspan=2)
    comment = Entry(win)
    comment.grid(row=6, column=2)

    # =======================================LISTE DEROULANTE=====================================
    # Liste d??roulante animaux
    frame1 = Frame(win)
    frame1.grid(row=3, column=2)
    vlist1 = ["chien", "chat", "lapin", "chinchille", "gerbille", "souris", "d??gue du Chili", "furet", "poule",
              "caille", "canard", "oie", "cochon d'inde", "ch??vre", "ch??vre", "Perruche", "Perroquet", "Vache",
              "Mouton", "poisson", "ch??vre", "??ne", "autruche", "alpagua", "serpent", "Plusieurs animaux"]
    Combo1 = ttk.Combobox(frame1, values=vlist1)
    Combo1.set("Veuillez choisir")
    Combo1.pack()
    Combo1.bind('<<ComboboxSelected>>', lambda e: print(Combo1.get()))
    a = Combo1.get()

    # Liste d??roulante type de consultations
    frame2 = Frame(win)
    frame2.grid(row=4, column=2)
    vlist2 = ["Vaccination", "St??rilisation", "Vermifuge", "Radiographie", "Puce ??lectronique", "Visite ?? domicile",
              "Dentition", "Op??ration chirurgie", "Plusieurs animaux"]
    Combo2 = ttk.Combobox(frame2, values=vlist2)
    Combo2.set("Veuillez choisir")
    Combo2.pack()
    Combo2.bind('<<ComboboxSelected>>', lambda e: print(Combo2.get()))
    b = Combo2.get()

    # CODE POSTAUX : LISTE DEROULANTE
    frame3 = Frame(win)
    frame3.grid(row=5, column=2)
    conn = sqlite3.connect("db_VTONLINE.db")
    cursor = conn.cursor()

    cp = cursor.execute("SELECT code FROM user WHERE type ='staff'")
    codes = cp.fetchall()

    # vlist3 = [CP]
    Combo3 = ttk.Combobox(frame3, values=codes)
    Combo3.set("Veuillez choisir")
    Combo3.pack()
    Combo3.bind('<<ComboboxSelected>>', lambda e: print(Combo3.get()))

    # IMAGE VT
    width = 200
    height = 150
    imageVT1 = PhotoImage(file="Image1.png").zoom(35).subsample(32)
    canvas1 = Canvas(win, width=width, height=height, bg='orange', bd=0, highlightthickness=0)
    canvas1.create_image(width / 2, height / 2, image=imageVT1)
    canvas1.grid(row=3, column=3, rowspan=4, padx=50, pady=10)

    frame4 = Frame(win)
    frame4.grid(row=8, columnspan=4, rowspan=4, pady=15)

    frame5 = Frame(win)
    # frame5 ['bg'] = "orange"
    frame5.grid(row=12, columnspan=4, rowspan=4, pady=25, padx=15)

    ############################################################
    # RESULTATS de la requ??te
    ############################################################

    def RESULTS():
        global conn, cursor, codeP, Nom
        lbl0 = Label(frame4, text="Voici les v??t??rinaires de votre r??gion : ", fg="black", font="Verdana 18")
        lbl0.grid(row=1, column=2, pady=10, padx=10)
        codeP = Combo3.get()
        l = cursor.execute("SELECT nom, prenom FROM user WHERE type='staff' AND code = (?) ", [codeP])
        vetes = l.fetchall()
        Combo4 = ttk.Combobox(frame4, values=vetes, width=25)
        Combo4.set("Veuillez choisir")
        Combo4.grid(row=2, column=2, pady=10, padx=10)
        Combo4.bind('<<ComboboxSelected>>', lambda e: AFFICHE())

        def AFFICHE():
            Nom = Combo4.get()
            a = Combo1.get()
            b = Combo2.get()
            cursor.execute("SELECT adresse, code, ville, users_id, tel, email FROM user WHERE nom = ? AND prenom = ? ",
                           Nom.split(" "))
            rslt = cursor.fetchone()
            lbl1 = Label(frame5, text="Vous avez s??lectionn??", fg="blue", font="Verdana 18")
            lbl1.grid(row=3, column=2, columnspan=3, pady=10, padx=10)
            lbl2 = Label(frame5, text=f"{Nom} ", fg="grey", font="Verdana 18")
            lbl2.grid(row=4, column=2, pady=10, padx=10)
            lbl3 = Label(frame5, text=f"{rslt[0]} {rslt[1]} {rslt[2]}", fg="grey", font="Verdana 18")
            lbl3.grid(row=5, column=2, pady=10, padx=10)
            lbl4 = Label(frame5, text=("Pour votre " + a + " pour " + b), fg="black", font="Verdana 18")
            lbl4.grid(row=6, column=2, pady=10, padx=10)

            def REQUETE(user_id):
                vt = Toplevel()
                vt.title("Planing Consultation")
                vt.geometry("1250x800+100+0")
                vt.minsize(480, 360)
                vt['bg'] = "orange"

                lbl_titre = Label(vt, text="Bienvenue dans l'application VT_ONLINE", fg="white", bg="grey",
                                  font="Verdana 34")
                lbl_titre.pack()

                lbl1 = Label(vt, text="Voici les horaires de consultation de : " + Nom, fg="black", bg="orange",
                             font="Verdana 22")
                lbl1.place(x=50, y=100)
                lbl2 = Label(vt, text=f"{rslt[0]} ?? {rslt[1]} {rslt[2]} ", fg="grey", font="Verdana 18")
                lbl2.place(x=700, y=100)
                lbl3 = Label(vt, text=f"{rslt[4]} ", fg="grey", font="Verdana 18")
                lbl3.place(x=700, y=140)
                lbl4 = Label(vt, text=f"{rslt[5]} ", fg="grey", font="Verdana 18")
                lbl4.place(x=700, y=180)

                FrameL = Frame(vt)
                FrameL.pack(side=LEFT, pady=10, padx=150)

                lbl_sstitre = Label(vt, text="Choisissez vos jours de consultations et vos horaires", fg="black",
                                    bg="orange", font="Verdana 22")
                lbl_sstitre.place(x=60, y=220)

                label = Label(FrameL, text="  AM  -  PM      ", font=("Arial", 20), bg="grey", fg="white")
                label.grid(row=0, column=2, columnspan=4, pady=10, padx=18)

                lbl1 = Label(FrameL, text="LUNDI", fg="black", font="Verdana 18")
                lbl1.grid(row=1, column=1, pady=10, padx=10)
                lbl2 = Label(FrameL, text="MARDI", fg="black", font="Verdana 18")
                lbl2.grid(row=2, column=1, pady=10, padx=10)
                lbl3 = Label(FrameL, text="MERCREDI", fg="black", font="Verdana 18")
                lbl3.grid(row=3, column=1, pady=10, padx=10)
                lbl4 = Label(FrameL, text="JEUDI", fg="black", font="Verdana 18")
                lbl4.grid(row=4, column=1, pady=10, padx=10)
                lbl5 = Label(FrameL, text="VENDREDI", fg="black", font="Verdana 18")
                lbl5.grid(row=5, column=1, pady=10, padx=10)

                lundi = (
                    cursor.execute(
                        "SELECT debut_AM, fin_AM, debut_PM,fin_PM FROM horaire WHERE (jour,users_id) = (?,?) ",
                        ("LUNDI", user_id)).fetchone())
                mardi = (
                    cursor.execute(
                        "SELECT debut_AM, fin_AM, debut_PM,fin_PM FROM horaire WHERE (jour,users_id) = (?,?) ",
                        ("MARDI", user_id)).fetchone())
                mercredi = (
                    cursor.execute(
                        "SELECT debut_AM, fin_AM, debut_PM,fin_PM FROM horaire WHERE (jour,users_id) = (?,?) ",
                        ("MERCREDI", user_id)).fetchone())
                jeudi = (
                    cursor.execute(
                        "SELECT debut_AM, fin_AM, debut_PM,fin_PM FROM horaire WHERE (jour,users_id) = (?,?) ",
                        ("JEUDI", user_id)).fetchone())
                vendredi = (
                    cursor.execute(
                        "SELECT debut_AM, fin_AM, debut_PM,fin_PM FROM horaire WHERE (jour,users_id) = (?,?) ",
                        ("VENDREDI", user_id)).fetchone())

                lbl6 = Label(FrameL, text="", fg="black", font="Verdana 18")
                lbl6.grid(row=1, column=2, pady=10, padx=10)
                lbl6.config(text=f"{lundi[0]} {lundi[1]}    -   {lundi[2]} {lundi[3]} ")

                lbl7 = Label(FrameL, text="", fg="black", font="Verdana 18")
                lbl7.grid(row=2, column=2, pady=10, padx=10)
                lbl7.config(text=mardi)

                lbl8 = Label(FrameL, text="", fg="black", font="Verdana 18")
                lbl8.grid(row=3, column=2, pady=10, padx=10)
                lbl8.config(text=mercredi)

                lbl9 = Label(FrameL, text="", fg="black", font="Verdana 18")
                lbl9.grid(row=4, column=2, pady=10, padx=10)
                lbl9.config(text=jeudi)

                lbl10 = Label(FrameL, text="", fg="black", font="Verdana 18")
                lbl10.grid(row=5, column=2, pady=10, padx=10)
                lbl10.config(text=vendredi)

                frameR = Frame(vt)
                frameR.pack(side=RIGHT)
                width = 500
                height = 300
                imageVT2 = PhotoImage(file="Image3.png").zoom(10).subsample(10)
                canvas1 = Canvas(frameR, width=width, height=height, bg='orange', bd=0, highlightthickness=0)
                canvas1.create_image(width / 2, height / 2, image=imageVT2)
                canvas1.pack(pady=10, padx=10)

                vt.mainloop()

            button_voir = Button(frame5, text="Prendre rendez-vous", command=lambda: REQUETE(rslt[3]), fg="blue",
                                 font="Verdana 12", bd=2,
                                 bg="light blue", relief="groove")
            button_voir.grid(row=4, column=3, padx=15, pady=10)

            width = 100
            height = 100
            imageVT2 = PhotoImage(file="sihouette.png").zoom(10).subsample(10)
            canvas2 = Canvas(frame5, width=width, height=height, bg='grey', bd=1, highlightthickness=1)
            canvas2.create_image(width / 2, height / 2, image=imageVT2)
            canvas2.grid(row=3, column=1, rowspan=5, pady=10, padx=20)

            # frameB = Frame(win)
            # frameB.pack(side=BOTTOM, pady=10, padx=10)
            # width = 500
            # height = 200
            # imageVT2 = PhotoImage(file="Image4.png").zoom(15).subsample(10)
            # canvas2 = Canvas(frameB, width=width, height=height, bg='grey', bd=1, highlightthickness=1)
            # canvas2.create_image(width / 2, height / 2, image=imageVT2)
            # canvas2.grid(row=1, column=1, rowspan=4, pady=10, padx=20)





    button_valider = Button(win, text="Valider", command=RESULTS, fg="blue", font="Verdana 16", bd=2, bg="light blue",
                            relief="groove")
    button_valider.grid(row=7, column=3, padx=15)

    win.mainloop()



############################################################################################
# ============================ OUVERTURE DE LA FENETRE VETERINAIRE==========================
############################################################################################

def staff():
    vt = Toplevel()
    vt.title("Planing Consultation")
    vt.geometry("1250x800+100+0")
    vt.minsize(480, 360)
    vt['bg'] = "orange"

    lbl_titre = Label(vt, text="Bienvenue dans l'application VT_ONLINE", fg="white", bg="grey", font="Verdana 34")
    lbl_titre.pack(pady=10)
    lbl2 = Label(vt, text="", fg="grey", font="Verdana 18")
    lbl2.pack(pady=10)

    ######################################
    # RECUPERATION DU LOGIN DU VETERINAIRE
    ######################################

    # cursor.execute("SELECT prenom,nom FROM user WHERE login = ?", LOGIN)
    # reslt = cursor.fetchone()
    # print(reslt)
    # lbl2.config(text=f"Bonjour {reslt[0]}{reslt[1]}")


    #######################################
    # IMAGE
    ######################################
    frameR = Frame(vt)
    frameR.pack(side=RIGHT)
    width = 500
    height = 300
    imageVT2 = PhotoImage(file="Image3.png").zoom(10).subsample(10)
    canvas1 = Canvas(frameR, width=width, height=height, bg='orange', bd=0, highlightthickness=0)
    canvas1.create_image(width / 2, height / 2, image=imageVT2)
    canvas1.pack(padx=20)

    #######################################
    # GRILLE HORAIRES
    ######################################
    FrameL = Frame(vt)
    FrameL.pack(side=LEFT, pady=0, padx=50)

    lbl_sstitre = Label(vt, text="Choisissez vos jours de consultations et vos horaires", fg="black", bg="orange",
                        font="Verdana 22")
    lbl_sstitre.place(x=40, y=200)

    label = Label(FrameL, text="                 AM                      PM                 ", font=("Arial", 20),
                  bg="grey", fg="white")
    label.grid(row=0, column=2, columnspan=4, pady=10, padx=18)

    lbl1 = Label(FrameL, text="LUNDI", fg="black", font="Verdana 18")
    lbl1.grid(row=1, column=1, pady=10, padx=10)
    lbl2 = Label(FrameL, text="MARDI", fg="black", font="Verdana 18")
    lbl2.grid(row=2, column=1, pady=10, padx=10)
    lbl3 = Label(FrameL, text="MERCREDI", fg="black", font="Verdana 18")
    lbl3.grid(row=3, column=1, pady=10, padx=10)
    lbl4 = Label(FrameL, text="JEUDI", fg="black", font="Verdana 18")
    lbl4.grid(row=4, column=1, pady=10, padx=10)
    lbl5 = Label(FrameL, text="VENDREDI", fg="black", font="Verdana 18")
    lbl5.grid(row=5, column=1, pady=10, padx=10)

    ######### Les Entr??es pour les heures de consultations
    # LUNDI
    e1 = Entry(FrameL, font=('arial', 20), width=5)
    e1.grid(row=1, column=2, pady=10, padx=10)
    e2 = Entry(FrameL, font=('arial', 20), width=5)
    e2.grid(row=1, column=3, pady=10, padx=10)
    e3 = Entry(FrameL, font=('arial', 20), width=5)
    e3.grid(row=1, column=4, pady=10, padx=10)
    e4 = Entry(FrameL, font=('arial', 20), width=5)
    e4.grid(row=1, column=5, pady=10, padx=10)
    # MARDI
    e5 = Entry(FrameL, font=('arial', 20), width=5)
    e5.grid(row=2, column=2, pady=10, padx=10)
    e6 = Entry(FrameL, font=('arial', 20), width=5)
    e6.grid(row=2, column=3, pady=10, padx=10)
    e7 = Entry(FrameL, font=('arial', 20), width=5)
    e7.grid(row=2, column=4, pady=10, padx=10)
    e8 = Entry(FrameL, font=('arial', 20), width=5)
    e8.grid(row=2, column=5, pady=10, padx=10)
    # MERCREDI
    e9 = Entry(FrameL, font=('arial', 20), width=5)
    e9.grid(row=3, column=2, pady=10, padx=10)
    e10 = Entry(FrameL, font=('arial', 20), width=5)
    e10.grid(row=3, column=3, pady=10, padx=10)
    e11 = Entry(FrameL, font=('arial', 20), width=5)
    e11.grid(row=3, column=4, pady=10, padx=30)
    e12 = Entry(FrameL, font=('arial', 20), width=5)
    e12.grid(row=3, column=5, pady=10, padx=30)
    e13 = Entry(FrameL, font=('arial', 20), width=5)
    # JEUDI
    e13.grid(row=4, column=2, pady=10, padx=30)
    e14 = Entry(FrameL, font=('arial', 20), width=5)
    e14.grid(row=4, column=3, pady=10, padx=30)
    e15 = Entry(FrameL, font=('arial', 20), width=5)
    e15.grid(row=4, column=4, pady=10, padx=30)
    e16 = Entry(FrameL, font=('arial', 20), width=5)
    e16.grid(row=4, column=5, pady=10, padx=10)
    # VENDREDI
    e17 = Entry(FrameL, font=('arial', 20), width=5)
    e17.grid(row=5, column=2, pady=10, padx=10)
    e18 = Entry(FrameL, font=('arial', 20), width=5)
    e18.grid(row=5, column=3, pady=10, padx=10)
    e19 = Entry(FrameL, font=('arial', 20), width=5)
    e19.grid(row=5, column=4, pady=10, padx=10)
    e20 = Entry(FrameL, font=('arial', 20), width=5)
    e20.grid(row=5, column=5, pady=10, padx=10)

    ###########################################
    # Connexion ?? la base de donn??es


    def VALIDATE(users_id):

        jour1 = "LUNDI"
        a, b, c, d = e1.get(), e2.get(), e3.get(), e4.get()
        jour2 = "MARDI"
        e, f, g, h = e5.get(), e6.get(), e7.get(), e8.get()
        jour3 = "MERCREDI"
        i, j, k, l = e9.get(), e10.get(), e11.get(), e12.get()
        jour4 = "JEUDI"
        m, n, o, p = e13.get(), e14.get(), e15.get(), e16.get()
        jour5 = "VENDREDI"
        q, r, s, t = e17.get(), e18.get(), e19.get(), e20.get()

        ## Communication avec la base de donn??es
        cursor.execute("INSERT INTO horaire (users_id, jour,debut_AM, fin_AM, debut_PM, fin_PM) VALUES(?,?,?,?,?,?)",
                       (users_id, jour1, a, b, c, d))
        cursor.execute("INSERT INTO horaire (users_id, jour,debut_AM, fin_AM, debut_PM, fin_PM) VALUES(?,?,?,?,?,?)",
                       (users_id, jour2, e, f, g, h))
        cursor.execute("INSERT INTO horaire (users_id, jour,debut_AM, fin_AM, debut_PM, fin_PM) VALUES(?,?,?,?,?,?)",
                       (users_id, jour3, i, j, k, l))
        cursor.execute("INSERT INTO horaire (users_id, jour,debut_AM, fin_AM, debut_PM, fin_PM) VALUES(?,?,?,?,?,?)",
                       (users_id, jour4, m, n, o, p))
        cursor.execute("INSERT INTO horaire (users_id, jour,debut_AM, fin_AM, debut_PM, fin_PM) VALUES(?,?,?,?,?,?)",
                       (users_id, jour5, q, r, s, t))
        conn.commit()

    lbl = Label(vt, text="Voulez-vous enregistrer vos modifications ?", fg="black", bg="orange", font="Verdana 24")
    lbl.place(x=60, y=640)
    button_valider = Button(vt, text="Valider", command=VALIDATE, fg="black", font="Verdana 20", bd=2, bg="light blue",
                            relief="groove")
    button_valider.place(x=700, y=640)

    vt.mainloop()


# ============================ VERIFICATION DU LOGIN ET DU MOT DE PASSE ==========================
def Login():
    Database()
    if LOGIN.get == "" or PASSWORD.get() == "":
        lbl_result1.config(text="Veuiller compl??tez le formulaire : Login et/ou mot de passe manquant", fg="orange")
    else:
        cursor.execute("SELECT * FROM user WHERE login = ? and password = ?",
                       (LOGIN.get(), PASSWORD.get()))

        if cursor.fetchone() is not None:
            lbl_result1.config(text="Identification REUSSIE", fg="green")
            l = cursor.execute("SELECT type FROM user WHERE login=? AND password = ?",
                               (LOGIN.get(), PASSWORD.get()))
            us = l.fetchone()
            if us [0]== "user":
                utilisateur()
            else :
                staff()
        else:
            lbl_result1.config(text="Mot de passe et/ou login invalides", fg="red")

LoginForm()

# ========================================MENUBAR WIDGETS==================================
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=Exit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)

# ========================================INITIALIZATION===================================
if __name__ == '__main__':
    root.mainloop()
