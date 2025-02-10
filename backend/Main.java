import java.util.*;
import java.util.regex.*;

public class Main {
    public int square(int x) {
return x * x;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Main solution = new Main();
        
        // Parse input
        int x = Integer.parseInt(scanner.nextLine());
        
        // Call the solution function
        int result = solution.square(x);
        
        // Print the result
        System.out.println(result);
        
        scanner.close();
    }
}