from zoautil_py import MVSCmd, Datasets
from zoautil_py.types import DDStatement
# Import os, needed to get the environment variables
import os

cc_contents = Datasets.read(os.getenv('USER')+".SOURCE.SUBHA") # Dataset to read the records from

# FUNCTION WRITE IN A FILE IN SPECIFIC ORDER
def writeFile(str1):
    output_dataset=os.getenv('USER')+".SOURCE.SUBHA" # dataset to write the record in
    str2=str1
    if Datasets.exists(output_dataset) != True:
        print ("Dataset Created")
        Datasets.create(output_dataset, "SEQ")
        str2="Details of Customers\nName                   Account No       Balance\n===================================\n" + str1
        #name 0-24 1 Acc 26-36 5 Bal 42-48
    Datasets.write(output_dataset, str2, append=True)

#FUNCTION TO CHECK THE HIGHEST AND LOWEST ACCOUMT BALANCE
def readFile():
    # cc_contents = Datasets.read(os.getenv('USER')+".SOURCE.SUBHA") # Dataset to read the records from
    cc_list = cc_contents.splitlines()
    y=0
    if (len(cc_list)==0):
        return ("No records")
    max_y=3
    min_y=3
    print("Lines:" + str(len(cc_list)))
    min_1 = int(cc_list[3][41:].strip())
    max_1 = int(cc_list[3][41:].strip())

    for y in range(4, len(cc_list)):
        present_1 = int(cc_list[y][41:].strip())
        if(present_1>max_1):
            max_1 = present_1
            max_y=y
        if(present_1<min_1):
            min_1 = present_1
            min_y=y
    x = [cc_list[max_y][0:].strip(), cc_list[min_y][0:].strip()]    
    return (x)

#FUNCTION TO VIEW DETAILS ON BASIS OF ACCOUNT NUMBER
def viewDetails(account_1):
    cc_list = cc_contents.splitlines()
    for i in range(len(cc_list)-1, 3, -1):
        if(account_1==cc_list[i][26:36]):
            return cc_list[i][0:].strip()
    return 0

while (True):
    print("\n1. Add Details\n2. Get Maximum and Minimun Balance\n3. View Details\n4. Update Balance\n5. Exit")
    options = input("Enter your choice: ")
    if (options=="1"):
        
        name = input("Enter the name [max 20 charecters]: ")
        if (len(name)>25):
            name=name[0:25]
        if(len(name)<25):
            name=name+(" "*(25-len(name)))
        
        acct = input("Enter the Account No [fixed 10 charecters]: ")
        if (len(acct)!=10):
            print("Invalid Account Number")
            break
        if (viewDetails(acct)!=0):
            print("Already have an account, please update")
            continue
        
        bal = input("Enter the balance [<1 Million]: ")
        if (bal.isnumeric()!=True and int(bal)<1000000):
            print("Wrong value or trying to add more than 1 million")
            break
        bal=bal

        print("Writing in the database")
        str1=name+" "+acct+"     "+bal
        writeFile(str1)
        cc_contents = Datasets.read(os.getenv('USER')+".SOURCE.SUBHA") # Dataset to read the records from
        print("Writing successful")

    if (options=="2"):
        str1 = readFile()
        print("\nMaximum:")
        print(str1[0])
        print("\nMinimum:")
        print(str1[1])

    if(options=="3"):
        account_1=input("Enter the Account number: ")
        print(viewDetails(account_1))
    
    if(options=="4"):
        account_1=input("Enter the Account number: ")
        details=viewDetails(account_1)
        if (details!=0):
            bal_add=input("Enter Balance to be deposited[<1 Million] : ")
            s = int(details[41:].strip())+int(bal_add)
            if (s<1000000):
                str1=details[0:25]+" "+account_1+"     "+str(s)
                print("Writing to the dataset")

                writeFile(str1)
                cc_contents = Datasets.read(os.getenv('USER')+".SOURCE.SUBHA") # Dataset to read the records from
                print("\nUpdated Balance:")
                print(viewDetails(account_1))
            else:
                print("Exceeding 1 Million")




    if (options=="5"):
        exit()

