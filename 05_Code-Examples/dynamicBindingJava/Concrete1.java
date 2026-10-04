public class Concrete1<T> extends Abstract1 implements Interface1<T> {
  private T data;
  public Concrete1(T t) {
		System.out.println
			("Making Concrete1<"+
			t.getClass().getName()+
			"> from data "+t);
		data = t;
	}
  public T tell() { return data; }
	// Keep exactly one of the listen methods,
	// and see the effects in each case.
  public void listen(T t) { data = t; }
  // public void listen(Object t) { data = ((T)t); }
}
