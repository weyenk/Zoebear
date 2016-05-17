from data_driven_engine import DataDrivenEngine
import os
__author__ = 'weyenk'
email_address = ""

DataDrivenEngine.run_script(DataDrivenEngine("demo", "big_cat_country_script.json"))

# os.remove("big_cat_country_script.json")



