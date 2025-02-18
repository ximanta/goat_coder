import java.util.*;
            import java.io.*;
            import java.text.*;
            import java.time.*;
            import java.math.*;
            import java.util.regex.*;
            
public class Main {

public double calculateTotalPrice(double originalPrice, double taxRate) {
    // Calculate the tax amount (taxRate is a percentage, so divide by 100)
    double taxAmount = originalPrice * (taxRate / 100.0);
    // Calculate the total price by adding the original price and tax amount
    double totalPrice = originalPrice + taxAmount;
    // Round the total price to two decimal places
    return Math.round(totalPrice * 100.0) / 100.0;
}


    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Main solution = new Main();
        
        // Parse input
        double originalPrice = Double.parseDouble(scanner.nextLine());
        double taxRate = Double.parseDouble(scanner.nextLine());
        
        // Call the solution function
        double result = solution.calculateTotalPrice(originalPrice, taxRate);
        
        // Print the result
        System.out.println(result);
        scanner.close();
    }
}