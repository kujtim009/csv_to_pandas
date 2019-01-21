import pandas
import csv
import pickle

class CsvFiles(object):
    def __init__(self, filename_1, filename_2 = None, from_line = 0, to_line = 100):
        self.filename_1 = filename_1        
        self.filename_2 = filename_2
        self.from_line = from_line
        self.to_line = to_line

        try:
            self.csv_data = pickle.load(open("{}.pickle".format(filename_1), "rb"))
        except (OSError, IOError) as e:
            self.csv_data = pandas.read_csv(filename_1, encoding = "latin1", engine='python')
            pickle.dump(self.csv_data, open("{}.pickle".format(filename_1), "wb"))

        
        if filename_2 is not None:
            try:
                self.csv_data2 = pickle.load(open("{}.pickle".format(filename_2), "rb"))
            except (OSError, IOError) as e:
                self.csv_data2 = pandas.read_csv(filename_2, encoding = "latin1", engine='python')
                pickle.dump(self.csv_data2, open("{}.pickle".format(filename_2), "wb"))
        

    def display_json_data(self):
        self.csv_data = self.csv_data[self.from_line:self.to_line]
        jsonFile = self.csv_data.to_json(orient='records')
        return jsonFile

    def pop_report(self, file_num=1):
        if file_num == 1:
            count_data = list(self.csv_data.notnull().sum())
        else:
            count_data = list(self.csv_data2.notnull().sum())   
        return count_data

    def get_rec_count(self, file_num=1):
        if file_num == 1:
            count_data = self.csv_data.shape[0]
        else:
            count_data = self.csv_data2.shape[0]
        return count_data    

    def getFields(self, file_num=1):
        if file_num == 1:
            fields = self.csv_data.columns.values
        else:
            fields = self.csv_data2.columns.values
        return list(fields)

    def sort_by(self, listOfCols, sort_type):
        if sort_type == "Desc":
            self.csv_data = self.csv_data.sort_values(by=listOfCols, ascending=[False])
        else:
            self.csv_data = self.csv_data.sort_values(by=listOfCols)
        return self 

    def group_by(self, listOfCols):
        self.csv_data = self.csv_data.groupby(listOfCols).size().reset_index(name='Count')
        self.csv_data = self.csv_data.sort_values(by='Count', ascending=False)
        return self   

    def filter_by(self, filterbycol, value_to_filter):
        self.csv_data = self.csv_data.loc[self.csv_data[filterbycol] == value_to_filter]
        return self  

    def remove_dups(self, uniqueCol):
        self.csv_data = self.csv_data.drop_duplicates(uniqueCol ,keep = "first")
        return self   

    def compare_layouts(self):
        fields_1 = list(self.csv_data.columns.values)
        fields_2 = list(self.csv_data2.columns.values)
        two_layouts = {}
        for field in fields_1:
            if field in fields_2:
                two_layouts[field] = True
            else:
                two_layouts[field] = False
        return {"field_compare":two_layouts, "file1_count": len(fields_1), "file2_count": len(fields_2)}        
