SCHEMA_LINKING_PROMPT = """
You will be given a user utterance, the associated database schema, an incorrect data visualization query and the corresponding guidance that helps you correct the incorrect data visualization query to the correct one.
The 'user utterance' is a natural language text describing the requirement of user. The information of the keyword of the 'data visualization query' is as follows. 'visualize' specifies the visualization type. 'select' extracts the selected columns, of which the first column refers to the x-axis and the second one refers to the y-axis. 'from' refers to the the source table. 'order by' sorts the selected column. 'transform'  transforms the selected columns like binning and grouping by. 

Your task is to identify the potential database schema links which will be used to correct the incorrect data visualization query, given the database schema, the incorrect data visualization query and the corresponding guidance.

Provide your answer in JSON format as follows:

Answer:
{
    "reason": "(your rationale for the potential database schema links, as a text)",
    "answer": "(the potential database schema links, as a text)"
}

You MUST provide text for 'reason' and 'answer' in your answer.

Now here are the database schema, the user utterance, incorrect data visualization query and the guidance.

SQLite SQL tables, with their properties:
Table people , columns = [ People_ID , Age , Name , Nationality , Graduation_College ] Table company , columns = [ Company_ID , Name , Headquarters , Industry , Sales_in_Billion , Profits_in_Billion , Assets_in_Billion , Market_Value_in_Billion ] Table employment , columns = [ Company_ID , People_ID , Year_working ]
Primary_keys = [ people.People_ID , company.Company_ID , employment.Company_ID ]
Foreign_keys = [ employment.People_ID = people.People_ID , employment.Company_ID = company.Company_ID ]
User utterance: Show the number of headquarters from each headquarters
Incorrect data visualization query: visualize bar select headquarters , count ( headquarters ) from company group by industry
Guidance on the incorrect data visualization query: To create a bar chart that displays the count of companies for each headquarters location, make sure to group the data by the 'headquarters' column, not by the 'industry' column. This will ensure that the x-axis represents the headquarters locations and the y-axis represents the count of companies.

Answer: 
{
    "reason": "In the utterance, we asked 'Show the number of headquarters from each headquarters' so we need [company.Headquarters].In the incorrect query 'visualize bar select headquarters , count ( headquarters ) from company group by industry', there are existing schema links [company, company.Headquarters, company.Industry]. In the guidance, we asked: 'make sure to group the data by the 'headquarters' column, not by the 'industry' column', so we need [company.Headquarters].",
    "answer": "[company, company.Headquarters, company.Industry]"
}
"""


CLAUSE_LOCATION_PROMPT = """
You will be given a user utterance, the potential database schema links, an incorrect data visualization query and the corresponding guidance that helps you correct the incorrect query to the correct one.
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

SQLite SQL schema links:
[company, company.Headquarters, company.Industry]
User utterance: Show the number of headquarters from each headquarters
Incorrect data visualization query: visualize bar select headquarters , count ( headquarters ) from company group by industry
Guidance on the incorrect query: To create a bar chart that displays the count of companies for each headquarters location, make sure to group the data by the 'headquarters' column, not by the 'industry' column. This will ensure that the x-axis represents the headquarters locations and the y-axis represents the count of companies.
Answer: 
{
    "reason": "In the guidance, we asked: 'make sure to group the data by the 'headquarters' column, not by the 'industry' column', so the wrong clause of the visualization query is ['group by industry'].",
    "answer": "['group by industry']"
}
"""



GENERATION_PROMPT="""
You will be given a user utterance, the potential database schema links, an incorrect data visualization query, the identified wrong clauses, the corresponding guidance that helps you correct the incorrect query to the correct one.

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

SQLite SQL schema links:
[company, company.Headquarters, company.Industry]
User utterance: Show the number of headquarters from each headquarters
Incorrect data visualization query: visualize bar select headquarters , count ( headquarters ) from company group by industry
Wrong clauses: ['group by industry']
Guidance on the incorrect query: To create a bar chart that displays the count of companies for each headquarters location, make sure to group the data by the 'headquarters' column, not by the 'industry' column. This will ensure that the x-axis represents the headquarters locations and the y-axis represents the count of companies.

Answer: 
{
    "reason": "The wrong clauses is 'group by industry'. In the guidance, we asked: 'make sure to group the data by the 'headquarters' column, not by the 'industry' column', so the  correct clause should be ['group by headquarters']",
    "answer": "['group by headquarters']"
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
"""



