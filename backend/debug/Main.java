import java.util.*;
            import java.io.*;
            import java.text.*;
            import java.time.*;
            import java.math.*;
            import java.util.regex.*;
            
public class Main {

public boolean areAnagrams(String str1, String str2) {
    // Your implementation code goes here
    return null;  // Replace with actual return value
}


    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Main solution = new Main();
        
        // Parse input
        String str1 = scanner.nextLine();
        String str2 = scanner.nextLine();
        
        // Call the solution function
        boolean result = solution.areAnagrams(str1, str2);
        
        // Print the result
        System.out.println(result);
        scanner.close();
    }
}