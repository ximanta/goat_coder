import java.util.*;
import java.util.regex.*;

public class Main {
    public int[] uniqueValues(int[] numbers) {
/*DO NOT modify this method.*/

    // Use a LinkedHashMap to preserve the order of insertion while counting frequencies.
    Map<Integer, Integer> frequencyMap = new LinkedHashMap<>();
    
    // Count the occurrences of each number.
    for (int num : numbers) {
        frequencyMap.put(num, frequencyMap.getOrDefault(num, 0) + 1);
    }
    
    // Create a list to hold the unique values (appear exactly once).
    List<Integer> uniqueList = new ArrayList<>();
    for (int num : numbers) {
        if (frequencyMap.get(num) == 1) {
            uniqueList.add(num);
        }
    }
    
    // If there are no unique values, return an empty array.
    if (uniqueList.isEmpty()) {
        return new int[0];
    }
    
    // Convert the List<Integer> to an int[] array.
    int[] result = new int[uniqueList.size()];
    for (int i = 0; i < uniqueList.size(); i++) {
        result[i] = uniqueList.get(i);
    }
    
    return result;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Main solution = new Main();
        
        // Parse input
        List<String> lines = new ArrayList<>();
        while(scanner.hasNextLine()){
            String line = scanner.nextLine();
            if(line.trim().isEmpty()) break;
            lines.add(line);
        }
        String allInput = String.join(" ", lines);
        String[] tokens = allInput.trim().isEmpty() ? new String[0] : allInput.split("\\s+");
        int[] numbers = new int[tokens.length];
        for(int i = 0; i < tokens.length; i++) {
            numbers[i] = Integer.parseInt(tokens[i]);
        }
        
        // Call the solution function
        int[] result = solution.uniqueValues(numbers);
        
        // Print the result
        System.out.println(Arrays.toString(result));
        
        scanner.close();
    }
}