public abstract class Abstract1 {
  public abstract Object tell();
	// Try making tell()
	// return anything but Object
	public String tellType() {
		return tell().getClass().getName();
	}
}
