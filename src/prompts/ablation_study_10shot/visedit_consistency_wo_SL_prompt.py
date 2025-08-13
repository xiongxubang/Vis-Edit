CLAUSE_LOCATION_PROMPT = """
You will be given a user utterance, the associated database schema, an incorrect data visualization query and the corresponding guidance that helps you correct the incorrect query to the correct one.
The 'user utterance' is a natural language text describing the requirement of user. The information of the keyword of the 'data visualization query' is as follows. 'visualize' specifies the visualization type. 'select' extracts the selected columns, of which the first column refers to the x-axis and the second one refers to the y-axis. 'from' refers to the the source table. 'order by' sorts the selected column. 'transform'  transforms the selected columns like binning and grouping by. 

Your task is to detect the wrong clauses of the incorrect data visualization query, given the user utterance, the database schema, the incorrect data visualization query and the guidance. Please note that there may be one or more wrong clauses.

Provide your answer in JSON format as follows:

Answer:
{
    "reason": "(your rationale for the wrong clause, as a text)",
    "answer": "(the wrong clause, as a text)"
}

You MUST provide text for 'reason' and 'answer' in your answer.

Now here are the database schema, the user utterance, data visualization query and the guidance.

SQLite SQL tables, with their properties:
Table people , columns = [ People_ID , Age , Name , Nationality , Graduation_College ] Table company , columns = [ Company_ID , Name , Headquarters , Industry , Sales_in_Billion , Profits_in_Billion , Assets_in_Billion , Market_Value_in_Billion ] Table employment , columns = [ Company_ID , People_ID , Year_working ]
Primary_keys = [ people.People_ID , company.Company_ID , employment.Company_ID ]
Foreign_keys = [ employment.People_ID = people.People_ID , employment.Company_ID = company.Company_ID ]
User utterance: Show the number of headquarters from each headquarters
Incorrect data visualization query: visualize bar select headquarters , count ( headquarters ) from company group by industry
Guidance on the incorrect query: To create a bar chart that displays the count of companies for each headquarters location, make sure to group the data by the 'headquarters' column, not by the 'industry' column. This will ensure that the x-axis represents the headquarters locations and the y-axis represents the count of companies.

Answer: 
{
    "reason": "In the guidance, we asked: 'make sure to group the data by the 'headquarters' column, not by the 'industry' column', so the wrong clause of the visualization query is ['group by industry'].",
    "answer": "['group by industry']"
}

SQLite SQL tables, with their properties:
Table basketball_match , columns = [ Team_ID , School_ID , Team_Name , ACC_Regular_Season , ACC_Percent , ACC_Home , ACC_Road , All_Games , All_Games_Percent , All_Home , All_Road , All_Neutral ] Table university , columns = [ School_ID , School , Location , Founded , Affiliation , Enrollment , Nickname , Primary_conference ] 
Primary_keys = [ basketball_match.Team_ID , university.School_ID ]
Foreign_keys = [ basketball_match.School_ID = university.School_ID ]
User utterance: Show me about the distribution of All_Road and Team_ID in a bar chart, rank by the x axis from low to high.
Incorrect data visualization query: visualize bar select all_road , team_id from basketball_match order by acc_regular_season asc
Guidance on the incorrect query: To correct the query, make sure to sort the data by the column you want to display the distribution of, which is 'all_road' in this case, in ascending order. Also, ensure that you are grouping the data by the correct column, which is 'team_id', to show the distribution of 'all_road' values for each team.

Answer: 
{
    "reason": "In the guidance, we asked: 'make sure to sort the data by the column you want to display the distribution of, which is 'all_road' in this case, in ascending order', so the wrong clause of the visualization query is ['order by acc_regular_season asc'].",
    "answer": "['order by acc_regular_season asc']"
}

SQLite SQL tables, with their properties:
Table party , columns = [ Party_ID , Party_Theme , Location , First_year , Last_year , Number_of_hosts ] Table host , columns = [ Host_ID , Name , Nationality , Age ] Table party_host , columns = [ Party_ID , Host_ID , Is_Main_in_Charge ] 
Primary_keys = [ party.Party_ID , host.Host_ID , party_host.Party_ID ]
Foreign_keys = [ party_host.Party_ID = party.Party_ID , party_host.Host_ID = host.Host_ID ]
User utterance: Give me a bar chart, that group by location and count them, rank x axis in ascending order.
Incorrect data visualization query: visualize bar select location , count ( location ) from station group by location order by location asc
Guidance on the incorrect query: To correct the query, make sure to select the correct table, which is "party", as the source of the data. This will ensure that the bar chart displays the count of each location from the correct table.

Answer: 
{
    "reason": "In the guidance, we asked: 'make sure to select the correct table, which is "party"', so the wrong clause of the visualization query is ['select location , count ( location ) from station'].",
    "answer": "['select location , count ( location ) from station']"
}

SQLite SQL tables, with their properties:
Table regions , columns = [ REGION_ID , REGION_NAME ] Table countries , columns = [ COUNTRY_ID , COUNTRY_NAME , REGION_ID ] Table departments , columns = [ DEPARTMENT_ID , DEPARTMENT_NAME , MANAGER_ID , LOCATION_ID ] Table jobs , columns = [ JOB_ID , JOB_TITLE , MIN_SALARY , MAX_SALARY ] Table employees , columns = [ EMPLOYEE_ID , FIRST_NAME , LAST_NAME , EMAIL , PHONE_NUMBER , HIRE_DATE , JOB_ID , SALARY , COMMISSION_PCT , MANAGER_ID , DEPARTMENT_ID ] Table job_history , columns = [ EMPLOYEE_ID , START_DATE , END_DATE , JOB_ID , DEPARTMENT_ID ] Table locations , columns = [ LOCATION_ID , STREET_ADDRESS , POSTAL_CODE , CITY , STATE_PROVINCE , COUNTRY_ID ] 
Primary_keys = [ regions.REGION_ID , countries.COUNTRY_ID , departments.DEPARTMENT_ID , jobs.JOB_ID , employees.EMPLOYEE_ID , job_history.EMPLOYEE_ID , locations.LOCATION_ID ]
Foreign_keys = [ countries.REGION_ID = regions.REGION_ID , employees.JOB_ID = jobs.JOB_ID , employees.DEPARTMENT_ID = departments.DEPARTMENT_ID , job_history.JOB_ID = jobs.JOB_ID , job_history.DEPARTMENT_ID = departments.DEPARTMENT_ID , job_history.EMPLOYEE_ID = employees.EMPLOYEE_ID , locations.COUNTRY_ID = countries.COUNTRY_ID ]
User utterance: For those employees who was hired before 2002-06-21, show me about the distribution of job_id and the sum of employee_id , and group by attribute job_id in a bar chart, and I want to order JOB_ID in asc order.
Incorrect data visualization query: visualize bar select job_id , sum ( employee_id ) from employees where hire_date < {value} group by job_id order by job_id desc
Guidance on the incorrect query: To correct the query, specify the exact date '2002-06-21' in the where clause and change the order by clause to ascending order to match the user's requirement. This will ensure that the bar chart shows the correct distribution of job_id and the sum of employee_id for employees hired before the specified date, with the job_id sorted in ascending order.

Answer: 
{
    "reason": "In the guidance, we asked: 'specify the exact date '2002-06-21' in the where clause', so the wrong clause of the visualization query is ['where hire_date < {value}']; we asked: 'change the order by clause to ascending order to match the user's requirement', so the wrong clause of the visualization query is ['order by job_id desc']",
    "answer": "['where hire_date < {value}', 'order by job_id desc']"
}

SQLite SQL tables, with their properties:
Table Accounts , columns = [ account_id , customer_id , account_name , other_account_details ] Table Customers , columns = [ customer_id , customer_first_name , customer_last_name , customer_address , customer_phone , customer_email , other_customer_details ] Table Customers_Cards , columns = [ card_id , customer_id , card_type_code , card_number , date_valid_from , date_valid_to , other_card_details ] Table Financial_Transactions , columns = [ transaction_id , previous_transaction_id , account_id , card_id , transaction_type , transaction_date , transaction_amount , transaction_comment , other_transaction_details ] 
Primary_keys = [ Accounts.account_id , Customers.customer_id , Customers_Cards.card_id ]
Foreign_keys = [ Financial_Transactions.account_id = Accounts.account_id , Financial_Transactions.card_id = Customers_Cards.card_id ]
User utterance: Return a histogram on what are the different transaction types, and how many transactions of each have taken place?, and show in descending by the transaction_type.
Incorrect data visualization query: visualize bar select transaction_type , sum ( transaction_amount ) from financial_transactions group by transaction_type order by transaction_type asc
Guidance on the incorrect query: To correct the query, you should use the count function to get the number of transactions for each type, and sort the results in descending order to show the most frequent transaction types first. Make sure to update the aggregation function and the sorting order accordingly.

Answer: 
{
    "reason": "In the guidance, we asked: 'you should use the count function to get the number of transactions for each type', so the wrong clause of the visualization query is ['select transaction_type , sum ( transaction_amount ) from financial_transactions']; we asked: 'sort the results in descending order to show the most frequent transaction types first', so the wrong clause of the visualization query is ['order by transaction_type asc']",
    "answer": "['select transaction_type , sum ( transaction_amount ) from financial_transactions', 'order by transaction_type asc']"
}

SQLite SQL tables, with their properties:
Table Student , columns = [ StuID , LName , Fname , Age , Sex , Major , Advisor , city_code ] Table Has_Pet , columns = [ StuID , PetID ] Table Pets , columns = [ PetID , PetType , pet_age , weight ] 
Primary_keys = [ Student.StuID , Pets.PetID ]
Foreign_keys = [ Has_Pet.StuID = Student.StuID , Has_Pet.PetID = Pets.PetID ]
User utterance: What are the different first names and ages of the students who do have pets. Visualize by bar chart.
Incorrect data visualization query: visualize bar select fname , age from student as t1 join student as t2 on t1 . stuid = t2 . stuid
Guidance on the incorrect query: To create a bar chart that displays the distribution of students\' ages grouped by their first names, considering only students who have pets, you need to join the student table with the has_pet table based on the student ID, not with itself. This will allow you to filter out students who do not have pets and get the correct information for the chart.

Answer: 
{
    "reason": "In the guidance, we asked: 'you need to join the student table with the has_pet table based on the student ID, not with itself', so the wrong clause of the visualization query is ['join student as t2 on t1 . stuid = t2 . stuid']",
    "answer": "['join student as t2 on t1 . stuid = t2 . stuid']"
}

SQLite SQL tables, with their properties:
Table college , columns = [ College_ID , Name , Leader_Name , College_Location ] Table member , columns = [ Member_ID , Name , Country , College_ID ] Table round , columns = [ Round_ID , Member_ID , Decoration_Theme , Rank_in_Round ] 
Primary_keys = [ college.College_ID , member.Member_ID , round.Member_ID ]
Foreign_keys = [ member.College_ID = college.College_ID , round.Member_ID = member.Member_ID ]
User utterance: Return a bar chart showing how many members have visited for each college, I want to display by the X in descending.
Incorrect data visualization query: visualize bar select t1 . name , count ( t1 . name ) from office_locations as t1 join buildings as t2 on t1 . college_id = t2 . college_id group by t1 . name order by t1 . name asc
Guidance on the incorrect query: To correct the query, make sure to join the 'college' and'member' tables on the 'college_id' column, and then group the results by the 'name' column of the 'college' table. Also, change the sorting order to descending to display the colleges with the most members first.

Answer: 
{
    "reason": "In the guidance, we asked: 'make sure to join the 'college' and'member' tables on the 'college_id' column', so the wrong clause of the visualization query is ['from office_locations as t1 join buildings as t2']; we asked: 'change the sorting order to descending to display the colleges with the most members first', so the wrong clause of the visualization query is ['order by t1 . name asc']",
    "answer": "['from office_locations as t1 join buildings as t2', 'order by t1 . name asc']"
}

SQLite SQL tables, with their properties:
Table swimmer , columns = [ ID , name , Nationality , meter_100 , meter_200 , meter_300 , meter_400 , meter_500 , meter_600 , meter_700 , Time ] Table stadium , columns = [ ID , name , Capacity , City , Country , Opening_year ] Table event , columns = [ ID , Name , Stadium_ID , Year ] Table record , columns = [ ID , Result , Swimmer_ID , Event_ID ] 
Primary_keys = [ swimmer.ID , stadium.ID , event.ID , record.Swimmer_ID ]
Foreign_keys = [ event.Stadium_ID = stadium.ID , record.Swimmer_ID = swimmer.ID , record.Event_ID = event.ID ]
User utterance: Return a scatter chart about the correlation between  ID and  meter_100 .
Incorrect data visualization query: visualize scatter select people_id , meter_100 from swimmer
Guidance on the incorrect query: To create a scatter plot, make sure to select the correct columns for the x and y axes. In this case, use 'id' for the x-axis and'meter_100' for the y-axis to visualize their correlation.

Answer: 
{
    "reason": "In the guidance, we asked: 'use 'id' for the x-axis and'meter_100' for the y-axis to visualize their correlation', so the wrong clause of the visualization query is ['select people_id , meter_100 from swimmer']",
    "answer": "['select people_id , meter_100 from swimmer']"
}

SQLite SQL tables, with their properties:
Table employee , columns = [ Employee_ID , Name , Age , City ] Table shop , columns = [ Shop_ID , Name , Location , District , Number_products , Manager_name ] Table hiring , columns = [ Shop_ID , Employee_ID , Start_from , Is_full_time ] Table evaluation , columns = [ Employee_ID , Year_awarded , Bonus ] 
Primary_keys = [ employee.Employee_ID , shop.Shop_ID , hiring.Employee_ID , evaluation.Employee_ID ]
Foreign_keys = [ hiring.Employee_ID = employee.Employee_ID , hiring.Shop_ID = shop.Shop_ID , evaluation.Employee_ID = employee.Employee_ID ]
User utterance: Draw a line chart about the change of the amount of Start_from over  Start_from bin start_from by time.
Incorrect data visualization query: visualize line select start_from , count ( start_from ) from hiring group by is_full_time bin start_from by year
Guidance on the incorrect query: To correct the query, remove the 'group by is_full_time' clause and replace 'group by' with 'bin' to bin the'start_from' column by year. This will allow you to visualize the count of'start_from' occurrences over time, grouped by year.

Answer: 
{
    "reason": "In the guidance, we asked: 'remove the 'group by is_full_time' clause', so the wrong clause of the visualization query is ['group by is_full_time']",
    "answer": "['group by is_full_time']"
}

SQLite SQL tables, with their properties:
Table artist , columns = [ Artist_ID , Name , Country , Year_Join , Age ] Table exhibition , columns = [ Exhibition_ID , Year , Theme , Artist_ID , Ticket_Price ] Table exhibition_record , columns = [ Exhibition_ID , Date , Attendance ] 
Primary_keys = [ artist.Artist_ID , exhibition.Exhibition_ID , exhibition_record.Exhibition_ID ]
Foreign_keys = [ exhibition.Artist_ID = artist.Artist_ID , exhibition_record.Exhibition_ID = exhibition.Exhibition_ID ]
User utterance: Show the average of artists' age by country, and I want to order by the X-axis in asc.
Incorrect data visualization query: visualize bar select country , avg ( age ) from singer group by country order by country asc
Guidance on the incorrect query: To correct the query, make sure to use the correct table that corresponds to the desired data, in this case, the 'artist' table. Replace'singer' with 'artist' to get the average age of artists by country.

Answer: 
{
    "reason": "In the guidance, we asked: 'Replace'singer' with 'artist' to get the average age of artists by country', so the wrong clause of the visualization query is ['select country , avg ( age ) from singer']",
    "answer": "['select country , avg ( age ) from singer']"
}
"""



GENERATION_PROMPT="""
You will be given a user utterance, the associated database schema, an incorrect data visualization query, the identified wrong clauses, the corresponding guidance that helps you correct the incorrect query to the correct one.

The 'user utterance' is a natural language text describing the requirement of user. The information of the keyword of the 'data visualization query' is as follows. 'visualize' specifies the visualization type. 'select' extracts the selected columns, of which the first column refers to the x-axis and the second one refers to the y-axis. 'from' refers to the the source table. 'order by' sorts the selected column. 'transform'  transforms the selected columns like binning and grouping by. 

Your task is to generate the correct clause, given the user utterance, the database schema, the incorrect data visualization query, the identified wrong clauses and the guidance.

Provide your answer in JSON format as follows:

Answer:
{
    "reason": "(your rationale for the generated clause, as a text)",
    "answer": "(your generated clause, as a text)"
}

You MUST provide text for 'reason' and 'answer' in your answer.

Now here are the database schema, the user utterance, the incorrect data visualization query and the guidance.

SQLite SQL tables, with their properties:
Table people , columns = [ People_ID , Age , Name , Nationality , Graduation_College ] Table company , columns = [ Company_ID , Name , Headquarters , Industry , Sales_in_Billion , Profits_in_Billion , Assets_in_Billion , Market_Value_in_Billion ] Table employment , columns = [ Company_ID , People_ID , Year_working ]
Primary_keys = [ people.People_ID , company.Company_ID , employment.Company_ID ]
Foreign_keys = [ employment.People_ID = people.People_ID , employment.Company_ID = company.Company_ID ]
User utterance: Show the number of headquarters from each headquarters
Incorrect data visualization query: visualize bar select headquarters , count ( headquarters ) from company group by industry
Wrong clauses: ['group by industry']
Guidance on the incorrect query: To create a bar chart that displays the count of companies for each headquarters location, make sure to group the data by the 'headquarters' column, not by the 'industry' column. This will ensure that the x-axis represents the headquarters locations and the y-axis represents the count of companies.

Answer: 
{
    "reason": "The wrong clause is 'group by industry'. In the guidance, we asked: 'make sure to group the data by the 'headquarters' column, not by the 'industry' column', so the  correct clause should be ['group by headquarters']",
    "answer": "['group by headquarters']"
}

SQLite SQL tables, with their properties:
Table basketball_match , columns = [ Team_ID , School_ID , Team_Name , ACC_Regular_Season , ACC_Percent , ACC_Home , ACC_Road , All_Games , All_Games_Percent , All_Home , All_Road , All_Neutral ] Table university , columns = [ School_ID , School , Location , Founded , Affiliation , Enrollment , Nickname , Primary_conference ] 
Primary_keys = [ basketball_match.Team_ID , university.School_ID ]
Foreign_keys = [ basketball_match.School_ID = university.School_ID ]
User utterance: Show me about the distribution of All_Road and Team_ID in a bar chart, rank by the x axis from low to high.
Incorrect data visualization query: visualize bar select all_road , team_id from basketball_match order by acc_regular_season asc
Wrong clauses: ['order by acc_regular_season asc']
Guidance on the incorrect query: To correct the query, make sure to sort the data by the column you want to display the distribution of, which is 'all_road' in this case, in ascending order. Also, ensure that you are grouping the data by the correct column, which is 'team_id', to show the distribution of 'all_road' values for each team.

Answer: 
{
    "reason": "The wrong clause is 'order by acc_regular_season asc'. In the guidance, we asked: 'make sure to sort the data by the column you want to display the distribution of, which is 'all_road' in this case, in ascending order', so the correct clause of the visualization query is ['order by all_road asc'].",
    "answer": "['order by all_road asc']"
}

SQLite SQL tables, with their properties:
Table party , columns = [ Party_ID , Party_Theme , Location , First_year , Last_year , Number_of_hosts ] Table host , columns = [ Host_ID , Name , Nationality , Age ] Table party_host , columns = [ Party_ID , Host_ID , Is_Main_in_Charge ] 
Primary_keys = [ party.Party_ID , host.Host_ID , party_host.Party_ID ]
Foreign_keys = [ party_host.Party_ID = party.Party_ID , party_host.Host_ID = host.Host_ID ]
User utterance: Give me a bar chart, that group by location and count them, rank x axis in ascending order.
Incorrect data visualization query: visualize bar select location , count ( location ) from station group by location order by location asc
Wrong clauses: ['select location , count ( location ) from station']
Guidance on the incorrect query: To correct the query, make sure to select the correct table, which is "party", as the source of the data. This will ensure that the bar chart displays the count of each location from the correct table.

Answer: 
{
    "reason": "The wrong clause is 'select location , count ( location ) from station'. In the guidance, we asked: 'make sure to select the correct table, which is "party"', so the correct clause of the visualization query is ['select location , count ( location ) from party'].",
    "answer": "['select location , count ( location ) from party']"
}

SQLite SQL tables, with their properties:
Table regions , columns = [ REGION_ID , REGION_NAME ] Table countries , columns = [ COUNTRY_ID , COUNTRY_NAME , REGION_ID ] Table departments , columns = [ DEPARTMENT_ID , DEPARTMENT_NAME , MANAGER_ID , LOCATION_ID ] Table jobs , columns = [ JOB_ID , JOB_TITLE , MIN_SALARY , MAX_SALARY ] Table employees , columns = [ EMPLOYEE_ID , FIRST_NAME , LAST_NAME , EMAIL , PHONE_NUMBER , HIRE_DATE , JOB_ID , SALARY , COMMISSION_PCT , MANAGER_ID , DEPARTMENT_ID ] Table job_history , columns = [ EMPLOYEE_ID , START_DATE , END_DATE , JOB_ID , DEPARTMENT_ID ] Table locations , columns = [ LOCATION_ID , STREET_ADDRESS , POSTAL_CODE , CITY , STATE_PROVINCE , COUNTRY_ID ] 
Primary_keys = [ regions.REGION_ID , countries.COUNTRY_ID , departments.DEPARTMENT_ID , jobs.JOB_ID , employees.EMPLOYEE_ID , job_history.EMPLOYEE_ID , locations.LOCATION_ID ]
Foreign_keys = [ countries.REGION_ID = regions.REGION_ID , employees.JOB_ID = jobs.JOB_ID , employees.DEPARTMENT_ID = departments.DEPARTMENT_ID , job_history.JOB_ID = jobs.JOB_ID , job_history.DEPARTMENT_ID = departments.DEPARTMENT_ID , job_history.EMPLOYEE_ID = employees.EMPLOYEE_ID , locations.COUNTRY_ID = countries.COUNTRY_ID ]
User utterance: For those employees who was hired before 2002-06-21, show me about the distribution of job_id and the sum of employee_id , and group by attribute job_id in a bar chart, and I want to order JOB_ID in asc order.
Incorrect data visualization query: visualize bar select job_id , sum ( employee_id ) from employees where hire_date < {value} group by job_id order by job_id desc
Wrong clauses: ['where hire_date < {value}', 'order by job_id desc']
Guidance on the incorrect query: To correct the query, specify the exact date '2002-06-21' in the where clause and change the order by clause to ascending order to match the user's requirement. This will ensure that the bar chart shows the correct distribution of job_id and the sum of employee_id for employees hired before the specified date, with the job_id sorted in ascending order.

Answer: 
{
    "reason": "The wrong clauses are 'where hire_date < {value}' and 'order by job_id desc'. In the guidance, we asked: 'specify the exact date '2002-06-21' in the where clause', so the correct clause of the visualization query is ['where hire_date < '2002-06-21'']; we asked: 'change the order by clause to ascending order to match the user's requirement', so the correct clause of the visualization query is ['order by job_id asc']",
    "answer": "['where hire_date < '2002-06-21'', 'order by job_id asc']"
}

SQLite SQL tables, with their properties:
Table Accounts , columns = [ account_id , customer_id , account_name , other_account_details ] Table Customers , columns = [ customer_id , customer_first_name , customer_last_name , customer_address , customer_phone , customer_email , other_customer_details ] Table Customers_Cards , columns = [ card_id , customer_id , card_type_code , card_number , date_valid_from , date_valid_to , other_card_details ] Table Financial_Transactions , columns = [ transaction_id , previous_transaction_id , account_id , card_id , transaction_type , transaction_date , transaction_amount , transaction_comment , other_transaction_details ] 
Primary_keys = [ Accounts.account_id , Customers.customer_id , Customers_Cards.card_id ]
Foreign_keys = [ Financial_Transactions.account_id = Accounts.account_id , Financial_Transactions.card_id = Customers_Cards.card_id ]
User utterance: Return a histogram on what are the different transaction types, and how many transactions of each have taken place?, and show in descending by the transaction_type.
Incorrect data visualization query: visualize bar select transaction_type , sum ( transaction_amount ) from financial_transactions group by transaction_type order by transaction_type asc
Wrong clauses: ['select transaction_type , sum ( transaction_amount ) from financial_transactions', 'order by transaction_type asc']
Guidance on the incorrect query: To correct the query, you should use the count function to get the number of transactions for each type, and sort the results in descending order to show the most frequent transaction types first. Make sure to update the aggregation function and the sorting order accordingly.

Answer: 
{
    "reason": "The wrong clauses are 'select transaction_type , sum ( transaction_amount ) from financial_transactions' and 'order by transaction_type asc'. In the guidance, we asked: 'you should use the count function to get the number of transactions for each type', so the correct clause of the visualization query is ['select transaction_type , count ( * ) from financial_transactions']; we asked: 'sort the results in descending order to show the most frequent transaction types first', so the correct clause of the visualization query is ['order by transaction_type desc']",
    "answer": "['select transaction_type , count ( * ) from financial_transactions', 'order by transaction_type desc']"
}

SQLite SQL tables, with their properties:
Table Student , columns = [ StuID , LName , Fname , Age , Sex , Major , Advisor , city_code ] Table Has_Pet , columns = [ StuID , PetID ] Table Pets , columns = [ PetID , PetType , pet_age , weight ] 
Primary_keys = [ Student.StuID , Pets.PetID ]
Foreign_keys = [ Has_Pet.StuID = Student.StuID , Has_Pet.PetID = Pets.PetID ]
User utterance: What are the different first names and ages of the students who do have pets. Visualize by bar chart.
Incorrect data visualization query: visualize bar select fname , age from student as t1 join student as t2 on t1 . stuid = t2 . stuid
Wrong clauses: ['join student as t2 on t1 . stuid = t2 . stuid']
Guidance on the incorrect query: To create a bar chart that displays the distribution of students\' ages grouped by their first names, considering only students who have pets, you need to join the student table with the has_pet table based on the student ID, not with itself. This will allow you to filter out students who do not have pets and get the correct information for the chart.

Answer: 
{
    "reason": "The wrong clause is 'join student as t2 on t1 . stuid = t2 . stuid'. In the guidance, we asked: 'you need to join the student table with the has_pet table based on the student ID, not with itself', so the correct clause of the visualization query is ['join has_pet as t2 on t1 . stuid = t2 . stuid']",
    "answer": "['join has_pet as t2 on t1 . stuid = t2 . stuid']"
}

SQLite SQL tables, with their properties:
Table college , columns = [ College_ID , Name , Leader_Name , College_Location ] Table member , columns = [ Member_ID , Name , Country , College_ID ] Table round , columns = [ Round_ID , Member_ID , Decoration_Theme , Rank_in_Round ] 
Primary_keys = [ college.College_ID , member.Member_ID , round.Member_ID ]
Foreign_keys = [ member.College_ID = college.College_ID , round.Member_ID = member.Member_ID ]
User utterance: Return a bar chart showing how many members have visited for each college, I want to display by the X in descending.
Incorrect data visualization query: visualize bar select t1 . name , count ( t1 . name ) from office_locations as t1 join buildings as t2 on t1 . college_id = t2 . college_id group by t1 . name order by t1 . name asc
Wrong clauses: ['from office_locations as t1 join buildings as t2', 'order by t1 . name asc']
Guidance on the incorrect query: To correct the query, make sure to join the 'college' and'member' tables on the 'college_id' column, and then group the results by the 'name' column of the 'college' table. Also, change the sorting order to descending to display the colleges with the most members first.

Answer: 
{
    "reason": "The wrong clauses are 'from office_locations as t1 join buildings as t2' and 'order by t1 . name asc'. In the guidance, we asked: 'make sure to join the 'college' and'member' tables on the 'college_id' column', so the correct clause of the visualization query is ['from college as t1 join member as t2']; we asked: 'change the sorting order to descending to display the colleges with the most members first', so the correct clause of the visualization query is ['order by t1 . name desc']",
    "answer": "['from college as t1 join member as t2', 'order by t1 . name desc']"
}

SQLite SQL tables, with their properties:
Table swimmer , columns = [ ID , name , Nationality , meter_100 , meter_200 , meter_300 , meter_400 , meter_500 , meter_600 , meter_700 , Time ] Table stadium , columns = [ ID , name , Capacity , City , Country , Opening_year ] Table event , columns = [ ID , Name , Stadium_ID , Year ] Table record , columns = [ ID , Result , Swimmer_ID , Event_ID ] 
Primary_keys = [ swimmer.ID , stadium.ID , event.ID , record.Swimmer_ID ]
Foreign_keys = [ event.Stadium_ID = stadium.ID , record.Swimmer_ID = swimmer.ID , record.Event_ID = event.ID ]
User utterance: Return a scatter chart about the correlation between  ID and  meter_100 .
Incorrect data visualization query: visualize scatter select people_id , meter_100 from swimmer
Wrong clauses: ['select people_id , meter_100 from swimmer']
Guidance on the incorrect query: To create a scatter plot, make sure to select the correct columns for the x and y axes. In this case, use 'id' for the x-axis and'meter_100' for the y-axis to visualize their correlation.

Answer: 
{
    "reason": "The wrong clause is 'select people_id , meter_100 from swimmer'. In the guidance, we asked: 'use 'id' for the x-axis and'meter_100' for the y-axis to visualize their correlation', so the wrong clause of the visualization query is ['select id , meter_100 from swimmer']",
    "answer": "['select id , meter_100 from swimmer']"
}

SQLite SQL tables, with their properties:
Table employee , columns = [ Employee_ID , Name , Age , City ] Table shop , columns = [ Shop_ID , Name , Location , District , Number_products , Manager_name ] Table hiring , columns = [ Shop_ID , Employee_ID , Start_from , Is_full_time ] Table evaluation , columns = [ Employee_ID , Year_awarded , Bonus ] 
Primary_keys = [ employee.Employee_ID , shop.Shop_ID , hiring.Employee_ID , evaluation.Employee_ID ]
Foreign_keys = [ hiring.Employee_ID = employee.Employee_ID , hiring.Shop_ID = shop.Shop_ID , evaluation.Employee_ID = employee.Employee_ID ]
User utterance: Draw a line chart about the change of the amount of Start_from over  Start_from bin start_from by time.
Incorrect data visualization query: visualize line select start_from , count ( start_from ) from hiring group by is_full_time bin start_from by year
Wrong clauses: ['group by is_full_time']
Guidance on the incorrect query: To correct the query, remove the 'group by is_full_time' clause and replace 'group by' with 'bin' to bin the'start_from' column by year. This will allow you to visualize the count of'start_from' occurrences over time, grouped by year.

Answer: 
{
    "reason": "The wrong clause is 'group by is_full_time'. In the guidance, we asked: 'remove the 'group by is_full_time' clause', so the wrong clause of the visualization query is ['group by is_full_time']",
    "answer": "['']"
}

SQLite SQL tables, with their properties:
Table artist , columns = [ Artist_ID , Name , Country , Year_Join , Age ] Table exhibition , columns = [ Exhibition_ID , Year , Theme , Artist_ID , Ticket_Price ] Table exhibition_record , columns = [ Exhibition_ID , Date , Attendance ] 
Primary_keys = [ artist.Artist_ID , exhibition.Exhibition_ID , exhibition_record.Exhibition_ID ]
Foreign_keys = [ exhibition.Artist_ID = artist.Artist_ID , exhibition_record.Exhibition_ID = exhibition.Exhibition_ID ]
User utterance: Show the average of artists' age by country, and I want to order by the X-axis in asc.
Incorrect data visualization query: visualize bar select country , avg ( age ) from singer group by country order by country asc
Wrong clauses: ['select country , avg ( age ) from singer']
Guidance on the incorrect query: To correct the query, make sure to use the correct table that corresponds to the desired data, in this case, the 'artist' table. Replace'singer' with 'artist' to get the average age of artists by country.

Answer: 
{
    "reason": "The wrong clause is 'select country , avg ( age ) from singer'. In the guidance, we asked: 'Replace'singer' with 'artist' to get the average age of artists by country', so the wrong clause of the visualization query is ['select country , avg ( age ) from artist']",
    "answer": "['select country , avg ( age ) from artist']"
}
"""


MERGE_PROMPT="""
You will be given an incorrect data visualization query, the identified wrong clause, the correct clause and the corresponding guidance that helps you correct the incorrect query to the correct one.
The information of the keyword of the 'data visualization query' is as follows. 'visualize' specifies the visualization type. 'select' extracts the selected columns, of which the first column refers to the x-axis and the second one refers to the y-axis. 'from' refers to the the source table. 'order by' sorts the selected column. 'transform'  transforms the selected columns like binning and grouping by. 

Your task is to correct the incorrect data visualiation query, given the wrong clause, the correct clause and the guidance.

Provide your answer in JSON format as follows:

Answer:
{
    "reason": "(your rationale for the generated data visualization query, as a text)",
    "answer": "(your data visualization query, as a text)"
}

You MUST provide text for 'reason' and 'answer' in your answer.

Now here are the incorrect data visualization query, the identified wrong clause, the corresponding clauses and the guidance.

Incorrect data visualization query: visualize bar select headquarters , count ( headquarters ) from company group by industry
Wrong clause: ['group by industry']
Correct clause: ['group by headquarters']
Guidance on the incorrect query: To create a bar chart that displays the count of companies for each headquarters location, make sure to group the data by the 'headquarters' column, not by the 'industry' column. This will ensure that the x-axis represents the headquarters locations and the y-axis represents the count of companies.

Answer: 
{
    "reason": "Replace 'group by industry' with 'group by headquarters' in the 'group by' clause.",
    "answer": "visualize bar select headquarters , count ( headquarters ) from company group by headquarters"
}

Incorrect data visualization query: visualize bar select all_road , team_id from basketball_match order by acc_regular_season asc
Wrong clause: ['order by acc_regular_season asc']
Correct clause: ['order by all_road asc']
Guidance on the incorrect query: To correct the query, make sure to sort the data by the column you want to display the distribution of, which is 'all_road' in this case, in ascending order. Also, ensure that you are grouping the data by the correct column, which is 'team_id', to show the distribution of 'all_road' values for each team.

Answer: 
{
    "reason": "Replace 'order by acc_regular_season asc' with 'order by all_road asc' in the 'order by' clause.",
    "answer": "visualize bar select all_road , team_id from basketball_match order by all_road asc"
}

Incorrect data visualization query: visualize bar select location , count ( location ) from station group by location order by location asc
Wrong clause: ['select location , count ( location ) from station']
Correct clause: ['select location , count ( location ) from party']
Guidance on the incorrect query: To correct the query, make sure to select the correct table, which is "party", as the source of the data. This will ensure that the bar chart displays the count of each location from the correct table.

Answer: 
{
    "reason": "Replace 'select location , count ( location ) from station' with 'select location , count ( location ) from party' in the 'select' clause.",
    "answer": "visualize bar select location , count ( location ) from party group by location order by location asc"
}

Incorrect data visualization query: visualize bar select job_id , sum ( employee_id ) from employees where hire_date < {value} group by job_id order by job_id desc
Wrong clause: ['where hire_date < {value}', 'order by job_id desc']
Correct clause: ['where hire_date < '2002-06-21'', 'order by job_id asc']
Guidance on the incorrect query: To correct the query, specify the exact date '2002-06-21' in the where clause and change the order by clause to ascending order to match the user's requirement. This will ensure that the bar chart shows the correct distribution of job_id and the sum of employee_id for employees hired before the specified date, with the job_id sorted in ascending order.

Answer: 
{
    "reason": "Replace 'where hire_date < {value}' with 'where hire_date < '2002-06-21'' in the 'where' clause. Replace 'order by job_id desc' with 'order by job_id asc' in the 'order by' clause.",
    "answer": "visualize bar select job_id , sum ( employee_id ) from employees where hire_date < '2002-06-21' group by job_id order by job_id asc"
}

Incorrect data visualization query: visualize bar select transaction_type , sum ( transaction_amount ) from financial_transactions group by transaction_type order by transaction_type asc
Wrong clause: ['select transaction_type , sum ( transaction_amount ) from financial_transactions', 'order by transaction_type asc']
Correct clause: ['select transaction_type , count ( * ) from financial_transactions', 'order by transaction_type desc']
Guidance on the incorrect query: To correct the query, you should use the count function to get the number of transactions for each type, and sort the results in descending order to show the most frequent transaction types first. Make sure to update the aggregation function and the sorting order accordingly.

Answer: 
{
    "reason": "Replace 'select transaction_type , sum ( transaction_amount ) from financial_transactions' with 'select transaction_type , count ( * ) from financial_transactions' in the 'select' clause. Replace 'order by transaction_type asc' with 'order by transaction_type desc' in the 'order by' clause.",
    "answer": "visualize bar select transaction_type , count ( * ) from financial_transactions group by transaction_type order by transaction_type desc"
}

Incorrect data visualization query: visualize bar select fname , age from student as t1 join student as t2 on t1 . stuid = t2 . stuid
Wrong clause: ['join student as t2 on t1 . stuid = t2 . stuid']
Correct clause: ['join has_pet as t2 on t1 . stuid = t2 . stuid']
Guidance on the incorrect query: To create a bar chart that displays the distribution of students\' ages grouped by their first names, considering only students who have pets, you need to join the student table with the has_pet table based on the student ID, not with itself. This will allow you to filter out students who do not have pets and get the correct information for the chart.

Answer: 
{
    "reason": "Replace 'join student as t2 on t1 . stuid = t2 . stuid' with 'join has_pet as t2 on t1 . stuid = t2 . stuid' in the 'join' clause.",
    "answer": "visualize bar select fname , age from student as t1 join has_pet as t2 on t1 . stuid = t2 . stuid"
}

Incorrect data visualization query: visualize bar select t1 . name , count ( t1 . name ) from office_locations as t1 join buildings as t2 on t1 . college_id = t2 . college_id group by t1 . name order by t1 . name asc
Wrong clause: ['from office_locations as t1 join buildings as t2', 'order by t1 . name asc']
Correct clause: ['from college as t1 join member as t2', 'order by t1 . name desc']
Guidance on the incorrect query: To correct the query, make sure to join the 'college' and'member' tables on the 'college_id' column, and then group the results by the 'name' column of the 'college' table. Also, change the sorting order to descending to display the colleges with the most members first.

Answer: 
{
    "reason": "Replace 'from office_locations as t1 join buildings as t2' with 'from college as t1 join member as t2' in the 'from' clause. Replace 'order by t1 . name asc' with 'order by t1 . name desc' in the 'order by' clause.",
    "answer": "visualize bar select t1 . name , count ( t1 . name ) from college as t1 join member as t2 on t1 . college_id = t2 . college_id group by t1 . name order by t1 . name desc"
}

Incorrect data visualization query: visualize scatter select people_id , meter_100 from swimmer
Wrong clause: ['select people_id , meter_100 from swimmer']
Correct clause: ['select id , meter_100 from swimmer']
Guidance on the incorrect query: To create a scatter plot, make sure to select the correct columns for the x and y axes. In this case, use 'id' for the x-axis and'meter_100' for the y-axis to visualize their correlation.

Answer: 
{
    "reason": "Replace 'select people_id , meter_100 from swimmer' with 'select id , meter_100 from swimmer' in the 'select' clause.",
    "answer": "visualize scatter select id , meter_100 from swimmer"
}

Incorrect data visualization query: visualize line select start_from , count ( start_from ) from hiring group by is_full_time bin start_from by year
Wrong clause: ['group by is_full_time']
Correct clause: ['']
Guidance on the incorrect query: To correct the query, remove the 'group by is_full_time' clause and replace 'group by' with 'bin' to bin the'start_from' column by year. This will allow you to visualize the count of'start_from' occurrences over time, grouped by year.

Answer: 
{
    "reason": "Remove the 'group by is_full_time' in the 'group by' clause.",
    "answer": "visualize line select start_from , count ( start_from ) from hiring bin start_from by year"
}

Incorrect data visualization query: visualize bar select country , avg ( age ) from singer group by country order by country asc
Wrong clause: ['select country , avg ( age ) from singer']
Correct clause: ['select country , avg ( age ) from artist']
Guidance on the incorrect query: To correct the query, make sure to use the correct table that corresponds to the desired data, in this case, the 'artist' table. Replace'singer' with 'artist' to get the average age of artists by country.

Answer: 
{
    "reason": "Remove the 'group by is_full_time' in the 'group by' clause.",
    "answer": "visualize bar select country , avg ( age ) from artist group by country order by country asc"
}
"""



