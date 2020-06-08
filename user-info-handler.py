from flask import Flask, render_template, request, make_response, session, redirect, url_for
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def helloWorld():
        return "Hello, World!"
        
        
@app.route('/assignment11.html-account-info.txt')
def showAccountInfo():
    accountArray = [] 
    with open("assignment11.html-account-info.txt") as textFile:
        for line in textFile:
            accountArray.append(line) 
            accountArray.append("\n")
    accountsString = "\n".join(accountArray)
    return render_template("testing.html", textFile=accountsString)
    
@app.route('/assignment11.html-account-info-backup.txt') #change to original file 
def showAccountInfoBackup():
    accountArray = [] 
    with open("assignment11.html-account-info.txt") as textFile:
        for line in textFile:
            accountArray.append(line) 
            accountArray.append("\n")
    accountsString = "\n".join(accountArray)
    return render_template("testing.html", textFile=accountsString)


@app.route("/assignment11.html", methods=["GET", "POST"])
def assignment11():
    # If link is opened in new tab, make sure when info is edited on tab1, the info (when refreshed) is correctly edited on tab2 (sessions!)
    reset = False    
    unameValid = False
    pwordValid = False
    fnameValid = False
    lnameValid = False
    
    uname = ""
    pword = ""
    fname = ""
    lname = ""
    
    errorMessage = "No login attempted."
    errorColor = "red"
    
    backgroundColor = "white"
    titleBoi = "Welcome to Alan Torres' Assignment 11 web site!"
    imageURL = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Stick_Figure.svg/170px-Stick_Figure.svg.png"
    
    permaUname = ""
    permaPword = ""
            
    if "create" in request.args: 
        if "lname" in request.args:
            lname = request.args["lname"]
            if len(lname) != 0:
                lnameValid = True
            else:
                errorMessage="Please enter a last name."
                
        if "fname" in request.args:
            fname = request.args["fname"]
            if len(fname) != 0:
                fnameValid = True
            else:
                errorMessage = "Please enter a first name."    
                
        if "newpword" in request.args:
            pword = request.args["newpword"]
            if len(pword) != 0:
                pwordValid = True
            else:
                errorMessage = "Please enter valid password."
                    
        if "newuname" in request.args:
            uname = request.args["newuname"]
            if len(uname) != 0:
                unameValid = True
            else:
                errorMessage = "Please enter valid user name."
        if unameValid and pwordValid and fnameValid and lnameValid:
            #accountInfoText=open("assignment11.html-account-info.txt", "r") ????????????????????????????????????????????????????????????????????????????
            accountArray = [] 
            with open("assignment11.html-account-info.txt") as accountInfoText:
                for line in accountInfoText:
                    accountArray.append(line) #each element is string of info
            unameCheck = ""
            usernameTaken = False
            for n in range(0, len(accountArray)):
                unameCheck=""
                infoString = accountArray[n]
                for i in range(0, len(infoString)):
                    if infoString[i] == ";":
                        break
                    else:
                        unameCheck = unameCheck+infoString[i]
                if unameCheck == str(uname):
                    usernameTaken = True
                    unameCheck = ""
                    break
                    
            
            if usernameTaken == True:
                unameCheck= ""
                errorMessage="Can't create account. User '" + uname + "' already exists."
                return render_template("assignment11.html", uname=uname, pword=pword, fname=fname, lname=lname, errorMessage=errorMessage, errorColor=errorColor)
            else:
                permaUname = str(uname)
                permaPword = str(pword)
                accountInfoText=open("assignment11.html-account-info.txt", "a")
                accountInfoText.write(uname+";"+pword+";"+fname+";"+lname+";"+backgroundColor+";"+titleBoi+";"+imageURL+"\n")
                accountInfoText.close()
                updatedMessage = "Account for user '" + uname + "' successfully created."
                return render_template("createdNewAccount.html", uname=uname, pword=pword, fname=fname, lname=lname, backgroundColor=backgroundColor, titleBoi=titleBoi, imageURL=imageURL, updatedMessage=updatedMessage) #Patitz's site does not include uname....HOW?
        else:
            return render_template("assignment11.html", errorMessage=errorMessage, errorColor=errorColor)
            
    elif "editAccountInfo" in request.args: 
        editAccount = request.args["editAccountInfo"]
        if editAccount == "True":
            #accountInfoText=open("assignment11.html-account-info.txt", "r")
            accountArray = [] 
            with open("assignment11.html-account-info.txt") as accountInfoText:
                for line in accountInfoText:
                    accountArray.append(line)
            
            #NOW, gather new information into a string and replace it at the index where the user matches. 
            #Also erase the text file and fill it with new information 
            
            #if "uname" in request.args: # MAYBE THIS DOES NOT NEED TO BE HERE 
              #  uname = request.args["uname"] # MAYBE THIS DOES NOT NEED TO BE HERE 
                 
            if "fname" in request.args:
                fname = request.args["fname"]
    
            if "lname" in request.args:
                lname = request.args["lname"]
                
            if "backgroundColor" in request.args:
                backgroundColor = request.args["backgroundColor"]
            
            if "titleBoi" in request.args:
                titleBoi = request.args["titleBoi"]
                
            if "imageBoi" in request.args:
                imageURL = request.args["imageBoi"]
                
            uname = permaUname
            
            testUname = uname
            if "unameHere" in request.args:
                testUname = request.args["unameHere"]
            uname=testUname
            
            pword = permaPword
            pwordHere = pword
            if "pwordHere" in request.args:
                pwordHere = request.args["pwordHere"]
            pword = pwordHere
            
            #make new string with all new information 
            myNewInformationString = uname+";"+pword+";"+fname+";"+lname+";"+backgroundColor+";"+titleBoi+";"+imageURL+"\n" #PWORD MAY BE PROBLEMATIC
            
            #find index where username has all its information
            myUsernameString = ""
            correctIndex = False
            indexValue = 0
            
            for test in range(0, len(accountArray)):
                myInformationString = accountArray[test]
                for i in range(0, len(myInformationString)):
                    if myInformationString[i] == ';':
                        break
                    else:
                        myUsernameString = myUsernameString + myInformationString[i]
                if str(uname) == str(myUsernameString):
                    correctIndex = True
                    indexValue = test
                else:
                    myUsernameString = ""
                if correctIndex:
                    break
            
            #replace the user's information in accountArray[indexValue] with new information string
            accountArray[indexValue] = myNewInformationString      
            #accountArray now is array of strings: ["uname;pword;etc...",  "user;pass;etc..." , "pluto;pass2;fname;\n" ]
            
            #rewrite the account-info.txt file with new information 
            outF = open("assignment11.html-account-info.txt", "w+")
            for line in accountArray:
                outF.write(line)
            outF.close()
     
            unameHere = uname
            if "unameHere" in request.args:
                unameHere=request.args["unameHere"]
            
            pword = permaPword
            if "pwordHere" in request.args:
                pwordHere = request.args["pwordHere"]
                pword = pwordHere
                
            updatedMessage = "Account information for " + unameHere + " successfully edited."
            return render_template("createdNewAccount.html", uname=unameHere, pword=pword, fname=fname, lname=lname, backgroundColor=backgroundColor, titleBoi=titleBoi, imageURL=imageURL, updatedMessage=updatedMessage) #again, Patitz somehow does not have uname in the querry...HOW?

    elif "logout" in request.args:
        unameHereNew = ""
        if "unameGet" in request.args:
            unameHereNew = request.args["unameGet"]
        logOutMsg = unameHereNew + " has logged out"
        return render_template("assignment11.html", errorMessage=logOutMsg, errorColor="black")

    elif "returningUser" in request.args:
        if "uname" in request.args: 
            uname = request.args["uname"]
        if "pword" in request.args:
            pword = request.args["pword"]
            
        permaUname = uname        
        permaPword = pword
        
        #Check file if uname and pword are valid. If so, open createdNewAccount.html with their info.
        accountInfoText=open("assignment11.html-account-info.txt", "r")
        accountArray = [] 
        with open("assignment11.html-account-info.txt") as accountInfoText:
                for line in accountInfoText:
                    accountArray.append(line) 
        unameCheck=""
        pwordCheck=""
        usernameValid = False
        passwordValid = False
        bothValid = False
        correctIndex = 0
        
        for n in range(0, len(accountArray)):
            correctIndex = n
            unameCheck=""
            pwordCheck = ""
            infoString = accountArray[n]
            semiColonCounter = 0
            for i in range(0, len(infoString)):
                x = 1
                if infoString[i] == ";":
                   while infoString[i+x] != ";":
                       pwordCheck = pwordCheck + infoString[i+x]
                       x = x + 1 
                   break
                else:
                    unameCheck = unameCheck+infoString[i]
            if unameCheck == str(uname):
                usernameValid = True
            if pwordCheck == str(pword):
                passwordValid = True
            if usernameValid and passwordValid:
                bothValid = True
                break
        
        if bothValid:
            allVariablesString = accountArray[correctIndex]
            allVariablesArray = allVariablesString.split(";")
            uname = allVariablesArray[0]
            pword = allVariablesArray[1]
            fname = allVariablesArray[2]
            lname = allVariablesArray[3]
            backgroundColor = allVariablesArray[4]
            titleBoi = allVariablesArray[5]
            imageURL = allVariablesArray[6] 
            
            updatedMessage = "User " + uname + " successfully logged in."
            return render_template("createdNewAccount.html", uname=uname, pword=pword, fname=fname, lname=lname, backgroundColor=backgroundColor, titleBoi=titleBoi, imageURL=imageURL, updatedMessage=updatedMessage)
        else:
            pword = permaPword
            if "pwordHere" in request.args:
                pword = request.args["pwordHere"]
            return render_template("assignment11.html", uname=uname, pword=pword, fname=fname, lname=lname, errorMessage="User account not found.", errorColor=errorColor)
                

    return render_template("assignment11.html", errorMessage="No login attempted.", errorColor="black")

