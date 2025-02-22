import java.util.*;
            import java.io.*;
            import java.text.*;
            import java.time.*;
            import java.math.*;
            import java.util.regex.*;
            
public class Main {

public int[] adjustInventory(int[] quantities) {
    // Iterate through each product quantity and add one
    for (int i = 0; i < quantities.length; i++) {
        quantities[i] += 1;
    }
    // Return the updated list of quantities
    return quantities;
}


    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Main solution = new Main();
        
        // Parse input
        String line = scanner.hasNextLine() ? scanner.nextLine().trim() : "";
        int[] quantities;
        if (line.isEmpty()) {
            quantities = new int[0];
        } else {
            String[] allItems = line.split("\\s+");
            quantities = new int[allItems.length];
            for (int i = 0; i < allItems.length; i++) {
                quantities[i] = Integer.parseInt(allItems[i].trim());
            }
        }
        
        // Call the solution function
        int[] result = solution.adjustInventory(quantities);
        
        // Print the result
        System.out.println(Arrays.toString(result));
        scanner.close();
    }
}