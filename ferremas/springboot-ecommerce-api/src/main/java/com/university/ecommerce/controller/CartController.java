import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.university.ecommerce.model.Cart;
import com.university.ecommerce.service.CartService;

@RestController
@RequestMapping("/api/cart")
public class CartController {

    @Autowired
    private CartService cartService;

    @PostMapping("/add")
    public ResponseEntity<Cart> addToCart(@RequestParam Long productId, @RequestParam int quantity) {
        Cart updatedCart = cartService.addToCart(productId, quantity);
        return ResponseEntity.ok(updatedCart);
    }

    @DeleteMapping("/remove/{productId}")
    public ResponseEntity<Cart> removeFromCart(@PathVariable Long productId) {
        Cart updatedCart = cartService.removeFromCart(productId);
        return ResponseEntity.ok(updatedCart);
    }

    @PostMapping("/checkout")
    public ResponseEntity<String> checkoutCart() {
        String response = cartService.checkoutCart();
        return ResponseEntity.ok(response);
    }
}