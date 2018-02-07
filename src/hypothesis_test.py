import scipy.stats as scs
import pandas as pd
import numpy as np


def compare_two_pops(pop1, pop2):
    '''
    find p-val for Ha : pop1 is higher liked than pop2
    '''
    
    mean_dif = pop1.mean() - pop2.mean()
    est_pop_std = np.sqrt(pop1.std()**2/len(pop1) + pop2.std()**2/len(pop2))
    df = find_deg_free(pop1, pop2)
    t= mean_dif/ est_pop_std
    students = scs.t(df=df)
    p_val = 1-students.cdf(t)
    return "Ha: pop1 is higher liked than pop2. p-val: {}".format(p_val)
    
def find_deg_free(sample_1, sample_2):
    ss1 = len(sample_1)
    ss2 = len(sample_2)
    df = (
        ((np.var(sample_1)/ss1 + np.var(sample_2)/ss2)**(2.0)) / 
        ((np.var(sample_1)/ss1)**(2.0)/(ss1 - 1) + (np.var(sample_2)/ss2)**(2.0)/(ss2 - 1))
    )
    return df

def plot_pdf_with_alpha():
    x = np.linspace(-3, 3, num=250)
    fig, ax = plt.subplots(1, figsize=(16, 3))
    students = scs.t(df=df)
    ax.plot(x, students.pdf(x), linewidth=2, label="Degree of Freedom: {:2.2f}".format(df))
    _ = ax.fill_between(x, students.pdf(x), where=(x >= t), color="red", alpha=0.25)
    ax.legend()
    ax.set_title("p-value Reigon")