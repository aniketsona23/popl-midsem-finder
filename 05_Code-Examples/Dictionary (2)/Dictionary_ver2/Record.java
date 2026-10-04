class Record extends AbstractRecord {
	public int key;
	public double value;
	public Record(double givenValue) {
		value=givenValue;
		key=(int)Math.round(givenValue);
	}
	public void show() {
		System.out.print("Key: "+key+" Value: "+value);
	}
	public Comparison compare(AbstractRecord r) {
		this.show();
		r.show();
		return Comparison.INCOMPARABLE;
	}
	public Object value() {
		return value;
	}
	public Comparable key() {
		return Double.valueOf(key);
	}
}
