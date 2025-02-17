import java.util.*;
            import java.io.*;
            import java.text.*;
            import java.time.*;
            import java.math.*;
            import java.util.regex.*;
            
public class Main {
    public int findLongestDistinctSubarray(int[] array) {
if (array == null || array.length == 0) {
        return 0;
    }
    
    int left = 0, right = 0;
    int maxLength = 0;
    HashSet<Integer> seen = new HashSet<>();
    
    while (right < array.length) {
        // If the current element is not in the set, add it and update maxLength.
        if (!seen.contains(array[right])) {
            seen.add(array[right]);
            maxLength = Math.max(maxLength, right - left + 1);
            right++;
        } else {
            // If it's already in the set, remove the element at 'left' and move the left pointer.
            seen.remove(array[left]);
            left++;
        }
    }
    
    return maxLength;
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
        int[] array = new int[tokens.length];
        for(int i = 0; i < tokens.length; i++) {
            array[i] = Integer.parseInt(tokens[i]);
        }
        
        // Call the solution function
        int result = solution.findLongestDistinctSubarray(array);
        
        // Print the result
        System.out.println(result);
        scanner.close();
    }
}