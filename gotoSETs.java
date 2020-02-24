import java.io.File;
import java.io.*;
import java.io.FileWriter;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class gotoSETs {
    public static void main(String[] args) throws IOException {
        Scanner scan = new Scanner(new File(args[0]));
        String line;
        FileWriter output = new FileWriter("sets.tsv");
        while(scan.hasNextLine())
        {
            line=scan.nextLine();
            String replaced = line.replace("\"", "");
            String[] parts = replaced.split("\t");
            output.write(parts[0] + "\t" + parts[1] +"\n");
        }
        output.close();
    }
}
