public class Main {
  public static void main(String args[]) {
		// Adding primitite literal constant strings:
		System.out.println
		  ("Adding primitite literal constant strings:");
		System.out.println("String1"+" + String2");
		// What is the type of the result of such addition?
		System.out.println
		  ("The type of the result of such addition:");
		System.out.println(("S1"+" + S2").getClass().getName());
		// And what is the type of a primitive string?
		System.out.print("The type of \"S1 + S2\" is: ");
		System.out.println("S1 + S2".getClass().getName());
		// -- So, looking at the foregoing, is there no
		//    difference between primitive and Object strings?
		// --------------------------------------------------------
		// Make a concrete object with data of String type:
		System.out.println("Concrete1<String>:");
		Concrete1<String> s = new Concrete1<String>("Some string");
		// Another concrete object with data of Integer type:
		System.out.println("Concrete1<Integer>:");
    Concrete1<Integer> i = new Concrete1<Integer>(0);
		// Making a concrete object with data of Object type
		//  -- but passing a String type object:
		System.out.println("Concrete1<Object>:");
		Concrete1<Object> t = new Concrete1<Object>("String");
		// What are the types of data in each?
		// See the output of the next three lines.
		System.out.println("Type of s.data " + s.tellType());
		System.out.println("Type of i.data " + i.tellType());
		System.out.println("Type of t.data " + t.tellType());
		System.out.println
			("Changing s.data from "+s.tell()+" to "+i.tell());
    s.listen(i.tell());
		System.out.println
			("Changing t.data from "+t.tell()+" to "+i.tell());
    t.listen(i.tell());
		System.out.println("Type of s.data " + s.tellType());
		System.out.println("Type of t.data " + t.tellType());
  }
}
