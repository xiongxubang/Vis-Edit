import re


def strip_query(query):
    '''
    return keywords of vql query
    '''
    query_keywords = []
    query = query.strip().replace(";","").replace("\t","").replace(",", " , ")
    query = query.replace("(", " ( ").replace(")", " ) ")
    query = query.replace(">=", " >= ").replace("<=", " <= ").replace("!=", " != ").replace("=", " = ")

    # then replace all stuff enclosed by "" with a numerical value to get it marked as {VALUE}
    str_1 = re.findall("\"[^\"]*\"", query)
    str_2 = re.findall("\'[^\']*\'", query)
    
    values = str_1 + str_2

    query_tokenized = query.split()
    # float_nums = re.findall("[-+]?\d*\.\d+", query)

    # query = " ".join(query_tokenized)
    # int_nums = [i.strip() for i in re.findall("[^tT]\d+", query)]
    
    for tok in query_tokenized:
        if "." in tok:
            table = re.findall("[Tt]\d+\.", tok)
            if len(table)>0:
                to = tok.replace(".", " . ").split()
                to = [t.lower() for t in to if len(t)>0]
                query_keywords.extend(to)
            else:
                query_keywords.append(tok.lower())

        elif len(tok) > 0:
            query_keywords.append(tok.lower())
    query_keywords = [w for w in query_keywords if len(w)>0]
    query_sentence = " ".join(query_keywords)
    query_sentence = query_sentence.replace("> =", ">=").replace("! =", "!=").replace("< =", "<=")

    return query_sentence




def is_match(prediction: str, gt_vql: str):
    # print(strip_query(prediction).strip())
    # print(strip_query(gt_vql).strip())
    return strip_query(prediction).strip() == strip_query(gt_vql).strip()

# gt_vql = "Visualize BAR SELECT Rank , count(*) FROM Faculty GROUP BY rank ORDER BY count(*) DESC"
# pred = "visualize bar select  *, count ( * ) from faculty group by rank order by count ( *) desc"

# print(is_match(pred, gt_vql))