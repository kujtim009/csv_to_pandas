from flask_restful import Resource, reqparse, request
from controller.files import CsvFiles


class ReadCsvFiles(Resource):
    def get(self):
        filename = request.args.get('file', None)
        csv_file = CsvFiles(filename, to_line=2000)
        sort = request.args.get('sort', None)
        sort_type = request.args.get('sort_t', None)
        group = request.args.get('group', None)

        filter_col = request.args.get('filterby', None)
        filter_val = request.args.get('filterval', None)

        unique = request.args.get('unique', None)

        if group is not None:
            group_array = group.split(',')
            csv_file = csv_file.group_by(group_array)    

        if sort is not None and sort_type is not None:
            # sort_array = sort.split(',')
            csv_file = csv_file.sort_by(sort, sort_type)

        if filter_col is not None and filter_val is not None:
            csv_file = csv_file.filter_by(filter_col, filter_val)   
            
        if unique is not None:
            unique_array = unique.split(',')
            # return {"message": unique}, 201
            csv_file = csv_file.remove_dups(unique_array)     
        
        myFields = csv_file.getFields()
        myCount = csv_file.pop_report()
        pop_report = dict(zip(myFields, myCount))

        total_record_count = csv_file.get_rec_count()

        
        myData = csv_file.display_json_data()  
        return {"message": myData, "pop_report": pop_report, "fields": myFields, "Record_count": total_record_count}, 201


class Compare_layouts(Resource):
    def get(self):
        filename1 = request.args.get('file1', None)
        filename2 = request.args.get('file2', None)
        csv_file = CsvFiles(filename1,filename2, to_line=2000)

        myFields = csv_file.getFields(2)
        myCount = csv_file.pop_report(2)
        pop_report = {"pop_report_2": dict(zip(myFields, myCount))}
        compare_result = csv_file.compare_layouts()
        # return compare_result.update(pop_report)
        return {"compare_results": compare_result, "pop_report": pop_report}
        # return {"Message":"Working"}