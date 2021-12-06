# program for a small business to manage tasks
from datetime import datetime

today = datetime.today() # fetches todays date see: https://www.programiz.com/python-programming/datetime/current-datetime
date_today = today.strftime("%d %b %Y") # formats it to: 13 Oct 1977
login = False
correct_name = False
administrator = False # set admin priveleges off by default
username_list = []
password_list = []
user_index = -1 # set to out of bounds as default
user_name = ""

def reg_user():
    # two booleans admin, and unique_id control access to user registration
    unique_id = False
    if administrator:
        while not unique_id: 
            new_user = input("Please enter a new username: ")
            new_pass = input("Please enter a new password: ")
            confirm_pass = input("Please confirm your password: ")
            
            if username_list.count(new_user) == 0:
                unique_id = True
                # if the pass matches - copy the old file to a string, update string - overwrite to file
                if new_pass == confirm_pass:
                    # build a string of existing credentials
                    credentials = "" 
                    f = open('user.txt','r')
                    
                    for line in f:
                        credentials += line
                    f.close
                    
                    # write new string to file
                    f = open('user.txt', 'w')           
                    credentials += (f"\n{new_user}, {new_pass}") 
                    f.write(credentials)
                    f.close()

                    print("registration succesful!")
                
                else:
                    print("registration unsuccesful!, passwords did not match!")
            
            else:
                print("Error: Username already exists!")

    else:
        print("Only administrators have this privilege")

    return 

def add_task():
    task_doer = input("Please enter the username of the person undertaking the task: ") 
    task_title = input("Please enter the title of the task: ") 
    task_description = input("Please enter a description of the task: ")
    task_deadline = input("Please enter the deadline of the task: ")
    task_completion = "No"
    
    # lets read in the existing task file and copy it to a string
    all_tasks = ""
    f = open('tasks.txt','r')
    
    for line in f:
        all_tasks += line
    f.close()

    # lets write new string to file
    f = open('tasks.txt','w')
    all_tasks += (f"\n{task_doer}, {task_title}, {task_description}, {date_today}, {task_deadline}, {task_completion}")
    f.write(all_tasks)
    f.close()
    
    print("Task entered succesfully")   
    return

def view_all():
    #lets create a 2d list of the tasks: [[task1],[task2]...] where [task1] = [[task][info]...]
    task_list = []
        
    f = open('tasks.txt', 'r')
    task_string = f.readlines()
        
    # formats the string, appends to list, prints output
    for task in task_string:
        task = task.strip()
        task = task.split(', ')
        task_list.append(task)
        # this creates a 2d array with this key:
        task_display = "" 
        task_doer = task[0]
        task_title = task[1]  
        task_description = task[2]
        date_today = task[3]
        task_deadline = task[4]
        task_completion = task[5]

        task_display += (
            f"#############################################################\n"
            f"\n"
            f"Task:                   {task_title}\n"
            f"Assigned to:            {task_doer}\n"
            f"Date Assigned:          {date_today}\n"
            f"Due date:               {task_deadline}\n"
            f"Task Complete?          {task_completion}\n"
            f"Task description:\n"
            f"  {task_description}\n"
        )
        print(task_display)
    f.close()
    return

def view_mine():
    task_list = []
    f = open('tasks.txt', 'r')
    task_string = f.readlines()
    
    for count, task in enumerate(task_string):
        # string formatting
        task = task.strip()
        task = task.split(', ')
        task_list.append(task)
        # display params
        task_display = "" 
        task_doer = task[0]
        task_title = task[1]  
        task_description = task[2]
        date_today = task[3]
        task_deadline = task[4]
        task_completion = task[5]

        task_display += (
            f"#############################################################\n"
            f"Task ID: {count + 1}\n"
            f"\n"
            f"Task:                   {task_title}\n"
            f"Assigned to:            {task_doer}\n"
            f"Date Assigned:          {date_today}\n"
            f"Due date:               {task_deadline}\n"
            f"Task Complete?          {task_completion}\n"
            f"Task description:\n"
            f"  {task_description}\n"
        )
        if user_name == task[0]:
            print(task_display)
            
    f.close()
    user_task = input(
        f"###################\n"
        f"Options\n"
        f"- you may select a specific task by entering its Task ID\n"
        f"OR\n"
        f"- enter '-1' to exit\n"
    )
    if user_task != '-1':
        user_input = input(
            f"you have selected the following task: {task_list[int(user_task) - 1][1]}\n"
            f"You may either\n"
            f"(a) - mark the task as complete\n"
            f"(b) - edit the task\n"
        )
        if user_input == 'a':
            # we need to edit the list first, then write
            task_list[int(user_task) - 1][5] = "Yes"
            print("task succesfully marked as complete!")
        
        if user_input == 'b':
            if task_list[int(user_task) - 1][5] == 'No':
                user_input = input(
                    f"You may either edit:\n"
                    f"(a) - the assignee of the task\n"
                    f"OR\n"
                    f"(b) - the due date of the task\n"
                )
                if user_input == 'a':
                    new_task_doer = input("please enter a new task assignee: ")
                    task_list[int(user_task) - 1][0] = new_task_doer
                    print("task succesfully given new assignee!")

                if user_input == 'b':
                    new_due_date = input("Please enter a new due date(e.g. '10 Oct 2022'): ")
                    task_list[int(user_task) - 1][4] = new_due_date
                    print("task succesfully given a new due date!")
            else:
                print("task already completed")
        # read in all tasks again with updated values
        all_tasks = ""
        for task in task_list:
            for detail in task:
                all_tasks += detail + "," + " "
            all_tasks = all_tasks[:-2]    # removes trailing comma + space in a line
            all_tasks += "\n"

        # write to file
        with open('tasks.txt', 'w') as f:
            f.write(all_tasks)
    else:
        return
    return

def generate_report():
    # this function creates two
    tot_task = 0
    tot_complete = 0
    tot_incomplete = tot_task - tot_complete
    tot_overdue = 0

    task_list = []
    
    with open('tasks.txt', 'r') as f:
        # populates our task list with correct indexing
        for task in f:
            task = task.strip()
            task = task.split(', ')
            task_list.append(task)
    
    # count tasks
    for task in task_list:
        tot_task += 1

        if task[5] == 'Yes':
            tot_complete += 1
        if task[5] == 'No':
            tot_incomplete += 1
        # compare dates to see if overdue and incomplete
        if (datetime.strptime(task[4],"%d %b %Y") < today) and (task[5] == 'No'):
            tot_overdue += 1
    
    # build the report     
    task_report = (
        f"Total number of tasks:            {tot_task}\n"
        f"Completed tasks:                  {tot_complete}\n"
        f"Incomplete tasks:                 {tot_incomplete}\n"
        f"Total overdue:                    {tot_overdue}\n"
        f"percentage of incomplete tasks:   {round((tot_incomplete/tot_task*100), 2)}%\n"
        f"percentage of overdue tasks:      {round((tot_overdue/tot_task*100), 2)}%"
    )
    
    # write to file
    with open('task_overview.txt', 'w') as f:
        f.write(task_report)

    # now lets generate the second report
    user_report = ""
    #iterate through each user and build a report
    for user in username_list:
        task_assigned = 0
        task_complete = 0
        task_overdue = 0
        
        # iterate each task - check for tasks assigned, overdue etc and update variables above
        for task in task_list:
            if user == task[0]:
                task_assigned += 1
                if task[5] == 'Yes':
                    task_complete += 1
                elif (task[5] == 'No') and (datetime.strptime(task[4],"%d %b %Y") < today):
                    task_overdue += 1
        
        #calculations for user percentages            
        percent_ta = round((task_assigned / tot_task * 100), 2)
        # the next variables may induce float division errors so we check for it
        if task_assigned != 0:
            percent_tc = round((task_complete / task_assigned * 100), 2)
            percent_to = round((task_overdue / task_assigned * 100), 2) 
        else:
            percent_tc = 0
            percent_to = 0
        
        percent_ti = 100 - percent_tc   
        
        # we will build a report with the following format: 
        # {name}, {task_assigned}, {task_complete}, {task_overdue} 
        user_report += (
            f"{user}, {task_assigned}, {percent_ta}, {percent_tc}, {percent_ti}, {percent_to}\n"
            )
    # now lets write the report to file
    with open('user_overview.txt', 'w') as f:
        f.write(user_report)
                    
    return

def display_statistics():
    # first generate the report wether or not ithasnt already been called
    generate_report()
    # variables to count users, tasks
    tot_task = num_lines = sum(1 for line in open('tasks.txt'))  
    tot_user = num_lines = sum(1 for line in open('user.txt'))
    
    # The beginning of the overall statistics page
    combined_report = (
        f"####################################################\n"
        f"Task Overview\n"
        f"####################################################\n" 
    )

    # add the task overview to the combined report
    with open('task_overview.txt', 'r') as f:
        combined_report += f.read() + "\n"

    #add an interstitial to seperate the task overview from the user overview
    combined_report += (
        f"####################################################\n"
        f"User Overview\n"
        f"####################################################\n"
        f"Total number of registered users:         {tot_user}\n"
        f"Total number of tasks tracked:            {tot_task}\n"
        f"----------------------------------------------------\n"
        f"User Reports\n"
        f"----------------------------------------------------\n"
    )

    # add the user overview to the combined report
    with open('user_overview.txt', 'r') as f:
        # iterate through each user and addd to combined report
        # user[0] = username, [1] = tasks assigned, [2] = incomplete, [overdue]
        for user in f:
            user = user.strip()
            user = user.split(', ')
            combined_report += user[0] + "\n"
            combined_report += (
                f"Tasks Assigned:                           {user[1]}\n"
                f"Percentage of tasks assigned to user:     {user[2]}%\n"
                f"Percentage of tasks completed:            {user[3]}%\n"
                f"Percentage of incomplete tasks:           {user[4]}%\n"
                f"Percentage of unfinished, overdue tasks:  {user[5]}%\n"
                f"----------------------------------------------------\n"
            )
    print(combined_report)
    return
    

# keep prompting the user to login in a while loop until both valid usernames and passwords
while not login:
    #this logic runs until it determines you have entered a valid username
    while not correct_name:
        user_name = input("Please enter your username: ")
        f = open('user.txt','r')
        
        # first lets read in the user file to username_list
        for line in f:
            user_cred = line.split(', ')
            username_list.append(user_cred[0])
        
        f.close()

        # now lets check if the username matched what we have on file
        for names in username_list:
            if user_name == names:
                user_index = username_list.index(user_name)
                correct_name = True 
            
        if not correct_name:        
            print("you have entered an incorrect username!")
    
    user_pass = input("Please enter your password: ")
    
    f = open('user.txt','r')
    
    # first lets read in the user file to password_list
    for line in f:
        user_cred = line.strip() # removes pesky newline chars
        user_cred = user_cred.split(', ') # splits contents to a list
        password_list.append(user_cred[1])
    
    f.close()

    # now lets check if the user entered the appropriate password - we saved the user_index for this
    if user_pass == password_list[user_index]:
        # check to see if user has admin status
        if user_name == "admin": 
            administrator = True
        print("You have succesfully signed in!")
        login = True
    else:
        print("your username was correct but your password wasn't!")
        
while login:
    if administrator:
        user_input = input(
            f"Please select one of the following options:\n"
            f"r -  register user\n"
            f"a -  add task\n"
            f"va - view all tasks\n"
            f"vm - view my tasks\n"
            f"gr - generate reports\n"
            f"ds - display statistics\n"
            f"e -  exit\n"
        ).lower()
    else:
        user_input = input(
            f"Please select one of the following options:\n"
            f"r -  register user\n"
            f"a -  add task\n"
            f"va - view all tasks\n"
            f"vm - view my tasks\n"
            f"e -  exit\n"
        ).lower()

    # register a new user by appending to user.txt
    if user_input == 'r':
        reg_user()

    # add to tasks
    if user_input == 'a':
        add_task()
        
    # view all tasks
    if user_input == 'va':
        view_all()
    
    # print out tasks that are exclusive to the user signed in currently
    if user_input == 'vm':
        view_mine()

    # generate reports
    if user_input == 'gr':
        generate_report() 

    # statistics output
    if user_input == 'ds':
        display_statistics()

    # exit program    
    if user_input == 'e':
        quit()

# references
# https://www.programiz.com/python-programming/datetime/current-datetime
# https://stackoverflow.com/questions/845058/how-to-get-line-count-of-a-large-file-cheaply-in-python
# https://www.programiz.com/python-programming/datetime/strptime