from data_driven_engine import DataDrivenEngine
import os
__author__ = 'weyenk'
email_address = ""


dda = DataDrivenEngine("demo", "Demo.json")
dda.run_script()
# os.remove("big_cat_country_script.json")



