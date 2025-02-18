import java.util.*;
            import java.io.*;
            import java.text.*;
            import java.time.*;
            import java.math.*;
            import java.util.regex.*;
            
public class Main {
    public Boolean isHappyMessage(String message) {
/*DO NOT modify this method.*/

    // Your implementation code goes here
    
    return message.toLowerCase().contains("happy");
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Main solution = new Main();
        
        // Parse input
        String message = scanner.nextLine();
        
        // Call the solution function
        Boolean result = solution.isHappyMessage(message);
        
        // Print the result
        System.out.println(result);
        scanner.close();
    }
}