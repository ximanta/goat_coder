import java.util.*;
import java.util.regex.*;

public class Main {
    public int[] findUniqueElements(int[] array) {
LinkedHashMap<Integer, Integer> frequencyMap = new LinkedHashMap<>();
    
    // Count occurrences of each element
    for (int num : array) {
        frequencyMap.put(num, frequencyMap.getOrDefault(num, 0) + 1);
    }
    
    // Collect unique elements
    List<Integer> uniqueList = new ArrayList<>();
    for (int num : array) {
        if (frequencyMap.get(num) == 1) {
            uniqueList.add(num);
        }
    }
    
    // Convert list to array
    return uniqueList.stream().mapToInt(i -> i).toArray();
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Main solution = new Main();
        
        // Parse input
        String[] input0 = scanner.nextLine().split(" ");
            int[] array = new int[input0.length];
            for(int i = 0; i < input0.length; i++) {
                array[i] = Integer.parseInt(input0[i]);
            }
        
        // Call the solution function
        int[] result = solution.findUniqueElements(array);
        
        // Print the result
        System.out.println(Arrays.toString(result));
        
        scanner.close();
    }
}