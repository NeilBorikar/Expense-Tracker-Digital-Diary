import java.io.*;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Scanner;

class Expense{
    String category;
    double amount;
    LocalDate date;

    public Expense(String category, double amount) {
        this(category, amount, LocalDate.now());
    }

    public Expense(String category, double amount, LocalDate date) {
        this.category = category;
        this.amount = amount;
        this.date = date;
    }

    @Override
    public String toString() {
        return String.format("[%s] %s: ₹%.2f", date, category, amount);
    }
}

 public class DigitalDiaryExpenseTracker {
    private static final String DIARY_FILE = "diary.txt";
    private static final String EXPENSES_FILE = "expenses.txt";
    private static final Scanner scanner = new Scanner(System.in);
    private static final ArrayList<Expense> expenses = new ArrayList<>();

    public static void main(String[] args) {
        loadExpenses();
        
        while (true) {
            System.out.println("\n=== Digital Diary with Expense Tracker ===");
            System.out.println("1. Write New Diary Entry");
            System.out.println("2. View All Diary Entries");
            System.out.println("3. Add New Expense");
            System.out.println("4. View All Expenses");
            System.out.println("5. View Expense Report");
            System.out.println("6. View Total Expenses");
            System.out.println("7. Exit");
            System.out.print("Choose an option: ");

            try {
                int choice = Integer.parseInt(scanner.nextLine());

                switch (choice) {
                    case 1 -> writeDiaryEntry();
                    case 2 -> viewDiaryEntries();
                    case 3 -> addExpense();
                    case 4 -> viewAllExpenses();
                    case 5 -> expenseReport();
                    case 6 -> showTotalExpenses();
                    case 7 -> {
                        saveExpenses();
                        System.out.println("Goodbye! All data saved.");
                        return;
                    }
                    default -> System.out.println("Invalid choice. Please try again.");
                }
            } catch (NumberFormatException e) {
                System.out.println("Please enter a valid number (1-7).");
            }
        }
    }

 
    private static void writeDiaryEntry() {
        System.out.println("\nEnter your diary entry (type 'END' on a new line to finish):");
        StringBuilder entry = new StringBuilder();
        String line;

        while (!(line = scanner.nextLine()).equalsIgnoreCase("END")) {
            entry.append(line).append("\n");
        }

        try (BufferedWriter writer = new BufferedWriter(new FileWriter(DIARY_FILE, true))) {
            writer.write("=== Entry [" + LocalDate.now() + "] ===\n");
            writer.write(entry.toString());
            writer.write("=====================\n\n");
            System.out.println("✓ Diary entry saved successfully!");
        } catch (IOException e) {
            System.out.println("✗ Error saving entry: " + e.getMessage());
        }
    }

    private static void viewDiaryEntries() {
        System.out.println("\n=== Your Diary Entries ===\n");
        try (BufferedReader reader = new BufferedReader(new FileReader(DIARY_FILE))) {
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
        } catch (FileNotFoundException e) {
            System.out.println("No diary entries found yet.");
        } catch (IOException e) {
            System.out.println("✗ Error reading diary: " + e.getMessage());
        }
    }


    private static void addExpense() {
        System.out.print("Enter expense category: ");
        String category = scanner.nextLine().trim();
        
        double amount = getValidDouble("Enter expense amount: ₹");
        
        expenses.add(new Expense(category, amount));
        saveExpenses();
        System.out.println("✓ Expense added successfully!");
    }

    private static void viewAllExpenses() {
        if (expenses.isEmpty()) {
            System.out.println("No expenses recorded yet.");
            return;
        }
        
        System.out.println("\n=== All Expenses ===");
        expenses.forEach(System.out::println);
    }

    private static void expenseReport() {
        if (expenses.isEmpty()) {
            System.out.println("No expenses to report.");
            return;
        }
        
        System.out.println("\n1. View by category\n2. View by date\n3. View by amount range");
        System.out.print("Choose report type: ");
        
        try {
            int choice = Integer.parseInt(scanner.nextLine());
            switch (choice) {
                case 1 -> {
                    System.out.print("Enter category to filter: ");
                    String category = scanner.nextLine();
                    expenses.stream()
                           .filter(e -> e.category.equalsIgnoreCase(category))
                           .forEach(System.out::println);
                }
                case 2 -> {
                    System.out.print("Enter date (YYYY-MM-DD) to filter: ");
                    LocalDate date = LocalDate.parse(scanner.nextLine());
                    expenses.stream()
                           .filter(e -> e.date.equals(date))
                           .forEach(System.out::println);
                }
                case 3 -> {
                    double min = getValidDouble("Enter minimum amount: ₹");
                    double max = getValidDouble("Enter maximum amount: ₹");
                    expenses.stream()
                           .filter(e -> e.amount >= min && e.amount <= max)
                           .forEach(System.out::println);
                }
                default -> System.out.println("Invalid report type.");
            }
        } catch (Exception e) {
            System.out.println("Error generating report: " + e.getMessage());
        }
    }

    private static void showTotalExpenses() {
        double total = expenses.stream()
                             .mapToDouble(e -> e.amount)
                             .sum();
        System.out.printf("\nTotal expenses: ₹%.2f\n", total);
    }

 
    private static void loadExpenses() {
        try (BufferedReader reader = new BufferedReader(new FileReader(EXPENSES_FILE))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(",");
                expenses.add(new Expense(
                    parts[0], 
                    Double.parseDouble(parts[1]), 
                    LocalDate.parse(parts[2]))
                );
            }
        } catch (FileNotFoundException e) {
           
        } catch (IOException e) {
            System.out.println("✗ Error loading expenses: " + e.getMessage());
        }
    }

    private static void saveExpenses() {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(EXPENSES_FILE))) {
            for (Expense expense : expenses) {
                writer.write(String.format("%s,%.2f,%s\n", 
                    expense.category, 
                    expense.amount, 
                    expense.date));
            }
        } catch (IOException e) {
            System.out.println("✗ Error saving expenses: " + e.getMessage());
        }
    }

    private static double getValidDouble(String prompt) {
        while (true) {
            System.out.print(prompt);
            try {
                return Double.parseDouble(scanner.nextLine());
            } catch (NumberFormatException e) {
                System.out.println("Invalid amount. Please enter a valid number.");
            }
        }
    }
}
