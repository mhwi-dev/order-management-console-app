# Console Shop App

A small console application written in Python for managing users, products, shopping carts and orders.
Data is stored in local JSON files. I built this project to practice **layered architecture** and clean code in Python, and I am improving it step by step (see the [Roadmap](#roadmap)).

## Features

**Admin**
- Sign up new admin or customer accounts
- View invalid users and invalid products
- Add a new product
- Review and update products
- Review and delete products

**Customer**
- Sign up and log in
- Browse products
- Add products to the cart
- View the cart
- Place an order

## Project structure

The code is split into layers. Each layer has one job and only talks to the layer below it.

```
.
├── main.py             # Entry point: creates all objects and connects them
├── controllers/        # Console menus and user input/output
├── services/           # Business rules (validation, checkout logic)
├── repositories/       # Reading and writing JSON files
├── mappers/            # Convert between JSON data and model objects
├── models/             # Plain classes: User, Product, Cart, Order
├── utils/              # Shared helpers (for example, input validation)
├── data/               # JSON data files
└── tests/              # Tests
```

How the layers work together:

```
Controller  ->  Service  ->  Repository  ->  JSON file
(menu, I/O)   (rules)      (storage)         (data/)
```

Dependencies are passed in through constructors (dependency injection) and wired up in `main.py`. This makes it easy to replace a layer later, for example switching from JSON files to a database by writing a new repository.

Files are saved safely: the repository writes to a temporary file first and then replaces the real file, so a crash in the middle of saving does not corrupt the data.

## Getting started

**Requirements:** Python 3.10 or newer (no external packages needed).

1. Clone the repository:

   ```bash
   git clone https://github.com/mhwi-dev/order-management-console-app.git
   cd order-management-console-app
   ```

2. Create your data files from the samples. The real `data/*.json` files are ignored by Git, so they are not in the repository:

   ```bash
   cp data/users.sample.json data/users.json
   cp data/products.sample.json data/products.json
   cp data/carts.sample.json data/carts.json
   cp data/orders.sample.json data/orders.json
   ```

3. Run the app:

   ```bash
   python main.py
   ```

4. Log in with a demo account from `data/users.sample.json`, or choose **Sign up** to create a new one.

> The sample accounts contain fake data for demo purposes only.

## Tests

Tests are in the `tests/` folder. Test coverage is still in progress, and adding tests for the cart, product and order services is the next step.

## Roadmap

- [ ] Add tests for cart, product and order services
- [ ] Hash passwords instead of storing plain text
- [ ] Make placing an order safe: save the order and update stock together, or neither
- [ ] Replace JSON storage with SQLite or PostgreSQL (only the repository layer should change)
- [ ] Build a REST API with FastAPI on top of the existing services

## What I learned

- Splitting an application into controller, service and repository layers
- Dependency injection through constructors
- Writing data to files safely
- Separating data models from storage with mappers

## Author

**Nguyen Minh Huy** — [GitHub](https://github.com/mhwi-dev)