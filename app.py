import os
import subprocess
from flask import Flask, redirect

app = Flask(__name__)

@app.route("/")
def index():
    return redirect("/streamlit/")

def run_streamlit():
    os.system("streamlit run frontend.py --server.port 8501 --server.address 0.0.0.0")

if __name__ == "__main__":
    subprocess.Popen(run_streamlit, shell=True)
    app.run(host="0.0.0.0", port=5000)