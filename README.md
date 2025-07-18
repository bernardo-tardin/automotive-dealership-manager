# Automotive Dealership Management System
This is a complete desktop management solution built in Python for a small-scale automotive dealership. The application provides a full suite of tools to handle the entire sales lifecycle, from initial financing simulations to final contract generation and payment tracking.

## Core Features
* **Sales & Client Management** 🧑‍💼

    * A comprehensive sales interface to register new clients, vehicle details, and complete sales transactions.

    * Stores all client and sales data persistently in a local database.json file.

    * Includes fields for client identification (Citizen's Card, Residence Permit, Passport).

* **Financing & Simulation** 🧮

    * Calculates complete loan amortization schedules based on total value, down payment, interest rate, and number of installments.

    * Generates a detailed Financing Simulation PDF with a full payment table (principal, interest, remaining balance) for clients.

* **Automated Document Generation** 📄

    * Sales Contracts: Automatically generates a multi-page, professionally formatted PDF contract for each sale. This document includes all buyer and vehicle information, financial terms, and a complete installment schedule table.

    * Payment Receipts: Instantly generates PDF receipts for both the initial down payment and subsequent installment payments.

    * All documents are branded with a company logo and a watermark.

* **Financial Tracking & Reporting** 📈

    * A dedicated "Transactions" module to view a complete history of all sales, cash inflows, and cash outflows.

    * Data can be sorted and viewed by category.

    * Allows for the export of financial statements (Extratos) to a .csv file for use in spreadsheet software.
