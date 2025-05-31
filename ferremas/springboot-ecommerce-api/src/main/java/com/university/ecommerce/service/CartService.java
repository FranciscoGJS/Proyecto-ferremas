package com.university.ecommerce.service;

import com.university.ecommerce.model.Cart;
import com.university.ecommerce.model.Product;
import com.university.ecommerce.repository.CartRepository;
import com.university.ecommerce.repository.ProductRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class CartService {

    @Autowired
    private CartRepository cartRepository;

    @Autowired
    private ProductRepository productRepository;

    public void addToCart(Long productId, int quantity) {
        Optional<Product> productOpt = productRepository.findById(productId);
        if (productOpt.isPresent()) {
            Product product = productOpt.get();
            if (product.getStock() >= quantity) {
                // Logic to add product to cart
                // Deduct stock
                product.setStock(product.getStock() - quantity);
                productRepository.save(product);
            } else {
                throw new RuntimeException("Not enough stock available");
            }
        } else {
            throw new RuntimeException("Product not found");
        }
    }

    public void removeFromCart(Long productId) {
        // Logic to remove product from cart
    }

    public void checkoutCart(Long cartId) {
        // Logic to checkout cart
        // This will involve payment processing and clearing the cart
    }
}