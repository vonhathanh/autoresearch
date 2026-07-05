# Overview

An implementation from Karpathy's idea of autoresearch, focusing on Smart Contract Auditing & Low Frequency Trading

# The loop
## Smart contract audit
1. Agent read contracts code in /target folder
2. Read audit history in history.csv
3. Conduct new exploit direction

    3.1 Check past experiments to see if they are worth exploit more or it's better to just seek for new direction

4. Implement & test that approach
5. Evaluate the result then save this experiment to history.csv
6. If goal is reached: stop, else repeat step 2.

## Low frequency trading
Two agents:
- The Trader: invent new trading strategy and follow the rules from start to finish (backtest period)
- The Evaluator: review the trading history, strategy and add comments, suggestion based on the result

Loop until PnL is > predefined threshold
Evaluator's suggestion may recommend based on the current chart -> it's suggestion might overfit the price data -> The Trader must be able to push back what The Evaluator said