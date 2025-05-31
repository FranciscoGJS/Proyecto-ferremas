# Spring Boot E-commerce API

This project is a simple e-commerce API built with Spring Boot. It manages product stock and allows users to add products to their shopping cart and purchase them. The API is designed for educational purposes and serves as a foundation for further development, including future integration with PayPal for payment processing.

## Features

- Manage products with CRUD operations
- Handle shopping cart functionality
- Deduct stock when products are added to the cart and purchased
- Future integration with PayPal for payment processing

## Project Structure

```
springboot-ecommerce-api
├── src
│   ├── main
│   │   ├── java
│   │   │   └── com
│   │   │       └── university
│   │   │           └── ecommerce
│   │   │               ├── EcommerceApplication.java
│   │   │               ├── controller
│   │   │               │   ├── ProductController.java
│   │   │               │   └── CartController.java
│   │   │               ├── model
│   │   │               │   ├── Product.java
│   │   │               │   └── Cart.java
│   │   │               ├── repository
│   │   │               │   ├── ProductRepository.java
│   │   │               │   └── CartRepository.java
│   │   │               └── service
│   │   │                   ├── ProductService.java
│   │   │                   └── CartService.java
│   │   └── resources
│   │       ├── application.properties
│   │       └── data.sql
│   └── test
│       └── java
│           └── com
│               └── university
│                   └── ecommerce
│                       └── EcommerceApplicationTests.java
├── pom.xml
└── README.md
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
   cd springboot-ecommerce-api
   ```

3. Build the project using Maven:
   ```
   mvn clean install
   ```

4. Run the application:
   ```
   mvn spring-boot:run
   ```

5. Access the API at `http://localhost:8080`.

## Usage Guidelines

- Use the `ProductController` to manage products.
- Use the `CartController` to manage the shopping cart.
- Ensure that stock is available before adding products to the cart.

## Future Enhancements

- Integrate PayPal for payment processing.
- Implement user authentication and authorization.
- Add more advanced features such as order history and product reviews.