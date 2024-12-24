import json
import csv
from enum import Enum

class ConditionType(Enum):
    EQUALS = 1
    IN_QUERY = 2
    GREATER_EQUALS = 3
    LESS_EQUALS = 4
    GREATER = 5
    LESS = 6

def create_json(location_scope, table_scope, type, context, refresh_condition, readFromFile=False, column_name=None,  conditionType=None):
    dynamic_json = []
    condition_list = [];
    if(readFromFile and column_name != None and conditionType != None):
        with open("refresh-condition.csv", "r") as refreshConditionSource:
            data = csv.reader(refreshConditionSource,delimiter=',')
            for row in data:
                for current_element in row:
                    condition_list.append(int(current_element))
        match(conditionType):
            
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
    with open("dynamic_json.json", "w") as outfile:
        outfile.write(json_object)

# create_json("Global", "cusips", "Restrict", "product_Type", "product_Type == 'Bond'")
create_json("Global", "cusips", "Restrict", "product_Type", None,True, "product_Type", 2)