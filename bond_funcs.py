
import numpy as np 
import plotly.express as px 

#BOND PRICING
def price(n,c,A,y):
    """
    Calculate the present value of a bond.

    Parameters:
    - n: Maturity (years)
    - c: Coupon Rate (%)
    - A: Principal ($)
    - y: Discount Rate (%)

    Returns:
    - B: Present value of the bond
    """

    C = A*c 
    B = 0
    for t in range(1,n+1):
        d =  np.exp(-y*t)  
        B = B + C*d 

    B = B + A*np.exp(-y*n) 

    return B

# DURATION
def duration(n,c,A,y):
    """
    Calculate the duration of a given bond.

    Parameters:
    - n: Maturity (years)
    - c: Coupon Rate (%)
    - A: Principal ($)
    - y: Discount Rate (%)

    Returns:
    - D: Duration of the bond (years)
    """
    B = price(n,c,A,y)
    C = A*c 
    D = 0
    for t in range(1,n+1):
        d_w =  t*np.exp(-y*t)  
        D = D + C*d_w 

    D = (D + A*np.exp(-y*n)*n)/B
    return D

# CONVEXITY
def convexity(n,c,A,y):
    """
    Calculate the convexity of a given bond.

    Parameters:
    - n: Maturity (years)
    - c: Coupon Rate (%)
    - A: Principal ($)
    - y: Discount Rate (%)

    Returns:
    - C: Convexity of the bond 
    """
    B = price(n,c,A,y)
    C = A*c 
    Cvx = 0
    for t in range(1,n+1):
        d_w =  (t**2)*np.exp(-y*t)  
        Cvx = Cvx + C*d_w 

    Cvx = (Cvx + A*np.exp(-y*n)*(n**2))/B 
    return Cvx

# SECOND ORDER APPROX. FOR BOND PRICES
def sensibility(n,c,A,y,delta_y):
    """
    Calculate the second order approximation for bond price movements

    Parameters:
    - n: Maturity (years)
    - c: Coupon Rate (%)
    - A: Principal ($)
    - delta_y: Change on interest rates

    Returns:
    - risk_B: percentage changes in bond price (%) 
    """
    D = duration(n,c,A,y)
    C = convexity(n,c,A,y)
    risk_B = -D*delta_y + 0.5*C*(delta_y)**2
    return risk_B