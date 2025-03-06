import java.util.*;
            import java.io.*;
            import java.text.*;
            import java.time.*;
            import java.math.*;
            import java.util.regex.*;
            
public class Main {

public String cleanBookTitle(String title) {
    // Remove all characters that are not letters, digits, or whitespace.
    String cleaned = title.replaceAll("[^a-zA-Z0-9\\s]", "");
    // Trim the result and replace multiple spaces with a single space.
    cleaned = cleaned.trim().replaceAll("\\s+", " ");
    return cleaned;
}


    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Main solution = new Main();
        
        // Parse input
        String title = scanner.nextLine();
        
        // Call the solution function
        String result = solution.cleanBookTitle(title);
        
        // Print the result
        System.out.println(result);
        scanner.close();
    }
}