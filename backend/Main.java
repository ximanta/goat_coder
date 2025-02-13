import java.util.*;
            import java.io.*;
            import java.text.*;
            import java.time.*;
            import java.math.*;
            import java.util.regex.*;

public class Main {
    public int[] filterPopularTracks(int[] ratings, int threshold) {
/*DO NOT modify this method.*/

    // First, count how many ratings are greater than the threshold.
    int count = 0;
    for (int rating : ratings) {
        if (rating > threshold) {
            count++;
        }
    }
    
    // Create a new array to store the ratings that exceed the threshold.
    int[] popularTracks = new int[count];
    int index = 0;
    
    // Add qualifying ratings to the new array.
    for (int rating : ratings) {
        if (rating > threshold) {
            popularTracks[index++] = rating;
        }
    }
    
    // Return the array of popular tracks.
    return popularTracks;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Main solution = new Main();
        
        // Parse input
        String line0 = scanner.nextLine();
        String[] input0 = line0.trim().isEmpty() ? new String[0] : line0.split(" ");
        int[] ratings = new int[input0.length];
        for(int i = 0; i < input0.length; i++) {
            ratings[i] = Integer.parseInt(input0[i]);
        }
        int threshold = Integer.parseInt(scanner.nextLine());
        
        // Call the solution function
        int[] result = solution.filterPopularTracks(ratings, threshold);
        
        // Print the result
        System.out.println(Arrays.toString(result));
        
        scanner.close();
    }
}