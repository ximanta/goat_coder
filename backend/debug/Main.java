import java.util.*;
            import java.io.*;
            import java.text.*;
            import java.time.*;
            import java.math.*;
            import java.util.regex.*;
            
public class Main {

public int countLowScores(int[] scores, int threshold) {
    if (scores == null) {
        return 0;
    }
    int count = 0;
    for (int score : scores) {
        if (score < threshold) {
            count++;
        }
    }
    return count;
}


    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Main solution = new Main();
        
        // Parse input
        String[] scoresStr = scanner.nextLine().split("\\|");
int[] scores = new int[scoresStr.length];
for (int i = 0; i < scoresStr.length; i++) {
    scores[i] = Integer.parseInt(scoresStr[i]);
}
        int threshold = Integer.parseInt(scanner.nextLine());
        
        // Call the solution function
        int result = solution.countLowScores(scores, threshold);
        
        // Print the result
        System.out.println(result);
        scanner.close();
    }
}