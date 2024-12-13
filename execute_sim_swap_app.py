import streamlit
import pandas
import xlsxwriter
import streamlit.web.cli as stcli
import streamlit.runtime.scriptrunner.magic_funcs
import os, sys
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="extra_streamlit_components")

if __name__ == "__main__":
     os.chdir(os.path.dirname(__file__))
     
     sys.argv=["streamlit", "run", "app.py", "--server.port=8501", "--global.developmentMode=false",
               "--theme.base=light", "--theme.primaryColor=#10475a", "--theme.secondaryBackgroundColor=#f2f9f2"]
     stcli.main()