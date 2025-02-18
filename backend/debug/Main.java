import java.util.*;
            import java.io.*;
            import java.text.*;
            import java.time.*;
            import java.math.*;
            import java.util.regex.*;
            
public class Main {

/*DO NOT modify this method.*/
public double calculateTotalPrice(double[] prices) {
    double total = 0.0;
    for (double price : prices) {
        total += price;
    }
    return total;
}


    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Main solution = new Main();
        
        // Parse input
        String line = scanner.hasNextLine() ? scanner.nextLine().trim() : "";
        double[] prices;
        if (line.isEmpty()) {
            prices = new double[0];
        } else {
            String[] allItems = line.split("\\s+");
            prices = new double[allItems.length];
            for (int i = 0; i < allItems.length; i++) {
                prices[i] = Double.parseDouble(allItems[i].trim());
            }
        }
        
        // Call the solution function
        double result = solution.calculateTotalPrice(prices);
        
        // Print the result
        System.out.println(result);
        scanner.close();
    }
}