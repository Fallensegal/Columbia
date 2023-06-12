# YFinance: Software Design Specification [Updated: 06-11-23]

YFinance will be used to acquire historical data and calculate daily, weekly, and monthly
closing prices on target ticker. The data will then be used to calculate technical indicators

## Capabilities

- Calculate the following technical indicator for a given ticker
	- RSI
	- Bollinger
	- MA (Simple)
	- MACD
	- VWAP

## Design

Each ticker will be inhereting an entity/equity class. In this case [STOCKS] will be the
entity that will need to be modeled out into a class.

```python

Class Entity:
	# contructor
	#	contructor parameters

	# Define Methods
	# (Getters for attributes, modeling functions, destructors for attributes)
```

Acceptance Criteries:
- Class should have attributes for time series data for each technical indicator
- Class should have functions for modeling technical indicators
- Class should be modular to add additional technical indicators and supporting functions
- Class should have finite range for time series data for each technical indicator for vectorized math operation performance considerations
- Class should be inheritable and be able to be used in arbitrary programs and should be agnostic to other micro-services in the ecosystem. 
