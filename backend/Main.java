import java.util.*;
            import java.io.*;
            import java.text.*;
            import java.time.*;
            import java.math.*;
            import java.util.regex.*;

public class Main {
    public int[] countUp(int number) {
/*DO NOT modify this method.*/

    // If the number is less than or equal to 0, return an empty array.
    if (number <= 0) {
        return new int[0];
    }
    
    // Create an array of size 'number'
    int[] result = new int[number];
    
    // Fill the array with values from 1 to number.
    for (int i = 0; i < number; i++) {
        result[i] = i + 1;
    }
    
    // Return the populated array.
    return result;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Main solution = new Main();
        
        // Parse input
        int number = Integer.parseInt(scanner.nextLine());
        
        // Call the solution function
        int[] result = solution.countUp(number);
        
        // Print the result
        System.out.println(Arrays.toString(result));
        
        scanner.close();
    }
}