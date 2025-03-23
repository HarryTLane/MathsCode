
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Callable, Generator, Any, Iterator

def calculate_monthly_payment(principal: float, monthly_interest_rate: float, number_of_payments: int) -> float:
    
    return ( principal * monthly_interest_rate ) / ( 1 - (1 + monthly_interest_rate) ** (-number_of_payments) )

def get_repayments_dataframe(principal: float, monthly_interest_rate: float, number_of_payments: int) -> pd.DataFrame:

    monthly_payment = calculate_monthly_payment(principal, monthly_interest_rate, number_of_payments)
    
    df = pd.DataFrame({
        'month': np.arange(1, number_of_payments + 1),
        'interest_paid': 0.0,
        'principal_paid': 0.0,
        'total_paid': 0.0,
        'remaining': 0.0,
    })
    
    remaining = principal

    for index in range(len(df)):

        df.at[index, 'interest_paid'] = remaining * monthly_interest_rate
        df.at[index, 'principal_paid'] = monthly_payment - df.at[index, 'interest_paid']
        df.at[index, 'total_paid'] = monthly_payment
        remaining -= df.at[index, 'principal_paid']
        df.at[index, 'remaining'] = remaining

    return df


def get_repayments_dataframe_nicely_formatted(principal: float, monthly_interest_rate: float, number_of_payments: int) -> pd.DataFrame:

    df = get_repayments_dataframe(principal, monthly_interest_rate, number_of_payments)
    df = df[['month', 'principal_paid', 'interest_paid', 'total_paid', 'remaining']]    
    
    for col in ['interest_paid', 'total_paid', 'principal_paid', 'remaining']:
        df[col] = df[col].map(lambda x: f'£{max(x, 0):.2f}')

    return df

def draw_interest_principal_chart(principal: float, monthly_interest_rate: float, number_of_payments: int) -> None:
    df = get_repayments_dataframe(principal, monthly_interest_rate, number_of_payments)
    
    plt.figure(figsize=(12, 6))
    plt.bar(df['month'], df['interest_paid'], label='Interest Paid', color='lightcoral')
    plt.bar(df['month'], df['principal_paid'], bottom=df['interest_paid'], label='Principal Paid', color='lightblue')
    plt.title('Loan Repayment Breakdown Over Time')
    plt.xlabel('Month')
    plt.ylabel('Payment Amount (£)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5, axis='y')
    plt.show()




def newtons_method(x: float, func: Callable[[float], float], deriv: Callable[[float], float]) -> float:
    return x - ( func(x) / deriv(x) )

def calculate_apr_newton(
        principal: float,
        monthly_payment: float,
        number_of_payments: int,
        start_apr: float = 0.5,
    ) -> Generator[float, None, None]:

    func = lambda x: 12 * monthly_payment - principal * x - 12 * monthly_payment * (1 + (1/12) * x) ** (- number_of_payments)
    deriv = lambda x: monthly_payment * (1 + 1/12 * x) ** (-number_of_payments - 1) - principal
    
    apr = start_apr
    fx = 1.0 # test value
    while fx != 0.0:
        fx = func(apr)
        apr = apr - (fx / deriv(apr))
        yield apr

    while True: yield apr



def sign_is_different(x: float, y: float) -> bool:
    return (x > 0) ^ (y > 0)

def calculate_apr_bisection(
        principal: float,
        monthly_payment: float,
        number_of_payments: int,
        start_a: float = 0.001,
        start_b: float = 1
    ) -> Generator[float, None, None]:

    func = lambda x: 12 * monthly_payment - principal * x - 12 * monthly_payment * (1 + (1/12) * x) ** (- number_of_payments)

    a, b = start_a, start_b


    fa, fb = func(a), func(b)

    if fa == 0.0:
        while True: yield a
    if fb == 0.0:
        while True: yield b

    assert sign_is_different(fa, fb), f'Could not find root in the supplied interval ( f({a})={fa}, f({b})={fb} ).'

    while True:
        c = (a + b) / 2
        fc = func(c)

        if sign_is_different(fa, fc):
            # root is between a and c
            b = c
            fb = func(b)
            if fb == 0.0:
                while True: yield b

        else:
            # root is between c and b
            a = c
            fa = func(a)
            if fa == 0.0:
                while True: yield a

        yield (a + b) / 2


# NOTE: I already derived the loan function so there is no need for SymPy I beleive.

# test function?

def compare_methods(
        principal: float,
        monthly_payment: float,
        number_of_payments: int,
        true_apr: float,
        iterations: int = 10
    ) -> None:
    newton_generator = calculate_apr_newton(principal, monthly_payment, number_of_payments)
    newton_estimates_list: list[float] = []
    for count, apr in enumerate(newton_generator):
        if count >= iterations: break
        newton_estimates_list.append(apr)

    bisection_generator = calculate_apr_bisection(principal, monthly_payment, number_of_payments)
    bisection_estimate_list: list[float] = []
    for count, apr in enumerate(bisection_generator):
        if count >= iterations: break
        bisection_estimate_list.append(apr)
        

    bisection_generator = calculate_apr_bisection(principal, monthly_payment, number_of_payments)




    newton_estimates, bisection_estimates = np.array(newton_estimates_list), np.array(bisection_estimate_list)
    newton_errors = np.abs(newton_estimates - true_apr) / np.abs(true_apr)
    bisection_errors = np.abs(bisection_estimates - true_apr) / np.abs(true_apr)

    plt.semilogy(np.arange(1, iterations + 1), newton_errors, label='Newton\'s Method')
    plt.semilogy(np.arange(1, iterations + 1), bisection_errors, label='Bisection Method')

    plt.xlabel('Iteration number')
    plt.ylabel('Error (log scale)')
    plt.title('Error vs Iteration')
    plt.legend()
    plt.show()

'''
Conditions under which methods might fail to converge:

Newton's Method:
- Bad Initial Guess
- Flat Derivative Near the Root
- Division by Zero or Near-Zero Values
- Non-Physical or Invalid Roots
- Complex Roots

Bisection Method:
- No Sign Change in the Interval
- Multiple Roots in the Interval
- If the function is very Flat over the Interval


'''



TEST_CASES: list[dict[str, Any]] = [
    {
        'principal': 512,
        'annual_interest_rate': 0.85,
        'number_of_payments': 24,
        'monthly_payment': 44.96781634956033,
    },
    {
        'principal': 1000,
        'annual_interest_rate': 0.10,
        'number_of_payments': 12,
        'monthly_payment': 87.91588723000987,
    },
    {
        'principal': 2000,
        'annual_interest_rate': 0.50,
        'number_of_payments': 6,
        'monthly_payment': 383.5964162614617,
    }
]

def generate_until_error_acceptable(target: float, acceptable_error: float, iterator: Iterator[float]) -> int:

    count = 0
    error = float('inf')
    while error > acceptable_error:
        count += 1
        error = abs(next(iterator) - target) / abs(target)

    return count


def compare_efficiency():

    acceptable_error = 10e-5

    for test_case in TEST_CASES:
        print (f"principal: {test_case['principal']}")
        print (f"monthly payment: {test_case['monthly_payment']}")
        print (f"number of payments: {test_case['number_of_payments']}")

        newton_estimate_generator = calculate_apr_newton(
            test_case['principal'],
            test_case['monthly_payment'],
            test_case['number_of_payments'],
        )
        bisection_estimate_generator = calculate_apr_bisection(
            test_case['principal'],
            test_case['monthly_payment'],
            test_case['number_of_payments'],
        )

        print (f"number of iterations newton: {generate_until_error_acceptable(test_case['annual_interest_rate'], acceptable_error, newton_estimate_generator)}")
        print (f"number of iterations bisection: {generate_until_error_acceptable(test_case['annual_interest_rate'], acceptable_error, bisection_estimate_generator)}")
        print()

# Write a Python function that calculates the monthly payment M given the principal P, monthly interest rate r, and number of payments n.

def run_task1():
    monthly_payment = calculate_monthly_payment(
        TEST_CASES[0]['principal'],
        TEST_CASES[0]['annual_interest_rate'] / 12,
        TEST_CASES[0]['number_of_payments']
    )
    print (
        f"For test case 1, monthly payment = {monthly_payment}"
    )

# Write a function that creates a table showing how much of each payment goes towards interest and how much goes towards paying off the loan (interest = P x r, principal = M-interest)

def run_task2():
    table = get_repayments_dataframe_nicely_formatted(
        TEST_CASES[0]['principal'],
        TEST_CASES[0]['annual_interest_rate'] / 12,
        TEST_CASES[0]['number_of_payments']
    )
    print (table)

# Create a visualization showing the balance reduction over time and the proportion of each payment that goes to interest versus principal.

def run_task3():
    draw_interest_principal_chart(
        TEST_CASES[0]['principal'],
        TEST_CASES[0]['annual_interest_rate'] / 12,
        TEST_CASES[0]['number_of_payments']
    )

# Implement Newton’s method to find the monthly interest rate r when P, M and n are known. This simulates finding the APR (Annual Percentage Rate) of a loan.

def run_task4():
    num_iterations = 10

    newtons_method_generator = calculate_apr_newton(
        TEST_CASES[0]['principal'],
        TEST_CASES[0]['monthly_payment'],
        TEST_CASES[0]['number_of_payments']
    )

    for index in range(num_iterations):
        print (f'APR{index} = {next(newtons_method_generator)}')

# Implement the bisection method to solve for the same problem and compare the efficiency and accuracy of both methods.

def run_task5():
    num_iterations = 10

    bisection_method_generator = calculate_apr_bisection(
        TEST_CASES[0]['principal'],
        TEST_CASES[0]['monthly_payment'],
        TEST_CASES[0]['number_of_payments']
    )

    for index in range(num_iterations):
        print (f'APR{index} = {next(bisection_method_generator)}')

# Use SymPy to find the derivative of the loan equation with respect to r for use in Newton’s method. (Be careful of the difference between functions in SymPy and Python)

# NOTE: I didn't use SymPy since I already differentiated the function for Newton's method.

# Test your root-finding implementation on several example cases where you know the correct answer by creating test cases.

def run_task7():
    
    num_iterations = 10

    for index, test_case in enumerate(TEST_CASES):
        
        newtons_method_generator = calculate_apr_newton(
            test_case['principal'],
            test_case['monthly_payment'],
            test_case['number_of_payments']
        )

        bisection_method_generator = calculate_apr_bisection(
            test_case['principal'],
            test_case['monthly_payment'],
            test_case['number_of_payments']
        )
        newton_apr = bisection_apr = 0.0
        for _ in range(num_iterations): newton_apr = next(newtons_method_generator)
        for _ in range(num_iterations): bisection_apr = next(bisection_method_generator)
        
        print (f'Test {index + 1}')
        print (f"Actual APR = {test_case['annual_interest_rate']}")
        print (f'Newton APR Estimate = {newton_apr}')
        print (f'Bisection APR Estimate = {bisection_apr}')
        print()

# Plot the error versus iteration number for both methods on a logarithmic scale

def run_task8():
    compare_methods(
        TEST_CASES[0]['principal'],
        TEST_CASES[0]['monthly_payment'],
        TEST_CASES[0]['number_of_payments'],
        TEST_CASES[0]['annual_interest_rate']
    )

# Compare the computational efficiency of both methods by measuring the number of iterations required to reach a given precision.

def run_task9():
    compare_efficiency()


def test():
    run_task9()

if __name__ == '__main__':

    test()
