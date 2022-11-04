# DjangoREST

Tykee REST microservice using Django and Postgres.


## Setup

### Pre-requisites

- Python 3.10
- Postgres 15.0

### Installation

In my experience the best way to work with backend is to first write schema and initailize the database. This is done by running the following command:

```bash
psql -U postgres -d postgres -a -f schema.sql
```

This will create a database called `tykee` and a user called `tykee` with password `tykee`. You can change this in the `postgres/schema.sql` file.

Afterwards run the following command to insert initial data into the database:

```bash
psql -U tykee -d tykee -a -f data.sql
```

- Clone the repository
- Create a virtual environment
- Install the requirements
- Create a .env file in the root directory and add the following variables

```
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=*
DATABASE_URL=postgres://user:password@localhost:5432/db_name
```



## Business Logic

In this DEMO repository, I have implemented the following business logic:

```mermaid
graph LR
    A[MetaTrader4] -->|Web Request| B(Django)
    B --> C{Processing POST}
    C --> D[Save Strategy]
    C -->E[Backtest Positions]
    E -->|Calculate Backtest Stats| F[Save Backtest]
    D --> F
    F -->G[Save Positions]
```

The following is a brief description of each step:
1. MetaTrader4 sends a POST request to the Django REST API.
    ```json
    {
      "strategy_name": "",
      "backtest": {},
      "positions": []
    }
    ```
   
2. The Django REST API saves the strategy if it's new model.
3. Before saving Backtest results, we must calculate few statistics from positions, like
    * Profit and Profit Factor
    * Maximum Drawdown
    * Total Trades
    * Win Rate

4. The Django REST API saves the backtest results.
5. The Django REST API saves the positions.

### Main Entity Relationship Diagram

```mermaid
    erDiagram
        STRATEGY ||--o{ BACKTEST : has
        BACKTEST ||--o{ POSITION : has
```