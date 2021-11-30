from flask import Flask, request, render_template

import scipy
from scipy import stats
from scipy.stats import norm

app = Flask(__name__)

def get_pvalue_student(mean_control, std_control, nobs_control, mean_test, std_test, nobs_test):
    return round(stats.ttest_ind_from_stats(mean_control, std_control, nobs_control, mean_test, std_test, nobs_test, equal_var = True)[1],3)

def get_pvalue_conversion(control_size,control_conversion,experiment_size,experiment_conversion):

  ### STEP1: calculate standard error for both groups
  def standard_error(sample_size, successes):
    p = float(successes) / sample_size
    return ((p * (1 - p)) / sample_size) ** 0.5

  ### STE2: calculate z-score
  def zscore(size_a, successes_a, size_b, successes_b):
    p_a = float(successes_a) / size_a
    p_b = float(successes_b) / size_b
    se_a = standard_error(size_a, successes_a)
    se_b = standard_error(size_b, successes_b)
    numerator = (p_b - p_a)
    denominator = (se_a ** 2 + se_b ** 2) ** 0.5
    return numerator / denominator

  ### STEP3: translated z-score to p-value
  def percentage_from_zscore(zscore):
    return norm.sf(abs(zscore))
    
  exp_zscore = zscore(control_size, control_conversion, experiment_size, experiment_conversion)
  
  return percentage_from_zscore(exp_zscore)

@app.route("/")
def home():
    return render_template('page.html') 

@app.route("/pvaluestudent", methods = ['POST'])
def pvalue_student_page():
    message = [item for item in request.form.values()]
    
    mean_control = int(message[0])
    std_control = int(message[1])
    nobs_control = int(message[2])

    mean_test = int(message[3])
    std_test = int(message[4])
    nobs_test = int(message[5])

    pvalue = get_pvalue_student(mean_control, std_control, nobs_control, mean_test, std_test, nobs_test)

    return render_template('page.html', prediction_text1 = 'P-value is: {}'.format(str(pvalue)))

@app.route("/pvalueconversion", methods = ['POST'])
def pvalue_conversion_page():
    message = [item for item in request.form.values()]
    
    numerator_control = int(message[0])
    denominator_control = int(message[1])

    numerator_test = int(message[2])
    denominator_test = int(message[3])    

    pvalue = get_pvalue_conversion(denominator_control, numerator_control, numerator_test, denominator_test)

    return render_template('page.html', prediction_text2 = 'P-value is: {}'.format(str(pvalue)))

if __name__  == '__main__': 
    app.run(debug=True)