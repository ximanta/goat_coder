import java.util.*;
            import java.io.*;
            import java.text.*;
            import java.time.*;
            import java.math.*;
            import java.util.regex.*;
            
public class Main {

public String formatProductName(String product_name) {
    if (product_name == null || product_name.trim().isEmpty()) {
        return "No product";
    }
    // Trim and convert the entire string to lowercase first
    product_name = product_name.trim().toLowerCase();
    // Capitalize the first letter and concatenate with the rest of the string
    return product_name.substring(0, 1).toUpperCase() + product_name.substring(1);
}


    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Main solution = new Main();
        
        // Parse input
        String productName = scanner.nextLine();
        
        // Call the solution function
        String result = solution.formatProductName(productName);
        
        // Print the result
        System.out.println(result);
        scanner.close();
    }
}