from email.mime.text import MIMEText  # MIMEText reads the wanted file and transfers it to text for the email
from datetime import date  # Supplies classes for manipulating dates and times
import smtplib, sys  # SMTP is Simple Mail Transfer Protocol, SMTP comes built-in in Python. It establishes a safe connection to SMTP server which forwards the wanted message to email
import getpass  # getpass hides the password promt so it doesnt show it when you type in your password


def shoplist():

        shoppinglist_file = open("shoppinglist.txt", "a")
        shoppinglist_file.close()

        # Quitshop exits the program when turned true (when pressing option 9)
        quitshop = False

        # Program returns to menu everytime quitshop is false (option 9 is not pressed) and prints the current contents of the shoppinglist.txt -file
        while (quitshop == False):
            print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
            print("         Ostoslista          ")
            shoppinglist_file = open("shoppinglist.txt", "r")
            file_contents = shoppinglist_file.read()
            print(file_contents)
            print("_ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
            print(" ")
            shoppinglist_file.close()

            # Menu for app, clicking a number activates loop to check which statement to run
            print ("MENU:")
            print ("1 = add item to list")
            print ("2 = remove specific item")
            print ("3 = clear shoppinglist")
            print ("4 = send shoppinglist to email")
            print ("9 = quit")
            userchoice = input ("Choose an option (1-4 or 9): ")

            # Choice #1 adds items to the list typed by the user
            if (userchoice =="1"):
                additem = input ("Please enter an item you want to add: ")
                shoppinglist_file = open("shoppinglist.txt", "a")
                shoppinglist_file.write(additem + "\n")
                shoppinglist_file.close()

            # Choice #2 lets the user remove an item from the txt-file, doesnt require the file to be closed at the end. With - As does it automatically.
            elif (userchoice =="2"):
                item_string = input("Which item to remove? ")
                with open("shoppinglist.txt", "r") as f:
                    lines = f.readlines()
                with open("shoppinglist.txt", "w") as f:
                    for line in lines:
                        if line.strip("\n") != item_string:
                            f.write(line)

            # Choice #3 removes all the content from the txt-file
            elif (userchoice =="3"):
                open("shoppinglist.txt", "w").close()

            # Choice #4 sends the txt-file to a specified email
            elif (userchoice =="4"):

                # Add response for username password and store info locally
                SMTP_SERVER = "smtp.gmail.com"
                SMTP_PORT = 587
                usr = "USEREMAIL"

                # Connecting to SMTP server, gmail always requires port 587 to be used
                def passwordcheck(usr,psw):
                    server=smtplib.SMTP('smtp.gmail.com:587')
                    server.starttls()
                    try:
                        server.login(usr,psw)
                        ret = True
                    except:
                        ret = False
                    server.quit()
                    return ret

                # Gives 3 tries to input password, if password is incorrect the third time, the program ends
                for i in range(3):
                    psw = getpass.getpass("Enter Gmail Password: ")
                    if passwordcheck(usr,psw) is False:
                        print("Password was incorrect, try again.")
                        print("")
                    else:
                        print("Thank you. Password was correct.")
                        break

                # Fill out To/From/Subject fields
                EMAIL_TO = "RECEIVEREMAIL"
                EMAIL_FROM = "SENDEREMAIL"
                EMAIL_SUBJECT = "Ostoslista"

                # Date format to use in email subject-line
                DATE_FORMAT = "%d.%m.%Y"

                # Open log file and pull info
                LOG = open("shoppinglist.txt")
                DATA = LOG.read()

                # Send email function using smtplib
                def send_email():
                    msg = MIMEText(DATA)
                    LOG.close()
                    msg['Subject'] = EMAIL_SUBJECT + " %s" % (date.today().strftime(DATE_FORMAT))
                    msg['From'] = EMAIL_FROM
                    mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                    mail.starttls()
                    mail.login(usr, psw)
                    mail.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
                    mail.quit()

                # Main has to be determined like following or else the email wont be sent
                if __name__=='__main__':
                    send_email()
                    
                print("")
                print("*************************")
                print(" Email sent successfully ")
                print("*************************")

            # Choice #9 exits the program
            elif (userchoice =="9"):
                print("EXITTING PROGRAM")
                print("")
                quit
                quitshop = True

            # If none of the given options is pressed, an "error" text is printed and program loops to the start asking for a new input
            else:
                print("")
                print("****ERROR****")
                print("**try again**")

shoplist()