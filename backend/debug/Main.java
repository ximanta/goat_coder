import java.util.*;
            import java.io.*;
            import java.text.*;
            import java.time.*;
            import java.math.*;
            import java.util.regex.*;
            
public class Main {
    public Integer countVowels(String text) {
/*DO NOT modify this method.*/

    int count = 0;
    // Loop through each character in the string.
    for (int i = 0; i < text.length(); i++) {
        char c = Character.toLowerCase(text.charAt(i));
        // Check if the character is a vowel.
        if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') {
            count++;
        }
    }
    return count;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Main solution = new Main();
        
        // Parse input
        String text = scanner.nextLine();
        
        // Call the solution function
        Integer result = solution.countVowels(text);
        
        // Print the result
        System.out.println(result);
        scanner.close();
    }
}