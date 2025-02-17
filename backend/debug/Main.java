import java.util.*;
            import java.io.*;
            import java.text.*;
            import java.time.*;
            import java.math.*;
            import java.util.regex.*;
            
public class Main {
    public Integer sumEvenNumbers(List<Integer> numbers) {
/*DO NOT modify this method.*/

    int sum = 0;
    for (int number : numbers) {
        if (number % 2 == 0) {
            sum += number;
        }
    }
    return sum;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Main solution = new Main();
        
        // Parse input
        List<Integer> numbers = new ArrayList<>();
        while (scanner.hasNextLine()) {
            String line = scanner.nextLine().trim();
            if (line.isEmpty()) break;
            String[] parts = line.split("\\s+");
            for (String part : parts) {
                numbers.add(Integer.parseInt(part));
            }
        }
        
        // Call the solution function
        Integer result = solution.sumEvenNumbers(numbers);
        
        // Print the result
        System.out.println(result);
        scanner.close();
    }
}