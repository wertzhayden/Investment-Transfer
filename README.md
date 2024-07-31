# building-for-fun


Problem

1. Transfer Money from an “investor” account to the “funds” account
2. Handle Multiple Transaction Simultaneously 
    1. Use Async Tasks via Celery to handle multiple transactions at once
3. Ensure Proper Accounting & Record Keeping 
    1. Store the Transactions in the DB
        1. Ensure that we know when Investor A has sent “X dollars” to Funds A or Funds B
4. Provide Real-time Updates on Transaction Status


Solution

1. Create "Base" Model
    a. created_at - Date/Time
    b. updated_at - Date/Time

1. Create "Investor" Model w/ Base Model inherited
    a. ID - String
    b. Email - String
    c. Balance - Float

2. Create "Fund" Model  w/ Base Model inherited
    a. ID - String
    b. name - String
    c. minimum_investment - Integer
    d. seat_availability - Integer
    e. total_seats - Integer
    f. current_balance - Float
    g. max_fund_size - Integer | None
        i. This will ensure that the Fund does not get oversubscribed above its maximum, if applicable
 
3. Create "Transaction" Model w/ Base Model inherited
    a. ID - String
    b. Investor - Foreign Key
    c. Fund - Foreign Key
    d. Amount - Float
    e. Status - String
    f. Transaction_types - String

4. Create POST "Withdrawal" Endpoint
    a. Withdraw certain "amount" from "Investor.balance"
        b. If "Investor.balance" > "amount":
            i. Remove the amount from balance & Trigger the "Transfer" endpoint
        c. Else:
            i. Return Error that the Investor does not have the available funds

5. Create POST "Transfer" Endpoint
    a. If "Fund.seat_availability" > 0 and "amount" > "Fund.minimum_investment" and "Fund.current_balance" + "amount" < "Fund.max_fund_size" (If max_fund_size is not None)
        i. Transfer "amount" to the Fund.current_balance
        ii. Add "amount" to "Fund.current_balance" 
        iii. Decrease "seat_availability" by 1
    b. Return Error dependent upon which, if multiple, criteria that the "Investor" does not qualify for
        i. Provide a description as to why the "Investor" is not eligible for the given "Fund"

6. Link these two Tasks to run Async together
    a. Do not withdrawal the "amount" from the "Investor.balance" if not available funds & don't Transfer or Update the "Fund" IF:
        i. There are no seats available
        ii. The "amount" does not match the "Fund.minimum_investment" 
        iii. The "amount" + "Fund.current_balance" is less than the "Fund.max_fund_size" (if max_fund_size is not None) 

7. Create GET "Transactions" Endpoint 
    a. Retrieve the List of Transactions by:
        i. Investor
        ii. Fund
    b. Filter by:
        i. status
        ii. transaction_types
        iii. Funds that an Investor is in
        iv. Investors for a given Fund
        v. Any features about an Investor
        vi. Any features about a Fund

8. Create GraphQL Mutation and/or Query for each Endpoint for flexible & convenient client-side payloads


9. Create a Task to transfer to record the Investor Transaction and remove from Investors' balance via Celery
    a. Check if Investors' current_balance >= amount
        i. IF so:
            1. Send the Money to Fund
                a. Check if Fund.current_balance + amount <= Fund.max_fund_size && Fund.seat_availability > 0
                    i. If so:
                        1. Remove amount from Investor.balance (Withdrawal)
                        2. Add the amount to Fund.current_balance (Deposit)
                        3. Decrease the seat_availability by 1
                b. Else (Transaction Failed)
                    i. Return Error that Fund is at maximum seat capacity and/or max fund size
                        1. Dependent upon whether either/both are true
        ii. Else (Transaction Failed):
            1. Return Error that Investor does not have available funds  

10. I will need to create a Task to record the Transaction being added it to the Fund's current balance 


