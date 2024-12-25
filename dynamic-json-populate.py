import json
import csv
import random, string

def create_json(location_scope, table_scope, type, 
                refresh_condition, output_file_path, read_from_file=False, column_name=None,
                input_file_path=None):

    
    context = ''.join(random.choices(string.ascii_lowercase,k=16) +  random.choices(string.digits, k=8) + random.choices(string.ascii_lowercase,k=8))
    dynamic_json = []
    condition_list = [];
    if(read_from_file and column_name != None and input_file_path != None):
        with open(input_file_path, "r") as refreshConditionSource:
            data = csv.reader(refreshConditionSource,delimiter=',')
            for row in data:
                for current_element in row:
                    condition_list.append("\'"+str(current_element)+"\'")
                condition_string = ','.join(str(c)for c in condition_list)
                refresh_condition = column_name + " in (" + condition_string +")"
        dynamic_json.append({
            "loc_scope": location_scope,
            "table_scope": table_scope,
            "type": type,
            "paramas": {
                "Context": context,
                "RefreshCondition": refresh_condition
            }
        })
        json_object = json.dumps(dynamic_json)
    else:
        dynamic_json.append({
            "loc_scope": location_scope,
            "table_scope": table_scope,
            "type": type,
            "paramas": {
                "Context": context,
                "RefreshCondition": refresh_condition
            }
        })
        json_object = json.dumps(dynamic_json)
    with open(output_file_path, "w") as outfile:
        outfile.write(json_object)

create_json("Global", "cusips", "Restrict", "product_Type == val", "dynamic_json.json" )
# create_json("Global", "cusips", "Restrict", None, "dynamic_json.json" ,True, "product_Type", "refresh-condition.csv")