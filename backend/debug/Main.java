import java.util.*;
            import java.io.*;
            import java.text.*;
            import java.time.*;
            import java.math.*;
            import java.util.regex.*;
            
public class Main {

public int[] convertHexToRgb(String hex_color) {
    // Validate that the input is a valid hex color string.
    if (hex_color == null || !hex_color.matches("#[0-9A-Fa-f]{6}")) {
        throw new IllegalArgumentException("Invalid hex color format");
    }
    // Remove the '#' and parse the hexadecimal substrings.
    String hex = hex_color.substring(1);
    int red = Integer.parseInt(hex.substring(0, 2), 16);
    int green = Integer.parseInt(hex.substring(2, 4), 16);
    int blue = Integer.parseInt(hex.substring(4, 6), 16);
    
    return new int[]{red, green, blue};
}


    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Main solution = new Main();
        
        // Parse input
        String hexColor = scanner.nextLine();
        
        // Call the solution function
        int[] result = solution.convertHexToRgb(hexColor);
        
        // Print the result
        if (result == null) {
            System.out.println("null");
        } else {
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < result.length; i++) {
                if (i > 0) sb.append(" ");
                sb.append(result[i]);
            }
            System.out.println(sb.toString());
        }
        scanner.close();
    }
}