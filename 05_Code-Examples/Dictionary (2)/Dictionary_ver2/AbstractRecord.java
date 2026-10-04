abstract class AbstractRecord {
	abstract public Comparable key();
	abstract public Object value();
	abstract public Comparison compare(AbstractRecord another);
	abstract public void show();
}
