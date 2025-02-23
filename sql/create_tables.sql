CREATE TABLE stg.day_metadata (
    record_date DATE DEFAULT CURRENT_DATE,
    symbol VARCHAR(10),
    status VARCHAR(10),
    strategy VARCHAR(10),
    interval FLOAT,
    isDelayed BOOLEAN,
    isIndex BOOLEAN,
    interestRate FLOAT,
    underlyingPrice FLOAT,
    volatility FLOAT,
    daysToExpiration FLOAT,
    dividendYield FLOAT,
    numberOfContracts INT,
    assetMainType VARCHAR(10),
    assetSubType VARCHAR(10),
    isChainTruncated BOOLEAN
);