import json
import csv

def create_json(location_scope, table_scope, type, context, 
                refresh_condition, output_file_path, read_from_file=False, column_name=None,  condition_type=None,
                input_file_path=None):
    dynamic_json = []
    condition_list = [];
    if(read_from_file and column_name != None and condition_type != None and input_file_path != None):
        with open(input_file_path, "r") as refreshConditionSource:
            data = csv.reader(refreshConditionSource,delimiter=',')
            for row in data:
                for current_element in row:
                    condition_list.append(int(current_element))
        match(condition_type):
            
            case 2:
                x = ','.join(str(c)for c in condition_list)
                refresh_condition = column_name + " in (" + x +")"  
            case _:
                print("Invalid Condition Type")

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

# create_json("Global", "cusips", "Restrict","Random", "product_Type","dynamic_json.json", "product_Type == 'Bond'")
create_json("Global", "cusips", "Restrict","Random", None, "dynamic_json.json" ,True, "product_Type", 2,"refresh-condition.csv")