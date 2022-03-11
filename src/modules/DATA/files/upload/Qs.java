import java.util.*;
import java.lang.reflect.Array;
public class Qs{
  public static Scanner kb = new Scanner(System.in);
//Methods for simplification
  //Forces user to enter valid integer
  public static int getInt(String output){
    int input;
    boolean isInt;
    System.out.print(output);
    do{
      try{
        input = Integer.parseInt(kb.nextLine());
        isInt = true;
      } catch (Exception e){
        print("Invalid input. Please enter again: ");
        input = 0;
        isInt = false;
      }
    } while (isInt != true);
    return input;
  }
  //Forces user to enter valid double
  public static double getDouble(String output){
    double input;
    boolean isDouble;
    System.out.print(output);
    do{
      try{
        input = Double.parseDouble(kb.nextLine());
        isDouble = true;
      } catch (Exception e){
        print("Invalid input. Please enter again: ");
        input = 0;
        isDouble = false;
      }
    } while (isDouble != true);
    return input;
  }
  //Forces user to enter valid string
  public static String getString(String output){
    String input;
    boolean ok;
    System.out.print(output);
    do{
      try{
        input = kb.nextLine();
        ok = true;
      } catch (Exception e){
        print("Invalid input. Please enter again: ");
        input = "";
      ok = false;
      }
    } while (ok != true);
    return input;
  }
  //Reduce length of print and println
  public static void print(String output){
    System.out.print(output);
  }
  public static void println(String output){
    System.out.println(output);
  }
  //Generate random integer within range
  public static int getRandomInt(int min, int max) {
    return (int) (Math.random()*(max-min+1)+min);
  }
  public static int countOccurrenceInArray(int value, int[] intArray){
    int arrayLength = intArray.length;
    int counter = 0;
    for (int i = 0; i < arrayLength; i++) {
      if (intArray[i] == value) {
        counter++;
      }
    }
    return counter;
  }
  public static boolean isBetween(int x, int lower, int upper) {
    return lower <= x && x <= upper;
  }
  public static void printArray2(String[][] array){
    for (String[] row : array) {
      System.out.println(Arrays.toString(row));
    }
  }
  public static void printArray1(int[] array){
    for (int value : array) {
      System.out.println(value);
    }
  }
  public static void printArray1(String[] array){
    for (String value : array) {
      System.out.println(value);
    }
  }
  public static int getArraySum(int[] array){
    int total = 0;
    for (int i : array) {
      total = total + i;
    }
    return total;
  }
  ////////////////////////////////////// Main /////////////////////////////////////////////////
  public static void main(String[] args) {
    Q1();
    Q2();
    Q3();
    Q4();
    Q5();
    Q6();
    Q7();
  }
  //////////////////////////////////// Questions ////////////////////////////////////////////
  //Doofingies
  //PRE None
  //CALLS getInt(), printArray1(), getArraySum()
  //DESC Manage sales for Winnipeg and Calgary
  //POST void
  static void Q1(){
    //Initiate variables
    int[] winni = new int[10];
    int[] calga = new int[10];
    boolean keepGoing = true;
    int option, region;
    do {
      option = getInt("1) See sales 2) Enter sales 3) See total 0) Quit");
      region = getInt("1) Winnipeg 2) Calgary 3) N/A ");
      if (option == 1) {
        switch (region) {
          case 1: printArray1(winni); break;
          case 2: printArray1(calga); break;
          default: println("???");
        }
      }
      else if (option == 2) {
        if (region == 1) {
          for (int i = 0; i < winni.length; i++) {
            winni[i] = getInt("Enter sales for size " + i + ": ");
          }
        }
        else if (region == 2) {
          for (int i = 0; i < calga.length; i++) {
            calga[i] = getInt("Enter sales for size " + i + ": ");
          }
        }
      }
      else if (option == 3){
        println("The total sales are: " + (getArraySum(winni) + getArraySum(calga)) + " units");
      }
      else if (option == 0) {
        keepGoing = false;
      }
    } while (keepGoing == true);
  }
  //Book index
  //PRE None
  //CALLS getString(), getInt(), printArray1()
  //DESC Allows for viewing and editing table of 10 comic book titles
  static void Q2(){
    //Initiate variables
    int option;
    String[] titlesDB = new String[10];
    int indexNum;
    String newTitle;
    for (int i = 0; i < titlesDB.length; i++) {
      newTitle = getString("Enter title for index #" + i + ": ");
      titlesDB[i] = newTitle;
    }
    do {
      option = getInt("1) Display database 2) See index title 3) Chnage index title 0) Quit ");
      if (option == 1) {
        printArray1(titlesDB);
      }
      else if (option == 2) {
        indexNum = getInt("Enter index number (0-9): ");
        println("Title: " + titlesDB[indexNum]);
      }
      else if (option == 3) {
        indexNum = getInt("Enter index number (0-9): ");
        newTitle = getString("Enter new title: ");
        titlesDB[indexNum] = newTitle;
      }
    } while (option != 0);
  }
  //Dumb random stuff
  //PRE None
  //CALLS getRandomInt(), printArray1(), getInt()
  //DESC Generates 10 random numbers between 1 and 99 to find the Maximum and Minimum
  //POST void
  static void Q3(){
    //Initiate variables
    int[] array = new int[10];
    int min = 100, max = 0, playAgain;
    do{
      array = new int[10];
      min = 100; max = 0;
      for (int i = 0; i < array.length; i++) {
        array[i] = getRandomInt(1,99);
      }
      //Get min and max
      for (int n : array){
        if (n > max) {
          max = n;
        }
        if (n < min) {
          min = n;
        }
      }
      //Output
      println("Array:");
      printArray1(array);
      println("Max: " + max);
      println("Min: " + min);
      playAgain = getInt("1) Run again 0) Quit");
    }while(playAgain != 0);
  }
  //Guessing game
  //PRE None
  //CALLS getRandomInt(), printArray2(), getInt(), isBetween(), getString()
  //DESC Places prizes in two locations on a two by two board and allows the user to guess 10 times
  //POST void
  static void Q4(){
    //Initiate variables
    String[][] prizes = new String[4][5], userGuesses = new String[4][5];
    int randRow, randCol, tries, guessRow, guessCol;
    boolean win = false, compF = false, uterF = false;
    String guessVal;
    //Place prizes
    randRow = getRandomInt(0,3);
    randCol = getRandomInt(0,4);
    prizes[randRow][randCol] = "COMP";
    println("COMP location : " + randRow + ", " + randCol);
    do {
      randRow = getRandomInt(0,3);
      randCol = getRandomInt(0,4);
    } while (prizes[randRow][randCol] == "COMP");
    prizes[randRow][randCol] = "UTER";
    println("UTER location : " + randRow + ", " + randCol);
    //Display board
    printArray2(userGuesses);
    //Guess
    tries = 0;
    do {
      //Get guess
      do {
        println("Please guess within the valid range");
        guessRow = getInt("Guess row (0-3): ");
        guessCol = getInt("Guess column (0-4): ");
      } while (!isBetween(guessRow, 0, 3) || !isBetween(guessCol, 0, 4));
      //Get location value
      guessVal = prizes[guessRow][guessCol];
      //Check if got prize
      if (guessVal != null) {
        if (guessVal.equals("COMP")) {
          compF = true;
          userGuesses[guessRow][guessCol] = "✅";
          println("You have found COMP!");
        }
        else if (guessVal.equals("UTER")) {
          uterF = true;
          userGuesses[guessRow][guessCol] = "✅";
          println("You have found UTER!");
        }
      }
      else{userGuesses[guessRow][guessCol] = "❌"; println("Nope!");}
      //Display board
      printArray2(userGuesses);
      //Increment counter
      println("You have " + (10-tries) + " tries left.");
      tries++;
      //Check of all found
      if (compF == true && uterF == true) {
        win = true;
        println("You WIN!");
      }
    } while (win != true && tries < 10);
    if (win != true) {
      println("10 tries are up... Better luck next time.");
    }
    String tryAgain = getString("Play again? y/n: ");
    if (tryAgain.equals("y")) {Q4();}
  }
  //Student calc
  //PRE None
  //CALLS getDouble()
  //DESC Allows teacher to enter grades for students and find statistics (STDEV, AVERAGE, MIN, MAX)
  //POST void
  static void Q5(){
    //Initialize variables
    double[] stuGrades = new double[(getInt("How many students are there in the class? "))];
    //Loop for students to enter grades
    for (int i = 0; i < stuGrades.length; i++) {
      stuGrades[i] = getDouble("Enter grade for student #" + (i+1) + ": ");
    }
    //Calculate stuff
    //Get max and min
    double max = stuGrades[0];
    double min = stuGrades[0];
    for (double grade : stuGrades) {
      if (grade > max) {
        max = grade;
      }
      else if (grade < min) {
        min = grade;
      }
    }
    //Get mean
    double totalScore = 0;
    for (double grade : stuGrades) {
      totalScore = totalScore + grade;
    }
    double mean = totalScore / stuGrades.length;
    //Get STDEV
    double arraySquaredSum = 0;
    for (double grade : stuGrades) {
      arraySquaredSum = arraySquaredSum + Math.pow(grade, 2);
    }
    int countOfElements = stuGrades.length;
    double stdev = Math.sqrt((arraySquaredSum/countOfElements)-Math.pow(mean, 2));
    //Output
    print("Maximum score: ");
    System.out.format("%.2f", max);
    println("");
    print("Minimum score: ");
    System.out.format("%.2f", min);
    println("");
    print("Mean average: ");
    System.out.format("%.2f", mean);
    println("");
    print("STDEV: ");
    System.out.format("%.2f", stdev);
    println("");
  }
  //////////////////////////// Weird Lockers ///////////////////////////
  //PRE None
  //CALLS getInt()
  //DESC Locks or unlocks lockers based on a pattern
  //POST void
  static void Q6(){
    //Initialize variables
    boolean[] lockers = new boolean[30];
    boolean keepRunning = true;
    int option;
    int n = 2;
    //Loop
    do {
      option = getInt("1) Simulate Hassan 2) Reset 0) Quit ");
      if (option == 1) {
        //Do weird locker stuff
        for (int i = 0; i < 30; i = i+n) {
          lockers[i] = (!lockers[i]);
        }
        //Show lockers
        int counter = 1;
        for (boolean Lstatus : lockers) {
          if (Lstatus == true) {
            println("Locker " + counter + ": Open");
          }
          else {
            println("Locker " + counter + ": Closed");
          }
          counter++;
        }
        //Increment counter
        n++;
      }
      else if (option == 2) {
        lockers = new boolean[30];
        n = 2;
      }
      else if (option == 0) {
        keepRunning = false;
      }
    } while (keepRunning == true);
  }
    ///////////////////////// Risk Game ///////////////////////////////
    //PRE None
    //CALLS getRandomInt(), getInt(), redeemCards(),
    //DESC Generates 10 random numbers between 1 and 99 to find the Maximum and Minimum
    //POST void
  static void Q7(){
    int[] cardSet = new int[72];
    int count = 0;
    boolean redeemed;
    int countRedeemed = 0;
    String unit;
    //Options
    int option;
    do {
      println("");
      option = getInt("1) Draw new card 2) Redeem cards 3) Reset deck 4) Show deck 0) Quit ");
      println("");
      if (option == 1) {
        //1 is Infantry, 2 is Cavalry, and 3 is Artillery
        cardSet[count] = getRandomInt(1,3);
        switch (cardSet[count]) {
          case 1: unit = "Infantry"; break;
          case 2: unit = "Cavalry"; break;
          case 3: unit = "Artillery"; break;
          default: unit = "Nothing";
        }
        println("Your draw: " + unit);
        count++;
      }
      else if (option == 2) {
        redeemed = redeemCards(cardSet);
        if (redeemed == true) {
          println("Cards redeemed. Deck resetting...");
          cardSet = new int[72];
          count = 0;
          countRedeemed++;
        }
        else{
          println("Nothing to redeem... Just keep playing");
        }
      }
      else if (option == 3) {
        println("Deck resetting...");
        cardSet = new int[72];
        count = 0;
      }
      else if (option == 4) {
        print("Deck: ");
        for (int i = 0; i < count; i++) {
          print(Integer.toString(cardSet[i]));
        }
        println("");
      }
    } while (option != 0);
    println("You have redeemed " + countRedeemed + " cards.");
  }
  //PRE cardSet
  //CALLS countOccurrenceInArray()
  //DESC Redeems cards based on rules of risk game
  //POST Whether or not a card was redeemed
  static boolean redeemCards(int[] cardSet){
    String redeemedType;
    int infantry = countOccurrenceInArray(1, cardSet);
    int cavalry = countOccurrenceInArray(2, cardSet);
    int artillery = countOccurrenceInArray(3, cardSet);
    boolean success;
    if (infantry >= 3) {
      redeemedType = "Infantry";
      success = true;
    }
    else if (cavalry >= 3) {
      redeemedType = "Cavalry";
      success = true;
    }
    else if (artillery >= 3) {
      redeemedType = "Artillery";
      success = true;
    }
    else if (infantry >= 1 && cavalry >= 1 && artillery >= 1) {
      redeemedType = "Mixed batch";
      success = true;
    }
    else{
      redeemedType = "Nothing";
      success = false;
    }
    println("You have redeemed: " + redeemedType);
    return success;
  }
}
