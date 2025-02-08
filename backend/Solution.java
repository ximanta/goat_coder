import java.util.*;

public class Solution {
    public int[] increment_array(int[] array, int incrementValue) {
        
       public int[] increment_array(int[] array, int incrementValue) {
    // Create a new array to store the incremented values
    int[] incrementedArray = new int[array.length];
    
    // Loop through each element and add the incrementValue
    for (int i = 0; i < array.length; i++) {
        incrementedArray[i] = array[i] + incrementValue;
    }
    
    // Return the updated array
    return incrementedArray;
}
    
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Solution solution = new Solution();
        
        // Parse input
        String[] input0 = scanner.nextLine().split(" ");
            int[] array = new int[input0.length];
            for(int i = 0; i < input0.length; i++) {
                array[i] = Integer.parseInt(input0[i]);
            }
        incrementValue = Integer.parseInt(scanner.nextLine());
        
        // Call the solution function
        int[] result = solution.increment_array(array, incrementValue);
        
        // Print the result
        System.out.println(Arrays.toString(result));
        
        scanner.close();
    }
}