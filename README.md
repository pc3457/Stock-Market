# Stock Market and Personalized Portfolio

## Introduction

### Overview
- Stock market prediction is a crucial aspect of financial planning and investment strategy. By accurately forecasting stock prices, investors can make informed decisions, potentially maximizing their returns and minimizing risks. This project leverages advanced software engineering techniques to develop a robust stock market prediction system.
- In this report, we will explore the journey of our project, starting from the initial requirements gathering to the deployment of our application. We'll delve into the technical intricacies of our design, development, and deployment processes, highlighting the challenges we faced and the solutions we implemented.

## Technologies Used
- AWS S3
- Azure ML Studio
- Python
- JavaScript
- Streamlit
- Socket.io

## Requirements Engineering

### Requirements Gathering

**Python Package: yfinance**

Overview: yfinance is a widely used Python library that enables easy access to historical and real-time market data from Yahoo Finance.

**Features:**
- **Historical Data:** Fetches historical market data for a variety of financial instruments, including stocks, ETFs, and mutual funds.
- **Real-Time Information:** Provides real-time price updates and fundamental data such as earnings, dividends, and stock splits.
- **Data Manipulation:** Offers robust support for data manipulation and analysis, facilitating deeper insights and integration with predictive models.

### Functional Requirements
- **Data Retrieval:** Ability to fetch historical and real-time stock data using yfinance.
- **Prediction Algorithm:** Implement a reliable prediction algorithm using ML Studio for forecasting stock prices.
- **User Interface:** Develop a user-friendly interface for users to view predictions and historical data.
- **Real-Time Updates:** Ensure the system can provide real-time stock market updates.

### Non-Functional Requirements
- **Performance:** The system should process and return predictions quickly.
- **Scalability:** Able to handle increasing amounts of data and users.
- **Security:** Ensure data privacy and secure user transactions.
- **Usability:** Interface should be intuitive and easy to navigate.

## Stakeholders
- **Investors:** Primary users who will utilize the system for making investment decisions.
- **Financial Analysts:** Professionals who might use the tool for market analysis and reporting.
- **Developers:** Team responsible for developing and maintaining the system.

## Feasibility Report

### Technical Feasibility
- **Technology Stack:** Assess the suitability of technologies like Python, Azure, AWS, Socket.io, and Heroku.
- **Development Tools:** Evaluate tools for development, testing, and deployment.
- **Integration:** Ensure seamless integration of yfinance with the prediction algorithms and user interface.

### Operational Feasibility
- **Resource Availability:** Confirm availability of required resources (developers, financial data, computational power).
- **Team Expertise:** Assess the team's expertise in the necessary technologies and domains.
- **Maintenance:** Plan for ongoing maintenance and updates post-deployment.

### Economic Feasibility
- **Cost-Benefit Analysis:** Compare the project's costs against the expected benefits.
- **Budget:** Ensure the project stays within budget, including development, deployment, and maintenance costs.
- **ROI:** Estimate the return on investment based on improved prediction accuracy and user adoption.

### Legal and Ethical Feasibility
- **Compliance:** Ensure the system adheres to financial regulations and data privacy laws.
- **Ethical Use:** Address ethical considerations in the use of prediction algorithms and data handling.

![Screenshot 2024-06-14 at 11 38 56 AM](https://github.com/pc3457/Stock-Market-App/assets/146313699/48d61362-9bf9-4a3d-b64d-4e6de5bf8150)

## Tools and Technologies

- **Programming Languages:** Primarily used Python for back-end development and JavaScript and HTML/CSS for the front-end.
- **Frameworks and Libraries:**
  - **Flask:** For developing the back-end web application and handling server-side logic.
  - **HTML/CSS:** Used for building a responsive and dynamic front-end user interface.
  - **Socket.io:** Enabled real-time communication between the client and server.
  - **yfinance:** For fetching and handling stock market data.
- **Version Control:** Utilized Git and GitHub for version control, facilitating collaborative development and code management.
- **IDE:** Primarily used Visual Studio Code for coding due to its extensive features and extensions.

## User Information Storage

### AWS S3 Storage for User Login Details
- User login details are stored securely in an AWS S3 bucket.
- The S3 bucket is configured to restrict public access and ensure data security.
- An example of the S3 bucket structure is shown below:

![Screenshot 2024-06-14 at 11 41 53 AM](https://github.com/pc3457/Stock-Market-App/assets/146313699/3e35cd2b-70da-4be0-8736-d3ab7484265a)

### Every user will have their portfolio and login credentials stored as shown below:

![Screenshot 2024-06-14 at 11 42 41 AM](https://github.com/pc3457/Stock-Market-App/assets/146313699/8985f592-b241-4b0f-b698-2f1e93ad3699)

![Screenshot 2024-06-14 at 11 43 15 AM](https://github.com/pc3457/Stock-Market-App/assets/146313699/6842ef09-74f1-456d-b08f-1dbee3d602d3)

![Screenshot 2024-06-14 at 11 43 49 AM](https://github.com/pc3457/Stock-Market-App/assets/146313699/3c55778a-40e4-43c2-9439-3de71a6c5cee)

## Peer-to-Peer (Using Socket.io)

### Introduction to Socket.io
- Socket.io is a JavaScript library for real-time, bidirectional, event-based communication between clients and servers.

### Implementation
- **Server-Side:**
  - **Initialization:** Configured on the JavaScript server.
  - **Event Handling:** Managed events like connect and disconnect.
  - **Broadcasting:** Real-time chat updates to all connected clients.
- **Client-Side:**
  - **Connection:** Established from the JavaScript frontend.
  - **Event Listeners:** Handled real-time updates and interactions.
  - **Data Display:** Updated UI with latest chat updates.

### Benefits
- **Real-Time Updates:** Provides instant information.
- **Efficient Communication:** Facilitates smooth data exchange.
- **Enhanced User Experience:** Dynamic UI updates without page refresh.

### Challenges & Solutions
- **Multiple Connections:** Managed efficiently with load balancing.
- **Data Consistency:** Ensured with robust validation and synchronization.
- **Performance:** Optimized to minimize latency.

![Screenshot 2024-06-14 at 12 36 45 PM](https://github.com/pc3457/Stock-Market-App/assets/146313699/b4aeada4-67a9-459b-a8f1-ea91d10b6f20)

![Screenshot 2024-06-14 at 12 37 19 PM](https://github.com/pc3457/Stock-Market-App/assets/146313699/27a3fdcd-eb6c-4f8a-9032-4dead9688dfe)

## Future Work

### Database Optimization
- Optimize database queries and indexing for faster data retrieval and processing.
- Use distributed databases or data lakes for efficient storage and access to large datasets.

### Alternative Data Integration
- Incorporate alternative data sources such as social media sentiment (Twitter, Reddit), news articles, and economic indicators.
- Use natural language processing (NLP) to analyze text data for sentiment analysis and trend prediction.

### Enhanced Security Measures
- Implement advanced security measures such as two-factor authentication (2FA), encryption, and secure API access.
- Conduct regular security audits and vulnerability assessments to ensure the application’s integrity.

### Final Application Screenshots

![Screenshot 2024-06-14 at 12 42 08 PM](https://github.com/pc3457/Stock-Market-App/assets/146313699/b138179a-6da0-4c14-9f39-b65a3e371aff)

![Screenshot 2024-06-14 at 12 42 34 PM](https://github.com/pc3457/Stock-Market-App/assets/146313699/a4a5906a-5cba-4852-9736-8c17b69b6d30)
