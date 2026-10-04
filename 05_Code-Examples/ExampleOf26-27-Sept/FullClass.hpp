using namespace std;

class FullClass {
	public :
		FullClass(void);
		FullClass(int);
		FullClass(int, int*);
		FullClass(const FullClass&);
		void tell(void);
		void setNthElement(int,int);
		~FullClass(void);
};
