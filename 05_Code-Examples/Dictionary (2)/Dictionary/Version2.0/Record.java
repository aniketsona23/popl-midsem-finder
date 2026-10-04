class Record extends AbstractRecord {
	private Object key, value;

	public Record(Object givenKey, Object givenValue) {
		key = givenKey;
		value = givenValue;
	}

	public Object getKey() {
		return key;
	}

	public Object getValue() {
		return value;
	}

}

