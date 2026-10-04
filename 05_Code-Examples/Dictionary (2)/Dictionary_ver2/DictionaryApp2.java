import java.util.Scanner; // Why do we need this?

class DictionaryApp2 {
  // Provides only a main method for instantiating and demonstrating a dictionary
  public static void main(String args[]) {
    int size; // Maximum possible number of elements in the dictionary
    int count; // Current number of elements in the dictionary
    Scanner myScanner = new Scanner(System.in);
		// Preparing to read from the keyboard
		//   (or if redirected from the shell by "<",
		//   then from the redirected input file)

    System.out.print("Size of Dictionary: ");
    size = myScanner.nextInt();

    System.out.print("Count of entries: ");
    count = myScanner.nextInt();
    // What is the difference between size and count?

    System.out.println("Reading " + count + " elements into a dictionary of size " + size);
    MyDictionary dictionary = new MyDictionary(size);
		// Create a dictionary of the given size

		Long minKey=Long.MAX_VALUE, maxKey=Long.MIN_VALUE;
    for (int i = 0; i < count; i++) {
			// Insert each element into the dictionary
      double nextValue;
      //System.out.print("Enter element: ");
			//   Prompt can be dropped, to avoid cluttering on the display,
			//   if we are streaming the input in.
      nextValue = myScanner.nextDouble();
			Long nextKey = Long.valueOf(Math.round(nextValue));
      dictionary.put(new Record(nextKey,nextValue));
			if(minKey.compareTo(nextKey)==1) minKey=nextKey;
			if(maxKey.compareTo(nextKey)==-1) maxKey=nextKey;
    }
    dictionary.show();
		for (int i = 0; dictionary.getLength()>count/2; i++) {
			System.out.print("Operation " + i + " : ");
			if(Math.random()<=0.5) {
				Long searchKey = minKey+Long.valueOf(Math.round((maxKey-minKey)*Math.random()));
				System.out.print("Searching for a key close to " + searchKey);
				AbstractRecord found = dictionary.get(searchKey);
				System.out.println(": Found " + (found==null?" N O T H I N G #":found.toString()));
			}
			else {
				Long searchKey = minKey+Long.valueOf(Math.round((maxKey-minKey)*Math.random()));
				System.out.print("Trying to find and remove a record with a key close to " + searchKey);
				AbstractRecord found = dictionary.remove(searchKey);
				System.out.println(": Found " + (found==null?" N O T H I N G #":found.toString()));
				System.out.print("Dictionary length now "+dictionary.getLength());
			}
			System.out.println(" ... operation" + i + " completed.");
		}
    myScanner.close(); // Is this necessary? What does this do? Can you use this instance Scanner
                       // again?
  }
}

