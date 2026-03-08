## How to do the taxes?
This script focuses on transations from a foreign broker which doesn't provide
PIT-8C. 
For such operations a PIT-38 has to be filled.
In the tax settlement should be covered transactions that involve
sale of financial instruments.

### For each transaction, we need:
- instrument
- currency
- transaction type
- size
- price
- net amount
- commission

### We calculate:
- revenue (price x size)
- costs:
  - expenditure (FIFO, first bought first sold)
    - for each part, get net amount
  - commission (FIFO)
  - other
    - account cost
    - currency convertion cost

### Convert to PLN:
- calculate working day in Poland preceding the settlement (in other words, one day before the settlement)
  - for broker costs it's usually one day before the cost was settled
  - for revenues and commissions it's a day preceding the settlement
- fetch NBP middle exchange rate
- calculate the revenues and costs by rounding up to 1 grosz (0,01 PLN)

## High level implementation

### 1. Generate reports from Interactive Brokers
Manually generate report..
activity statement
needed:

### 2. Convert the Interactive Brokers report into a list of transactions

### 3. Convert to PLN

### 4. Calculate totals
