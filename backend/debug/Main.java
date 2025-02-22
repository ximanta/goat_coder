import java.util.*;
            import java.io.*;
            import java.text.*;
            import java.time.*;
            import java.math.*;
            import java.util.regex.*;
            
public class Main {

public double calculateAverageScore(int[] scores) {
    if (scores == null || scores.length == 0) {
        return 0;
    }
    int sum = 0;
    for (int score : scores) {
        sum += score;
    }
    return (double) sum / scores.length;
}


    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Main solution = new Main();
        
        // Parse input
        String[] scoresStr = scanner.nextLine().split(" ");
        int[] scores = new int[scoresStr.length];
        for (int i = 0; i < scoresStr.length; i++) {
            scores[i] = Integer.parseInt(scoresStr[i]);
        }
        
        // Call the solution function
        double result = solution.calculateAverageScore(scores);
        
        // Print the result
        System.out.println(result);
        scanner.close();
    }
}