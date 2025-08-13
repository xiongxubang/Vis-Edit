from baselines import visedit_consistency
# metrics
from evaluations.exact_match import is_match
from main import get_parser

# input data
db_id = "allergy_1"
question = "Show all allergies with number of students affected with a bar chart."
prediction = "visualize bar select allergy , count ( * ) from allergy_type group by allergy order by count ( * ) desc"
feedback = "I want to visualize the specific allergies instead of the general allergy types."
tokenized_query = "Visualize BAR SELECT Allergy , count(*) FROM Has_allergy GROUP BY Allergy ORDER BY count(*) DESC"     
  
        
args = get_parser()
model = visedit_consistency.Model(args)
input_data = {
    "question":question,
    "prediction": prediction,
    "tokenized_query": tokenized_query,
    "feedback": feedback,
    "db_id":db_id
}


gold_query = tokenized_query
prediction = model.generate(args, input_data)
print(prediction)
print(tokenized_query)


if is_match(prediction, gold_query):
    print("True")
else:
    print("False")
