import java.util.*;
            import java.io.*;
            import java.text.*;
            import java.time.*;
            import java.math.*;
            import java.util.regex.*;
            
public class Main {

/*DO NOT modify this method.*/
public String[] reshuffleList(String[] items) {
    // If the array is null or has 0 or 1 item, return it as is.
    if (items == null || items.length <= 1) {
        return items;
    }
    
    // Create a new array to hold the reshuffled list.
    String[] reshuffled = new String[items.length];
    
    // Move the last item to the front.
    reshuffled[0] = items[items.length - 1];
    
    // Shift the remaining items one position to the right.
    for (int i = 0; i < items.length - 1; i++) {
        reshuffled[i + 1] = items[i];
    }
    
    return reshuffled;
}


    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Main solution = new Main();
        
        // Parse input
        List<String> items = new ArrayList<>();
        while (scanner.hasNextLine()) {
            String line = scanner.nextLine().trim();
            if (line.isEmpty()) break;
            String[] parts = line.split("\\s+");
            for (String part : parts) {
                items.add(part);
            }
        }
        
        // Call the solution function
        List<String> result = solution.reshuffleList(items);
        
        // Print the result
        System.out.println(result);
        scanner.close();
    }
}