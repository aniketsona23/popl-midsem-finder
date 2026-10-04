extern int globalSrNo;

class Class1 {
	private:
		int srno;
	public:
		Class1(int nosr = globalSrNo) {
			if(nosr <= 0)
				srno = ++globalSrNo;
			else
				srno = nosr;
		}
		~Class1() {
			globalSrNo+=(1<<21);
		}
		double SrNo() {
			return srno*1.0/(globalSrNo & ((1<<21)-1));
		}

};
