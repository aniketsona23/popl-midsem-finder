import java.util.Scanner;

class DictionaryApp {
  // Provides only a main method for instantiating and demonstrating a dictionary
  public static void main(String args[]) {
    int size;
    int count;
		Scanner myScanner = new Scanner(System.in);
		size=myScanner.nextInt(); //size=Integer.parseInt(args[0]);
		count=myScanner.nextInt(); //count=Integer.parseInt(args[1]);
    System.out.println("Reading " + count + " elements into a dictionary of size " + size);
    MyDictionary d=new MyDictionary(size);
    //String[] elems=java.util.Arrays.copyOfRange(args, 2, args.length);
    for(int i=0; i<count; i++) {
			double nextValue;
			nextValue=myScanner.nextDouble();
      d.put(new Record(nextValue)); //Record(Double.parseDouble(elems[i])));
    }
    d.show();
  }
}
