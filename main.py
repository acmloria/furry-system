import re
import ast
import pandas as pd

#importing two libraries
#re for regular expression
#pandas, our data cleaning tool


df = pd.read_excel ("../../Downloads/02 Lloyd APPLICATION TEMPLATE 2020.xlsx", sheet_name="Applications")

#Drop unnecessary columns
to_drop_column_names = []

for col in df.columns: 
    if re.search("^Unnamed", col) is None:
        to_drop_column_names.append(col)

    

# print(to_drop_column_names)
df = df.dropna(how="all", axis=1)
df = df.dropna(how="all", axis=0)
df = df.drop(to_drop_column_names+["Unnamed: 24", "Unnamed: 26", "Unnamed: 47"], axis=1)

# df = pd.DataFrame(df)

df["row_number"] = df.index
df["Unnamed: 1"] = df["Unnamed: 1"].replace(" ","_",regex=True).str.lower()
df["Unnamed: 2"] = df["Unnamed: 2"].apply(lambda x: x if x else "NaN").astype(str)

df["Notice_Credit_Decision"] = df["Unnamed: 1"].astype(str) +" | " +df["Unnamed: 2"].astype(str)

first_dataset = df["Notice_Credit_Decision"].to_dict()

first_dataset_list = []
def first_function(x):
#     x is a multiple of 26
    y = x/26
#     if x<100:
#     print(key)
    applicant_data={}
    applicant_set = {k:v for k,v in first_dataset.items() if k>=x and k<26*(y+1)}
    applicant_data[x] = {v for v in applicant_set.values()}
    first_dataset_list.append(applicant_data)

for key, value in first_dataset.items():
    if key%26 == 0:
        first_function(key)

first_ds = []
for i in range(len(first_dataset_list)):
    first_ds.append(list(first_dataset_list[i].values())[0])

first_df = pd.DataFrame(first_ds)

first_df["row_number"] = first_df.index


for col in first_df.columns:

    if col!="row_number":
        feature_columns  = [ "{col}_category".format(col=col), "{col}_data".format(col=col) ]

        first_df2 = first_df[col].str.split(" | ", n = 2, expand = True) 
        first_df[feature_columns[0]]= first_df2[0]
        first_df[feature_columns[1]]= first_df2[2]
        first_df["category"] = first_df2[0]
        first_df["data"] = first_df2[2]
        first_df["row_number"] = first_df.index
        if col == 0:
            first_df_off = first_df[["row_number","0_category" ,"0_data"]]
            first_df_off.columns = ["row_number", "category", "data"]
        else:
            first_df_off = pd.concat([first_df_off[["row_number","category", "data"]], first_df[["row_number","category", "data"]]])

        first_df = first_df.drop(col, axis=1)
        

first_df_off.drop_duplicates(subset=["row_number","category"], keep="first", inplace=True)
first_df_off.reset_index().set_index(['row_number'])

first_df_off = first_df_off.pivot(index="row_number", columns=["category"], values="data")
first_df_off = first_df_off.dropna(how="all", axis=1)
first_df_off = first_df_off.dropna(how="all", axis=0)

if __name__ == "__main__":
