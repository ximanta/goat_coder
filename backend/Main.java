import java.util.*;
import java.util.regex.*;

public class Main {
    public int[] rotateArray(int[] array, int k) {
/*DO NOT modify this method.*/

    int n = array.length;
    if (n == 0) return array; // Handle empty array case
    
    k = k % n; // Handle cases where k is greater than the length of the array
    if (k == 0) return array; // No rotation needed if k is 0

    // Reverse the entire array
    reverse(array, 0, n - 1);
    // Reverse the first k elements
    reverse(array, 0, k - 1);
    // Reverse the remaining elements
    reverse(array, k, n - 1);

    return array;
}

// Helper method to reverse a portion of the array
private void reverse(int[] array, int start, int end) {
    while (start < end) {
        int temp = array[start];
        array[start] = array[end];
        array[end] = temp;
        start++;
        end--;
    }
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
        int k = Integer.parseInt(scanner.nextLine());
        
        // Call the solution function
        int[] result = solution.rotateArray(array, k);
        
        // Print the result
        System.out.println(Arrays.toString(result));
        
        scanner.close();
    }
}