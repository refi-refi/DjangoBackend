DROP DATABASE IF EXISTS tykee_dj;
DROP ROLE IF EXISTS tykee_dj;

CREATE ROLE tykee_dj
SUPERUSER
LOGIN
PASSWORD 'tykee';

-- DROP DATABASE IF EXISTS test_tykee;
CREATE DATABASE tykee_dj
-- CREATE DATABASE test_tykee
	WITH
	OWNER = tykee
	TEMPLATE = template0
	ENCODING = 'UTF8'
  	LC_COLLATE = 'en_US.UTF-8'
  	LC_CTYPE = 'en_US.UTF-8';

\c tykee_dj;
-- \c test_tykee;

DROP SCHEMA IF EXISTS forex CASCADE;
CREATE SCHEMA forex
-- DROP SCHEMA IF EXISTS test_forex CASCADE;
-- CREATE SCHEMA test_forex
	CREATE TABLE position_types(
		id 		                BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
		position_type_value     BIGINT NOT NULL UNIQUE,
		name	                TEXT NOT NULL UNIQUE
		)
	CREATE TABLE breakeven_flags(
		id 		                BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
		breakeven_flag_value 	BIGINT NOT NULL UNIQUE,
		name 	                TEXT NOT NULL UNIQUE
		)
	CREATE TABLE close_types(
		id 		            BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
		close_type_value 	BIGINT NOT NULL UNIQUE,
		name 	            TEXT NOT NULL UNIQUE
		)
	CREATE TABLE periods(
		id 					BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
		period_id 			BIGINT NOT NULL UNIQUE,
		name 				TEXT NOT NULL UNIQUE,
		period_minutes      BIGINT NOT NULL,
		trunc_period 		TEXT NOT NULL,
		part_period 		TEXT,
		part_value 			INTEGER,
		period_interval 	TEXT NOT NULL
		)
	CREATE TABLE symbols(
		id 				BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
		symbol_id       BIGINT NOT NULL UNIQUE,
        name 			TEXT NOT NULL UNIQUE,
		base_currency 	TEXT NOT NULL,
		quote_currency 	TEXT NOT NULL,
		digits 			INT NOT NULL
		)
	CREATE TABLE strategies(
		id 				BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        strategy_id     BIGINT NOT NULL UNIQUE,
		name 			TEXT NOT NULL UNIQUE
		)
	CREATE TABLE backtests(
		id 						BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        backtest_id             BIGINT NOT NULL UNIQUE,
		strategy_id 			BIGINT NOT NULL,
		symbol_id				BIGINT NOT NULL,
		period_id 				BIGINT NOT NULL,
		start_balance 			REAL NOT NULL,
        account_currency 		TEXT NOT NULL,
		date_from 				BIGINT NOT NULL,
		date_to 				BIGINT NOT NULL,
		session_limits 			TEXT NOT NULL,
		inputs 					TEXT NOT NULL,
		entry_list 				TEXT NOT NULL,
		exit_list 				TEXT NOT NULL,
		confirmation_list 		TEXT NOT NULL,
		profit 					REAL NOT NULL,
		profit_factor 			REAL NOT NULL,
		drawdown 				REAL NOT NULL,
		total_trades 			INTEGER NOT NULL,
		win_rate 				REAL NOT NULL,
		FOREIGN KEY(strategy_id) REFERENCES strategies(strategy_id) ON DELETE CASCADE,
		FOREIGN KEY(symbol_id) REFERENCES symbols(symbol_id),
		FOREIGN KEY(period_id) REFERENCES periods(period_id)
		)
	CREATE TABLE positions(
		id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
		order_number INT NOT NULL,
		open_time BIGINT NOT NULL,
		close_time BIGINT NOT NULL,
		lot_size REAL NOT NULL,
		open_price REAL NOT NULL,
		close_price REAL NOT NULL,
		sl_price REAL NOT NULL,
		tp_price REAL NOT NULL,
		gross_profit REAL NOT NULL,
		net_profit REAL NOT NULL,
		commission REAL NOT NULL,
		swap REAL NOT NULL,
        balance REAL NOT NULL,
        backtest_id BIGINT NOT NULL,
        position_type_id INT NOT NULL,
		breakeven_flag_id INTEGER NOT NULL,
		close_type_id INTEGER NOT NULL,
		FOREIGN KEY(backtest_id) REFERENCES backtests(backtest_id) ON DELETE CASCADE,
		FOREIGN KEY(position_type_id) REFERENCES position_types(id),
		FOREIGN KEY(breakeven_flag_id) REFERENCES breakeven_flags(id),
		FOREIGN KEY(close_type_id) REFERENCES close_types(id)
		)
	CREATE TABLE bars(
		id 				BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
		symbol_id 		BIGINT NOT NULL,
		period_id		BIGINT NOT NULL,
		start_dt	 	TIMESTAMP WITH TIME ZONE NOT NULL,
		end_dt	 		TIMESTAMP WITH TIME ZONE NOT NULL,
		open 			INT NOT NULL,
		high 			INT NOT NULL,
		low 			INT NOT NULL,
		close 			INT NOT NULL,
		spread 			INT NOT NULL,
		volume 			INT NOT NULL,
		created_at 		TIMESTAMP WITH TIME ZONE NOT NULL,
		updated_at 		TIMESTAMP WITH TIME ZONE NOT NULL,
	 	FOREIGN KEY (symbol_id) REFERENCES symbols (symbol_id) ON DELETE CASCADE,
	 	FOREIGN KEY (period_id) REFERENCES periods (period_id),
	 	UNIQUE(symbol_id, start_dt, end_dt)
	 	)
	CREATE TABLE ticks(
		id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
		symbol_id BIGINT NOT NULL,
		ts_utc BIGINT NOT NULL,
		bid BIGINT NOT NULL,
		ask BIGINT NOT NULL,
		flags INT NOT NULL,
		FOREIGN KEY (symbol_id) REFERENCES symbols (symbol_id) ON DELETE CASCADE
		);


INSERT INTO forex.position_types (position_type_value, name)
VALUES (0, 'Long'),(1, 'Short');

INSERT INTO forex.breakeven_flags (breakeven_flag_value, name)
VALUES (0, 'No BreakEven'),(1, 'BreakEven');


INSERT INTO forex.close_types (close_type_value, name)
VALUES (0, 'Manual'), (1, 'Automatic');

INSERT INTO forex.periods (period_id, name, period_minutes, trunc_period, part_period, part_value, period_interval)
VALUES
(1, 'M1', 1, 'hour', 'minute', 1, '1 minute'),
(2, 'M5', 5, 'hour', 'minute', 5, '5 minutes'),
(3, 'M10', 10, 'hour', 'minute', 10, '10 minutes'),
(4, 'M15', 15, 'hour', 'minute', 15, '15 minutes'),
(5, 'M30', 30, 'hour', 'minute', 30, '30 minutes'),
(6, 'H1', 60, 'hour', 'minute', 60, '60 minutes'),
(7, 'H4', 240, 'day', 'hour', 4, '4 hours'),
(8, 'DAY', 1440, 'day', 'hour', 24, '24 hours');
INSERT INTO forex.periods (period_id, name, period_minutes, trunc_period, period_interval)
VALUES
(9, 'WEEK', 10800, 'week', '7 days'),
(10, 'MONTH', 43200, 'month', '1 month');

INSERT INTO forex.symbols (symbol_id, name, base_currency, quote_currency, digits)
VALUES
(1, 'AUDCAD', 'AUD', 'CAD', 5),
(2, 'AUDCHF', 'AUD', 'CHF', 5),
(3, 'AUDJPY', 'AUD', 'JPY', 3),
(4, 'AUDNZD', 'AUD', 'NZD', 5),
(5, 'AUDUSD', 'AUD', 'USD', 5),
(6, 'CADCHF', 'CAD', 'CHF', 5),
(7, 'CADJPY', 'CAD', 'JPY', 3),
(8, 'CHFJPY', 'CHF', 'JPY', 3),
(9, 'EURAUD', 'EUR', 'AUD', 5),
(10, 'EURCAD', 'EUR', 'CAD', 5),
(11, 'EURCHF', 'EUR', 'CHF', 5),
(12, 'EURGBP', 'EUR', 'GBP', 5),
(13, 'EURJPY', 'EUR', 'JPY', 3),
(14, 'EURNZD', 'EUR', 'NZD', 5),
(15, 'EURUSD', 'EUR', 'USD', 5),
(16, 'GBPAUD', 'GBP', 'AUD', 5),
(17, 'GBPCAD', 'GBP', 'CAD', 5),
(18, 'GBPCHF', 'GBP', 'CHF', 5),
(19, 'GBPJPY', 'GBP', 'JPY', 3),
(20, 'GBPNZD', 'GBP', 'NZD', 5),
(21, 'GBPUSD', 'GBP', 'USD', 5),
(22, 'NZDCAD', 'NZD', 'CAD', 5),
(23, 'NZDCHF', 'NZD', 'CHF', 5),
(24, 'NZDJPY', 'NZD', 'JPY', 3),
(25, 'NZDUSD', 'NZD', 'USD', 5),
(26, 'USDCAD', 'USD', 'CAD', 5),
(27, 'USDCHF', 'USD', 'CHF', 5),
(28, 'USDJPY', 'USD', 'JPY', 3);