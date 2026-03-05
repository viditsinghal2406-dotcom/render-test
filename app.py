from flask import Flask, render_template, request
import numpy as np
from scipy import stats

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():

    result = None

    if request.method == "POST":

        try:

            data = request.form.get("data","")
            pop_mean = float(request.form.get("pop_mean",0))
            hypothesis = request.form.get("hypothesis","two-sided")
            alpha = float(request.form.get("alpha",0.05))

            data = [float(x.strip()) for x in data.split(",") if x.strip()!=""]

            if len(data) < 2:
                raise ValueError("Enter at least 2 numbers")

            sample_mean = np.mean(data)
            sample_std = np.std(data, ddof=1)
            n = len(data)

            t_stat, p_val = stats.ttest_1samp(data,pop_mean,alternative=hypothesis)

            decision = "Reject Null Hypothesis" if p_val < alpha else "Fail to Reject Null Hypothesis"

            result = {
                "n": n,
                "mean": round(sample_mean,4),
                "std": round(sample_std,4),
                "t": round(t_stat,4),
                "p": round(p_val,6),
                "decision": decision
            }

        except Exception as e:

            result = {
                "n": "-",
                "mean": "-",
                "std": "-",
                "t": "-",
                "p": "-",
                "decision": "Error: " + str(e)
            }

    return render_template("index.html",result=result)


if __name__ == "__main__":
    app.run(debug=True)